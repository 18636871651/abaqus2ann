# Hot-compression flow-curve data

This directory contains the experimental workbook and its processed HDF5
representation for the Gleeble ANN constitutive-model workflow.

## Files and experimental conditions

- `raw/gleeble_data.xlsx`: source workbook, with one sheet per temperature.
- `processed/gleeble_data.h5`: 24 extracted flow curves containing 11,870 points.
- Temperatures: 800, 850, 900, 950, 1000, and 1050 degrees Celsius.
- Strain rates: 0.01, 0.1, 1, and 10 s^-1 at each temperature.
- Strain is dimensionless; stress is expressed in MPa.

The workbook stores strain/stress column pairs. Strain columns have headers
starting with `epsilon`; the adjacent stress-column header identifies the strain
rate. Some sheets contain additional column pairs. The processed representation
retains the eligible pair with the most valid points for each strain rate.

## Processing and HDF5 layout

Extraction converts each pair to numeric values, removes pairs containing
non-finite values, sorts by strain, and removes duplicate strain coordinates,
retaining the first occurrence in the sorted array. Column pairs must contain
at least 30 cleaned points to be eligible. This extraction does not smooth the
stress values or apply a terminal-unloading cutoff.

The HDF5 file contains:

- `/T`: unique temperatures in degrees Celsius.
- `/depsp`: unique strain rates in s^-1.
- `/Data/T{temperature}_deps{strain_rate}`: an N-by-2 array, with strain in
  column 0 and stress in column 1.
- Each curve dataset has `T` and `depsp` attributes identifying its conditions.
- `/Data` has a `Number` attribute recording the number of curves.

All 24 processed arrays were checked against extraction from the included
workbook and match exactly. These files provide source data, not model
predictions or a fixed train/validation/test split. Reproducing a particular
experiment also requires its preprocessing, split, and training configuration.
Multiple points on a curve should not be treated as independent experimental
curves when defining grouped validation.

## Reading the processed data

```python
import h5py

with h5py.File("data/processed/gleeble_data.h5", "r") as data:
    for curve_id, curve in data["Data"].items():
        strain = curve[:, 0]
        stress_mpa = curve[:, 1]
        temperature_c = float(curve.attrs["T"])
        strain_rate = float(curve.attrs["depsp"])
        print(curve_id, len(strain), temperature_c, strain_rate)
```
