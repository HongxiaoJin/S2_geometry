"""
Example:

python -m scripts.plot_geometry data/SE-St1.csv --pdf
"""

import argparse
from pathlib import Path
from s2geom.plotting import generate_polar_plot


def main():

    parser = argparse.ArgumentParser(
        description="Generate Sentinel-2 sun–sensor polar geometry plot."
    )

    parser.add_argument("csv", help="Input CSV file")
    parser.add_argument(
        "--site",
        default=None,
        help="Site ID (default: inferred from filename)",
    )
    parser.add_argument(
        "--pdf",
        action="store_true",
        help="Save as PDF (default: PNG)",
    )

    args = parser.parse_args()

    csv_path = Path(args.csv)

    if not csv_path.exists():
        raise FileNotFoundError(csv_path)

    # Infer site_id from filename if not provided
    site_id = args.site or csv_path.stem.split("_")[-1]

    # Output path
    suffix = ".pdf" if args.pdf else ".png"
    out_path = csv_path.with_name(f"{site_id}_sun_sensor_geometry{suffix}")

    generate_polar_plot(
        csv_path=csv_path,
        site_id=site_id,
        out_path=out_path,
    )

    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()