# Plant Protein Detection for Archaeological Pottery Residues

## What This Does

Detects proteins from Native American domesticated and wild plants in archaeological pottery residues using mass spectrometry (ZooMS-like approach for plants).

**Plants covered:**
- **Domesticated**: Beans, maize, squash, sunflower, chenopodium, amaranth
- **Wild resources**: Wild rice, hickory, walnut, Jerusalem artichoke

## Quick Start

### Analyze Your Pottery Residues

```bash
python pampa_classify.py \
    -s your_spectra_directory/ \
    -e 0.1 \
    -p plant_markers_deamidation.tsv \
    -t plant_taxonomy.tsv \
    --deamidation \
    -o results.tsv
```

**That's it!** Results will show which plants were detected in your pottery.

## Files You Need

All files are already generated:

| File | Purpose | Size |
|------|---------|------|
| `plant_markers_deamidation.tsv` | Peptide reference database | 1,278 peptides |
| `plant_taxonomy.tsv` | Taxonomic hierarchy | 13 species |
| `native_american_plants.fasta` | Protein sequences | 51 proteins |

## What You'll Find

### Eastern Agricultural Complex (EAC)
If you see these together → pre-maize indigenous agriculture
- Sunflower (*Helianthus annuus*)
- Chenopodium (*Chenopodium quinoa* - proxy for *C. berlandieri*)
- Squash (*Cucurbita pepo*)

### Three Sisters Complex
If you see these together → mature maize-bean-squash agriculture (Late Woodland/Mississippian)
- Maize (*Zea mays*) - zeins are diagnostic
- Beans (*Phaseolus vulgaris*) - phaseolin is diagnostic
- Squash (*Cucurbita pepo*)

### Transitional Pattern
Maize present, beans absent → early maize adoption

### Wild Resources
Multiple tree nuts, wild rice → foraging or supplementation

## Protein Stability Guide

**Most likely to preserve:**
1. **2S albumins** (disulfide-rich, 8-15 kDa) - sunflower, tree nuts, squash
2. **Protease inhibitors** (Bowman-Birk type) - beans
3. **Zeins** (hydrophobic) - maize, readily bind pottery
4. **Phaseolin fragments** (abundant) - beans

**May preserve with good conditions:**
5. Storage globulins (11S, 7S types)
6. Lectins (phytohemagglutinin in beans)

**Rarely preserve:**
7. Metabolic enzymes

## Understanding Your Results

### Good Identification
- Multiple peptides from same species
- Peptides from stable protein types (albumins, inhibitors)
- Makes sense for time period and region

### Requires Validation
- Single peptide match only
- Only from unstable proteins (enzymes)
- Unexpected for archaeological context

### Temporal Expectations

| Period | Expected Pattern |
|--------|------------------|
| Archaic (>3000 BP) | Wild nuts, diverse seeds |
| Early Woodland (3000-2200 BP) | EAC crops appearing |
| Middle Woodland (2200-1200 BP) | EAC intensification |
| Late Woodland (1200-1000 BP) | Maize arrives, EAC continues |
| Mississippian (1000-500 BP) | Three Sisters dominance |

## Advanced Usage

### Add New Plant Species

1. Edit `fetch_plant_proteins.py`
2. Add UniProt accessions for your species
3. Run:
```bash
python fetch_plant_proteins.py
python pampa_craft.py --allpeptides -f native_american_plants.fasta -o plant_markers.tsv
python pampa_craft.py --deamidation -p plant_markers.tsv -o plant_markers_deamidation.tsv
```

### Create Vessel-Specific Markers

If you want to focus on only peptides actually observed in your samples:

```bash
python pampa_craft.py --selection \
    -p plant_markers_deamidation.tsv \
    -s your_spectra/ \
    -e 0.1 \
    -o vessel_specific_markers.tsv
```

### Batch Process Multiple Vessels

```bash
for vessel in vessel_*/; do
    python pampa_classify.py \
        -s "$vessel" \
        -e 0.1 \
        -p plant_markers_deamidation.tsv \
        -t plant_taxonomy.tsv \
        --deamidation \
        -o "results/$(basename "$vessel")_plants.tsv"
done
```

## Documentation

- **`PLANT_WORKFLOW.md`** - Quick reference for common tasks
- **`PLANT_PROTEIN_GUIDE.md`** - Comprehensive guide (20 pages)
  - Detailed protein descriptions
  - Archaeological interpretation
  - Processing indicators
  - Troubleshooting
  - Future directions

