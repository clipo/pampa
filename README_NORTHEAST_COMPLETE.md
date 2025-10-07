# Complete Northeast North American Archaeological Reference Database

## Overview

This is a comprehensive protein reference database for archaeological analysis of food residues from Northeastern North America. It includes animals, fish, birds, shellfish, reptiles, amphibians, and plants - covering virtually all potential food sources that might appear in cooking vessels.

## Quick Start

### Analyze Your Archaeological Samples

```bash
python pampa_classify.py \
    -s your_spectra_folder/ \
    -e 0.1 \
    -p northeast_markers_deam.tsv \
    -t northeast_taxonomy.tsv \
    --deamidation \
    -o results.tsv
```

That's it! Results will show which animals, fish, birds, shellfish, and/or plants were processed in your pottery.

## Database Contents

**Total: 50 species/proxies covering all major food resources**

### Mammals (12 species/proxies)
- **Ungulates**: White-tailed deer, moose, elk/wapiti
- **Carnivores**: Black bear, wolf/dog, lynx/bobcat
- **Small game**: Rabbit/hare/cottontail
- **Rodents**: Beaver, muskrat, squirrel, woodchuck, chipmunk, porcupine (via rat proxy)
- **Marine**: Harbor seal, gray seal, hooded seal
- **Proxies**: Cattle (general ungulate), pig (general omnivore)

### Birds (6 species)
- **Galliforms**: Wild turkey
- **Waterfowl**: Canada goose, mallard, wood duck, black duck, canvasback, tundra swan
- **Other**: Passenger pigeon (via rock pigeon), ruffed grouse, bobwhite, loon, grebe
- **Proxy**: Chicken (general bird)

### Fish - Anadromous (5 species)
- Atlantic salmon
- American shad, alewife (via Atlantic herring)
- Atlantic sturgeon (via sterlet)
- American eel (via European eel)

### Fish - Freshwater (5 species)
- Northern pike
- Largemouth/smallmouth bass
- Yellow perch, walleye (via European perch)
- Channel catfish, brown bullhead
- Pumpkinseed, sunfish, crappie (via bluegill)

### Fish - Marine/Coastal (3 species)
- Atlantic cod
- Winter flounder (via European flounder)
- Striped bass, cunner (via ballan wrasse)

### Shellfish (4 species)
- American lobster
- Eastern oyster
- Hard clam/quahog
- Blue mussel

### Reptiles & Amphibians (3 species)
- Snapping turtle, painted turtle (via red-eared slider)
- Water snake (via Burmese python)
- Bullfrog (via African clawed frog)

### Plants (11 species)
**Domesticated:**
- Common bean, lima bean
- Maize
- Squash (summer & winter)
- Sunflower
- Chenopodium/goosefoot
- Amaranth

**Wild:**
- Wild rice
- Black walnut
- Hickory/pecan
- Jerusalem artichoke

### Contamination Controls
- Human proteins (collagen, keratin, albumin) to identify handling contamination

## Protein Types Included

### Structural Proteins
- **Type I Collagen (COL1A1/COL1A2)** - Primary bone/tissue identifier
  - Present in all vertebrates
  - Survives cooking and burial well
  - Species-specific peptides allow discrimination

### Muscle Proteins
- **Myosin heavy chains** - Abundant in fresh meat
- **Actin** - Survives moderate cooking
- **Tropomyosin** - Important for shellfish identification

### Blood Proteins
- **Hemoglobin** - Indicates fresh meat or blood processing
- **Serum albumin** - Abundant, relatively stable

### Heat-Stable Proteins
- **Ferritin** - Iron storage, survives extended cooking
- **Transferrin** - Iron transport, heat-stable
- **LDH (Lactate dehydrogenase)** - Metabolic enzyme, species-specific
- **GAPDH** - Glycolysis enzyme, diagnostic
- **Creatine kinase** - Muscle enzyme

