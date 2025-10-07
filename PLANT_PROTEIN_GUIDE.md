# Native American Plant Protein Detection Guide

## Overview

This guide describes how to use PAMPA to detect proteins from domesticated and wild plants in archaeological pottery residues from Native American contexts. The database focuses on plants from the Eastern Agricultural Complex, Three Sisters agriculture, and important wild plant resources.

## Quick Start

### 1. Database Already Built

The following files have been generated:

- **`native_american_plants.fasta`** - 52 protein sequences from 13 plant species
- **`plant_markers.tsv`** - 715 tryptic peptides without modifications
- **`plant_markers_deamidation.tsv`** - 1,279 peptides with deamidation variants
- **`plant_taxonomy.tsv`** - Taxonomic hierarchy for classification
- **`plant_database_info.txt`** - Database metadata

### 2. Analyze Your Pottery Residue Spectra

```bash
# Basic classification
python pampa_classify.py -s your_spectra_dir/ -e 0.1 \
    -p plant_markers_deamidation.tsv \
    -t plant_taxonomy.tsv \
    -o plant_results.tsv

# With deamidation consideration (for aged proteins)
python pampa_classify.py -s your_spectra_dir/ -e 0.1 \
    -p plant_markers_deamidation.tsv \
    -t plant_taxonomy.tsv \
    --deamidation \
    -o plant_results_deam.tsv
```

### 3. Interpret Results

Check the output TSV file for species identifications. Higher peptide counts indicate more confident identifications.

---

## Plant Species Included

### Domesticated Plants (Eastern Agricultural Complex & Three Sisters)

#### 1. **Common Bean** (*Phaseolus vulgaris*)
- **Key proteins**: Phaseolin (40-50% of seed protein), Phytohemagglutinin (PHA-L, PHA-E)
- **Diagnostic markers**: Arcelin, alpha-amylase inhibitors, Bowman-Birk inhibitors
- **Thermal stability**: Phaseolin fragments (20-27 kDa) survive cooking; PHA denatures during boiling
- **Archaeological significance**: Late Woodland/Mississippian introduction
- **UniProt entries**: 18 proteins covering storage globulins, lectins, inhibitors

#### 2. **Maize** (*Zea mays*)
- **Key proteins**: Zeins (alpha, beta, gamma variants), globulins, glutelins
- **Diagnostic markers**: Hydrophobic zeins readily bind pottery surfaces
- **Thermal stability**: Zeins stable; nixtamalization creates characteristic modifications
- **Archaeological significance**: Increasingly important from Middle Woodland through Mississippian
- **UniProt entries**: 9 major zein and storage protein variants

#### 3. **Squash/Pumpkin** (*Cucurbita pepo*, *C. maxima*)
- **Key proteins**: Cucurbitin (anthelmintic properties), Cucumisin (stable protease)
- **Diagnostic markers**: 2S albumins with disulfide bonds
- **Thermal stability**: Cucumisin shows unusual stability; albumins preserve well
- **Archaeological significance**: Early cultigen in Eastern Agricultural Complex
- **UniProt entries**: 6 proteins from seed and flesh

#### 4. **Sunflower** (*Helianthus annuus*)
- **Key proteins**: Helianthinin (11S globulin, 40-60% seed protein), 2S albumins
- **Diagnostic markers**: Albumins more stable than helianthinin
- **Thermal stability**: 11S globulin dissociates during heating; albumins resist degradation
- **Archaeological significance**: Domesticated ~4000 BP in eastern North America
- **UniProt entries**: 4 proteins including major storage globulins

#### 5. **Chenopodium** (*Chenopodium berlandieri*, proxy: *C. quinoa*)
- **Key proteins**: Chenopodin (11S globulin), 2S albumins
- **Diagnostic markers**: Similar to amaranth proteins; requires careful discrimination
- **Thermal stability**: Comparable to other seed storage proteins
- **Archaeological significance**: Major crop across Eastern Woodlands
- **UniProt entries**: Limited due to understudied species; quinoa used as proxy

