''''
NSA Mass-Size Relation Analysis

Goal:

Study the relationship between stellar mass and galaxy size for nearby 
galaxies in the NASA-Sloan Atlas (NSA).

Planned steps :
1. Load NSA FITS file 
2. Inspect column names and units
3. Identify stellar mass and size columns
4. Clean data (remove invalid values)
5. Plot log (Stellar mass) vs log(size)

'''
from astropy.io import fits
from astropy.table import Table
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u
import numpy as np
import matplotlib.pyplot as plt

DATA_PATH = "data/nsa_v1_0_1.fits"

print("Opening NSA FITS file...")

# Open FITS file
hdul = fits.open(DATA_PATH)

# Print HDU information
hdul.info()

# Load the main galaxy table (HDU 1)
data = Table(hdul[1].data)

print("\nNumber of galaxies in NSA catalog:")
print(len(data))

print("\nFirst 30 column names:")
for col in data.colnames[:30]:
    print(col)

print("\n=== Stellar mass related columns ===")
for col in data.colnames:
    if "MASS" in col.upper() or "MSTAR" in col.upper():
        print(col)

print("\n=== Galaxy size related columns ===")
for col in data.colnames:
    key = col.upper()
    if ("TH50" in key or "R50" in key or "PETRO" in key or "SERSIC" in key):
        print(col)

mass = data["SERSIC_MASS"]

print("\n=== SERSIC_MASS sanity check ===")
print("Min:", np.nanmin(mass))
print("Max:", np.nanmax(mass))
print("Median:", np.nanmedian(mass))

size = data["SERSIC_TH50"]

print("\n ==== SERSIC_TH50 sanity check ===")
print("Min:", np.nanmin(size))
print("Max:", np.nanmax(size))
print("Median:", np.nanmedian(size))

# Quality cuts
good = (
    (data["SERSIC_OK"]== 1) &
    np.isfinite(data["SERSIC_MASS"]) &
    np.isfinite(data["SERSIC_TH50"]) &
    (data["SERSIC_MASS"] > 0) &
    (data["SERSIC_TH50"] > 0)
)

print("\nNumber of galaxies before cuts:", len(data))
print("Number of galaxies after cuts:", np.sum(good))

# Cosmology (Standard)

cosmo = FlatLambdaCDM(H0 = 70, Om0 = 0.3)

# Extract clean sample

mass = data["SERSIC_MASS"][good]
size_arcsec = data["SERSIC_TH50"][good]
z = data["Z"][good]

# Convert mass to log10

logM = np.log10(mass)

# Convert size from arcsec to kpc

ang_diam_dist = cosmo.angular_diameter_distance(z)
size_kpc = (size_arcsec * u.arcsec).to(u.rad).value * ang_diam_dist.to(u.kpc).value

#Minimum physical size cut 

size_cut = size_kpc > 0.5 #kpc

# Final cleaned sample

logM_clean = logM[size_cut]
size_kpc_clean = size_kpc[size_cut]

print("\nAfter size cut (Re > 0.5 kpc):")
print("Number of galaxies :", len(logM_clean))


#Plot

plt.figure(figsize=(6, 5))
plt.scatter(logM_clean, size_kpc_clean, s=1, alpha=0.1)
plt.xlabel(r"$\log_{10}(M_\star/M_\odot)$")
plt.ylabel(r"$R_e$ [kpc]")
plt.yscale("log")
plt.title("Galaxy Stellar Mass-Size Relation (NSA)\n$R_e > 0.5$ kpc")
plt.tight_layout()
plt.savefig("mass_size_relation_cleaned.png", dpi=300)
plt.close()



# Close the file
hdul.close()