### Plant-Specific Proteins
- **Zeins** (maize) - Diagnostic, hydrophobic, bind pottery
- **Phaseolin** (beans) - Major storage protein
- **Helianthinin** (sunflower) - Seed protein
- **Cucurbitin** (squash) - Unique to Cucurbita

### Egg Proteins
- **Lysozyme** - Bird egg white
- **Ovalbumin** - Major egg protein
- **Ovotransferrin** - Egg white protein

### Roe/Caviar Proteins
- **Vitellogenin** - Fish egg yolk protein (salmon, sturgeon)

## Database Statistics

- **Protein sequences**: 300+ from UniProt
- **Peptide markers (base)**: 6,409
- **Peptide markers (with deamidation)**: 11,285
- **Deamidation variants added**: 4,876
- **Species/proxies**: 50
- **Categories**: 20

## Usage Examples

### Basic Animal + Plant Analysis

```bash
# Detect both animals and plants in pottery
python pampa_classify.py \
    -s pottery_spectra/ \
    -e 0.1 \
    -p northeast_markers_deam.tsv \
    -t northeast_taxonomy.tsv \
    --deamidation \
    -o complete_results.tsv
```

### High-Resolution MS (Orbitrap, Q-TOF, timsTOF)

```bash
# Tighter mass tolerance for high-resolution instruments
python pampa_classify.py \
    -s spectra/ \
    -e 0.01 \
    -p northeast_markers_deam.tsv \
    -t northeast_taxonomy.tsv \
    --deamidation \
    -o results.tsv
```

### Batch Processing Multiple Vessels

```bash
for vessel in vessel_*/; do
    python pampa_classify.py \
        -s "$vessel" \
        -e 0.1 \
        -p northeast_markers_deam.tsv \
        -t northeast_taxonomy.tsv \
        --deamidation \
        -o "results/$(basename "$vessel")_complete.tsv"
done
```

## Interpretation Guide

### Mammals
| Match | Likely Species | Confidence |
|-------|----------------|------------|
| Odocoileus virginianus | White-tailed deer | Very High |
| Ursus americanus | Black bear | Very High |
| Bos taurus | Deer/moose/elk (ungulate) | Moderate |
| Canis lupus | Wolf/dog | High |
| Rattus norvegicus | Beaver/muskrat/squirrel | Moderate |
| Oryctolagus cuniculus | Rabbit/hare/cottontail | Moderate |
| Phoca vitulina | Harbor/gray seal | High |

### Birds
| Match | Likely Species | Confidence |
|-------|----------------|------------|
| Meleagris gallopavo | Wild turkey | Very High |
| Anas platyrhynchos | Mallard/duck | High |
| Branta canadensis | Canada goose | High |
| Gallus gallus | Any galliforme bird | Low |

### Fish
| Match | Likely Species | Confidence |
|-------|----------------|------------|
| Salmo salar | Atlantic salmon | High |
| Esox lucius | Northern pike | Very High |
| Ictalurus punctatus | Channel catfish/bullhead | High |
| Gadus morhua | Atlantic cod | Very High |
| Perca fluviatilis | Yellow perch/walleye | Moderate |

### Shellfish
| Match | Identification | Confidence |
|-------|----------------|------------|
| Homarus americanus | American lobster | Very High |
| Crassostrea virginica | Eastern oyster | Very High |
| Mercenaria mercenaria | Hard clam/quahog | Very High |
| Mytilus edulis | Blue mussel | Very High |

### Plants
| Match | Identification | Significance |
|-------|----------------|--------------|
| Zea mays | Maize | Definitive - zeins unique |
| Phaseolus vulgaris | Common bean | Very High - PHA diagnostic |
| Helianthus annuus | Sunflower | High - EAC crop |
| Cucurbita pepo | Squash | High - Three Sisters/EAC |

### Co-occurrence Patterns

**Indicates varied diet:**
- Deer + fish + turkey + nuts = broad-spectrum subsistence
- Multiple fish species = seasonal fishing camp