#### 6. **Amaranth** (*Amaranthus hypochondriacus*)
- **Key proteins**: Amarantin (11S globulin), storage albumins
- **Diagnostic markers**: Structurally similar to quinoa; peptide selection critical
- **Thermal stability**: Proteins survive popping and boiling
- **Archaeological significance**: Important pseudocereal in various regions
- **UniProt entries**: 4 proteins including major storage forms

### Wild Plant Resources

#### 7. **Wild Rice** (*Zizania palustris*)
- **Key proteins**: Glutelins, storage proteins (distinct from *Oryza*)
- **Archaeological significance**: Great Lakes region staple
- **UniProt entries**: 2 proteins

#### 8. **Black Walnut** (*Juglans nigra*)
- **Key proteins**: 2S albumins (juglanin-like), storage proteins
- **Thermal stability**: Tree nut albumins generally stable
- **Archaeological significance**: Important fall resource
- **UniProt entries**: 2 proteins

#### 9. **Pecan/Hickory** (*Carya illinoinensis* as proxy)
- **Key proteins**: Storage albumins and globulins
- **Archaeological significance**: Major nut resource in Southeast
- **UniProt entries**: Limited; pecan used as hickory proxy

#### 10. **Jerusalem Artichoke** (*Helianthus tuberosus*)
- **Key proteins**: Sporamin-like proteins, metabolic enzymes
- **Thermal stability**: Tuber proteins generally less stable than seeds
- **Archaeological significance**: Root crop supplement
- **UniProt entries**: Broad organism search returned reviewed proteins

#### 11. **Groundnut** (*Apios americana*)
- **Key proteins**: Lectins, protease inhibitors (high protein content)
- **Thermal stability**: Inhibitors may survive due to disulfide bonds
- **Archaeological significance**: Important tuber crop
- **UniProt entries**: No reviewed entries; requires alternative approaches

#### 12. **Lima Bean** (*Phaseolus lunatus*)
- **Key proteins**: Phaseolin variants, storage globulins
- **Archaeological significance**: Southern variant of bean cultivation
- **UniProt entries**: 2 proteins

---

## Protein Characteristics by Type

### Storage Proteins (Best Preservation Potential)

**11S Globulins (Legumins)**
- Examples: Helianthinin (sunflower), Amarantin (amaranth), Chenopodin (chenopodium)
- Structure: Hexameric, 300-400 kDa native
- Stability: Dissociates during heating but leaves diagnostic peptides
- Mass range: Individual subunits ~50-60 kDa

**7S Globulins (Vicilins)**
- Examples: Phaseolin (beans), various legume storage proteins
- Structure: Trimeric, ~150-190 kDa native
- Stability: Partially hydrolyzes during cooking, producing 20-27 kDa fragments
- Mass range: Subunits ~40-50 kDa

**2S Albumins**
- Examples: Sunflower albumin, squash albumins, tree nut albumins
- Structure: Compact, disulfide-rich, 10-15 kDa
- Stability: **Exceptional** - disulfide bonds promote preservation
- Mass range: 8-15 kDa

**Prolamins** (Grass-specific)
- Examples: Zeins (maize), hordeins (barley)
- Structure: Hydrophobic, monomeric
- Stability: Very stable; readily bind ceramic surfaces
- Mass range: 20-30 kDa

**Glutelins**
- Examples: Maize glutelins, wild rice glutelins
- Structure: Polymeric, alkali-soluble
- Stability: Moderate; affected by pH during cooking
- Mass range: Variable, 30-60 kDa subunits

### Defensive Proteins (Moderate to High Preservation)

**Protease Inhibitors**
- Examples: Bowman-Birk inhibitors (beans), kunitz inhibitors
- Structure: Small, multiple disulfide bonds
- Stability: **Exceptional** - among most stable plant proteins
- Mass range: 8-20 kDa

**Alpha-amylase Inhibitors**
- Examples: Bean alpha-AI1, alpha-AI2
- Structure: Disulfide-stabilized
- Stability: **Exceptional** - thermal resistant
- Mass range: 12-16 kDa

**Lectins**
- Examples: Phytohemagglutinin (PHA-L, PHA-E), Arcelin
- Structure: Tetrameric, carbohydrate-binding
- Stability: Moderate - denatures during extended boiling
- Mass range: 30-34 kDa subunits

### Enzymatic Proteins (Poor to Moderate Preservation)

