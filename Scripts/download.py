import os
import pandas as pd
import pubchempy as pcp
import requests

# Get the directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Set the base directory for the sdf_library relative to the script location
BASE_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "Data", "sdf_library")

def search_pubchem(compound):
    try:
        results = pcp.get_compounds(compound, 'name', record_type='3d')
        return results[0].cid
    except (IndexError, pcp.PubChemHTTPError) as e:
        print(f"Error searching for {compound}: {str(e)}")
        return None

def download_sdf(cid):
    # Request the 3D SDF file
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/{cid}/SDF?record_type=3d"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except (requests.exceptions.RequestException, pcp.PubChemHTTPError) as e:
        print(f"Error downloading SDF for CID {cid}: {str(e)}")
        return None

def get_compound_details(cid):
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
        return None

def process_compounds(csv_file):
    os.makedirs(BASE_DIR, exist_ok=True)

    df = pd.read_csv(csv_file)
    
    for _, row in df.iterrows():
        compound_name = row['Compound Name']
        cid = search_pubchem(compound_name)
        
        if cid:
            cid_dir = os.path.join(BASE_DIR, str(cid))
            os.makedirs(cid_dir, exist_ok=True)
            
            sdf_content = download_sdf(cid)
            if sdf_content:
                with open(os.path.join(cid_dir, f"{cid}.sdf"), "w") as sdf_file:
                    sdf_file.write(sdf_content)
            
            details = get_compound_details(cid)
            if details:
                with open(os.path.join(cid_dir, "README.txt"), "w") as readme_file:
                    readme_file.write(f"Compound: {compound_name}\n")
                    readme_file.write(f"CID: {cid}\n\n")
                    for key, value in details.items():
                        readme_file.write(f"{key}: {value}\n")
            
            print(f"Processed {compound_name} (CID: {cid})")
        else:
            print(f"Could not process {compound_name}")

if __name__ == "__main__":
    csv_file = os.path.join(SCRIPT_DIR, "compounds.csv")  # Assuming the CSV is in the same directory as the script
    process_compounds(csv_file)