**Indicates agriculture:**
- Maize + beans + squash = Three Sisters complex
- Sunflower + chenopodium + squash = Eastern Agricultural Complex

**Indicates specialized processing:**
- Multiple shellfish, no terrestrial animals = shellfish processing station
- Egg proteins + bird collagen = bird with egg preparation
- Vitellogenin + fish collagen = fish roe processing

## Proxy Species Strategy

Many Northeast species lack UniProt entries. We use taxonomically related species as proxies:

**Why proxies work:**
- Collagen is highly conserved within taxonomic groups
- Peptides from closely related species often match
- Better to detect "ungulate" or "carnivore" than miss entirely

**Proxy relationships:**
- Cattle → deer, moose, elk (all Artiodactyla)
- Pig → bear, raccoon (omnivore metabolism)
- Rat → all rodents (beaver, muskrat, squirrel, etc.)
- Chicken → grouse, quail (all Galliformes)
- European fish → American congeners (conserved proteins)

**Reporting proxies:**
Always report as taxonomic group, not specific species:
- "Bos taurus match indicates ungulate (likely deer family)"
- "Rattus match indicates rodent (beaver, muskrat, or squirrel)"

## Protein Preservation Expectations

### Excellent Preservation
- **Collagen** - survives thousands of years in bone, pottery
- **Ferritin, Transferrin** - compact, stable structures
- **Plant 2S albumins** - disulfide-stabilized
- **Zeins** - hydrophobic, binds ceramics

### Good Preservation
- **Hemoglobin** - if not overcooked
- **Muscle proteins** - in moderate cooking
- **Storage globulins** - abundant in plants
- **Tropomyosin** - shellfish identification

### Moderate Preservation
- **Enzymes** (LDH, GAPDH, CK) - degrade with heat
- **Albumins** - water-soluble, may leach
- **Plant lectins** - heat-labile

### Poor Preservation
- **Highly glycosylated proteins** - complex degradation
- **Small peptide hormones** - easily lost
- **Unstable enzymes** - denature readily

## Technical Considerations

### Always Use Deamidation Flag!

Archaeological proteins undergo deamidation (N→D, Q→E):
```bash
--deamidation  # REQUIRED for ancient samples
```

### Mass Error Tolerance

| Instrument | -e value | Tolerance |
|------------|----------|-----------|
| MALDI-TOF | 0.1 | ±100 ppm |
| Q Exactive (Orbitrap) | 0.01 | ±10 ppm |
| timsTOF Pro 2 | 0.01-0.02 | ±10-20 ppm |
| Q-TOF | 0.01-0.02 | ±10-20 ppm |
| Degraded samples | 0.2 | ±200 ppm |

### File Formats

PAMPA accepts:
- **MGF** (Mascot Generic Format) - recommended
- **mzML** (standard XML format)
- **CSV** (simple: m/z, intensity)

## Validation & Quality Control

### Multiple Peptides Required
- **High confidence**: 5+ peptides
- **Moderate confidence**: 3-4 peptides
- **Low confidence**: 1-2 peptides (needs validation)

### Check for Contamination
If human proteins detected:
- **COL1A1/COL1A2**: Possible handling, or actual human bone
- **Keratin**: Definitely contamination (skin, hair)
- **Albumin**: Possible contamination or preserved blood

### Validate Unexpected Results
- **Marine fish inland?** Check if anadromous (salmon, shad)
- **Tropical species?** Likely misidentification or contamination
- **Domestic animals before contact?** Proxy match, not actual species

## Updating the Database

### Add New Species

Edit `fetch_northeast_complete.py` and add to `NE_PROTEINS` dictionary:

```python
"Species_name": {
    "common_name": "Common name",
    "category": "Mammal - Category",
    "proteins": {
        "COL1A1": ["P12345"],
        "COL1A2": ["P67890"]
    }
}
```

### Regenerate Database

