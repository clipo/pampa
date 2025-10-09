# Northeast Archaeological Protein Database Guide

## Overview

This guide explains how to create a comprehensive protein database for identifying fauna and flora remains from Northeast North American archaeological sites. The database includes proteins from 266 species across mammals, birds, fish, reptiles, mussels, and plants found in the region.

## Database Contents

### Species Coverage
- **64 Faunal species**: Mammals (deer, elk, bear, canids, etc.), Birds (waterfowl, raptors, turkeys), Mussels
- **41 Fish species**: Bass, trout, perch, catfish, minnows, pike, suckers
- **6 Reptile species**: Turtles (snapping, wood, box, painted, musk) and snakes
- **155 Plant species**:
  - Cultivated: Corn, beans, squash, nuts
  - Wild foods: Berries, roots, greens, onions
  - Tree nuts: Walnut, hazelnut, beech, chestnut, acorns
  - Mushrooms: Morels, boletes, hen-of-the-woods, etc.

### Protein Targets

#### Animal Proteins (Heat-Stable & Diagnostic)

**Primary ZooMS Proteins:**
1. **Collagen (Types I, II, III)** - Most abundant, survives cooking/burial
   - COL1A1, COL1A2: Bone, skin, tendon
   - COL2A1: Cartilage
   - COL3A1: Blood vessels, organs

2. **Muscle Proteins** - Partially heat-stable
   - Myosin (MYH1, MYH2, MYH4, MYH7)
   - Actin (ACTA1, ACTB, ACTG1)
   - Tropomyosin (TPM1, TPM2, TPM3) - allergen marker

3. **Blood Proteins**
   - Hemoglobin (HBA, HBB, HBD)
   - Myoglobin (MB)

4. **Serum Proteins** - Survive some cooking
   - Albumin (ALB)
   - Transferrin (TF)

5. **Structural Proteins**
   - Keratin (KRT1, KRT5, KRT10) - feathers, hair, scales

6. **Fish-Specific Markers**
   - Parvalbumin (PVALB) - highly heat-stable allergen

#### Plant Proteins (Cooking-Resistant)

**Storage Proteins** (seeds, nuts, grains):
1. **Seed Storage Globulins**
   - 11S globulins (legumins, glycinins)
   - 7S globulins (vicilins)
   - 2S albumins (napins)

2. **Grain Proteins**
   - Zeins (corn/maize - Zea mays)
   - Gliadins/Glutenins (wheat, barley relatives)
   - Avenins (oats)
   - Hordeins (barley)
   - Oryzins/Glutelins (wild rice)

3. **Enzyme Inhibitors** (very heat-stable)
   - Trypsin inhibitors
   - Protease inhibitors
   - Amylase inhibitors

4. **Other Abundant Proteins**
   - RuBisCO (ribulose bisphosphate carboxylase)
   - Heat shock proteins (HSP70)
   - Allergens (nut-specific)

#### Fungal Proteins (Mushrooms)
- Hydrophobins (structural)
- Laccases (enzymes)
- Chitin synthases

## Why These Proteins?

### Heat Stability
Cooking alters protein structure but doesn't destroy all peptides:
- **Collagen** → Gelatin (peptides remain)
- **Albumin**: Coagulates but partially survives
- **Storage proteins**: Very heat-stable (evolved to survive)
- **Enzyme inhibitors**: Extremely heat-stable
- **Tropomyosin, Parvalbumin**: Allergen proteins, very stable

### Archaeological Preservation
Proteins that survive cooking also tend to survive burial:
- Collagen survives thousands of years in pottery residues
- Storage proteins resist degradation
- Enzyme inhibitors are chemically stable

### Taxonomic Resolution
Different proteins provide different levels of identification:
- **Collagen**: Best for genus/species level (ZooMS standard)
- **Muscle proteins**: Species-specific isoforms
- **Serum proteins**: Family-level markers
- **Storage proteins**: Species/variety specific (cultivars)

