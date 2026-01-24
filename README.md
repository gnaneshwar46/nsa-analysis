# NSA Galaxy Mass–Size Relation Analysis

## Overview

This project explores how **galaxy size scales with stellar mass** in the nearby universe using data from the **NASA–Sloan Atlas (NSA)**.

The goal is not just to reproduce the well-known mass–size relation, but to understand **why it looks the way it does**, and how galaxy structure and morphology influence it.

The analysis follows a clean, reproducible workflow starting from the raw survey catalog and ending with physically interpretable results.

---

## Data

- **Catalog**: NASA–Sloan Atlas (NSA), SDSS DR17  
- **Total galaxies**: 641,409  
- **Final working sample (after cuts)**: 632,495 galaxies  

### Key quantities used

- **Stellar mass**: `SERSIC_MASS`  
- **Galaxy size**: `SERSIC_TH50` (Sérsic half-light radius)  
- **Redshift**: `Z`  
- **Morphology proxy**: `SERSIC_N` (Sérsic index)  

Sérsic-based measurements are used throughout to ensure that mass and size are defined consistently.

---

## Methodology

### Data cleaning and selection

The following minimal, physically motivated cuts are applied:

- successful Sérsic fits (`SERSIC_OK == 1`)
- finite and positive stellar mass and size
- a minimum physical size cut  
 $$\( R_e > 0.5 \,\mathrm{kpc} \)$$
  which removes unresolved systems and pathological fits

### Physical units

- Stellar mass is converted to  
  $$\( \log_{10}(M_\star / M_\odot) \)$$
- Angular sizes are converted from arcseconds to kiloparsecs using a flat ΛCDM cosmology  
  ($$\( H_0 = 70 \), \( \Omega_m = 0.3 \)$$)

### Fitting approach

The mass–size relation is modeled as:

$$\[
\log R_e = \alpha (\log M_\star - 10) + \beta
\]$$

where:
- \($\alpha$\) is the slope
- \($\beta$\) is the normalization at \($10^{10} M_\odot$\)

---

## Results

### Global mass–size relation

For the full galaxy sample, the best-fit relation is:

- **Slope**: \($\alpha = 0.248$\)  
- **Normalization**: \($\beta = 0.627$\)  
  (corresponding to \($R_e \approx 4.2 \,\mathrm{kpc}$\) at \($10^{10} M_\odot$\))  
- **Scatter**:$\sim 0.33$ dex in \( $\log R_e$\)

The shallow slope and large scatter reflect the fact that this relation mixes galaxies with different formation histories.

---

### Mass–size relation by morphology

Galaxies are separated using the Sérsic index:

- **Disk-like**: \($n < 2.5$\)  
- **Spheroid-like**: \( $n \ge 2.5$ \)

| Population | Number | Slope \( $\alpha$ \) |
|----------|--------|------------------|
| Disk-like | 306,870 | 0.264 |
| Spheroid-like | 325,625 | 0.428 |

Disk galaxies follow a shallower relation, consistent with gradual, inside-out growth.  
Spheroid-dominated galaxies show a steeper relation, consistent with merger-driven size evolution.

This split explains a large fraction of the scatter seen in the global relation.

---

## Physical Interpretation

The results support a picture in which:

- disk galaxies grow steadily through star formation and gas accretion
- spheroidal systems grow primarily through mergers, which increase size more efficiently than mass

The observed mass–size relation is therefore not universal, but the result of combining these two distinct growth channels.

---

## Relation to the Literature

The measured slopes and trends are consistent with previous studies of nearby galaxies, including:

- Shen et al. (2003)
- van der Wel et al. (2014)
- Lange et al. (2015)

This project independently reproduces these results using a large, homogeneous local-universe sample.

---

## Repository Structure

```text
nsa-analysis/
├── data/
│   └── nsa_v1_0_1.fits
├── scripts/
│   └── explore_nsa.py
├── mass_size_relation_fit.png
├── mass_size_relation_morphology.png
├── .gitignore
└── README.md
```