"""
Cycloidal Drive Visualizer & Calculator
Visualizes cycloidal disc profiles and computes key design parameters
Usage: python cycloid_visualizer.py
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Circle
from matplotlib.widgets import Slider, Button
import warnings
warnings.filterwarnings('ignore')

# Color palette
BG        = "#0f1117"
PANEL     = "#1a1d27"
ACCENT    = "#4fc3f7"  
ACCENT2   = "#ff6b6b"  
GREY_MID  = "#3a3f52"
GREY_TEXT = "#8892a4"
WHITE     = "#e8edf4"
GREEN     = "#69db7c"
YELLOW    = "#ffd43b"

# Return X, Z arrays for the cycloidal disc profile
def compute_profile(N, Rr, R, E, n_points=2000):
    t = np.linspace(1e-6, 2 * np.pi, n_points)
    denom = (R / (E * N)) - np.cos((1 - N) * t)
    psi = -np.arctan(np.sin((1 - N) * t) / denom)
    X = R * np.cos(t) - Rr * np.cos(t - psi) - E * np.cos(N * t)
    Z = -R * np.sin(t) + Rr * np.sin(t - psi) + E * np.sin(N * t)
    return X, Z, psi

# Return dict of all engineering metrics
def compute_metrics(N, Rr, R, E):
    n_lobes    = N - 1
    ratio      = N - 1

    X, Z, psi = compute_profile(N, Rr, R, E)
    r = np.sqrt(X**2 + Z**2)
    max_r      = r.max()
    min_r      = r.min()
    lobe_depth = max_r - min_r
    req_bore   = 2 * (max_r + E)

    max_pa_deg  = np.degrees(np.max(np.abs(psi)))
    mean_pa_deg = np.degrees(np.mean(np.abs(psi)))

    E_over_Rr      = E / Rr
    pin_arc_spacing = 2 * np.pi * R / N

    return {
        "ratio":           ratio,
        "n_lobes":         n_lobes,
        "max_dia":         2 * max_r,
        "min_dia":         2 * min_r,
        "lobe_depth":      lobe_depth,
        "req_bore":        req_bore,
        "max_pa":          max_pa_deg,
        "mean_pa":         mean_pa_deg,
        "E_over_Rr":       E_over_Rr,
        "pin_arc_spacing": pin_arc_spacing,
        "X": X, "Z": Z,
        "min_wall": pin_arc_spacing - 2*Rr,
    }

# Return formatted parametric equation string with values substituted
def format_equation_block(N, Rr, R, E):
    lines = [
        "─" * 58,
        "  PARAMETRIC EQUATIONS  (Onshape-compatible format)",
        "─" * 58,
        "",
        "  Variables:",
        f"    #R  = {R:<8} mm   (pin-center circle radius)",
        f"    #N  = {N}       (number of pins / rollers)",
        f"    #E  = {E} mm   (eccentricity)",
        f"    #Rr = {Rr} mm  (roller radius)",
        f"    #t  = parameter, 0 → 360 deg",
        "",
        "  X equation:",
        "    (#R * cos(#t deg))",
        "    - (#Rr * cos(#t deg - (-atan(",
        "        sin((1-#N) * #t deg) /",
        "        ((#R / (#E * #N)) - cos((1-#N) * #t deg))",
        "      ))))",
        "    - (#E * cos(#N * #t deg))",
        "",
        "  Z equation:",
        "    (-#R * sin(#t deg))",
        "    + (#Rr * sin(#t deg - (-atan(",
        "        sin((1-#N) * #t deg) /",
        "        ((#R / (#E * #N)) - cos((1-#N) * #t deg))",
        "      ))))",
        "    + (#E * sin(#N * #t deg))",
        "",
        "─" * 58,
    ]
    return "\n".join(lines)

# Print full engineering report to terminal
def print_report(N, Rr, R, E):
    m = compute_metrics(N, Rr, R, E)

    print("\n" + "=" * 58)
    print("  CYCLOIDAL DRIVE — ENGINEERING REPORT")
    print("=" * 58)
    print(f"  Inputs:  N={N}  Rr={Rr}mm  R={R}mm  E={E}mm")
    print("=" * 58)

    print("\n  ── REDUCTION RATIO ──────────────────────────────────")
    print(f"  Lobes on disc    : {m['n_lobes']}")
    print(f"  Reduction ratio  : {m['ratio']}:1")

    print("\n  ── DISC GEOMETRY ────────────────────────────────────")
    print(f"  Max disc diameter: {m['max_dia']:.3f} mm")
    print(f"  Min disc diameter: {m['min_dia']:.3f} mm")
    print(f"  Lobe depth       : {m['lobe_depth']:.3f} mm")
    print(f"  Required bore Ø  : {m['req_bore']:.3f} mm  (2 x (lobe tip radius + E))")

    print("\n  ── PRESSURE ANGLES ──────────────────────────────────")
    print(f"  Max pressure angle : {m['max_pa']:.2f}°")
    print(f"  Mean pressure angle: {m['mean_pa']:.2f}°")
    #status = "✓ Good" if m['max_pa'] < 25 else ("⚠ Marginal" if m['max_pa'] < 30 else "✗ High — review")
    #print(f"  Status             : {status}  (target < 25°)")

    print("\n  ── ECCENTRICITY / ROLLER RATIO ──────────────────────")
    print(f"  E / Rr = {m['E_over_Rr']:.3f}")
    #if m['E_over_Rr'] < 0.3:
    #    rating = "✗ Too low — shallow lobes, poor contact"
    #elif m['E_over_Rr'] < 0.5:
    #    rating = "✓ Conservative — efficient, compact"
    #elif m['E_over_Rr'] < 0.8:
    #    rating = "✓ Moderate — good balance"
   #else:
    #    rating = "⚠ High — check pressure angle and bore size"
    #print(f"  Rating : {rating}  (recommended: 0.3–0.8)")

    print("\n  ── PIN / ROLLER GEOMETRY ────────────────────────────")
    print(f"  Pin-center circle Ø : {2*R:.1f} mm")
    print(f"  Pin arc spacing     : {m['pin_arc_spacing']:.3f} mm")
    print(f"  Min wall between pins: {m['min_wall']:.3f} mm")

    print("\n" + format_equation_block(N, Rr, R, E))

# Draw cycloidal disc, pins, bore, and annotations on ax
def draw_plot(ax, m, N, Rr, R, E, crank_deg=0):
    ax.clear()
    ax.set_facecolor(BG)

    X, Z = m["X"], m["Z"]

    # Apply eccentricity offset to show real operating position
    crank_rad = np.radians(crank_deg)
    disc_rot = -crank_rad / (N - 1)          # counter-rotation: 1/ratio of crank angle
    cos_r, sin_r = np.cos(disc_rot), np.sin(disc_rot)
    Xr = X * cos_r - Z * sin_r               # rotate profile around disc center
    Zr = X * sin_r + Z * cos_r
    ox, oz = E*np.cos(crank_rad), E*np.sin(crank_rad)
    Xo, Zo = Xr + ox, Zr + oz               # then translate by eccentricity

    # Housing bore (clearance envelope)
    bore_r = m["req_bore"] / 2
    bore_circle = Circle((0, 0), bore_r, fill=False,
                          edgecolor=GREY_MID, linewidth=1.2, linestyle="--")
    ax.add_patch(bore_circle)

    # Pin-center circle
    pc_circle = Circle((0, 0), R, fill=False,
                        edgecolor=GREY_TEXT, linewidth=0.8, linestyle=":")
    ax.add_patch(pc_circle)

    # Pins
    pin_angles = np.linspace(0, 2 * np.pi, N, endpoint=False)
    for a in pin_angles:
        px, py = R * np.cos(a), R * np.sin(a)
        pin = Circle((px, py), Rr, fill=True,facecolor=GREY_MID, edgecolor=WHITE, linewidth=0.8, alpha=0.85)
        ax.add_patch(pin)

    # Disc profile (offset position)
    ax.fill(Xo, Zo, color=ACCENT2, alpha=0.18)
    ax.plot(Xo, Zo, color=ACCENT2, linewidth=1.8, label="Cycloidal disc")

    # Centers
    ax.plot(0, 0, "+", color=WHITE, markersize=10, markeredgewidth=1.5, label="Housing center")
    ax.plot(ox, oz, "+", color=ACCENT, markersize=10, markeredgewidth=1.5, label=f"Disc center (offset {E}mm)")

    # Eccentricity arrow
    ax.annotate("", xy=(ox, oz), xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.2))

    # Labels
    lim = R + Rr + E + 4
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.tick_params(colors=GREY_TEXT, labelsize=7)
    for spine in ax.spines.values():
        spine.set_edgecolor(GREY_MID)

    # Legend
    leg = ax.legend(loc="upper right", fontsize=7,
                    facecolor=PANEL, edgecolor=GREY_MID, labelcolor=WHITE)

    # Annotations
    ax.set_title(f"Cycloidal Disc Profile  |  N={N}  Rr={Rr}mm  R={R}mm  E={E}mm",
                 color=WHITE, fontsize=9, pad=6)

    # Quick stats overlay
    stats = (f"Ratio {m['ratio']}:1  |  "
             f"Max PA {m['max_pa']:.1f}°  |  "
             f"E/Rr {m['E_over_Rr']:.2f}  |  "
             f"Bore Ø {m['req_bore']:.1f}mm")
    ax.set_xlabel(stats, color=GREY_TEXT, fontsize=7.5)

# Draw a text metrics panel
def draw_metrics_panel(ax, m):
    ax.clear()
    ax.set_facecolor(PANEL)
    ax.axis("off")

    # E/Rr color
    if m["E_over_Rr"] < 0.3 or m["E_over_Rr"] > 0.8:
        eratio_color = ACCENT2
    elif m["E_over_Rr"] <= 0.5:
        eratio_color = GREEN
    else:
        eratio_color = YELLOW

    # PA color
    pa_color = GREEN if m["max_pa"] < 25 else (YELLOW if m["max_pa"] < 30 else ACCENT2)

    y = 0.97
    def row(label, value, color=WHITE, bold=False):
        nonlocal y
        weight = "bold" if bold else "normal"
        ax.text(0.04, y, label, transform=ax.transAxes,
                color=GREY_TEXT, fontsize=8, va="top", family="monospace")
        ax.text(0.62, y, value, transform=ax.transAxes,
                color=color, fontsize=8, va="top", family="monospace", fontweight=weight)
        y -= 0.072

    def divider(label=""):
        nonlocal y
        ax.text(0.04, y, label, transform=ax.transAxes,
                color=GREY_MID, fontsize=7, va="top", family="monospace")
        y -= 0.055

    row("REDUCTION RATIO", f"{m['ratio']}:1", ACCENT, bold=True)
    row("Lobes on disc", f"{m['n_lobes']}")
    divider("── Disc Geometry ─────────────")
    row("Max disc Ø", f"{m['max_dia']:.2f} mm")
    row("Min disc Ø", f"{m['min_dia']:.2f} mm")
    row("Lobe depth", f"{m['lobe_depth']:.2f} mm")
    row("Required bore Ø", f"{m['req_bore']:.2f} mm", ACCENT)
    divider("── Pressure Angles ───────────")
    row("Max pressure angle", f"{m['max_pa']:.2f}°", pa_color, bold=True)
    row("Mean pressure angle", f"{m['mean_pa']:.2f}°", pa_color)
    divider("── E / Rr Ratio ──────────────")
    row("E / Rr", f"{m['E_over_Rr']:.3f}", eratio_color, bold=True)
    rating = ("Too low" if m["E_over_Rr"] < 0.3 else
              "Conservative" if m["E_over_Rr"] < 0.5 else
              "Moderate" if m["E_over_Rr"] < 0.8 else "High")
    #row("Rating", rating, eratio_color)
    divider("── Pin Geometry ──────────────")
    row("Pin arc spacing", f"{m['pin_arc_spacing']:.2f} mm")
    row("Min wall btw pins", f"{m['min_wall']:.2f} mm")

def main():
    # Initial values
    params = {"N": 10, "Rr": 2.5, "R": 36.5, "E": 1.25}

    # Figure layout
    fig = plt.figure(figsize=(14, 8), facecolor=BG)
    try:
        fig.canvas.manager.set_window_title("Cycloidal Drive Visualizer")
    except AttributeError:
        pass

    gs = gridspec.GridSpec(1, 2, width_ratios=[1.5, 1],
                           left=0.04, right=0.97, top=0.90, bottom=0.22, wspace=0.08)

    ax_plot    = fig.add_subplot(gs[0])
    ax_metrics = fig.add_subplot(gs[1])

    #ax_plot.set_facecolor(BG)
    #ax_metrics.set_facecolor(PANEL)

    # Sliders
    slider_specs = [
        # (label,  left,   bot,  valmin, valmax, valinit, valstep)
        ("N (pins)",    0.06, 0.145, 6,    20,    params["N"],  1),
        ("Rr (mm)",     0.06, 0.105, 0.5,  8.0,   params["Rr"], 0.25),
        ("R (mm)",      0.06, 0.065, 10,   80,    params["R"],  0.5),
        ("E (mm)",      0.06, 0.025, 0.25, 5.0,   params["E"],  0.125),
    ]

    sliders = {}
    for label, l, b, vmin, vmax, vinit, vstep in slider_specs:
        ax_s = fig.add_axes([l, b, 0.55, 0.028], facecolor=GREY_MID)
        s = Slider(ax_s, label, vmin, vmax, valinit=vinit, valstep=vstep,
                   color=ACCENT, initcolor=ACCENT)
        s.label.set_color(WHITE)
        s.label.set_fontsize(8)
        s.valtext.set_color(ACCENT)
        s.valtext.set_fontsize(8)
        sliders[label] = s

    # Crank angle slider (bottom right)
    ax_crank = fig.add_axes([0.7, 0.145, 0.27, 0.028], facecolor=GREY_MID)
    s_crank = Slider(ax_crank, "Crank (°) ", 0, 360, valinit=0, valstep=5,
                     color=YELLOW, initcolor=YELLOW)
    s_crank.label.set_color(WHITE)
    s_crank.label.set_fontsize(8)
    s_crank.valtext.set_color(YELLOW)
    s_crank.valtext.set_fontsize(8)

    # Print report button
    ax_btn = fig.add_axes([0.7, 0.065, 0.27, 0.04])
    btn = Button(ax_btn, "Print Report", color=GREY_MID, hovercolor=ACCENT)
    btn.label.set_color(WHITE)
    btn.label.set_fontsize(10)

    # Update function
    def update(val=None):
        N   = int(sliders["N (pins)"].val)
        Rr  = sliders["Rr (mm)"].val
        R   = sliders["R (mm)"].val
        E   = sliders["E (mm)"].val
        crank = s_crank.val

        m = compute_metrics(N, Rr, R, E)
        draw_plot(ax_plot, m, N, Rr, R, E, crank_deg=crank)
        draw_metrics_panel(ax_metrics, m)
        fig.canvas.draw_idle()

    def on_print(event):
        N   = int(sliders["N (pins)"].val)
        Rr  = sliders["Rr (mm)"].val
        R   = sliders["R (mm)"].val
        E   = sliders["E (mm)"].val
        print_report(N, Rr, R, E)

    for s in sliders.values():
        s.on_changed(update)
    s_crank.on_changed(update)
    btn.on_clicked(on_print)

    # Initial draw
    m = compute_metrics(**params)
    draw_plot(ax_plot, m, **params)
    draw_metrics_panel(ax_metrics, m)

    # Title
    fig.text(0.5, 0.985, "Cycloidal Drive Visualizer",
             ha="center", va="top", color=WHITE, fontsize=14, fontweight="bold")
    fig.text(0.5, 0.955, "Adjust sliders to explore geometry · Crank° rotates disc to operating position",
             ha="center", va="top", color=GREY_TEXT, fontsize=8)

    plt.show()

if __name__ == "__main__":
    main()