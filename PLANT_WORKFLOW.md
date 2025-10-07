# Quick Workflow: Plant Protein Detection in Archaeological Pottery

## Setup (One-time)

Already complete! You have:
- ✓ `native_american_plants.fasta` (52 proteins, 13 species)
- ✓ `plant_markers_deamidation.tsv` (1,279 peptides with PTMs)
- ✓ `plant_taxonomy.tsv` (taxonomic structure)

## Basic Analysis

### Single Vessel Analysis

```bash
python pampa_classify.py \
    -s path/to/your/spectra/ \
    -e 0.1 \
    -p plant_markers_deamidation.tsv \
    -t plant_taxonomy.tsv \
    --deamidation \
    -o my_vessel_results.tsv
```

**Parameters explained:**
- `-s`: Directory with MS/MS spectra (MGF, mzML, or CSV format)
- `-e 0.1`: Mass error tolerance (±100 ppm)
- `-p`: Peptide marker table
- `-t`: Taxonomy file for hierarchical classification
- `--deamidation`: Account for N→D, Q→E modifications (critical for old proteins)
- `-o`: Output results file

### Multiple Vessels (Batch Processing)

```bash
# If you have multiple vessel directories
for vessel in vessel_*/; do
    python pampa_classify.py \
        -s "$vessel" \
        -e 0.1 \
        -p plant_markers_deamidation.tsv \
        -t plant_taxonomy.tsv \
        --deamidation \
        -o results/$(basename "$vessel")_plants.tsv
done
```

## Interpreting Results

### Output File Format

The output TSV contains columns like:
- **Taxon name**: Identified species
- **Marker**: Peptide identifier
- **Sequence**: Peptide amino acid sequence
- **Mass**: Theoretical m/z
- **Matches**: Number of spectral matches

### Key Patterns to Look For

**Eastern Agricultural Complex (EAC)**
```
Helianthus_annuus    (sunflower)
Chenopodium_quinoa   (chenopodium proxy)
Cucurbita_pepo       (squash)
```
→ Pre-maize indigenous agriculture

**Three Sisters Complex**
```
Zea_mays            (maize)
Phaseolus_vulgaris  (beans)
Cucurbita_pepo      (squash)
```
→ Mature maize-bean-squash agriculture

**Transitional Period**
```
Zea_mays            (maize) ✓
Phaseolus_vulgaris  (beans) ✗
Helianthus_annuus   (sunflower) ✓
```
→ Early maize adoption alongside indigenous crops

**Wild Resources**
```
Juglans_nigra       (black walnut)
Zizania_palustris   (wild rice)
Carya_illinoinensis (hickory/pecan)
```
→ Foraging or supplementation

## Advanced Options

### Tighter Mass Tolerance (High-resolution MS)

```bash
python pampa_classify.py -s spectra/ -e 0.05 -p plant_markers_deamidation.tsv -o results.tsv
```

### Without Deamidation (Modern samples or testing)

```bash
python pampa_classify.py -s spectra/ -e 0.1 -p plant_markers.tsv -o results.tsv
```

### Generate Custom Markers from Spectra

If you want to filter markers to only those observed in your samples:

```bash
# Step 1: Create refined marker table from your spectra
python pampa_craft.py --selection \
    -p plant_markers_deamidation.tsv \
    -s your_spectra/ \
    -e 0.1 \
    -o refined_markers.tsv

# Step 2: Re-classify with refined markers
python pampa_classify.py \
    -s your_spectra/ \
    -e 0.1 \
    -p refined_markers.tsv \
    -o refined_results.tsv
```

## Updating the Database

### Add New Species

1. Edit `fetch_plant_proteins.py`
2. Add entry to `PLANT_PROTEINS` dictionary with UniProt accessions
3. Regenerate database:

```bash
python fetch_plant_proteins.py
python pampa_craft.py --allpeptides -f native_american_plants.fasta -o plant_markers.tsv
python pampa_craft.py --deamidation -p plant_markers.tsv -o plant_markers_deamidation.tsv
```

