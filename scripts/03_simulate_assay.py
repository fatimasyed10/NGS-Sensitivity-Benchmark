#!/usr/bin/env python3
"""
03_simulate_assay.py
Simulates an imperfect NGS assay from a truth VCF by:
- Randomly dropping 20% of variants (false negatives)
- This mimics a real caller that misses some true variants
Usage: python scripts/03_simulate_assay.py
"""

import cyvcf2
import random

random.seed(42)  # fixed seed = reproducible results every time

truth_vcf  = "data/processed/HG002.truth.filtered.vcf.gz"
output_vcf = "data/processed/HG002.assay.vcf.gz"

reader = cyvcf2.VCF(truth_vcf)
writer = cyvcf2.Writer(output_vcf, reader)

kept    = 0
dropped = 0

for variant in reader:
    if random.random() > 0.20:   # keep 80% → true positives
        writer.write_record(variant)
        kept += 1
    else:
        dropped += 1             # dropped 20% → false negatives

writer.close()
reader.close()

print(f"[03] Simulation complete")
print(f"     Kept   (TP candidates): {kept}")
print(f"     Dropped (FN candidates): {dropped}")
