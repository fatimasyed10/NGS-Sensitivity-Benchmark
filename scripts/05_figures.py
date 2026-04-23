#!/usr/bin/env python3
"""
05_figures.py
Generates publication-style figures from benchmark results:
- Figure 1: Sensitivity & Specificity bar chart at each VAF cutoff
- Figure 2: TP, FP, FN counts grouped bar chart
Usage: python scripts/05_figures.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # non-interactive backend for Linux

df = pd.read_csv("results/benchmark_stats.csv")

# ── Figure 1: Sensitivity & Specificity ──────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))

x = range(len(df))
width = 0.35

bars1 = ax.bar([i - width/2 for i in x], df["Sensitivity"],
               width, label="Sensitivity", color="#2196F3")
bars2 = ax.bar([i + width/2 for i in x], df["Specificity"],
               width, label="Specificity", color="#4CAF50")

# Add value labels on bars
for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 0.005,
            f"{bar.get_height():.4f}",
            ha="center", va="bottom", fontsize=9)
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 0.005,
            f"{bar.get_height():.4f}",
            ha="center", va="bottom", fontsize=9)

ax.set_xticks(list(x))
ax.set_xticklabels(df["VAF_cutoff"])
ax.set_xlabel("VAF Cutoff", fontsize=12)
ax.set_ylabel("Score", fontsize=12)
ax.set_title("Analytical Sensitivity & Specificity by VAF Cutoff", fontsize=13)
ax.set_ylim(0, 1.1)
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("results/figure1_sensitivity_specificity.png", dpi=150)
print("[05] Figure 1 saved")

# ── Figure 2: TP / FP / FN counts ────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))

width = 0.25
x = range(len(df))

ax.bar([i - width for i in x], df["TP"],
       width, label="TP", color="#2196F3")
ax.bar([i         for i in x], df["FP"],
       width, label="FP", color="#F44336")
ax.bar([i + width for i in x], df["FN"],
       width, label="FN", color="#FF9800")

ax.set_xticks(list(x))
ax.set_xticklabels(df["VAF_cutoff"])
ax.set_xlabel("VAF Cutoff", fontsize=12)
ax.set_ylabel("Variant Count", fontsize=12)
ax.set_title("TP / FP / FN Counts by VAF Cutoff", fontsize=13)
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("results/figure2_variant_counts.png", dpi=150)
print("[05] Figure 2 saved")

print("[05] All figures saved to results/")
