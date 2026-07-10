# abaqus2ann

Utilities and examples for developing ANN-based constitutive-model workflows and preparing Abaqus-oriented deployment scripts.

## Repository Layout

```text
abaqus2ann/
├── examples/              # Small runnable examples and templates
├── src/                   # Reusable Python package code
├── requirements.txt       # Python dependencies
└── README.md
```

## Environment

Create a Python environment and install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Typical Data Columns

Tabular datasets used by the examples generally follow this structure:

- `strain`
- `strain_rate`
- `temperature`
- `stress`

## Quick Check

Run the example template with a CSV or Excel file:

```bash
python examples/tabular_dataset_template.py path/to/data.csv
```

The script validates required columns and constructs a simple feature/target split for downstream modeling.
