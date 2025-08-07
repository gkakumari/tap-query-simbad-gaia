# SIMBAD TAP Query Tool for Gaia DR3 IDs

This project provides a Python-based tool for querying the [SIMBAD](http://simbad.u-strasbg.fr/simbad/) astronomical database using Gaia DR3 source IDs. It uses the ADQL (Astronomical Data Query Language) interface via PyVO's TAP client to extract astrophysical metadata such as object type, spectral type, effective temperature, and more.

---

## 📦 Features

- 🔍 Query **SIMBAD** using a list of **Gaia DR3** source IDs
- 📊 Retrieve key metadata:
  - Main identifier
  - Object type (`otype`)
  - Spectral type (`sptype`)
  - Effective temperature (`teff`)
  - Surface gravity (`log_g`)
- 🧼 Group and aggregate duplicate entries
- 💾 Export the final results to Excel

---

## 🧰 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
