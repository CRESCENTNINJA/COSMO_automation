import os
import pandas as pd
import pubchempy as pcp
import requests

# Get the directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Set the base directory for the sdf_library relative to the script location
BASE_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "Data", "sdf_library")
os.makedirs(BASE_DIR, exist_ok=True)  # Ensure base directory exists

def search_pubchem(compound):
    """Search for CID using compound name."""
    try:
        results = pcp.get_compounds(compound, 'name', record_type='3d')
        return results[0].cid if results else None
    except (IndexError, pcp.PubChemHTTPError) as e:
        print(f"Error searching for {compound}: {str(e)}")
        return None

def download_sdf(cid):
    """Download the 3D SDF file from PubChem."""
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/{cid}/SDF?record_type=3d"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error downloading SDF for CID {cid}: {str(e)}")
        return None

def get_compound_details(cid):
    """Retrieve compound details from PubChem."""
    try:
        compound = pcp.Compound.from_cid(cid)
        return {
            "Name": compound.iupac_name,
            "Molecular Formula": compound.molecular_formula,
            "Molecular Weight": compound.molecular_weight,
            "XLogP": compound.xlogp,
            "H-Bond Donor Count": compound.h_bond_donor_count,
            "H-Bond Acceptor Count": compound.h_bond_acceptor_count
        }
    except pcp.PubChemHTTPError as e:
        print(f"Error fetching details for CID {cid}: {str(e)}")
    except AttributeError:
        print(f"Invalid compound details for CID {cid}")
    return None

def process_compounds(csv_file):
    """Process compounds from CSV file, handling both names and CID numbers."""
    df = pd.read_csv(csv_file)

    for _, row in df.iterrows():
        cid = None
        compound_name = None

        # Check if the CID column exists and is valid
        if 'CID' in df.columns and pd.notna(row['CID']):
            try:
                cid = int(row['CID'])  # Convert to int safely
            except ValueError:
                print(f"Invalid CID: {row['CID']}, skipping.")
                continue

        # If no CID, check if a compound name is provided
        if cid is None and 'Compound Name' in df.columns and pd.notna(row['Compound Name']):
            compound_name = row['Compound Name']
            cid = search_pubchem(compound_name)

        # Skip if CID is still not found
        if cid is None:
            print(f"Could not process: {compound_name or 'Unknown'}")
            continue

        # Set up directory for the CID
        cid_dir = os.path.join(BASE_DIR, str(cid))
        os.makedirs(cid_dir, exist_ok=True)

        # Download SDF file
        sdf_content = download_sdf(cid)
        if sdf_content:
            with open(os.path.join(cid_dir, f"{cid}.sdf"), "w") as sdf_file:
                sdf_file.write(sdf_content)

        # Fetch compound details
        details = get_compound_details(cid)
        if details:
            with open(os.path.join(cid_dir, "README.txt"), "w") as readme_file:
                readme_file.write(f"Compound: {compound_name or 'Unknown'}\n")
                readme_file.write(f"CID: {cid}\n\n")
                for key, value in details.items():
                    readme_file.write(f"{key}: {value}\n")

        print(f"Processed CID {cid} ({compound_name or 'Unknown'})")

if __name__ == "__main__":
    csv_file = os.path.join(SCRIPT_DIR, "compounds.csv")  # Assuming CSV is in the same directory as the script
    process_compounds(csv_file)