```bash
python fetch_northeast_complete.py
python pampa_craft.py --allpeptides -f northeast_complete.fasta -o northeast_markers.tsv
python pampa_craft.py --deamidation -p northeast_markers.tsv -o northeast_markers_deam.tsv
```

## Integration with Other Evidence

Combine protein results with:
- **Zooarchaeology**: Bone identification
- **Paleobotany**: Seeds, charcoal
- **Starch grain analysis**: Complements plant proteins
- **Lipid analysis**: Fatty acid profiles
- **Stable isotopes**: δ13C, δ15N for diet reconstruction

Proteins provide:
- **Species-level ID** (better than lipids)
- **Functional info** (egg vs. meat, roe vs. fish flesh)
- **Processing evidence** (enzymes indicate fresh vs. stored)
- **Mixed foods** (detect multiple species in one vessel)

## Archaeological Research Questions

### Subsistence Patterns
- What animals/plants were most important?
- Seasonal variation in resource use?
- Change over time periods?

### Trade & Exchange
- Marine resources inland = trade networks?
- Exotic species = long-distance exchange?

### Specialized Processing
- Vessels dedicated to specific resources?
- Evidence for food storage vs. fresh cooking?
- Ritual foods vs. daily subsistence?

### Agricultural Transitions
- When do domesticated plants appear?
- Co-occurrence of wild and domesticated?
- Three Sisters complex formation?

### Site Function
- Residential vs. specialized processing?
- Seasonal camps vs. year-round occupation?
- Feast debris vs. daily meals?

## Limitations

### False Negatives (Resource Used but Not Detected)
- Protein degraded beyond recognition
- Processing method didn't deposit proteins
- Vessel used for non-protein foods (rendered fats, etc.)
- Species not in database

### False Positives (Protein Detected but Resource Not Used)
- Modern contamination
- Proxy species match (report as group, not species!)
- Cross-contamination between samples
- Misidentified peptide sequences

### Database Gaps
- Many Northeast species lack UniProt entries
- Ancient domesticates may differ from modern varieties
- Some protein types underrepresented

### Best Practices
- **Analyze multiple vessels per context**
- **Include extraction blanks**
- **Report proxy matches as taxonomic groups**
- **Require multiple peptides for confidence**
- **Integrate with other lines of evidence**

## Files Included

| File | Description | Size |
|------|-------------|------|
| `northeast_complete.fasta` | Protein sequences | 118 KB |
| `northeast_markers.tsv` | Base peptides | 875 KB (6,409 peptides) |
| `northeast_markers_deam.tsv` | With deamidation | 1.6 MB (11,285 peptides) |
| `northeast_taxonomy.tsv` | Taxonomic classification | 2.9 KB |
| `northeast_database_info.txt` | Detailed metadata | 10 KB |
| `fetch_northeast_complete.py` | Database builder script | — |

## Citation

If using this database, please cite:

- **This database**: "Complete Northeast North American Archaeological Protein Reference Database for PAMPA (2025)" - https://github.com/clipo/pampa
- **PAMPA software**: Touzet H. & Rodrigues Pereira A. (2024) PAMPA: Protein Analysis by Mass Spectrometry for Ancient Species. https://github.com/touzet/pampa
- **UniProt**: The UniProt Consortium (2023) UniProt: the universal protein knowledgebase in 2023. Nucleic Acids Research.

## Questions & Support

- **General PAMPA**: See main README.md
- **Plant proteins**: See README_PLANT_PROTEINS.md and PLANT_PROTEIN_GUIDE.md
- **Database contents**: See northeast_database_info.txt
- **Issues**: https://github.com/clipo/pampa/issues

---

**System Status:**
✓ 50 species/proxies covering all major Northeast food resources
✓ 11,285 peptide markers with deamidation variants
✓ 20 ecological/functional categories
✓ Animals, fish, birds, shellfish, reptiles, plants
✓ Contamination controls included
✓ Validated and ready for archaeological analysis

**Ready to analyze your archaeological pottery residues!**