## Using the Fetching Script

### Quick Start

```bash
# Fetch proteins from UniProt
python3 fetch_northeast_proteins.py "plant_animal data by site.xlsx"

# This generates:
# - northeast_reference_proteins.fasta (protein sequences)
# - northeast_taxonomy.tsv (taxonomic hierarchy)
# - northeast_protein_report.txt (summary statistics)
```

### Script Features

1. **Intelligent Querying**:
   - Prioritizes reviewed (SwissProt) entries
   - Falls back to genus-level if species not found
   - Handles hybrids, varieties, and subspecies
   - Rate-limited to respect UniProt server

2. **Protein Selection**:
   - Targets heat-stable, diagnostic proteins
   - Includes cooking-altered protein products
   - Species-specific where available
   - Family-level for rare species

3. **Output Organization**:
   - FASTA IDs: `Accession_Organism_ProteinType`
   - Descriptions include organism and protein name
   - Taxonomy file compatible with PAMPA

## Generating Peptide Markers

Once you have the protein sequences, generate tryptic peptides:

### Step 1: Generate All Tryptic Peptides

```bash
python pampa_craft.py --allpeptides \
  -f northeast_reference_proteins.fasta \
  -o northeast_markers_raw.tsv
```

This creates all possible tryptic peptides (800-3500 Da range).

### Step 2: Add Deamidation Variants

Deamidation (N→D, Q→E) occurs in ancient proteins:

```bash
python pampa_craft.py --deamidation \
  -p northeast_markers_raw.tsv \
  -o northeast_markers_deam.tsv
```

### Step 3: Fill in Taxonomy Information

```bash
python pampa_craft.py --fillin \
  -p northeast_markers_deam.tsv \
  -f northeast_reference_proteins.fasta \
  -t northeast_taxonomy.tsv \
  -o northeast_markers_complete.tsv
```

### Step 4 (Optional): Select Markers with Real Spectra

If you have spectra from known samples:

```bash
python pampa_craft.py --selection \
  -p northeast_markers_complete.tsv \
  -s known_spectra_dir/ \
  -e 0.1 \
  -o northeast_markers_validated.tsv
```

## Running Species Identification

### Basic Classification

```bash
python pampa_classify.py \
  -s archaeological_spectra/ \
  -e 0.1 \
  -p northeast_markers_complete.tsv \
  -t northeast_taxonomy.tsv \
  -o results.tsv
```

### With Deamidation Support

```bash
python pampa_classify.py \
  -s archaeological_spectra/ \
  -e 0.1 \
  -p northeast_markers_complete.tsv \
  -t northeast_taxonomy.tsv \
  --deamidation \
  -o results_deam.tsv
```

### Parameters

- `-s`: Directory with mass spectra (.csv, .mgf, or .mzML files)
- `-e`: Mass tolerance in Daltons (typically 0.05-0.2)
- `-p`: Peptide marker table
- `-t`: Taxonomy file
- `--deamidation`: Enable N→D and Q→E matching
- `-o`: Output results file

## Expected Results

### Database Size Estimates

Based on similar databases:
- **Animal proteins**: ~1,000-2,000 sequences
  - 111 species × ~10 proteins/species
  - Species-level where available
  - Genus-level for rare species

- **Plant proteins**: ~500-1,000 sequences
  - 155 species, but many lack UniProt data
  - More abundant for cultivated plants
  - Sparse for wild berries/mushrooms

- **Total peptide markers**: 10,000-50,000
  - After tryptic digestion
  - With deamidation variants: 2-3× more

### Coverage Limitations

**Good Coverage Expected:**
- Domestic mammals (deer, dog, pig, cattle relatives)
- Common fish (bass, trout, salmon family)
- Cultivated plants (corn, beans, nuts)
- Model organisms

**Limited Coverage Expected:**
- Rare wild berries
- Many mushroom species (fungi underrepresented in UniProt)
- Some regional fish species
- Invertebrates (mussels)

