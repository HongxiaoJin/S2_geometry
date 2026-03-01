import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ------------------------------------------------------------
# Helper: compute RAA
# ------------------------------------------------------------
def compute_raa(saa, vaa):
    """
    Compute relative azimuth angle (degrees in [0, 360)).
    Convention: RAA = (SAA - VAA) mod 360
    """
    raa = vaa - saa
    return np.mod(raa, 360.0)


# ------------------------------------------------------------
# Main: angle inset plot
# ------------------------------------------------------------
def plot_angle_insets(
    csv_path,
    sza_col="obs_SZA",
    vza_col="obs_VZA",
    saa_col="obs_SAA",
    vaa_col="obs_VAA",
    bins=24,
    rbins=36,
    width=3.2,
    height=1.2,
    dpi=300,
    out_path=None,
    save_pdf=False,
):
    """
    Create compact inset-style histograms:
        - SZA histogram
        - VZA histogram
        - RAA polar histogram
    """

    csv_path = Path(csv_path)
    df = pd.read_csv(csv_path, encoding="utf-8-sig")

    # Convert to numeric safely
    for col in [sza_col, vza_col, saa_col, vaa_col]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=[sza_col, vza_col, saa_col, vaa_col])

    sza = df[sza_col].to_numpy()
    vza = df[vza_col].to_numpy()
    saa = df[saa_col].to_numpy()
    vaa = df[vaa_col].to_numpy()

    raa = compute_raa(saa, vaa)

    # ------------------------------------------------------------
    # Styling (journal compact)
    # ------------------------------------------------------------
    plt.rcParams.update({
        "font.size": 6,
        "axes.labelsize": 6,
        "xtick.labelsize": 5,
        "ytick.labelsize": 5,
        "axes.linewidth": 0.6,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "xtick.major.size": 2.5,
        "ytick.major.size": 2.5,
    })

    fig = plt.figure(figsize=(width, height), constrained_layout=True)
    gs = fig.add_gridspec(1, 3, wspace=0.15)

    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[0, 2], projection="polar")

    # ------------------------------------------------------------
    # SZA histogram
    # ------------------------------------------------------------
    ax1.hist(sza, bins=bins)
    ax1.set_title("SZA", pad=1)
    ax1.set_xlabel("deg", labelpad=0.5)
    ax1.set_ylabel("")
    ax1.tick_params(pad=1)

    # ------------------------------------------------------------
    # VZA histogram
    # ------------------------------------------------------------
    ax2.hist(vza, bins=bins)
    ax2.set_title("VZA", pad=1)
    ax2.set_xlabel("deg", labelpad=0.5)
    ax2.set_ylabel("")
    ax2.tick_params(pad=1)

    # ------------------------------------------------------------
    # RAA polar histogram
    # ------------------------------------------------------------
    theta = np.deg2rad(raa)
    counts, edges = np.histogram(theta, bins=rbins, range=(0, 2*np.pi))
    widths = np.diff(edges)

    ax3.bar(edges[:-1], counts, width=widths, align="edge")
    ax3.set_title("RAA", pad=2)
    ax3.set_theta_zero_location("N")
    ax3.set_theta_direction(-1)
    ax3.set_yticklabels([])
    ax3.tick_params(pad=0.5)

    # ------------------------------------------------------------
    # Save
    # ------------------------------------------------------------
    if out_path is None:
        out_png = csv_path.with_name(csv_path.stem + "_angles_inset.png")
    else:
        out_png = Path(out_path)

    fig.savefig(out_png, dpi=dpi, bbox_inches="tight", pad_inches=0.02)

    if save_pdf:
        fig.savefig(out_png.with_suffix(".pdf"),
                    bbox_inches="tight", pad_inches=0.02)

    plt.close(fig)

    return out_png

def generate_polar_plot(csv_path, site_id, out_path=None):

    df = pd.read_csv(csv_path)

    MONTH_COLORS = {
        1: "#E0201A", 2: "#FF1B71", 3: "#572D86", 4: "#5A4FCE",
        5: "#2569E6", 6: "#1A8F9C", 7: "#17AB70", 8: "#C3D71A",
        9: "#FFED00", 10: "#FDA206", 11: "#FB6221", 12: "#ED3E15"
    }

    df['datetime_utc'] = pd.to_datetime(df['datetime_utc'], errors='coerce')
    df = df.dropna(subset=['datetime_utc'])

    for col in ['obs_SAA','obs_SZA','obs_VAA','obs_VZA']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna(subset=['obs_SAA','obs_SZA','obs_VAA','obs_VZA'])
    df = df.drop_duplicates(subset=['datetime_utc','satellite'])

    df['month'] = df['datetime_utc'].dt.month
    df['month_color'] = df['month'].map(MONTH_COLORS)

    df['SAA_rad'] = np.radians(df['obs_SAA'])
    df['VAA_rad'] = np.radians(df['obs_VAA'])

    fig = plt.figure(figsize=(3.94, 3.94))
    ax = fig.add_subplot(111, polar=True)

    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)

    ax.scatter(df['VAA_rad'], df['obs_VZA'],
               c='black', alpha=0.6, s=10)

    ax.scatter(df['SAA_rad'], df['obs_SZA'],
               c=df['month_color'],
               edgecolors='k',
               linewidths=0.3,
               alpha=0.9,
               s=10)

    ax.set_rlim(0, 90)
    ax.set_title(f"Sun–Sensor Geometry\n{site_id}")

    if out_path is None:
        out_path = f"{site_id}_sun_sensor_geometry.pdf"

    plt.savefig(out_path, bbox_inches="tight")
    plt.close()