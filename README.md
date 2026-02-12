# NSA Catalog Exploration and Preliminary Mass–Size Analysis

## Overview

This repository contains exploratory data analysis of the NASA-Sloan Atlas (NSA) catalog, focusing on validation, data inspection, and preliminary investigation of the stellar mass–size relation.

This project represents the initial exploratory phase prior to building a structured and reproducible scaling-relation analysis pipeline.

The fully modular and reproducible version of this analysis is available in:

👉 https://github.com/gnaneshwar46/galaxy-scaling-relations

---

## Purpose of This Repository

This project focuses on:

- Inspecting NSA catalog structure
- Validating key parameters (stellar mass, effective radius, Sérsic index)
- Performing initial quality cuts
- Generating preliminary mass–size visualizations

It serves as the exploratory foundation for subsequent structured analysis.

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
  \( R_e > 0.5 \,\mathrm{kpc} \)

which removes unresolved systems and pathological fits.

### Physical units

- Stellar mass is converted to  
  \( \log_{10}(M_\star / M_\odot) \)
- Angular sizes are converted from arcseconds to kiloparsecs using a flat ΛCDM cosmology  
  \( H_0 = 70 \), \( \Omega_m = 0.3 \)

### Fitting approach

The mass–size relation is modeled as:

\[
\log R_e = \alpha (\log M_\star - 10) + \beta
\]

where:

- \( \alpha \) is the slope  
- \( \beta \) is the normalization at \( 10^{10} M_\odot \)

---

## Preliminary Observations

### Global mass–size relation

For the full galaxy sample, the best-fit relation is:

- **Slope**: \( \alpha = 0.248 \)  
- **Normalization**: \( \beta = 0.627 \)  
  (corresponding to \( R_e \approx 4.2 \,\mathrm{kpc} \) at \( 10^{10} M_\odot \))  
- **Scatter**: \( \sim 0.33 \) dex in \( \log R_e \)

The shallow slope and substantial scatter indicate that the global relation combines galaxies with diverse structural properties and evolutionary histories.

---

### Morphology-separated mass–size relation

Galaxies are separated using the Sérsic index:

- **Disk-like**: \( n < 2.5 \)  
- **Spheroid-like**: \( n \ge 2.5 \)

| Population | Number | Slope \( \alpha \) |
|------------|--------|------------------|
| Disk-like | 306,870 | 0.264 |
| Spheroid-like | 325,625 | 0.428 |

The morphology-separated relations suggest that structural classification plays an important role in organizing the observed scaling behavior.

This exploratory result motivated a more structured investigation of morphology-dependent scaling relations.

---

## Exploratory Interpretation

The exploratory analysis suggests:

- Disk galaxies exhibit a shallower mass–size relation.
- Spheroid-dominated systems show a steeper slope.
- A significant fraction of the global scatter may be associated with structural differences.

These findings motivated the development of a modular and reproducible scaling-relation analysis pipeline.

---

## Relation to the Literature

The exploratory trends are broadly consistent with previous studies of nearby galaxies, including:

- Shen et al. (2003)
- van der Wel et al. (2014)
- Lange et al. (2015)

A more rigorous and structured comparison is carried out in the dedicated scaling-relation repository.

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