**Metabolic Enzymes**
- Examples: Lipoxygenase, amylases, urease
- Stability: Generally poor; denature readily
- Significance: May indicate fresh vs. stored plant processing

---

## Archaeological Interpretation

### Temporal Expectations

**Archaic Period** (pre-3000 BP)
- Expect: Diverse wild plant proteins (nuts, wild seeds)
- Look for: Tree nut albumins, wild grass proteins, wild tuber proteins

**Early Woodland** (3000-2200 BP)
- Expect: Initial Eastern Agricultural Complex proteins
- Look for: Sunflower, chenopodium, squash proteins
- Minimal: Bean proteins absent; maize rare/absent

**Middle Woodland** (2200-1200 BP)
- Expect: Intensified indigenous crop proteins
- Look for: Increased sunflower, chenopodium, squash, amaranth
- Variable: Early maize in some regions; beans still rare

**Late Woodland** (1200-1000 BP)
- Expect: Increasing maize proteins
- Look for: Zeins becoming dominant; continued indigenous crops
- Regional: Bean proteins beginning to appear

**Mississippian** (1000-500 BP)
- Expect: Three Sisters dominance
- Look for: Maize zeins abundant, bean phaseolin, squash proteins
- Pattern: Phaseolin + zein co-occurrence diagnostic

### Regional Variations

**Great Lakes**
- Emphasize: Wild rice glutelins, tree nut proteins
- Context: Late adoption of maize; continued wild resource use

**Southeast**
- Emphasize: Early squash, later Three Sisters
- Context: Hickory/acorn proteins throughout; intensified maize/bean by Mississippian

**Plains**
- Emphasize: Indigenous crops longer persistence
- Context: Sunflower, chenopodium, prairie turnip alongside later maize

**Southwest** (if applicable)
- Emphasize: Early maize, beans, squash
- Context: Agave, cactus, pine nut proteins regional

### Protein Co-occurrence Patterns

**Eastern Agricultural Complex Signature**
- Sunflower helianthinin/albumins + Chenopodium chenopodin + Squash cucurbitin
- Interpretation: Pre-maize indigenous agriculture

**Three Sisters Signature**
- Maize zeins + Bean phaseolin + Squash proteins
- Interpretation: Mature maize-bean-squash complex

**Transitional Pattern**
- Maize zeins present, bean proteins absent
- Interpretation: Early maize adoption before bean introduction

**Wild Resource Processing**
- Tree nut albumins, wild rice glutelins, diverse low-abundance proteins
- Interpretation: Foraging-based subsistence or supplementation

### Processing Indicators

**Nixtamalization** (if detectable in peptides)
- Modified maize proteins suggest alkali processing
- Indicates sophisticated maize preparation technology

**Germination**
- Amylase, protease presence suggests malting
- May indicate fermented beverage production

**Fresh vs. Stored**
- Active enzymes (lipoxygenase, etc.) suggest fresh plant processing
- Storage protein dominance suggests dried seed cooking

**Seed vs. Vegetative Parts**
- High storage protein suggests seed processing
- Metabolic enzymes might indicate vegetative part use (e.g., squash flesh vs. seeds)

---

## Technical Considerations

### Mass Spectrometry Parameters

**Mass Error Tolerance**
- Recommended: `-e 0.1` (±100 ppm) for pottery residues
- Consideration: Degraded samples may require wider tolerances

**Deamidation**
- Critical for archaeological samples: Use `--deamidation` flag
- Asparagine (N) → Aspartic acid (D): +0.984 Da
- Glutamine (Q) → Glutamic acid (E): +0.984 Da

**Other PTMs to Consider**
- Oxidation (M): +15.995 Da
- Glycation (Lys, Arg): Variable mass additions (Maillard products)

### Database Searching Strategy

**Hierarchical Approach**
1. Search specific well-characterized proteins (phaseolin, zeins, helianthinin)
2. Expand to protein families (11S globulins, 2S albumins)
3. Include conserved domains for understudied species

**Challenges with Understudied Species**
- Many indigenous plants lack comprehensive UniProt entries
- Strategy: Use related species as proxies (e.g., quinoa for chenopodium)
- Limitation: May miss species-specific peptides

