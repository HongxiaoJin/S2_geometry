"""
e.g. linux
python scripts/download_timeseries.py \
    --site SE-St1 \
    --lat 68.3541 \
    --lon 19.0503 \
    --out data/SE-St1.csv
windows    
python -m scripts.download_timeseries --site SE-St1 --lat 68.3541 --lon 19.0503 --out data/SE-St1.csv 
"""
import argparse
from s2geom.gee_download import initialize_ee, download_point_timeseries

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--site", required=True)
    parser.add_argument("--lat", type=float, required=True)
    parser.add_argument("--lon", type=float, required=True)
    parser.add_argument("--start", default="2016-01-01")
    parser.add_argument("--end", default="2025-12-31")
    parser.add_argument("--out", required=True)

    args = parser.parse_args()

    initialize_ee()

    download_point_timeseries(
        args.site,
        args.lat,
        args.lon,
        args.start,
        args.end,
        args.out
    )

if __name__ == "__main__":
    main()