![](https://github.com/touzet/pampa/blob/main/img/pampa_logo.svg)

__PAMPA (Protein Analysis by Mass Spectrometry for Ancient Species)__ is a software suite tailored to handle various tasks associated with ZooMS (Zooarchaeology by Mass Spectrometry) data and peptide markers.

## Table of Contents

- [Installation](#installation)
- [Quick Start for Archaeologists](#quick-start-for-archaeologists)
- [Archaeological Analysis Guide](#archaeological-analysis-guide-poverty-point-example)
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

## Bug Report

PAMPA is still under development. If you need any help or if you come across unexpected behavior, you may contact the author (helene.touzet@univ-lille.fr). We value all feedback and contributions.  Thank you for helping us make the PAMPA project better!