**Cultivar Variation**
- Ancient cultivars may have sequence differences from modern database entries
- Strategy: Allow mismatches or use genus-level classification

### Peptide Selection for Discrimination

**Distinguishing Similar Species**
- Chenopodium vs. Amaranth: Select non-homologous peptides
- Different Phaseolus species: Focus on variable regions
- Wild vs. cultivated variants: May require multiple peptide hits

**Diagnostic Peptides**
- Zeins: Unique to Zea mays (maize-specific)
- PHA (Phytohemagglutinin): Virtually unique to Phaseolus
- Arcelin: Specific to certain bean varieties

---

## Updating and Expanding the Database

### Adding New Species

Edit `fetch_plant_proteins.py` and add entries to the `PLANT_PROTEINS` dictionary:

```python
"Species_name": {
    "common_name": "Common name",
    "proteins": {
        "protein_type": ["P12345", "P67890"],  # UniProt accessions
    }
}
```

Then regenerate:
```bash
python fetch_plant_proteins.py
python pampa_craft.py --allpeptides -f native_american_plants.fasta -o plant_markers.tsv
python pampa_craft.py --deamidation -p plant_markers.tsv -o plant_markers_deamidation.tsv
```

### Searching for New Proteins

**UniProt Advanced Search**
```
organism_name:"Helianthus annuus" AND reviewed:true AND keyword:"Storage protein"
```

**Browse by Protein Family**
- Search for "11S globulin" + organism
- Search for "2S albumin" + organism
- Search for specific genes (e.g., "phaseolin")

### Adding Custom Sequences

If you have sequences not in UniProt (e.g., from transcriptomics):

1. Add to FASTA file in standard format:
```
>CustomID|Species_name|Protein_name
SEQUENCEHERE
```

2. Regenerate peptide tables with PAMPA

---

## Limitations and Caveats

### Protein Preservation Factors

**Promotes Preservation**
- High initial abundance (storage proteins)
- Disulfide bond stabilization (albumins, inhibitors)
- Hydrophobic character (zeins bind ceramics)
- Compact structure (small inhibitors)

**Inhibits Preservation**
- Low abundance (metabolic enzymes)
- Heat-labile structure (some lectins)
- Hydrophilic character (may not bind ceramics)
- Large, complex quaternary structure (may dissociate)

### False Negatives (Plant Present but Not Detected)

- Protein too degraded for identification
- Processing method didn't deposit proteins on ceramic
- Vessel used for non-protein-rich plant parts
- Species lacks diagnostic peptides in database

### False Positives (Protein Detected but Plant Not Used)

- Cross-contamination from soil/handling
- Modern contamination during excavation/storage
- Sequence similarity to unrelated proteins (requires careful validation)

### Absence of Evidence ≠ Evidence of Absence

- Negative results don't prove plant wasn't used
- Integrate with macrobotanical evidence (seeds, charcoal)
- Consider starch grain analysis, phytolith analysis
- Use multiple vessels/contexts for robust patterns

---

## Example Workflows

### Workflow 1: Regional Survey of Late Woodland Vessels

**Goal**: Document transition from Eastern Agricultural Complex to maize agriculture

```bash
# Analyze multiple vessels
for vessel in vessel_001 vessel_002 vessel_003; do
    python pampa_classify.py \
        -s spectra/${vessel}/ \
        -e 0.1 \
        -p plant_markers_deamidation.tsv \
        -t plant_taxonomy.tsv \
        --deamidation \
        -o results/${vessel}_plants.tsv
done

# Look for patterns:
# - Sunflower + chenopodium + squash = EAC
# - Maize without beans = transitional
# - Maize + beans + squash = Three Sisters
```

### Workflow 2: Single Vessel Deep Analysis

**Goal**: Comprehensive characterization of one well-preserved vessel

```bash
# Step 1: Initial broad search
python pampa_classify.py \
    -s vessel_spectra/ -e 0.1 \
    -p plant_markers_deamidation.tsv \
    -t plant_taxonomy.tsv \
    --deamidation \
    -o vessel_initial.tsv

# Step 2: If specific plant detected, create targeted database
# Example: Strong maize signal, create maize-only reference

python pampa_craft.py --selection \
    -p plant_markers_deamidation.tsv \
    -s vessel_spectra/ \
    -e 0.1 \
    -o vessel_refined_markers.tsv

# Step 3: Re-analyze with refined markers
python pampa_classify.py \
    -s vessel_spectra/ -e 0.1 \
    -p vessel_refined_markers.tsv \
    -o vessel_final.tsv
```

