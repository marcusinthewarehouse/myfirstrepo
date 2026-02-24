import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(10, 10))

units = 20

# ── Grid ──────────────────────────────────────────────
for i in range(units + 1):
    ax.axhline(i, color='#ddd', linewidth=0.5, zorder=0)
    ax.axvline(i, color='#ddd', linewidth=0.5, zorder=0)

# ── Box border ────────────────────────────────────────
ax.plot([0, units, units, 0, 0], [0, 0, units, units, 0], 'k-', linewidth=2)

# ── Jane axes (bottom & left) ────────────────────────
ax.set_xlim(-1.5, units + 1.5)
ax.set_ylim(-1.5, units + 1.5)
ax.set_xticks(range(0, units + 1, 2))
ax.set_yticks(range(0, units + 1, 2))
ax.set_xlabel("Jane's soft drinks (liters)", fontsize=13, fontweight='bold')
ax.set_ylabel("Jane's sandwiches", fontsize=13, fontweight='bold')
ax.tick_params(axis='both', labelsize=11)

# ── Bob axes (top & right) ───────────────────────────
ax2 = ax.secondary_xaxis('top')
ax2.set_xticks(range(0, units + 1, 2))
ax2.set_xticklabels([units - i for i in range(0, units + 1, 2)])
ax2.set_xlabel("Bob's soft drinks (liters)", fontsize=13, fontweight='bold', labelpad=10)
ax2.tick_params(labelsize=11)

ax3 = ax.secondary_yaxis('right')
ax3.set_yticks(range(0, units + 1, 2))
ax3.set_yticklabels([units - i for i in range(0, units + 1, 2)])
ax3.set_ylabel("Bob's sandwiches", fontsize=13, fontweight='bold', labelpad=10, rotation=270)
ax3.tick_params(labelsize=11)

# ── Origin labels ────────────────────────────────────
ax.text(-0.8, -0.8, 'Jane', fontsize=14, fontweight='bold', ha='center', va='center')
ax.text(units + 0.8, units + 0.8, 'Bob', fontsize=14, fontweight='bold', ha='center', va='center')

# ── Endowment point ─────────────────────────────────
ex, ey = 9, 8
ax.plot(ex, ey, 'o', color='#2a7f2a', markersize=12, zorder=10)
ax.annotate('Endowment (9, 8)', xy=(ex, ey), xytext=(ex + 0.5, ey + 1.2),
            fontsize=12, fontweight='bold', color='#000',
            arrowprops=dict(arrowstyle='->', color='#555', lw=1.2),
            zorder=10)

# ── Jane's indifference curve (U_J) ─────────────────
# Cobb-Douglas: U = x^a * y^(1-a)
# MRS = (a/(1-a))*(y/x) = 4 at (9,8)
# a/(1-a) = 4*9/8 = 4.5 => a = 9/11
aJ = 9.0 / 11.0
UJ = (ex ** aJ) * (ey ** (1 - aJ))

sd_j = np.linspace(0.3, 20, 500)
sw_j = (UJ / sd_j ** aJ) ** (1 / (1 - aJ))
mask_j = (sw_j >= 0) & (sw_j <= 20)
sd_j = sd_j[mask_j]
sw_j = sw_j[mask_j]

ax.plot(sd_j, sw_j, color='#1a6dcc', linewidth=3, label="Jane's IC  ($U_J$,  MRS = 4)", zorder=5)

# Label U_J on the curve
idx_j = len(sd_j) // 8
ax.text(sd_j[idx_j] - 0.5, sw_j[idx_j] + 0.6, '$U_J$', fontsize=16, fontweight='bold',
        fontstyle='italic', color='#1a6dcc', zorder=6)

# ── Bob's indifference curve (U_B) ──────────────────
# Bob's endowment from Bob's origin: (11, 12)
# MRS = (aB/(1-aB))*(12/11) = 3 => aB/(1-aB) = 33/12 = 2.75 => aB = 11/15
bex, bey = 11, 12
aB = 11.0 / 15.0
UB = (bex ** aB) * (bey ** (1 - aB))

sd_b = np.linspace(0.3, 20, 500)
sw_b = (UB / sd_b ** aB) ** (1 / (1 - aB))
mask_b = (sw_b >= 0) & (sw_b <= 20)
sd_b = sd_b[mask_b]
sw_b = sw_b[mask_b]

# Convert Bob's coords to Jane's frame (flip)
sd_b_jane = units - sd_b
sw_b_jane = units - sw_b

# Sort by x for proper plotting
sort_idx = np.argsort(sd_b_jane)
sd_b_jane = sd_b_jane[sort_idx]
sw_b_jane = sw_b_jane[sort_idx]

ax.plot(sd_b_jane, sw_b_jane, color='#cc3333', linewidth=3, label="Bob's IC  ($U_B$,  MRS = 3)", zorder=5)

# Label U_B on the curve
idx_b = len(sd_b_jane) * 7 // 8
ax.text(sd_b_jane[idx_b] + 0.3, sw_b_jane[idx_b] - 0.8, '$U_B$', fontsize=16, fontweight='bold',
        fontstyle='italic', color='#cc3333', zorder=6)

# ── Shade the lens (gains from trade) ────────────────
# Interpolate both curves onto a common x grid in the overlap region
x_min_overlap = max(sd_j.min(), sd_b_jane.min())
x_max_overlap = min(sd_j.max(), sd_b_jane.max())
x_common = np.linspace(x_min_overlap, x_max_overlap, 1000)

y_jane_interp = np.interp(x_common, sd_j, sw_j)
y_bob_interp = np.interp(x_common, sd_b_jane, sw_b_jane)

# Lens region: where Bob's curve is above Jane's curve
lens_mask = y_bob_interp > y_jane_interp
ax.fill_between(x_common, y_jane_interp, y_bob_interp,
                where=lens_mask, color='#ffdc64', alpha=0.4, zorder=3,
                label='Mutually beneficial trades')

# ── Annotation: not efficient ─────────────────────────
ax.text(ex + 0.5, ey - 1.5,
        '$MRS_{Jane} = 4$', fontsize=13, color='#1a6dcc', fontweight='bold', zorder=10)
ax.text(ex + 0.5, ey - 2.5,
        '$MRS_{Bob}\\;\\, = 3$', fontsize=13, color='#cc3333', fontweight='bold', zorder=10)
ax.text(ex + 0.5, ey - 3.8,
        '$MRS_J \\neq MRS_B \\Rightarrow$ Not Pareto efficient',
        fontsize=12, color='#8B0000', fontweight='bold', zorder=10)

# ── Dashed lines from endowment to axes ──────────────
ax.plot([ex, ex], [0, ey], '--', color='gray', linewidth=1, zorder=2)
ax.plot([0, ex], [ey, ey], '--', color='gray', linewidth=1, zorder=2)

# ── Legend ────────────────────────────────────────────
legend = ax.legend(loc='upper left', fontsize=12, framealpha=0.9, edgecolor='#999',
                   fancybox=False, borderpad=0.8)
legend.get_frame().set_linewidth(1)

ax.set_aspect('equal')
plt.tight_layout()
plt.savefig('/home/user/myfirstrepo/edgeworth_box.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("Saved edgeworth_box.png")
