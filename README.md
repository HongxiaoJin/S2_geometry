# Sentinel-2 Sun–Sensor Geometry Time Series Toolkit

A lightweight, reproducible Python toolkit to download Sentinel-2 surface reflectance (SR) time series for point locations, extract sun–sensor geometry (SZA, SAA, VZA, VAA), generate ordered CSV datasets, and produce publication-ready polar geometry plots and compact BRDF angle histograms.

Designed for ICOS flux sites, BRDF studies, and vegetation reflectance normalization research.

---

## 📦 Repository Structure

```
sentinel2-geometry-timeseries/
│
├── README.md
├── LICENSE
├── requirements.txt
├── setup.py
│
├── data/                    # (ignored via .gitignore)
│   └── example/
│
├── outputs/                 # (ignored)
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
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/HongxiaoJin/S2_geometry.git
cd S2_geometry
```

### 2. Create environment

Recommended (conda):

```bash
conda create -n s2geom python=3.11
conda activate s2geom
pip install -r requirements.txt
```

Optional but recommended (editable install):

```bash
pip install -e .
```

---

## 🌍 Google Earth Engine Setup

This toolkit uses the [Google Earth Engine (GEE)](https://earthengine.google.com/) Python API.

### Authenticate

```bash
earthengine authenticate
```

### Set your Cloud Project

```bash
earthengine set_project YOUR_PROJECT_ID
```

Before running, ensure that:
- The Earth Engine API is enabled in your Google Cloud Console
- Your Google account has Earth Engine access
- The selected project belongs to your account

**Test initialization:**

```python
import ee
ee.Initialize(project="YOUR_PROJECT_ID")
print("Earth Engine ready")
```

---

## 📥 Download Sentinel-2 Time Series

Example for ICOS site SE-St1:

```bash
python -m scripts.download_timeseries \
    --site SE-St1 \
    --lat 68.3541 \
    --lon 19.0503 \
    --out data/SE-St1.csv
```

### Output CSV Columns

| Column | Description |
|---|---|
| `site_id` | Site identifier |
| `datetime_utc` | Acquisition time (UTC) |
| `datetime_local` | Acquisition time (local) |
| `satellite` | Sentinel-2A/B/C |
| `system_index` | GEE system index |
| `obs_SZA`, `obs_SAA` | Solar zenith and azimuth angles |
| `obs_VZA`, `obs_VAA` | View zenith and azimuth angles |
| `B01`–`B12`, `B8A` | Sentinel-2 surface reflectance bands |
| `SCL` | Scene classification layer |

> Duplicate tile acquisitions are removed automatically.

---

## 📊 Generate Polar Geometry Plot

```bash
python -m scripts.plot_geometry data/SE-St1.csv --pdf
```

**Output:** `data/SE-St1_sun_sensor_geometry.pdf`

**Plot characteristics:**
- Radial axis: Zenith angle (0–90°)
- Angular axis: Azimuth angle (North at top, clockwise)
- Black markers: Sensor (view) geometry
- Month-colored markers: Solar geometry

---

## 📈 Generate Angle Histograms (BRDF Insets)

Creates compact inset-style plots including a SZA histogram, VZA histogram, and polar histogram of relative azimuth angle (RAA):

```bash
python -m scripts.plot_angles data/SE-St1.csv --pdf
```

Relative azimuth angle is computed as:

```
RAA = (SAA − VAA) mod 360°
```

---

## 🔄 Batch Processing

**Linux/macOS:**

```bash
for f in data/*.csv; do python -m scripts.plot_geometry "$f" --pdf; done
```

**Windows:**

```bat
for %f in (data\*.csv) do python -m scripts.plot_geometry %f --pdf
```

---

## 🧠 Scientific Context

Sentinel-2 provides near-nadir view geometry (VZA typically < 10°), a wide seasonal solar zenith range (0–85°), and full azimuth sampling (0–360°).

This toolkit supports BRDF normalization studies, geometry sampling assessment, multi-site comparisons, flux tower reflectance analysis, and time-series geometry diagnostics.

---

## 🛠 Key Features

- Modular architecture
- Clean CLI interface
- Robust numeric handling
- Automatic duplicate removal
- Publication-ready figures
- Compatible with Sentinel-2A/B/C

---

## 📑 Requirements

See `requirements.txt`. Core dependencies:

- `earthengine-api`
- `pandas`
- `numpy`
- `matplotlib`

---

## ⚠️ Notes

- Ensure Earth Engine authentication is active in your environment before running any scripts.
- Output directories (`data/`, `outputs/`) are excluded from version control via `.gitignore`.
- Figures are optimized for scientific publication.

---

## 🔮 Future Extensions

- Multi-site batch downloader
- BRDF kernel diagnostics
- NetCDF export
- Integration with WIMBALS normalization workflow
- Automated ICOS network processing

---

## 📄 License

See [LICENSE](LICENSE).

---

## 👤 Author

**Hongxiao Jin**  
Department of Physical Geography & Ecosystem Science  
Lund University

---

## 📌 Citation

If you use this toolkit in scientific work, please cite:

> Jin, H. (2026). *Sentinel-2 Sun–Sensor Geometry Time Series Toolkit*. GitHub repository. https://github.com/HongxiaoJin/S2_geometry

**BibTeX:**

```bibtex
@misc{jin2026s2geom,
  author    = {Jin, Hongxiao},
  title     = {Sentinel-2 Sun--Sensor Geometry Time Series Toolkit},
  year      = {2026},
  publisher = {GitHub},
  url       = {https://github.com/HongxiaoJin/S2_geometry}
}
```

> Consider archiving the repository on [Zenodo](https://zenodo.org) to obtain a citable DOI.