### Workflow 3: Comparative Analysis Across Time Periods

**Goal**: Document dietary change from Archaic through Mississippian

```bash
# Organize vessels by temporal period
# Archaic/, EarlyWoodland/, MiddleWoodland/, LateWoodland/, Mississippian/

for period in Archaic EarlyWoodland MiddleWoodland LateWoodland Mississippian; do
    python pampa_classify.py \
        -s ${period}/ \
        -e 0.1 \
        -p plant_markers_deamidation.tsv \
        -t plant_taxonomy.tsv \
        --deamidation \
        -o results/${period}_summary.tsv
done

# Analyze trends:
# - Diversity of wild plants (Archaic)
# - Appearance of EAC proteins (Early/Middle Woodland)
# - Rise of maize proteins (Late Woodland)
# - Dominance of Three Sisters (Mississippian)
```

---

## Troubleshooting

### No Proteins Detected

1. **Check spectra quality**: Ensure MS/MS spectra are in correct format (MGF, mzML, CSV)
2. **Verify mass error tolerance**: Try increasing `-e` parameter (0.1 → 0.2)
3. **Consider degradation**: Pottery residues may be highly degraded
4. **Review extraction protocol**: Ensure protein extraction was successful

### Unexpected Species Detected

1. **Check sequence homology**: Use BLAST to verify peptide uniqueness
2. **Review contamination**: Modern plants during excavation/processing?
3. **Consider database limitations**: May be matching related species
4. **Validate with multiple peptides**: Single peptide = insufficient evidence

### Conflicting Results Across Vessels

1. **Expected variation**: Different vessels had different uses
2. **Preservation variation**: Some contexts preserve better than others
3. **Temporal mixing**: Ensure secure stratigraphic context
4. **Statistical approach**: Analyze patterns across many vessels

---

## Future Directions

### Expanding Coverage

- **Additional crop species**: Bottle gourd, sumpweed, other EAC crops
- **Regional wild plants**: Acorns, other nuts with better sequence coverage
- **Southwestern plants**: Agave, cactus, mesquite with targeted sequencing
- **Aquatic plants**: Wapato, cattail, other wetland resources

### Methodological Improvements

- **Ancient protein damage patterns**: Implement damage-aware scoring
- **Quantitative analysis**: Estimate relative abundance of different plants
- **Protein-starch integration**: Combine with starch grain identifications
- **Lipid co-analysis**: Integrate with fatty acid analysis results

### Database Enhancements

- **Cultivar-specific sequences**: Ancient DNA informed protein sequences
- **Degradation simulation**: Model expected peptide profiles after diagenesis
- **Spectral libraries**: Build reference spectra for key plant peptides
- **Machine learning**: Pattern recognition for plant assemblages

---

## References and Resources

### UniProt Resources
- **Main site**: https://www.uniprot.org
- **REST API**: https://rest.uniprot.org/
- **Search syntax**: https://www.uniprot.org/help/query-fields

### PAMPA Documentation
- See main README.md for PAMPA usage
- See config.json for customization options
- See CLAUDE.md for codebase architecture

### Plant Protein Literature
- Storage protein nomenclature: Shewry et al. (1995) J Exp Bot
- Thermal stability: Mills et al. (2005) Food Chem
- Archaeological proteins: Hendy et al. (2018) Nature Ecol Evol
- Eastern Agricultural Complex: Smith (2006) PNAS

---

## Contact and Contributions

To add new plant species, update protein accessions, or report issues with the database, please update `fetch_plant_proteins.py` and regenerate the reference files.

For questions about PAMPA functionality, see the main PAMPA documentation and CLAUDE.md.

---

**Last Updated**: 2025-10-07
**Database Version**: 1.0
**Species Count**: 13
**Protein Count**: 52
**Peptide Markers**: 1,279 (with deamidation)
