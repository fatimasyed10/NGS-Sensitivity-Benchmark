#!/bin/bash
# 02_intersect_bed.sh
# Intersects lifted panel BED with GIAB high-confidence BED
# Only keeps regions covered by BOTH the panel and GIAB
# Usage: bash scripts/02_intersect_bed.sh

set -e

PANEL_BED="data/liftover/practice_panel_hg38.bed"
GIAB_BED="data/raw/HG002_GRCh38_1_22_v4.2.1_benchmark_noinconsistent.bed"
OUTPUT_BED="data/processed/panel_giab_intersect.bed"

echo "[02] Intersecting panel BED with GIAB high-confidence BED..."
echo "     Panel regions:  $(wc -l < $PANEL_BED)"
echo "     GIAB regions:   $(wc -l < $GIAB_BED)"

bedtools intersect \
    -a $PANEL_BED \
    -b $GIAB_BED \
    > $OUTPUT_BED

echo "[02] Intersection complete"
echo "     Overlapping regions: $(wc -l < $OUTPUT_BED)"
echo ""
echo "     Intersected regions:"
cat $OUTPUT_BED

