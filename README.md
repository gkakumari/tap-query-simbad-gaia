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
pip install -r requirements.txt ```
## 📂 Input Format
Prepare a text file called full_str that contains a column named source_id with Gaia DR3 source IDs Example:
```
source_id
123456789012345678
987654321098765432
...
```
This file is loaded in the notebook and passed to the query function.

## 🚀 How to Run
Clone the repo or download the files to your machine

Place your full_str file in the same directory

Open the notebook: tap_query_git.ipynb

Run all cells to:

## ✅ Load your Gaia DR3 IDs

## 🔍 Query SIMBAD (skipping IDs that don’t exist)

## 💾 Save grouped results to ful_star_rslts.xlsx
## 📁 Output
After running the notebook, you’ll get:

ful_star_rslts.xlsx — an Excel file with metadata from SIMBAD, including:

Gaia DR3 ID

SIMBAD main ID

Object type and label

Spectral type

Teff, log(g), and bibcodes

## 🔄 Customization
## 🛠 Want to query different data from SIMBAD?
Modify the ADQL query in sambad_query.py inside the function query_simbad_for_sources()

## 🗂 Want to use a different catalog?
Change the id_prefix parameter from "Gaia DR3" to your desired catalog prefix.

## 🧑‍💻 Author
Developed by Goutham Anitha Kumari
(Feel free to fork, use, modify, or build upon this!)