### Add Custom FASTA Sequences

If you have sequences not in UniProt:

```bash
# Add sequences to native_american_plants.fasta in FASTA format
# Then regenerate peptide tables:

python pampa_craft.py --allpeptides -f native_american_plants.fasta -o plant_markers.tsv
python pampa_craft.py --deamidation -p plant_markers.tsv -o plant_markers_deamidation.tsv
```

## File Formats

### Input Spectra Formats

PAMPA accepts:
- **MGF** (Mascot Generic Format) - recommended
- **mzML** (standard XML format)
- **CSV** (mass, intensity columns)

### Output Format

TSV (tab-separated values) with columns:
- Taxonomic information
- Peptide sequences and masses
- Match statistics
- Gene names and markers

## Troubleshooting

### No matches found
- Check spectra file format (MGF/mzML/CSV)
- Try wider mass tolerance: `-e 0.2`
- Verify protein extraction was successful
- Check that deamidation flag is used for old samples

### Too many matches (low specificity)
- Use tighter mass tolerance: `-e 0.05`
- Filter for multiple peptide hits per species
- Validate with homology searches (BLAST)

### Specific species not detected
- Verify proteins are in database: check `plant_database_info.txt`
- Check if UniProt has sequences for that species
- Consider using related species as proxy

## Expected Performance

### Temporal Patterns

| Period | Expected Plants | Key Proteins |
|--------|----------------|--------------|
| Archaic | Wild nuts, seeds | Tree nut albumins, wild grass proteins |
| Early Woodland | EAC crops appearing | Sunflower, chenopodium, squash |
| Middle Woodland | EAC intensification | Increased sunflower, chenopodium |
| Late Woodland | Maize arrives | Zeins appear, EAC continues |
| Mississippian | Three Sisters | Zeins + phaseolin + cucurbitin |

### Protein Stability Ranking

**Most Stable (best preservation):**
1. 2S albumins (disulfide-rich)
2. Protease inhibitors (Bowman-Birk, alpha-AI)
3. Zeins (hydrophobic, bind ceramics)
4. Phaseolin fragments (abundant)

**Moderately Stable:**
5. 11S/7S globulins (abundant but heat-sensitive)
6. Lectins (variable stability)

**Least Stable (poor preservation):**
7. Metabolic enzymes (degrade readily)

## Tips for Best Results

1. **Use deamidation flag** for archaeological samples
2. **Analyze multiple vessels** for robust patterns
3. **Compare across time periods** to see dietary change
4. **Integrate with other data**: macrobotanicals, starch grains, lipids
5. **Validate identifications**: Multiple peptides per species preferred
6. **Consider context**: Burial environment affects preservation

## Quick Reference: Common Commands

```bash
# Basic analysis
python pampa_classify.py -s spectra/ -e 0.1 -p plant_markers_deamidation.tsv --deamidation -o results.tsv

# With taxonomy
python pampa_classify.py -s spectra/ -e 0.1 -p plant_markers_deamidation.tsv -t plant_taxonomy.tsv --deamidation -o results.tsv

# Batch processing
for dir in vessel_*/; do python pampa_classify.py -s "$dir" -e 0.1 -p plant_markers_deamidation.tsv --deamidation -o "results/$(basename "$dir").tsv"; done

# Update database
python fetch_plant_proteins.py && python pampa_craft.py --allpeptides -f native_american_plants.fasta -o plant_markers.tsv && python pampa_craft.py --deamidation -p plant_markers.tsv -o plant_markers_deamidation.tsv
```

## Getting Help

- **PAMPA general help**: See README.md and CLAUDE.md
- **Plant protein details**: See PLANT_PROTEIN_GUIDE.md
- **Species list**: See plant_database_info.txt
- **Protein fetch script**: See fetch_plant_proteins.py

---

Ready to analyze! Just point PAMPA at your pottery residue spectra.
