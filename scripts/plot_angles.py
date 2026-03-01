# e.g. python -m scripts.plot_angles data/SE-St1.csv --pdf
import argparse
from s2geom.plotting import plot_angle_insets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv")
    parser.add_argument("--out", default=None)
    parser.add_argument("--pdf", action="store_true")

    args = parser.parse_args()

    plot_angle_insets(
        csv_path=args.csv,
        out_path=args.out,
        save_pdf=args.pdf,
    )


if __name__ == "__main__":
    main()