#!/bin/bash
# 01_liftover.sh
# Lifts over a BED file from hg19 to hg38 using CrossMap
# Usage: bash scripts/01_liftover.sh

set -e  # stop on any error

CHAIN="data/liftover/hg19ToHg38.over.chain.gz"
INPUT_BED="data/liftover/practice_panel_hg19.bed"
OUTPUT_BED="data/liftover/practice_panel_hg38.bed"
UNMAPPED="data/liftover/unmapped.bed"

echo "[01] Starting liftover: hg19 → hg38"
echo "     Input:  $INPUT_BED"
echo "     Output: $OUTPUT_BED"

CrossMap bed $CHAIN $INPUT_BED $OUTPUT_BED

echo "[01] Liftover complete"
echo "     Mapped regions:"
cat $OUTPUT_BED
echo ""
echo "     Line count hg19: $(wc -l < $INPUT_BED)"
echo "     Line count hg38: $(wc -l < $OUTPUT_BED)"
