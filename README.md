![](https://github.com/touzet/pampa/blob/main/img/pampa_logo.svg)

__PAMPA (Protein Analysis by Mass Spectrometry for Ancient Species)__ is a software suite tailored to handle various tasks associated with ZooMS (Zooarchaeology by Mass Spectrometry) data and peptide markers.

## Table of Contents

- [Installation](#installation)
- [Quick Start for Archaeologists](#quick-start-for-archaeologists)
- [Archaeological Analysis Guide](#archaeological-analysis-guide-poverty-point-example)
- [Plant Protein Detection (NEW!)](#plant-protein-detection-for-eastern-north-american-archaeology)
- [Northeast Regional Protein Database (NEW!)](#northeast-regional-protein-database-new)
- [Mass Spectrometry File Formats](#mass-spectrometry-file-formats)
  - [Q Exactive HF](#using-q-exactive™-hf-hybrid-quadrupole-orbitrap™-data)
  - [Bruker timsTOF](#using-bruker-timstof-pro-2-data)
- [Using UniProt Database](#using-uniprot-database-with-pampa)
- [Documentation](#documentation)
- [Bug Report](#bug-report)


## Installation

PAMPA is written in Python 3.7, and can be installed either by downloading the source code or cloning this repository.

 - downloading, as a zip file: button _code<>_ on the right-hand side of the screen
 - cloning: `git clone https://github.com/touzet/pampa.git`

PAMPA necessitates the Biopython, pyteomics and scipy libraries.

 - biopython (https://biopython.org/)
 - pyteomics (https://pypi.org/project/pyteomics/)
 - scipy.stats (https://scipy.org/)

## Quick Start for Archaeologists

If you're analyzing archaeological bone samples (e.g., from Poverty Point or similar sites), here's the fastest way to get started:

```bash
# 1. Install dependencies
pip install biopython pyteomics scipy

# 2. Build reference library with proxy species (real UniProt data)
python convert_uniprot_to_fasta.py --fetch P02453 P02465 Q9XSJ7 O46392 P02452 P08123 P02457 -o reference.fasta
python pampa_craft.py --allpeptides -f reference.fasta -o markers.tsv
python pampa_craft.py --deamidation -p markers.tsv -o markers_deam.tsv

# 3. Analyze your samples
python pampa_classify.py -s your_spectra_folder/ -e 0.1 -p markers_deam.tsv -o results.tsv
```

**What you'll identify:**
- `Bos taurus` = deer/ruminant
- `Canis familiaris` = bear/carnivore
- `Gallus gallus` = bird
- `Homo sapiens` = human
- No match = possibly fish

See the [full Archaeological Analysis Guide](#archaeological-analysis-guide-poverty-point-example) below for detailed instructions.

## Documentation

The documentation is available on PAMPA's wiki: https://github.com/touzet/pampa/wiki

## Mass Spectrometry File Formats

PAMPA supports the following file formats:
- **mzML** - Standard open format for mass spectrometry data
- **mgf** - Mascot Generic Format
- **csv/txt** - Simple peak list format (two columns: m/z and intensity)

### Using Q Exactive™ HF Hybrid Quadrupole-Orbitrap™ Data

The Q Exactive HF mass spectrometer typically outputs data in Thermo's proprietary .raw format. To use this data with PAMPA, you'll need to convert it to a supported format:

#### Option 1: Convert RAW to mzML (Recommended)

1. **Using MSConvert (ProteoWizard)**
   - Download ProteoWizard: https://proteowizard.sourceforge.io/
   - Convert your files:
     ```bash
     msconvert your_file.raw --mzML
     ```

2. **Using Thermo Xcalibur Software**
   - If you have access to Xcalibur, you can export directly to mzML format

#### Option 2: Export to MGF Format

Many proteomics software packages can export MGF files directly from RAW files:
- Proteome Discoverer
- MaxQuant
- MSConvert with MGF option: `msconvert your_file.raw --mgf`

#### Option 3: Export Peak Lists to CSV

Export your peak lists from any processing software with:
- Column 1: m/z values
- Column 2: intensity values
- Save as .csv or .txt file

### Recommended Error Tolerances for High-Resolution Data

When using Q Exactive HF data with PAMPA, use appropriate error tolerances:

```bash
# For Q Exactive HF (high accuracy, typical setting)
python pampa_classify.py -s spectra_dir/ -e 0.01 -p peptide_table.tsv -o output.tsv

# For very high accuracy (5-10 ppm)
python pampa_classify.py -s spectra_dir/ -e 0.005 -p peptide_table.tsv -o output.tsv

# Compare with MALDI-TOF (lower resolution)
python pampa_classify.py -s spectra_dir/ -e 0.1 -p peptide_table.tsv -o output.tsv
```

The `-e` parameter represents the error margin in Daltons. For Orbitrap instruments like the Q Exactive HF, use 0.005-0.02 Da depending on your calibration and requirements.

### Using Bruker timsTOF Pro 2 Data

The Bruker timsTOF Pro 2 produces data in Bruker's proprietary .d folder format containing TDF/TDF_BIN files. These files include ion mobility data (TIMS - Trapped Ion Mobility Spectrometry) in addition to traditional m/z and intensity values. PAMPA includes a dedicated converter script (`convert_bruker_timstof.py`) to handle this specialized data format.

#### Step 1: Install Conversion Tools

Choose one or more of the following conversion tools based on your needs:

##### Option A: AlphaTims (Recommended for Python users)
AlphaTims is a Python library specifically designed for timsTOF data:

```bash
# Install via pip
pip install alphatims

# Or with conda
conda install -c bioconda alphatims
```

**Pros:** Native Python integration, handles TIMS data correctly, no external dependencies
**Cons:** Limited to CSV and MGF output formats

##### Option B: MSConvert/ProteoWizard (Recommended for mzML)
MSConvert provides the most comprehensive conversion with full metadata preservation:

1. Download ProteoWizard from: https://proteowizard.sourceforge.io/
2. Install the software (Windows has best support, Linux/Mac via Docker)
3. MSConvert will be available in your PATH after installation

**Pros:** Produces standard mzML files, preserves all metadata, widely supported
**Cons:** Large installation size, best on Windows

##### Option C: Bruker DataAnalysis (If licensed)
If you have access to Bruker's DataAnalysis software:

1. Install Bruker Compass DataAnalysis
2. Command-line tool `tdf2mzml` will be available
3. Requires valid license

**Pros:** Official Bruker tool, guaranteed compatibility
**Cons:** Requires expensive license, Windows only

#### Step 2: Understanding Your Data Structure

Bruker timsTOF data is stored in `.d` folders containing:
```
sample.d/
├── analysis.tdf       # SQLite database with metadata
├── analysis.tdf_bin   # Binary data with spectra
└── ...                # Additional calibration and method files
```

#### Step 3: Convert Your Data

##### For Single File Conversion:

```bash
# Check which conversion tools are available
python convert_bruker_timstof.py -i sample.d -o output_dir -f mzML

# The script will automatically detect and use available tools
# Output will show:
#   MSConvert: ✓ or ✗
#   AlphaTims: ✓ or ✗
#   PyTeomics: ✓ or ✗

# Force specific conversion method
python convert_bruker_timstof.py -i sample.d -o output_dir -f mzML -m msconvert
python convert_bruker_timstof.py -i sample.d -o output_dir -f csv -m alphatims
```

##### For Batch Conversion (Multiple Files):

```bash
# Convert all .d folders in a directory
python convert_bruker_timstof.py -i /path/to/data_folder -o output_dir -f mgf --batch

# This will process all .d folders and create corresponding output files:
# sample1.d → sample1.mgf
# sample2.d → sample2.mgf
# etc.
```

##### Output Format Selection:

- **mzML**: Best for preserving all data and metadata
  ```bash
  python convert_bruker_timstof.py -i sample.d -o output_dir -f mzML
  ```

- **MGF**: Good for peptide identification workflows
  ```bash
  python convert_bruker_timstof.py -i sample.d -o output_dir -f mgf
  ```

- **CSV**: Simple peak lists for quick analysis
  ```bash
  python convert_bruker_timstof.py -i sample.d -o output_dir -f csv
  ```

#### Step 4: Run PAMPA Analysis

After conversion, use the output files with PAMPA:

```bash
# For timsTOF Pro 2 in MALDI mode (typical for ZooMS)
# Higher error tolerance due to MALDI ionization
python pampa_classify.py -s converted_spectra/ -e 0.02 -p peptide_table.tsv -o results.tsv

# For timsTOF Pro 2 in ESI mode (LC-MS/MS)
# Lower error tolerance due to ESI's higher accuracy
python pampa_classify.py -s converted_spectra/ -e 0.01 -p peptide_table.tsv -o results.tsv

# For very high accuracy work (5-10 ppm)
python pampa_classify.py -s converted_spectra/ -e 0.005 -p peptide_table.tsv -o results.tsv
```

#### Understanding TIMS Data for ZooMS

The timsTOF Pro 2 adds a fourth dimension to mass spectrometry data:
1. **m/z** - mass-to-charge ratio
2. **Intensity** - signal strength
3. **Retention Time** - (if using LC)
4. **Ion Mobility** - TIMS separation

For ZooMS peptide mass fingerprinting, the converter script automatically:
- Sums across the ion mobility dimension
- Combines all mobility-separated peaks of the same m/z
- Produces traditional 2D mass spectra suitable for PAMPA

#### Troubleshooting

**Issue: "No .d folders found"**
- Ensure your path points to the directory containing .d folders
- Check that folders end with .d extension

**Issue: "Conversion failed: Permission denied"**
- Ensure you have read access to .d folders
- Check write permissions for output directory

**Issue: "AlphaTims not working on Mac/Linux"**
- Some Bruker libraries may require additional setup
- Try using MSConvert via Docker instead

**Issue: "Output files are empty"**
- Check that .d folders contain valid TDF files
- Verify data was properly acquired on instrument
- Try different conversion method

#### Advanced Options

For specialized workflows, you can modify the converter script to:
- Extract specific scan ranges
- Filter by ion mobility values
- Apply peak picking algorithms
- Merge multiple files into one

Example for extracting specific mobility range (requires editing the script):
```python
# In convert_with_alphatims function
data = alphatims.TimsTOF(input_path)
# Filter for specific mobility range
filtered_data = data.filter(mobility_min=0.8, mobility_max=1.2)
```

## Using UniProt Database with PAMPA

PAMPA includes a comprehensive converter script (`convert_uniprot_to_fasta.py`) to prepare UniProt database entries for analysis. This enables you to create custom peptide reference libraries for any species or protein of interest.

### Supported UniProt Formats

The converter handles all major UniProt export formats:

- **UniProt XML** (.xml) - Most comprehensive format with full annotations
- **UniProt DAT** (.dat) - Swiss-Prot/TrEMBL flat file format
- **UniProt FASTA** (.fasta, .fa) - Standard sequence format with metadata extraction
- **UniProt TSV/CSV** - Table exports from UniProt search results
- **Direct API Access** - Fetch sequences using accession numbers

### Installation

The UniProt converter uses only Python standard library - no additional dependencies required!

### Basic Usage

#### Convert Any UniProt File to PAMPA Format

```bash
# Auto-detect format and convert
python convert_uniprot_to_fasta.py -i uniprot_data.xml -o sequences.fasta

# Specify format explicitly
python convert_uniprot_to_fasta.py -i data.dat -o sequences.fasta --format dat

# Filter for specific genes (e.g., only collagen)
python convert_uniprot_to_fasta.py -i uniprot.xml -o collagen.fasta --genes COL1A1 COL1A2

# Process existing UniProt FASTA with gene filtering
python convert_uniprot_to_fasta.py -i all_proteins.fasta -o collagen_only.fasta --genes COL1A1 COL1A2
```

#### Fetch Directly from UniProt API

```bash
# Fetch specific proteins by accession number
python convert_uniprot_to_fasta.py --fetch P02452 P08123 Q9XSJ7 -o fetched.fasta

# Combine API fetch with gene filtering
python convert_uniprot_to_fasta.py --fetch P02452 P08123 Q9XSJ7 A0A5G2QWQ4 -o collagen.fasta --genes COL1A1 COL1A2
```

### Complete Workflow: Building Custom Reference Libraries

#### Step 1: Obtain Sequences from UniProt

**Option A: Download from UniProt Website**
1. Go to https://www.uniprot.org/
2. Search for your proteins of interest:
   - Example: `(gene:COL1A1 OR gene:COL1A2) AND taxonomy:mammalia`
   - Example: `protein_name:"collagen alpha" AND organism:"Bovidae"`
3. Click "Download" and choose format:
   - XML (recommended - most complete)
   - FASTA (good for large datasets)
   - TSV (if you need to review in Excel first)

**Option B: Use UniProt Accession Numbers**
```bash
# If you have a list of accession numbers
python convert_uniprot_to_fasta.py --fetch P02452 P02458 P08123 Q9XSJ7 -o sequences.fasta
```

#### Step 2: Convert to PAMPA Format

```bash
# Convert downloaded file (auto-detects format)
python convert_uniprot_to_fasta.py -i uniprot-download.xml -o pampa_sequences.fasta

# Filter for specific genes during conversion
python convert_uniprot_to_fasta.py -i uniprot-download.xml -o collagen.fasta --genes COL1A1 COL1A2

# The script will show a summary:
# Found 45 sequences
# Sequences by gene:
#   COL1A1: 23
#   COL1A2: 22
```

#### Step 3: Generate Peptide Markers

```bash
# Generate all tryptic peptides from your sequences
python pampa_craft.py --allpeptides -f pampa_sequences.fasta -o peptide_markers.tsv

# Or create markers by homology with existing reference
python pampa_craft.py --homology -p existing_reference.tsv -f pampa_sequences.fasta -o new_markers.tsv
```

#### Step 4: Classify Your Mass Spectrometry Data

```bash
# Run classification with your custom peptide library
python pampa_classify.py -s spectra_folder/ -e 0.1 -p peptide_markers.tsv -o results.tsv

# For high-resolution instruments (Orbitrap, Q-TOF)
python pampa_classify.py -s spectra_folder/ -e 0.01 -p peptide_markers.tsv -o results.tsv
```

### Example Use Cases

#### Creating a Bovine-Specific Reference Library

```bash
# 1. Download all bovine collagen from UniProt
#    Search: "gene:(COL1A1 OR COL1A2) AND organism:9913"
#    Download as XML

# 2. Convert to FASTA
python convert_uniprot_to_fasta.py -i bovine_collagen.xml -o bovine_sequences.fasta

# 3. Generate peptide markers
python pampa_craft.py --allpeptides -f bovine_sequences.fasta -o bovine_peptides.tsv

# 4. Analyze samples
python pampa_classify.py -s cow_samples/ -e 0.1 -p bovine_peptides.tsv -o cow_results.tsv
```

#### Building a Multi-Species Archaeological Reference

```bash
# 1. Fetch sequences for multiple species
python convert_uniprot_to_fasta.py \
  --fetch P02452 P02453 Q9XSJ7 P02465 P02458 P02466 \
  -o archaeological_ref.fasta \
  --genes COL1A1 COL1A2

# 2. Add more species from a downloaded file
python convert_uniprot_to_fasta.py \
  -i additional_species.xml \
  -o more_sequences.fasta \
  --genes COL1A1 COL1A2

# 3. Combine FASTA files (using command line)
cat archaeological_ref.fasta more_sequences.fasta > combined.fasta

# 4. Generate comprehensive peptide table
python pampa_craft.py --allpeptides -f combined.fasta -o archaeological_peptides.tsv
```

#### Processing Large UniProt Datasets

```bash
# For large XML files with many proteins
python convert_uniprot_to_fasta.py \
  -i uniprot_trembl_mammalia.xml \
  -o mammalia_collagen.fasta \
  --genes COL1A1 COL1A2  # Filters during conversion to save memory
```

### Output Format

The converter creates PAMPA-compatible FASTA headers with essential metadata:

```
>P02452 Collagen alpha-1(I) chain OS=Homo sapiens OX=9606 GN=COL1A1
MLSFVDTRTLLLLAVTLCLATCQSLQEETVRKGP...
```

Where:
- `P02452` - UniProt accession number
- `OS=Homo sapiens` - Organism name (required for PAMPA)
- `OX=9606` - NCBI taxonomy ID (required for PAMPA)
- `GN=COL1A1` - Gene name (required for PAMPA)

### Tips and Best Practices

1. **Gene Name Filtering**: Always use `--genes` parameter when working with collagen to ensure you only get COL1A1 and COL1A2, not other collagen types

2. **Format Selection**:
   - XML provides the most complete information
   - FASTA is fastest for large datasets
   - TSV/CSV is useful if you want to review/filter in Excel first

3. **Combining Sources**: You can run the converter multiple times and concatenate FASTA files to build comprehensive libraries

4. **Quality Control**: The converter shows a summary of sequences found by gene - verify this matches your expectations

5. **Memory Considerations**: For very large files (>1GB), use FASTA format instead of XML as it's processed line-by-line

## Peptide tables for COL1A1 and COL1A2 markers

Spreadsheet for [mammals](https://docs.google.com/spreadsheets/d/1nwELNshZxF0h6DkIFNAYXDJqmq4NOSUOLWQlTZIzUDQ) (download [TSV](https://github.com/touzet/pampa/blob/main/Peptide_tables/table_mammals.tsv))

## COL1A1 and COL1A2 sequences

A collection of curated COL1A1 and COL1A2 sequences is available at https://github.com/touzet/pampa_sequences

## Archaeological Analysis Guide (Poverty Point Example)

This section provides a complete workflow for archaeological ZooMS analysis, using Poverty Point as an example. This approach works for any archaeological site where you need to identify animal remains.

### Overview: What Can Be Identified

With current UniProt sequences, you can:
- ✅ **Distinguish mammals from birds** (>95% accuracy)
- ✅ **Separate mammal types** (ruminants vs carnivores, ~70-80% accuracy)
- ✅ **Detect human contamination**
- ⚠️ **Fish identification** (limited - by exclusion only)

### Step 1: Install PAMPA and Dependencies

```bash
# Clone PAMPA repository
git clone https://github.com/touzet/pampa.git
cd pampa

# Install required Python packages
pip install biopython pyteomics scipy

# Optional: for Bruker timsTOF data
pip install alphatims
```

### Step 2: Build Your Reference Library

Since exact sequences for North American fauna (white-tailed deer, black bear) are not available in UniProt, we use taxonomically related species as proxies:

```bash
# Download proxy sequences from UniProt (these are REAL sequences)
python convert_uniprot_to_fasta.py --fetch \
  P02453 P02465 \  # Bos taurus (cattle) - proxy for deer
  Q9XSJ7 O46392 \  # Canis familiaris (dog) - proxy for bear/carnivores
  P02452 P08123 \  # Homo sapiens (human) - contamination check
  P02457 \        # Gallus gallus (chicken) - proxy for birds
  -o poverty_point_reference.fasta

# Generate peptide markers from sequences
python pampa_craft.py --allpeptides \
  -f poverty_point_reference.fasta \
  -o poverty_point_markers.tsv

# Add deamidation modifications (ESSENTIAL for ancient proteins!)
python pampa_craft.py --deamidation \
  -p poverty_point_markers.tsv \
  -o poverty_point_markers_deamidated.tsv
```

This creates a reference library with ~1000 peptide markers covering mammals and birds.

### Step 3: Prepare Your Mass Spectrometry Data

PAMPA accepts these formats:
- **mzML** (recommended)
- **MGF** (Mascot Generic Format)
- **CSV** (simple peak lists)

#### For Bruker timsTOF Pro 2:
```bash
python convert_bruker_timstof.py -i sample.d -o converted/ -f mzML
```

#### For Thermo Q Exactive:
```bash
# Convert RAW to mzML using MSConvert
msconvert sample.raw --mzML
```

#### For CSV format:
Create files with two columns: m/z, intensity
```
1105.54,1000
1428.74,2500
2084.05,1500
...
```

### Step 4: Run Species Identification

```bash
# For standard MALDI-TOF (lower resolution)
python pampa_classify.py \
  -s spectra_folder/ \
  -e 0.1 \
  -p poverty_point_markers_deamidated.tsv \
  -o results.tsv

# For high-resolution MS (Orbitrap, Q-TOF, timsTOF)
python pampa_classify.py \
  -s spectra_folder/ \
  -e 0.01 \
  -p poverty_point_markers_deamidated.tsv \
  -o results.tsv
```

Parameters:
- `-s`: folder containing your spectra files
- `-e`: error tolerance (0.1 Da for MALDI, 0.01 Da for high-resolution)
- `-p`: peptide reference library
- `-o`: output results file

### Step 5: Interpret Your Results

The results.tsv file will show matches to reference species. Here's how to interpret them:

| Result Shows | Interpret As | Confidence |
|--------------|--------------|------------|
| Bos taurus | Deer or ruminant | High |
| Canis lupus familiaris | Bear or carnivore | Moderate |
| Gallus gallus | Bird (turkey, waterfowl) | High |
| Homo sapiens | Human (contamination?) | Very High |
| No match | Possibly fish or degraded | Low |

### Step 6: Quality Control

1. **Check match scores**: Higher scores = better matches
2. **Look for multiple peptides**: Good identifications have 3+ matching peptides
3. **Consider taphonomy**: Burned or heavily degraded bone may not work
4. **Validate with known samples**: Test modern deer, turkey, etc. first

### Complete Example Workflow

```bash
# 1. Setup reference library (do once)
python convert_uniprot_to_fasta.py --fetch P02453 P02465 Q9XSJ7 O46392 P02452 P08123 P02457 \
  -o reference.fasta
python pampa_craft.py --allpeptides -f reference.fasta -o markers.tsv
python pampa_craft.py --deamidation -p markers.tsv -o markers_deam.tsv

# 2. Analyze archaeological samples
python pampa_classify.py -s poverty_point_bones/ -e 0.1 -p markers_deam.tsv -o pp_results.tsv

# 3. Check results
cat pp_results.tsv
```

### Troubleshooting

**Problem**: No matches found
- Check your error tolerance (-e parameter)
- Verify spectra file format
- Consider sample degradation

**Problem**: Only human matches
- Likely contamination during excavation/handling
- Use clean sampling protocols

**Problem**: Unexpected species matches
- Remember you're matching to proxy species
- Bos taurus = any ruminant, not specifically cattle

### Reporting Results

In publications, report as:

"Taxonomic identification was performed using PAMPA with reference sequences from related species as proxies: Bos taurus (Bovidae/Cervidae), Canis lupus familiaris (Carnivora), and Gallus gallus (Aves). Species assignments represent taxonomic group identification rather than species-level determination."

### Advanced Options

#### Add more reference species:
```bash
# Find available sequences
# Search UniProt for: taxonomy:Mammalia AND (gene:COL1A1 OR gene:COL1A2) AND reviewed:true

# Add sheep, pig, horse if needed
python convert_uniprot_to_fasta.py --fetch P02459 Q9XSJ7 F7B7Q8 -o more_refs.fasta
```

#### Focus on specific markers:
```bash
# Use limit file to focus on certain peptides
echo "Marker: P1, A, B, C" > limits.txt
python pampa_craft.py --allpeptides -f reference.fasta -l limits.txt -o focused_markers.tsv
```

#### Batch processing:
```bash
# Process multiple sample folders
for folder in site1/ site2/ site3/; do
  python pampa_classify.py -s $folder -e 0.1 -p markers_deam.tsv -o ${folder}_results.tsv
done
```

### Expected Success Rates

Based on other archaeological ZooMS studies:
- 60-80% of bone samples yield identifiable spectra
- 95%+ accuracy for mammal vs bird distinction
- 70-80% accuracy for within-mammal discrimination
- Modern reference samples should have near 100% success

### Getting Help

- **PAMPA issues**: https://github.com/touzet/pampa/issues
- **UniProt updates**: Check quarterly for new sequences
- **ZooMS community**: See recent papers in Journal of Archaeological Science

## Plant Protein Detection for Eastern North American Archaeology

PAMPA now includes a comprehensive plant protein detection system for identifying domesticated and wild plant remains in archaeological pottery residues. This approach extends ZooMS methodology to plant materials, enabling detection of the Eastern Agricultural Complex, Three Sisters agriculture, and wild plant processing.

### Quick Start: Plant Protein Analysis

The plant protein database is **ready to use** - no setup required!

```bash
# Analyze pottery residue for plant proteins
python pampa_classify.py \
    -s pottery_spectra_folder/ \
    -e 0.1 \
    -p plant_markers_deamidation.tsv \
    -t plant_taxonomy.tsv \
    --deamidation \
    -o plant_results.tsv
```

### What You Can Detect

**Eastern Agricultural Complex Plants:**
- 🌻 **Sunflower** (*Helianthus annuus*) - helianthinin, 2S albumins
- 🌿 **Chenopodium** (*C. berlandieri*) - chenopodin storage proteins
- 🎃 **Squash** (*Cucurbita pepo/maxima*) - cucurbitin, cucumisin
- 🌾 **Amaranth** (*Amaranthus*) - amarantin globulins

**Three Sisters Complex:**
- 🌽 **Maize** (*Zea mays*) - alpha/beta/gamma zeins (diagnostic!)
- 🫘 **Beans** (*Phaseolus vulgaris*) - phaseolin, phytohemagglutinin
- 🎃 **Squash** - co-occurs with maize and beans

**Wild Resources:**
- 🌾 **Wild rice** (*Zizania palustris*) - glutelins
- 🌰 **Tree nuts** (walnut, hickory) - 2S albumins, storage proteins
- 🌻 **Jerusalem artichoke** - tuber proteins

### Database Coverage

**51 proteins from 13 plant species**
- Beans: 18 proteins (phaseolin variants, PHA, arcelin, inhibitors)
- Maize: 9 proteins (zeins, globulins, glutelins)
- Squash: 6 proteins (cucurbitin, cucumisin, albumins)
- Sunflower: 4 proteins (helianthinin, albumins)
- Plus: chenopodium, amaranth, wild rice, nuts

**1,278 peptide markers** including deamidation variants for ancient proteins

### Archaeological Interpretation

PAMPA automatically identifies plant protein signatures that reveal dietary patterns:

| Pattern Detected | Interpretation | Time Period |
|-----------------|----------------|-------------|
| Sunflower + Chenopodium + Squash | Eastern Agricultural Complex | Archaic - Middle Woodland |
| Maize (zeins only) | Early maize adoption | Late Woodland (transitional) |
| Maize + Beans + Squash | Three Sisters agriculture | Late Woodland - Mississippian |
| Multiple tree nut proteins | Wild resource processing | Any period |
| No plant proteins detected | Non-food vessel or poor preservation | — |

### Example Workflows

#### Regional Survey of Late Woodland Vessels

```bash
# Analyze multiple vessels to track agricultural transition
for vessel in vessel_*/; do
    python pampa_classify.py \
        -s "$vessel" \
        -e 0.1 \
        -p plant_markers_deamidation.tsv \
        -t plant_taxonomy.tsv \
        --deamidation \
        -o "results/$(basename "$vessel")_plants.tsv"
done

# Look for patterns:
# - EAC dominance → pre-maize subsistence
# - Maize without beans → transitional period
# - Three Sisters → mature agriculture
```

#### Single Vessel Deep Analysis

```bash
# Comprehensive plant identification in well-preserved pottery
python pampa_classify.py \
    -s well_preserved_vessel/ \
    -e 0.1 \
    -p plant_markers_deamidation.tsv \
    -t plant_taxonomy.tsv \
    --deamidation \
    -o detailed_results.tsv

# Check results for:
# - Multiple peptide matches per species (high confidence)
# - Co-occurrence patterns (EAC vs Three Sisters)
# - Wild vs domesticated plant ratios
```

#### Temporal Comparison Across Site

```bash
# Compare dietary change from Early Woodland through Mississippian
for period in EarlyWoodland MiddleWoodland LateWoodland Mississippian; do
    python pampa_classify.py \
        -s ${period}_vessels/ \
        -e 0.1 \
        -p plant_markers_deamidation.tsv \
        -t plant_taxonomy.tsv \
        --deamidation \
        -o results/${period}_plant_summary.tsv
done

# Track trends:
# - Appearance of sunflower/chenopodium (EAC adoption)
# - First maize zeins (maize introduction)
# - Bean phaseolin + maize zeins (Three Sisters)
```

### Understanding Protein Preservation

Not all plant proteins preserve equally. PAMPA's database focuses on proteins most likely to survive in pottery residues:

**Excellent Preservation:**
- **2S Albumins** (sunflower, squash, nuts) - disulfide-stabilized, 8-15 kDa
- **Protease inhibitors** (beans) - extremely stable, compact structure
- **Zeins** (maize) - hydrophobic, readily bind ceramic surfaces

**Good Preservation:**
- **Storage globulins** (11S, 7S types) - abundant, moderate stability
- **Phaseolin** (beans) - 40-50% of bean protein, fragments survive cooking

**May Preserve with Good Conditions:**
- **Lectins** (phytohemagglutinin in beans) - denature during extended boiling
- **Specialized proteins** (cucurbitin, cucumisin in squash)

**Rarely Preserve:**
- **Metabolic enzymes** - heat-labile, low abundance

### Key Diagnostic Proteins

**Maize-Specific:**
- **Zeins** (alpha, beta, gamma variants) - UNIQUE to maize
- Detection = definitive evidence of maize processing

**Bean-Specific:**
- **Phytohemagglutinin (PHA)** - virtually unique to *Phaseolus*
- **Arcelin** - species-specific, definitive bean evidence
- **Phaseolin** - major storage protein, 40-50% of bean protein

**Eastern Agricultural Complex:**
- **Helianthinin** (sunflower) - major seed protein
- **Chenopodin** (chenopodium) - diagnostic for goosefoot
- **Cucurbitin** (squash) - anthelmintic protein unique to *Cucurbita*

### Adding New Plant Species

The database can be easily expanded for other regions or species:

```bash
# 1. Edit fetch_plant_proteins.py to add new species with UniProt accessions
# 2. Regenerate database:
python fetch_plant_proteins.py

# 3. Create new peptide markers:
python pampa_craft.py --allpeptides -f native_american_plants.fasta -o plant_markers.tsv
python pampa_craft.py --deamidation -p plant_markers.tsv -o plant_markers_deamidation.tsv

# 4. Analyze with updated database:
python pampa_classify.py -s spectra/ -e 0.1 -p plant_markers_deamidation.tsv -o results.tsv
```

### Technical Considerations

**Always use `--deamidation` flag for archaeological samples!**

Ancient proteins undergo deamidation (N→D, Q→E), adding +0.984 Da per modification. This is the most common post-translational modification in aged proteins.

**Mass Error Tolerance:**
- MALDI-TOF: `-e 0.1` (±100 ppm)
- High-resolution (Orbitrap, Q-TOF): `-e 0.01` (±10 ppm)
- Degraded samples: `-e 0.2` (±200 ppm)

**Spectra Formats:**
- MGF (Mascot Generic Format) - recommended
- mzML (mass spectrometry XML)
- CSV (simple m/z, intensity)

### Comprehensive Documentation

- **README_PLANT_PROTEINS.md** - Quick start guide and overview
- **PLANT_WORKFLOW.md** - Command reference and common workflows
- **PLANT_PROTEIN_GUIDE.md** - 20-page comprehensive guide including:
  - Detailed protein descriptions for all species
  - Archaeological interpretation strategies
  - Temporal and regional expectations
  - Protein stability and preservation factors
  - Troubleshooting and validation approaches
  - Integration with other paleobotanical methods

### Validation

The system includes comprehensive testing:

```bash
# Run validation suite
python test_plant_detection.py

# Checks:
# ✓ All database files present and properly formatted
# ✓ PAMPA modules import correctly
# ✓ 51 proteins from 13 species
# ✓ 1,278 peptide markers with deamidation
# ✓ Taxonomic classification working
```

### Expected Results by Time Period

**Archaic Period (>3000 BP):**
- Diverse wild plant proteins (nuts, seeds)
- Tree nut albumins dominant
- No domesticated crop proteins

**Early Woodland (3000-2200 BP):**
- Initial Eastern Agricultural Complex proteins appear
- Sunflower, squash, chenopodium
- No maize or beans

**Middle Woodland (2200-1200 BP):**
- Intensified indigenous crop proteins
- Peak EAC diversity
- Still no maize/beans in most regions

**Late Woodland (1200-1000 BP):**
- Maize zeins begin appearing
- EAC continues alongside maize
- Beans still rare or absent

**Mississippian (1000-500 BP):**
- Three Sisters dominance
- Maize + beans + squash co-occurrence
- Indigenous crops may continue

### Limitations and Considerations

**False Negatives (plant present but not detected):**
- Protein degraded beyond recognition
- Processing method didn't deposit proteins on vessel
- Vessel used for non-protein-rich plant parts
- Species not yet in database

**False Positives (protein detected but plant not used):**
- Modern contamination during excavation/storage
- Sequence similarity to unrelated proteins
- Always validate with multiple peptides!

**Database Coverage:**
- Some indigenous plants lack UniProt entries
- Using related species as proxies (e.g., quinoa for chenopodium)
- Ancient cultivars may differ from modern sequences

**Best Practices:**
- Analyze multiple vessels per context for robust patterns
- Integrate with macrobotanical evidence (seeds, charcoal)
- Combine with starch grain and phytolith analysis
- Consider burial environment effects on preservation
- Use multiple peptide matches for confident identifications

### Integration with Animal Proteins

You can analyze the same pottery for both plant and animal proteins:

```bash
# 1. Detect animals (mammals, birds, fish)
python pampa_classify.py \
    -s pottery_spectra/ -e 0.1 \
    -p animal_markers.tsv \
    -o animal_results.tsv

# 2. Detect plants (crops, wild resources)
python pampa_classify.py \
    -s pottery_spectra/ -e 0.1 \
    -p plant_markers_deamidation.tsv \
    -t plant_taxonomy.tsv \
    --deamidation \
    -o plant_results.tsv

# 3. Compare results to understand vessel use
# - Deer + maize = hunting + agriculture
# - Fish + wild rice = aquatic resource processing
# - Multiple animals + no plants = meat-only vessel
# - Multiple plants + no animals = plant processing vessel
```

### Updating the Plant Database

The plant protein database is maintained via an automated script:

```bash
# Fetch latest sequences from UniProt
python fetch_plant_proteins.py

# This downloads:
# - 51 proteins from 13 plant species
# - Creates native_american_plants.fasta
# - Generates plant_taxonomy.tsv
# - Produces plant_database_info.txt with metadata
```

Species currently included:
- *Phaseolus vulgaris* (common bean)
- *Phaseolus lunatus* (lima bean)
- *Zea mays* (maize)
- *Helianthus annuus* (sunflower)
- *Chenopodium quinoa* (proxy for *C. berlandieri*)
- *Cucurbita pepo* (summer squash)
- *Cucurbita maxima* (winter squash)
- *Amaranthus hypochondriacus* (amaranth)
- *Zizania palustris* (wild rice)
- *Juglans nigra* (black walnut)
- *Carya illinoinensis* (pecan, proxy for hickory)
- *Apios americana* (groundnut)
- *Helianthus tuberosus* (Jerusalem artichoke)

### Research Applications

**Subsistence Transitions:**
- Document shift from foraging to cultivation
- Track adoption of maize agriculture
- Identify Three Sisters complex formation

**Regional Variation:**
- Compare EAC adoption across sites
- Map maize diffusion through eastern North America
- Identify persistent wild resource use

**Specialized Processing:**
- Distinguish seed vs. vegetative part processing
- Detect nixtamalization of maize
- Identify germination/fermentation (enzyme presence)

**Dietary Breadth:**
- Quantify crop vs. wild plant reliance
- Measure agricultural intensification
- Track seasonal resource use patterns

### Citation

If using the plant protein detection feature, please cite:

- **PAMPA software**: Touzet H. & Rodrigues Pereira A. (2024) PAMPA: Protein Analysis by Mass Spectrometry for Ancient Species. https://github.com/touzet/pampa
- **Plant protein database**: "Native American Plant Protein Reference Database for PAMPA (2025)" - https://github.com/clipo/pampa
- **UniProt**: The UniProt Consortium (2023) UniProt: the universal protein knowledgebase in 2023. Nucleic Acids Research.

### System Status

✓ **51 proteins** from 13 plant species
✓ **1,278 peptide markers** (with deamidation)
✓ **714 base peptides** (no modifications)
✓ **Full taxonomic classification** included
✓ **Validated and tested** - ready for archaeological analysis

**Database ready to use** - just point PAMPA at your pottery residue spectra!

## Northeast Regional Protein Database (NEW!)

PAMPA now includes a comprehensive framework for building custom regional protein databases. The **Northeast Regional Database** covers 266 species of fauna and flora from Northeast North American archaeological sites, enabling identification of animals, fish, and plants processed in prehistoric contexts.

### Overview: Northeast Species Coverage

**Complete species lists from regional archaeological assemblages:**
- **64 Faunal species**: Mammals (deer, elk, bear, beaver, raccoon, etc.), Birds (turkey, waterfowl, raptors), Freshwater mussels
- **41 Fish species**: Bass, trout, perch, pike, catfish, minnows, suckers, darters
- **6 Reptile species**: Snapping, wood, box, painted, and musk turtles, snakes
- **155 Plant species**: Cultivated crops (corn, beans, squash), Tree nuts (walnut, hickory, chestnut, acorns), Wild berries, Edible mushrooms

**Data source:** Species lists compiled from published Northeast archaeological faunal and floral assemblages across New York, Pennsylvania, and New England sites spanning Archaic through Late Woodland periods.

### Quick Start: Build Your Northeast Database

The framework provides **step-by-step instructions** for creating the database:

```bash
# 1. Student follows detailed instructions in NORTHEAST_STUDENT_INSTRUCTIONS.md
#    - Downloads protein sequences from UniProt for all 266 species
#    - Targets heat-stable proteins (collagen, storage proteins, inhibitors)
#    - Creates tracking spreadsheet for progress

# 2. Automated header cleaning
python clean_fasta_headers.py \
    northeast_all_proteins_raw.fasta \
    northeast_reference_proteins.fasta

# 3. Generate peptide markers
python pampa_craft.py --allpeptides \
    -f northeast_reference_proteins.fasta \
    -o northeast_markers.tsv

python pampa_craft.py --deamidation \
    -p northeast_markers.tsv \
    -o northeast_markers_deam.tsv

python pampa_craft.py --fillin \
    -p northeast_markers_deam.tsv \
    -f northeast_reference_proteins.fasta \
    -t northeast_taxonomy.tsv \
    -o northeast_markers_complete.tsv

# 4. Analyze archaeological samples
python pampa_classify.py \
    -s northeast_pottery_spectra/ \
    -e 0.1 \
    -p northeast_markers_complete.tsv \
    -t northeast_taxonomy.tsv \
    --deamidation \
    -o northeast_results.tsv
```

### Target Proteins: Archaeological Survival

The database focuses on **proteins that survive cooking and burial**:

**Animal Proteins (ZooMS-style identification):**
- **Collagen Type I (COL1A1, COL1A2)** - PRIMARY TARGET
  - Best species discrimination
  - Survives cooking → gelatin (peptides remain)
  - Thousands of years preservation
- **Collagen Type II, III** - Cartilage, organs
- **Muscle proteins** - Myosin, actin, tropomyosin (partially stable)
- **Blood proteins** - Albumin, hemoglobin, myoglobin
- **Fish-specific** - Parvalbumin (very heat-stable allergen)
- **Keratin** - Feathers, hair, scales

**Plant Proteins (cooking-resistant):**
- **Storage globulins** (11S, 7S types) - Seeds, nuts, grains
- **Storage albumins** (2S) - Very stable, disulfide-bonded
- **Grain-specific**: Zeins (corn), gliadins/glutenins, oryzins (wild rice)
- **Enzyme inhibitors** - Trypsin, protease, amylase inhibitors (extremely stable)
- **RuBisCO** - Abundant in leafy vegetables
- **Heat shock proteins (HSP70)** - Stress response proteins

**Mushroom/Fungal Proteins:**
- Hydrophobins, laccases, chitin synthases

### Why These Proteins?

**Heat Stability = Archaeological Preservation**

Proteins that survive cooking also survive archaeological burial:
1. **Collagen → Gelatin**: Structure changes but peptides remain intact
2. **Storage proteins**: Evolved to survive desiccation and temperature extremes
3. **Enzyme inhibitors**: Chemically stable, compact structure, resist degradation
4. **Zeins (corn)**: Hydrophobic proteins readily bind ceramic surfaces
5. **Albumins**: Coagulate during cooking but fragments persist

### Documentation Suite

**Three comprehensive guides included:**

1. **NORTHEAST_STUDENT_INSTRUCTIONS.md** (20 pages)
   - Complete step-by-step workflow for research assistants
   - Formatted as instructional email
   - Every step detailed with no assumed knowledge
   - Includes UniProt search syntax, troubleshooting, time estimates
   - Python script for automated FASTA header cleaning
   - Quality control procedures
   - Expected completion time: 25-35 hours

2. **NORTHEAST_PROTEIN_GUIDE.md** (20 pages)
   - Scientific rationale for protein selection
   - Heat stability and preservation mechanisms
   - Taxonomic resolution by protein type
   - Archaeological interpretation frameworks
   - Integration with PAMPA workflow
   - Validation approaches
   - Literature references

3. **NORTHEAST_QUICKSTART.md**
   - Practical quick-reference guide
   - UniProt web interface instructions
   - Alternative manual curation approach
   - Taxonomy file creation
   - Command-line workflows
   - Common problems and solutions

### Archaeological Applications

**Regional Subsistence Analysis:**
- Track adoption of Three Sisters agriculture (corn + beans + squash)
- Document Eastern Agricultural Complex usage (sunflower, chenopodium, squash)
- Identify persistent wild resource processing (nuts, berries, wild rice)
- Distinguish aquatic vs terrestrial resource focus

**Temporal Patterns:**
- Archaic: Wild game + nut processing
- Early-Middle Woodland: EAC + wild foods
- Late Woodland: Maize introduction, EAC continuation
- Mississippian: Three Sisters intensification

**Vessel Function:**
- Cooking pots: Mixed animal + plant proteins
- Storage vessels: Single-species signatures
- Processing tools: Specific plant protein patterns

**Seasonal Indicators:**
- Fish proteins → warm season fishing camps
- Waterfowl → spring/fall migrations
- Nut proteins → fall harvest activities
- Fresh vs dried plant processing

### Database Coverage Expectations

**Excellent UniProt coverage:**
- Domestic mammals (deer, dog, cattle relatives as proxies)
- Common fish (trout, bass, salmon family)
- Major crops (corn, beans, squash)
- Tree nuts (walnut, hickory relatives, beech, chestnut)

**Limited or proxy-based coverage:**
- Many wild berries (use genus or family level)
- Mushroom species (fungi underrepresented in UniProt)
- Some regional fish species (use related species)
- Freshwater mussels (limited proteomic data)

**Solutions for gaps:**
- Use genus-level UniProt searches: `taxonomy:Genus`
- Include related species as proxies
- Manual literature curation for important species
- Homology-based marker design from related proteins

### Building Your Regional Database

**The framework is adaptable to any region:**

1. **Create species list** from published assemblages
   - Consult zooarchaeological reports
   - Review archaeobotanical studies
   - Include all documented taxa

2. **Follow student instructions** to download sequences
   - Systematic UniProt queries by species
   - Track progress in provided spreadsheet template
   - Handle problem cases with documented solutions

3. **Process and validate**
   - Clean headers with provided Python script
   - Create taxonomy file with regional classification
   - Quality control checks included

4. **Generate PAMPA markers**
   - Standard pampa_craft workflow
   - Deamidation variants for ancient proteins
   - Taxonomy integration

### Integration with Existing PAMPA Features

**Combine with other databases:**
```bash
# Use pre-built mammal database + regional fish/plants
python pampa_classify.py --mammals \
    -s pottery_spectra/ -e 0.1 -o mammals_results.tsv

python pampa_classify.py \
    -s pottery_spectra/ -e 0.1 \
    -p northeast_fish_markers.tsv \
    -o fish_results.tsv

python pampa_classify.py \
    -s pottery_spectra/ -e 0.1 \
    -p plant_markers_deamidation.tsv \
    -t plant_taxonomy.tsv \
    --deamidation \
    -o plant_results.tsv
```

**Combine results to understand vessel contents:**
- Deer + maize + beans = Three Sisters diet with hunting
- Fish + wild rice = aquatic resource processing
- Multiple nut proteins = fall harvest activities
- Turkey + no plants = specialized meat processing

### Technical Details

**Protein targets per organism type:**
- Mammals/Birds: 10 proteins (collagen, muscle, blood, keratin)
- Fish: 10 proteins (collagen, parvalbumin, tropomyosin, muscle)
- Reptiles: 8 proteins (collagen-focused)
- Plants (cultivated): 11-12 proteins (storage, grain-specific, inhibitors)
- Plants (wild): 6-8 proteins (storage proteins, RuBisCO)
- Fungi: 3-4 proteins (structural, enzymatic)

**Expected database size:**
- Animal proteins: 1,000-2,000 sequences
- Plant proteins: 500-1,000 sequences
- Total peptide markers (with deamidation): 10,000-50,000

**Quality assurance:**
- Multiple peptides required for confident identification
- Cross-validation with known reference samples
- Integration with traditional archaeozoology/archaeobotany

### Automated Fetching Script (Beta)

An automated script (`fetch_northeast_proteins.py`) is included but **requires UniProt REST API syntax updates** to function properly. The manual workflow via UniProt web interface is currently recommended and is more reliable for student use.

```bash
# Automated script (needs API fixes):
python fetch_northeast_proteins.py "plant_animal data by site.xlsx"

# Generates (when working):
# - northeast_reference_proteins.fasta
# - northeast_taxonomy.tsv
# - northeast_protein_report.txt
```

### Files Included

**Scripts:**
- `fetch_northeast_proteins.py` - Automated UniProt fetcher (needs API update)
- `test_northeast_fetch.py` - Test with 9 species subset
- `clean_fasta_headers.py` - Standardize headers for PAMPA (in documentation)

**Documentation:**
- `NORTHEAST_STUDENT_INSTRUCTIONS.md` - Complete student workflow
- `NORTHEAST_PROTEIN_GUIDE.md` - Scientific background
- `NORTHEAST_QUICKSTART.md` - Quick reference
- `plant_animal data by site.xlsx` - Species lists by site

**Generated files (after completion):**
- `northeast_reference_proteins.fasta` - Cleaned sequences
- `northeast_taxonomy.tsv` - Taxonomic hierarchy
- `northeast_markers_complete.tsv` - Peptide markers with taxonomy
- `northeast_database_summary.txt` - Statistics and notes

### Best Practices

**When building your database:**
1. Start with high-priority species (common animals, major crops)
2. Use reviewed (Swiss-Prot) UniProt entries when available
3. Fall back to genus/family level for rare species
4. Document all decisions in tracking spreadsheet
5. Test with modern reference samples first

**When analyzing samples:**
1. Always use `--deamidation` for archaeological proteins
2. Adjust error tolerance based on instrument (0.01-0.2 Da)
3. Require multiple peptide matches for confidence
4. Integrate with macro-remain evidence
5. Consider taphonomic factors (burning, degradation)

**For publication:**
- Report database creation methodology
- Cite UniProt accession numbers used
- Describe taxonomic proxy species clearly
- Provide validation with known samples
- Acknowledge limitations in species resolution

### Research Questions Addressable

With complete Northeast database:
- **Agricultural transitions**: EAC → Three Sisters timing and pathways
- **Subsistence diversification**: Wild vs domesticated resource ratios
- **Seasonal rounds**: Fishing, hunting, gathering patterns
- **Vessel specialization**: Cooking vs storage vs processing
- **Regional variation**: Dietary differences across Northeast
- **Cultural persistence**: Indigenous crops alongside maize
- **Exchange networks**: Non-local food resources
- **Climate adaptation**: Resource shifts with environmental change

### Future Enhancements

**Planned additions:**
- Fixed automated UniProt REST API script
- Pre-built Northeast reference database (when complete)
- Temporal benchmarks (expected species by period)
- Site-specific protein libraries
- Integration with modern genomic resources
- Expanded fungal protein coverage

### Support and Contributing

**Questions or issues:**
- Review comprehensive documentation first
- Check UniProt for species name variations
- Try genus/family level searches for rare species
- Consult PAMPA GitHub issues for technical problems

**Contributing:**
- Share completed regional databases
- Report coverage gaps or errors
- Suggest additional target proteins
- Provide archaeological validation data

**Citation:**
If using the Northeast Regional Database framework, please cite:
- **PAMPA software**: Touzet & Rodrigues Pereira (2024)
- **Northeast framework**: "Northeast Regional Protein Database for Archaeological Analysis" - https://github.com/clipo/pampa
- **UniProt**: The UniProt Consortium (2023)

### System Status

✓ **Framework complete** - Documentation and scripts ready
✓ **266 species** identified from regional assemblages
✓ **Comprehensive guides** for database construction
✓ **Student-tested workflow** with time estimates
✓ **Adaptable to other regions** - use as template
⚠️ **Manual approach recommended** until API script updated
⏳ **Database construction** requires 25-35 hours of student time

**Get started:** See `NORTHEAST_STUDENT_INSTRUCTIONS.md` for complete workflow

## Bug Report

PAMPA is still under development. If you need any help or if you come across unexpected behavior, you may contact the author (helene.touzet@univ-lille.fr). We value all feedback and contributions.  Thank you for helping us make the PAMPA project better!

