"""
NSA Mass–Size Relation Analysis

Goal:
Study the relationship between stellar mass and galaxy size for nearby
galaxies in the NASA–Sloan Atlas (NSA).

Steps:
1. Load NSA FITS file
2. Inspect catalog structure and columns
3. Identify stellar mass and size definitions
4. Apply quality and physical cuts
5. Convert to physical units
6. Measure and fit the mass–size relation
7. Save publication-quality figures
"""

# ----------------------------------------------------
# Imports
# ----------------------------------------------------
import os
from astropy.io import fits
from astropy.table import Table
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u

import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------------------
# Load data
# ----------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "nsa_v1_0_1.fits")

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(
        f"\nNSA FITS file not found at: {DATA_PATH}\n"
        "Please download the NSA catalog and place it inside the 'data/' directory.\n"
    )


print("Opening NSA FITS file...")
hdul = fits.open(DATA_PATH)
hdul.info()

data = Table(hdul[1].data)

print("\nNumber of galaxies in NSA catalog:", len(data))

# ----------------------------------------------------
# Column inspection (informational)
# ----------------------------------------------------

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
    if ("TH50" in key or "PETRO" in key or "SERSIC" in key):
        print(col)

# ----------------------------------------------------
# Sanity checks
# ----------------------------------------------------

mass = data["SERSIC_MASS"]
size = data["SERSIC_TH50"]

print("\n=== SERSIC_MASS sanity check ===")
print("Min:", np.nanmin(mass))
print("Max:", np.nanmax(mass))
print("Median:", np.nanmedian(mass))

print("\n=== SERSIC_TH50 sanity check ===")
print("Min:", np.nanmin(size))
print("Max:", np.nanmax(size))
print("Median:", np.nanmedian(size))

# ----------------------------------------------------
# Quality cuts
# ----------------------------------------------------

good = (
    (data["SERSIC_OK"] == 1) &
    np.isfinite(data["SERSIC_MASS"]) &
    np.isfinite(data["SERSIC_TH50"]) &
    (data["SERSIC_MASS"] > 0) &
    (data["SERSIC_TH50"] > 0)
)

print("\nNumber of galaxies before cuts:", len(data))
print("Number of galaxies after quality cuts:", np.sum(good))

#-----------------------------------------------------
# Sérsic index (morphology proxy)
sersic_n = data["SERSIC_N"][good]
# ----------------------------------------------------
# Physical conversions
# ----------------------------------------------------

cosmo = FlatLambdaCDM(H0=70, Om0=0.3)

mass = data["SERSIC_MASS"][good]
logM = np.log10(mass)

size_arcsec = data["SERSIC_TH50"][good]
z = data["Z"][good]

ang_diam_dist = cosmo.angular_diameter_distance(z)
size_kpc = (size_arcsec * u.arcsec).to(u.rad).value * ang_diam_dist.to(u.kpc).value

# ----------------------------------------------------
# Minimum physical size cut
# ----------------------------------------------------

size_cut = size_kpc > 0.5  # kpc

logM_clean = logM[size_cut]
size_kpc_clean = size_kpc[size_cut]

sersic_n_clean = sersic_n[size_cut]

# Morphology masks
disk = sersic_n_clean < 2.5
spheroid = sersic_n_clean >= 2.5

print("\nMorphology split:")
print("Disk-like galaxies (n < 2.5):", np.sum(disk))
print("Spheroid-like galaxies (n >= 2.5):", np.sum(spheroid))

print("\nAfter size cut (Re > 0.5 kpc):")
print("Number of galaxies:", len(logM_clean))

# ----------------------------------------------------
# Quantify the mass–size relation
# ----------------------------------------------------

logRe = np.log10(size_kpc_clean)

M0 = 10.0  # pivot mass
x = logM_clean - M0
y = logRe

alpha, beta = np.polyfit(x, y, 1)

# Prepare log sizes
logRe_clean = np.log10(size_kpc_clean)

M0 = 10.0 # same pivot

# Disk fit
x_disk = logM_clean[disk]-M0
y_disk = logRe_clean[disk]
alpha_d, beta_d = np.polyfit(x_disk, y_disk, 1)

# Spheroid fit
x_sph = logM_clean[spheroid]- M0
y_sph = logRe_clean[spheroid]
alpha_s, beta_s = np.polyfit(x_sph, y_sph, 1)

print("\nMass-size relation by morphology:")
print(f"Disk-like (n < 2.5): alpha = {alpha_d:.3f}, beta = {beta_d:.3f}")
print(f"Spheroid-like (n >= 2.5): alpha = {alpha_s:.3f}, beta = {beta_s:.3f}")

scatter = np.std(y - (alpha * x + beta))

print("\nMass–size relation fit:")
print(f"Slope alpha = {alpha:.3f}")
print(f"Intercept beta = {beta:.3f}  (at logM = {M0})")
print(f"Scatter (dex in log Re): {scatter:.3f}")

# ----------------------------------------------------
# Plot with fitted relation
# ----------------------------------------------------

xfit = np.linspace(x.min(), x.max(), 200)
yfit = alpha * xfit + beta

plt.figure(figsize=(6, 5))
plt.scatter(logM_clean, size_kpc_clean, s=1, alpha=0.1, label="Galaxies")
plt.plot(xfit + M0, 10**yfit, color="black", linewidth=2,
         label=rf"Fit: $\alpha={alpha:.2f}$")

plt.xlabel(r"$\log_{10}(M_\star/M_\odot)$")
plt.ylabel(r"$R_e$ [kpc]")
plt.yscale("log")
plt.title("Galaxy Stellar Mass–Size Relation (NSA)\n$R_e > 0.5$ kpc")
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig("mass_size_relation_fit.png", dpi=300)
plt.close()

#-----------------------------------------------------
# Generate fitted lines

xfit = np.linspace(logM_clean.min() - M0, logM_clean.max() - M0, 200)

yfit_disk = alpha_d * xfit + beta_d
yfit_sph = alpha_s * xfit + beta_s

plt.figure(figsize=(6, 5))
plt.scatter(logM_clean[disk], size_kpc_clean[disk], s=1, alpha=0.1, label="Disk-like (n < 2.5)")
plt.scatter(logM_clean[spheroid], size_kpc_clean[spheroid], s=1, alpha=0.1, label="Spheroid-like (n ≥ 2.5)")

plt.plot(xfit + M0, 10**yfit_disk, linewidth=2, label=rf"Disk fit ($\alpha={alpha_d:.2f}$)")
plt.plot(xfit + M0, 10**yfit_sph, linewidth=2, label=rf"Spheroid fit ($\alpha={alpha_s:.2f}$)")

plt.xlabel(r"$\log_{10}(M_\star/M_\odot)$")
plt.ylabel(r"$R_e$ [kpc]")
plt.yscale("log")
plt.title("Mass–Size Relation by Morphology (NSA)\n$R_e > 0.5$ kpc")
plt.legend(frameon=False, loc="upper left")
plt.tight_layout()
plt.savefig("mass_size_relation_morphology.png", dpi=300)
plt.close()

# ----------------------------------------------------
# Close file
# ----------------------------------------------------

hdul.close()
print("\nAnalysis complete.")
