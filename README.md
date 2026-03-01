Sentinel-2 Sun–Sensor Geometry Time Series Toolkit

A lightweight, reproducible Python toolkit to:

Download Sentinel-2 surface reflectance (SR) time series for point locations

Extract sun–sensor geometry (SZA, SAA, VZA, VAA)

Generate ordered CSV datasets

Produce publication-ready polar geometry plots

Create compact BRDF angle histograms

Designed for ICOS flux sites, BRDF studies, and vegetation reflectance normalization research.

📦 Repository Structure
sentinel2-geometry-timeseries/
│
├── README.md
├── LICENSE
├── requirements.txt
├── setup.py
│
├── data/                    (ignored via .gitignore)
│   └── example/
│
├── outputs/                 (ignored)
│
├── configs/
│   └── sites.csv
│
├── scripts/
│   ├── download_timeseries.py
│   ├── plot_geometry.py
│   └── reorder_csv.py
│
└── s2geom/
    ├── __init__.py
    ├── ee_download.py
    ├── plotting.py
    └── utils.py
🚀 Installation
1️⃣ Clone repository
git clone https://github.com/yourusername/sentinel2-geometry-timeseries.git
cd sentinel2-geometry-timeseries
2️⃣ Create environment

Recommended (conda):

conda create -n s2geom python=3.11
conda activate s2geom
pip install -r requirements.txt

Optional but recommended (editable install):

pip install -e .
🌍 Google Earth Engine Setup

This toolkit uses Google Earth Engine (GEE).

1️⃣ Authenticate
earthengine authenticate
2️⃣ Set your Cloud Project
earthengine set_project YOUR_PROJECT_ID

Make sure:

Earth Engine API is enabled in Google Cloud Console

Your Google account has Earth Engine access

The selected project belongs to your account

Test initialization:

import ee
ee.Initialize(project="YOUR_PROJECT_ID")
print("Earth Engine ready")
📥 Download Sentinel-2 Time Series

Example for ICOS site SE-St1:

python -m scripts.download_timeseries \
    --site SE-St1 \
    --lat 68.3541 \
    --lon 19.0503 \
    --out data/SE-St1.csv
Output CSV columns

site_id

datetime_utc

datetime_local

satellite

system_index

obs_SZA, obs_SAA

obs_VZA, obs_VAA

Sentinel-2 reflectance bands (B01–B12, B8A)

SCL (scene classification)

Duplicate tile acquisitions are removed automatically.

📊 Generate Polar Geometry Plot

Simple CLI usage:

python -m scripts.plot_geometry data/SE-St1.csv --pdf

Output:

data/SE-St1_sun_sensor_geometry.pdf
Plot Characteristics

Radial axis: Zenith angle (0–90°)

Angular axis: Azimuth (North at top, clockwise)

Black markers: Sensor geometry

Month-colored markers: Solar geometry

Designed for publication-quality figures.

📈 Generate Angle Histograms (BRDF Insets)

Creates compact inset-style plots:

SZA histogram

VZA histogram

Polar histogram of RAA

python -m scripts.plot_angles data/SE-St1.csv --pdf

Relative azimuth is computed as:

RAA = (SAA − VAA) mod 360°
🧠 Scientific Context

Sentinel-2 provides:

Near-nadir view geometry (VZA typically < 10°)

Wide seasonal solar zenith range (0–85°)

Full azimuth sampling (0–360°)

This toolkit supports:

BRDF normalization studies

Geometry sampling assessment

Multi-site comparisons

Flux tower reflectance analysis

Time-series geometry diagnostics

🛠 Key Features

✔ Modular architecture
✔ Clean CLI interface
✔ Robust numeric handling
✔ Automatic duplicate removal
✔ Publication-ready figures
✔ Compatible with Sentinel-2A/B/C

🔄 Batch Processing Example

Windows:

for %f in (data\*.csv) do python -m scripts.plot_geometry %f --pdf

Linux/macOS:

for f in data/*.csv; do python -m scripts.plot_geometry "$f" --pdf; done
📑 Requirements

See requirements.txt.

Core dependencies:

earthengine-api

pandas

numpy

matplotlib

📄 License

See LICENSE.

👤 Author

Hongxiao Jin
Department of Physical Geography & Ecosystem Science
Lund University

📌 Citation

If you use this toolkit in scientific work, please cite:

Jin, H. (2026). Sentinel-2 Sun–Sensor Geometry Time Series Toolkit. GitHub repository.

(Consider archiving the repository on Zenodo to obtain a DOI.)

🔮 Future Extensions

Multi-site batch downloader

BRDF kernel diagnostics

NetCDF export

Integration with WIMBALS normalization workflow

Automated ICOS network processing

⚠️ Notes

Ensure Earth Engine authentication is active in your environment.

Output directories (data/, outputs/) are ignored by default via .gitignore.

Figures are optimized for scientific publication.

This README is suitable for:

Public GitHub repository

Linking in journal supplementary materials

Zenodo archiving

Sharing with collaborators

If you would like, I can now generate:

requirements.txt

setup.py

.gitignore

Zenodo metadata (.zenodo.json)

A DOI-ready citation block (APA / BibTeX)"# S2_geometry"  git init git add README.md git commit -m "first commit" git branch -M main git remote add origin https://github.com/HongxiaoJin/S2_geometry.git git push -u origin main .or push an existing repository from the command line git remote add origin https://github.com/HongxiaoJin/S2_geometry.git git branch -M main git push -u origin main
"# S2_geometry" 