**Workarounds for Low Coverage:**
1. Use genus-level or family-level searches
2. Include related species as proxies
3. Use homology-based marker design
4. Manually curate from literature

## Troubleshooting

### Script Runs Slowly
- **Normal**: 266 species × 10 proteins × 0.5s = ~20-30 minutes
- **Solution**: Run overnight or use batch processing
- The script includes rate limiting to respect UniProt's servers

### Few Sequences Found
- Check UniProt for species name variations
- Try genus-level searches: `taxonomy:Genus`
- Use related species as proxies
- Check if species has genomic data available

### No Plant Proteins
- Many wild plants lack proteomic data in UniProt
- Focus on domesticated/cultivated species
- Consider using model species (Arabidopsis) as proxy
- Supplement with manual literature curation

### PAMPA Classification Issues
- **Low matches**: Adjust mass tolerance (`-e` parameter)
- **Wrong species**: Check for contamination or modern intrusions
- **Ambiguous results**: Normal for related species, use higher taxonomy

## Advanced: Manual Curation

For species with no UniProt data:

1. **Find Related Species**
   ```bash
   # Search UniProt manually for genus
   # Example: https://www.uniprot.org/uniprotkb?query=taxonomy:Rubus+AND+protein:storage
   ```

2. **Add to FASTA Manually**
   ```
   >MANUAL_Rubus_allegheniensis_storage_albumin
   MKVFLVLLALAAALAFPTTAHAECRCQNLQPEWNLGACRNYSRQGSCKNWVHCERKQHLK
   ...
   ```

3. **Update Taxonomy File**
   ```
   Rubus allegheniensis	Plantae	Rosaceae	Rubus	allegheniensis
   ```

## Integration with PAMPA Workflow

This database integrates with PAMPA's existing workflow:

```
northeast_reference_proteins.fasta  ──┐
                                      ├─→ pampa_craft.py --allpeptides
northeast_taxonomy.tsv  ──────────────┘
                                      │
                                      ↓
                        northeast_markers_complete.tsv
                                      │
                                      ↓
archaeological_spectra/  ──→ pampa_classify.py
                                      │
                                      ↓
                                  results.tsv
                                      │
                                      ↓
                            Species identifications
```

## Archaeological Interpretation

### Combined Evidence
Always interpret proteomic results with:
- Faunal remains (bones, shells)
- Botanical remains (seeds, charcoal)
- Residue context (cooking vs storage)
- Site chronology
- Regional subsistence patterns

### Cooking vs Storage Residues
- **Cooking pots**: Expect deamidated proteins, mixed species
- **Storage**: Less deamidation, single-species likely
- **Processing**: May show plant + animal (e.g., cooking with fat)

### Cultural Patterns
Look for:
- **Three Sisters**: Corn + beans + squash
- **Fish + wild plants**: Seasonal fishing camps
- **Nut processing**: Fall harvest activities
- **Bird diversity**: Waterfowl hunting patterns

## References & Further Reading

### ZooMS & Archaeological Proteomics
- Buckley et al. 2009 - ZooMS collagen fingerprinting
- Hendy et al. 2018 - Ancient proteins in archaeology
- Solazzo et al. 2008 - Pottery residue analysis

### Northeast Archaeology
- Hart & Lovis 2013 - *The Eastern Agricultural Complex*
- Crawford et al. 2006 - domestication in eastern North America
- Smith 1989 - Chenopodium, sunflower cultivation

### Protein Stability & Cooking
- Buckley et al. 2014 - Protein survival in cooking
- Warinner et al. 2014 - Dental calculus proteins
- Solazzo et al. 2008 - Protein preservation mechanisms

## Contact & Support

For issues with:
- **PAMPA software**: See main PAMPA documentation
- **UniProt queries**: https://www.uniprot.org/help
- **Archaeological interpretation**: Consult regional specialists

---

**Version**: 1.0
**Last Updated**: 2025-10-09
**Author**: Archaeological Proteomics Analysis
