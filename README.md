# NSA Mass–Size Relation

This project studies the relationship between stellar mass and galaxy size
for nearby galaxies using the NASA–Sloan Atlas (NSA).

## Data
- Catalog: NASA–Sloan Atlas (NSA) v1.0.1
- SDSS Data Release: DR13 (legacy catalog)
- Redshift range: Local universe (low-z galaxies)
- File: `nsa_v1_0_1.fits`

> Note: Although newer SDSS data releases exist (e.g. DR17),
> the NSA catalog is a DR13-era product and is still widely used,
> including in MaNGA-based studies.

---

## Research Question
What is the relationship between stellar mass and galaxy size
for nearby galaxies in the local universe?

## Planned Analysis
1. Load NSA FITS catalog
2. Inspect available columns
3. Identify stellar mass and size indicators
4. Clean data (remove invalid values)
5. Plot and interpret the mass–size relation

## Project Structure

```text
nsa-analysis/
├── data/        # Raw data files (not tracked by Git)
├── scripts/     # Analysis scripts
├── notebooks/   # Exploratory notebooks (optional)
├── venv/        # Python virtual environment (ignored by Git)
├── README.md
└── .gitignore

## Tools
- Python 3
- Astropy
- NumPy
- Matplotlib
- Linux (WSL Ubuntu)