## Key Proteins by Species

### Beans (*Phaseolus vulgaris*) - 18 proteins
- **Phaseolin**: 40-50% of seed protein, fragments survive cooking
- **Phytohemagglutinin (PHA)**: Diagnostic lectin, virtually unique to beans
- **Arcelin**: Species-specific, definitive evidence
- **Bowman-Birk inhibitors**: Extremely stable, small (8-10 kDa)

### Maize (*Zea mays*) - 9 proteins
- **Alpha-zeins**: Hydrophobic, bind ceramics, highly diagnostic
- **Beta/gamma-zeins**: Additional variants
- **Nixtamalization**: Creates characteristic modifications

### Sunflower (*Helianthus annuus*) - 4 proteins
- **Helianthinin**: Major 11S globulin (40-60% seed protein)
- **2S albumin**: More stable, better preservation

### Squash (*Cucurbita*) - 6 proteins
- **Cucurbitin**: Anthelmintic properties, may enhance preservation
- **Cucumisin**: Unusually stable protease
- **2S albumins**: Disulfide-stabilized

## Technical Details

### Mass Error Tolerance
- Standard: `-e 0.1` (±100 ppm)
- High-resolution MS: `-e 0.05` (±50 ppm)
- Degraded samples: `-e 0.2` (±200 ppm)

### Deamidation
**Always use `--deamidation` for archaeological samples!**
- Asparagine (N) → Aspartic acid (D): +0.984 Da
- Glutamine (Q) → Glutamic acid (E): +0.984 Da
- This is the most common post-translational modification in aged proteins

### Spectra Formats
PAMPA accepts:
- **MGF** (Mascot Generic Format) - recommended
- **mzML** (mass spectrometry XML)
- **CSV** (simple mass, intensity)

## Validation & Testing

Run the test suite:
```bash
python test_plant_detection.py
```

Checks:
- ✓ All files present and properly formatted
- ✓ PAMPA modules import correctly
- ✓ Database statistics (51 proteins, 1,278 peptides)
- ✓ Species coverage (13 species)

## Limitations

### False Negatives (plant present but not detected)
- Protein too degraded
- Processing method didn't deposit proteins on ceramic
- Vessel used for non-protein-rich plant parts
- Species not in database

### False Positives (protein detected but plant not used)
- Contamination (modern or ancient)
- Sequence similarity to unrelated proteins
- Validate with multiple peptides!

### Database Coverage
- Some indigenous plants lack UniProt entries
- Using related species as proxies (quinoa for chenopodium)
- Ancient cultivars may differ from modern sequences

## Integration with Other Data

Combine plant protein results with:
- **Macrobotanicals**: Seeds, charcoal, wood
- **Microbotanicals**: Starch grains, phytoliths
- **Lipid analysis**: Fatty acids, wax esters
- **Stable isotopes**: C3 vs C4 plants (maize)

Proteins complement other methods:
- More specific than lipids
- Better preservation than DNA
- Functional alongside starches

## Archaeological Applications

### Research Questions
1. **When did maize agriculture arrive?** Look for first zein appearances
2. **How long did indigenous crops persist?** Track EAC proteins through time
3. **What was the Three Sisters adoption sequence?** Compare maize/bean/squash timing
4. **Were wild resources supplementing agriculture?** Look for nut proteins alongside crops
5. **Did different vessels have specialized uses?** Compare protein profiles across vessel types

### Best Practices
- Analyze multiple vessels per context
- Include controls (blank extractions, modern vessels)
- Compare across time periods
- Integrate with other paleobotanical data
- Consider burial environment effects on preservation

## Citation

If using this plant protein reference database, please cite:
- PAMPA software: [main PAMPA citation]
- This database: "Native American Plant Protein Reference Database for PAMPA (2025)"
- UniProt: The UniProt Consortium (2023) Nucleic Acids Research

## Questions?

- **General PAMPA usage**: See main README.md
- **Plant protein details**: See PLANT_PROTEIN_GUIDE.md
- **Quick commands**: See PLANT_WORKFLOW.md
- **Database contents**: See plant_database_info.txt

## System Status

✓ **51 proteins** from 13 plant species
✓ **1,278 peptide markers** (including deamidation variants)
✓ **714 base peptides** (no modifications)
✓ **564 deamidation variants** added
✓ **Full taxonomic classification** included
✓ **Validated and tested** - ready to use!

---

**Ready to detect plants in your pottery residues!**

Just point `pampa_classify.py` at your MS/MS spectra with the plant marker database.
