import os
import csv
import re

# Define paths
base_dir = "D:/Kishant/COSMO/Data"
sdf_library_dir = os.path.join(base_dir, "sdf_library")
output_dir = os.path.join(base_dir, "combined_output")
combined_sdf_path = os.path.join(output_dir, "combined_compounds.sdf")
csv_path = os.path.join(output_dir, "compound_list.csv")

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Function to extract CID and compound name from SDF file
def extract_info(sdf_content):
    cid_match = re.search(r'> <PUBCHEM_COMPOUND_CID>\n(\d+)', sdf_content)
    name_match = re.search(r'> <PUBCHEM_IUPAC_NAME>\n(.+)', sdf_content)
    cid = int(cid_match.group(1)) if cid_match else None
    name = name_match.group(1) if name_match else "Unknown"
    return cid, name

# Collect and sort compound information
compounds = []
for cid_folder in os.listdir(sdf_library_dir):
    cid_path = os.path.join(sdf_library_dir, cid_folder)
    if os.path.isdir(cid_path):
        sdf_file = os.path.join(cid_path, f"{cid_folder}.sdf")
        if os.path.exists(sdf_file):
            with open(sdf_file, 'r') as f:
                content = f.read()
                cid, name = extract_info(content)
                if cid:
                    compounds.append((cid, name, content))

# Sort compounds by CID
compounds.sort(key=lambda x: x[0])

# Write combined SDF file
with open(combined_sdf_path, 'w') as sdf_out:
    for _, _, content in compounds:
        sdf_out.write(content)
        #sdf_out.write("$$====GonnaTestThingsOut====$$\n")

# Write CSV file
with open(csv_path, 'w', newline='') as csv_out:
    writer = csv.writer(csv_out)
    writer.writerow(["CID", "Compound Name"])
    for cid, name, _ in compounds:
        writer.writerow([cid, name])

print(f"Combined SDF file created at: {combined_sdf_path}")
print(f"CSV file created at: {csv_path}")
