import pandas as pd
import pyreadstat
from pathlib import Path
import os
from glob import glob

# script directory
script_dir = Path(__file__).resolve().parent

# folder containing all the sav files 
input_folder = script_dir.parent / "data" / "raw" / "Household Recode files (xlsx)" / "VariableView"

# output folder
output = script_dir.parent / "data" / "processed" / "Household Recode files (xlsx)" / "VariableView"

# look for the folder or make one if it doesn't
output.mkdir(parents=True, exist_ok=True)

# selected variables
selected_variables = [ 
    "Ecological region",
    "Province",
    "District",
    "Type of place of residence",
    "Cluster number",
    "Household number",
    "Respondent's line number (answering Household questionnaire)",
    "Wealth index combined",
    "Has a mobile telephone",
    "Mobile phone used financial transactions",
    "Has bank account",
    "Native language of the respondent",
    "Has electricity",
    "Type of toilet facility",
    "Has refrigerator",
    "Has television",
    "Has radio",
    "Has a computer",
    "Type of light at home",
 ]

files = [
    file for file in glob(os.path.join(input_folder, "*.xlsx"))
    if not Path(file).name.startswith("~$")
]

if not files:
    print(f"No .xlsx files found in: {input_folder}")

# Store all filtered dataframes
all_filtered = []

for file in files:
    df = pd.read_excel(file)

    # keep only the variables you want
    filtered = (
        df[df["Label"].isin(selected_variables)]
        [["Name", "Label", "Values"]]
        .copy()
    )

    filtered.insert(0, "Survey", Path(file).stem)

    # Add to combined list
    all_filtered.append(filtered)

    # save a filtered variable view
    output_file = os.path.join(
        output,
        os.path.basename(file).replace(".xlsx", "_Filtered.xlsx")
    )

    filtered.to_excel(output_file, index=False)

    print(f"Saved: {os.path.basename(output_file)}")

# Combine all surveys into one Excel file
if all_filtered:

    combined = pd.concat(all_filtered, ignore_index=True)

    # Sort alphabetically by Label
    combined = combined.sort_values(by="Label", ignore_index=True)

    combined_output = output / "Combined_Selected_Variables.xlsx"

    combined.to_excel(combined_output, index=False)

    print(f"Combined file saved: {combined_output.name}")

else:
    print("No matching variables were found.")
    
print("Finished")






    
