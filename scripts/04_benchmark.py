#!/usr/bin/env python3
"""
04_benchmark.py
Compares truth VCF vs assay VCF and calculates:
- True Positives (TP), False Negatives (FN), False Positives (FP)
- Sensitivity and Specificity at VAF cutoffs of 1%, 3%, 5%

Usage: python scripts/04_benchmark.py
"""

import cyvcf2
import random
import pandas as pd

random.seed(42)

truth_vcf = "data/processed/HG002.truth.filtered.vcf.gz"
assay_vcf = "data/processed/HG002.assay.vcf.gz"

# --- Step 1: Load truth variants into a set ---
print("[04] Loading truth variants...")
truth_variants = set()
for v in cyvcf2.VCF(truth_vcf):
    truth_variants.add((v.CHROM, v.POS, v.REF, str(v.ALT[0])))
print(f"     Truth variants loaded: {len(truth_variants)}")

# --- Step 2: Load assay variants and assign simulated VAFs ---
print("[04] Loading assay variants and assigning simulated VAFs...")
assay_variants = []
for v in cyvcf2.VCF(assay_vcf):
    key = (v.CHROM, v.POS, v.REF, str(v.ALT[0]))
    # Simulate VAF between 0.005 (0.5%) and 1.0 (100%)
    simulated_vaf = random.uniform(0.005, 1.0)
    assay_variants.append((key, simulated_vaf))
print(f"     Assay variants loaded: {len(assay_variants)}")

# --- Step 3: Calculate TP, FP, FN at each VAF cutoff ---
print("[04] Calculating metrics at VAF cutoffs...")

cutoffs = [0.01, 0.03, 0.05]
results = []

for cutoff in cutoffs:
    # Only keep assay variants above the VAF cutoff
    filtered_assay = {key for key, vaf in assay_variants if vaf >= cutoff}

    TP = len(filtered_assay & truth_variants)   # in both
    FP = len(filtered_assay - truth_variants)   # in assay only
    FN = len(truth_variants - filtered_assay)   # in truth only

    sensitivity = TP / (TP + FN) if (TP + FN) > 0 else 0
    specificity = TP / (TP + FP) if (TP + FP) > 0 else 0

    results.append({
        "VAF_cutoff": f"{int(cutoff*100)}%",
        "TP": TP,
        "FP": FP,
        "FN": FN,
        "Sensitivity": round(sensitivity, 4),
        "Specificity": round(specificity, 4)
    })

# --- Step 4: Save and display results ---
df = pd.DataFrame(results)
print("\n===== BENCHMARKING RESULTS =====")
print(df.to_string(index=False))

df.to_csv("results/benchmark_stats.csv", index=False)
print("\n[04] Results saved to results/benchmark_stats.csv")
