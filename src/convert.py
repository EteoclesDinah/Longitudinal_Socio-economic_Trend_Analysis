import pyreadstat
import pandas as pd
from pathlib import Path

# -------------------------
# Read SPSS file
# -------------------------
# path to .sav file
script_dir = Path(__file__).resolve().parent
sav_file = script_dir.parent / "data" / "raw" / "Household Recode files" / "NPHR81FL.SAV"

df, meta = pyreadstat.read_sav(sav_file)

rows = []

for var in meta.column_names:

    # Variable type
    if meta.readstat_variable_types[var] == "string":
        var_type = "String"
    else:
        var_type = "Numeric"

    # Variable width
    width = meta.variable_storage_width.get(var, "")

    # Decimals
    decimals = meta.variable_display_width.get(var, "")

    # Label
    label = meta.column_names_to_labels.get(var, "")

    # Value Labels
    value_labels = meta.variable_value_labels.get(var, {})
    if value_labels:
        values = "; ".join(
            f"{k} = {v}" for k, v in value_labels.items()
        )
    else:
        values = ""

    # Missing
    missing = meta.missing_ranges.get(var, "")

    # Measure
    measure = meta.variable_measure.get(var, "")

    # Alignment
    alignment = meta.variable_alignment.get(var, "")

    rows.append({
        "Name": var,
        "Type": var_type,
        "Width": width,
        "Decimals": "",
        "Label": label,
        "Values": values,
        "Missing": missing,
        "Columns": meta.variable_display_width.get(var, ""),
        "Align": alignment,
        "Measure": measure,
        "Role": "Input"
    })

variable_view = pd.DataFrame(rows)

# Export
variable_view.to_excel(
    sav_file.with_name(sav_file.stem + "_VariableView.xlsx"),
    index=False
)

print("Variable View exported successfully.")