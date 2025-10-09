Hi Petra,

I worked on some scripts that will build a comprehensive protein reference database for identifying animal and plant remains from Northeast archaeological sites. These data are based on the XSLX file that you send... the idea is that the database will be able to be used with our PAMPA software to analyze mass spectrometry data from pottery residues and other archaeological samples.

**IMPORTANT UPDATE:** The automated script is now working! You have two options:

## OPTION A: AUTOMATED APPROACH (RECOMMENDED) - 90-120 minutes

**The script now works!** It will automatically fetch all proteins for all 266 species.

```bash
# Run the automated script
python3 fetch_northeast_proteins.py "plant_animal data by site.xlsx"

# This will take ~90-120 minutes and create:
# - northeast_reference_proteins.fasta (~1,000-2,000 proteins)
# - northeast_taxonomy.tsv (taxonomic hierarchy)
# - northeast_protein_report.txt (summary statistics)
```

**Advantages:**
- Much faster (90-120 minutes vs 20-30 hours)
- No manual work
- Consistent results
- Automatic error handling

**What the script does:**
1. Reads all 266 species from the Excel file
2. Queries UniProt for heat-stable proteins (collagen, storage proteins, etc.)
3. Downloads 2-8 proteins per species
4. Organizes into PAMPA-compatible format
5. Generates taxonomy file and report

**When to use Option A:** Always try this first! It works reliably now.

---

## OPTION B: MANUAL APPROACH - 20-30 hours

**Only use this if the automated script fails!** Full manual instructions are provided below.

**Your task (manual):** Download protein sequences from UniProt for 266 species manually via the web interface.

**Time estimate:** 20-30 hours over 1-2 weeks
**Files you'll create:**
- FASTA file with protein sequences
- Taxonomy file
- Tracking spreadsheet

**When to use Option B:** Only if Option A encounters problems you can't resolve.

---

Please follow these instructions carefully and document everything you do.

---

## PART 1: SETUP AND PREPARATION (30 minutes)

### Step 1: Organize Your Workspace

1. Create a new folder on your computer called `Northeast_Proteins`
2. Inside that folder, create these subfolders:
   - `downloaded_sequences/` - for FASTA files from UniProt
   - `working_files/` - for your tracking spreadsheets
   - `final_output/` - for completed files

3. Copy the file `plant_animal data by site.xlsx` into `working_files/`

### Step 2: Create Your Tracking Spreadsheet

Create a new Excel file called `protein_download_tracker.xlsx` with these columns:

| Category | Common Name | Scientific Name | Proteins Found | Download Status | Notes | Date Completed |
|----------|-------------|-----------------|----------------|-----------------|-------|----------------|
| Faunal | White Tailed Deer | Odocoileus virginianus | | Not Started | | |

**Instructions for the spreadsheet:**
- Copy all species from `plant_animal data by site.xlsx` into this tracker
- You'll fill in the other columns as you work
- Use color coding: Green = Complete, Yellow = In Progress, Red = Problem

### Step 3: Read the Background Materials

Read these two files in the PAMPA directory:
1. `NORTHEAST_PROTEIN_GUIDE.md` - Explains which proteins we need and why
2. `NORTHEAST_QUICKSTART.md` - Technical reference

**Key points to remember:**
- We want proteins that survive cooking (collagen, storage proteins, enzyme inhibitors)
- Focus on reviewed (Swiss-Prot) entries when possible
- Download 3-5 proteins per animal species, 2-3 per plant species

---

## PART 2: DOWNLOADING PROTEINS FROM UNIPROT (15-20 hours)

You'll repeat this process for each of the 266 species. Start with animals, then fish, then plants.

### Step 4: Search UniProt for Animal Proteins

**For each animal species (mammals, birds, reptiles):**

1. **Go to UniProt website:** https://www.uniprot.org/

2. **Search for collagen** (most important protein):
   - In the search box, type: `organism:"Odocoileus virginianus" AND protein:collagen`
   - Replace "Odocoileus virginianus" with your species' scientific name
   - Press Enter

3. **Filter the results:**
   - On the left sidebar, click "Reviewed (Swiss-Prot)" under "Status"
   - This shows only high-quality, manually curated entries
   - If you get 0 results, remove this filter and use all results

4. **If you still get no results, try genus-level search:**
   - Change search to: `taxonomy:Odocoileus AND protein:collagen`
   - This searches the entire deer genus, not just white-tailed deer

5. **Select proteins to download:**
   - Look for these protein names in the results:
     - "Collagen alpha-1(I) chain" (COL1A1) - PRIORITY 1
     - "Collagen alpha-2(I) chain" (COL1A2) - PRIORITY 2
     - "Collagen alpha-1(II) chain" (COL2A1) - PRIORITY 3
   - Click the checkbox next to 3-5 relevant entries
   - **Tip:** Prefer entries with longer sequences (>1000 amino acids)

6. **Download the sequences:**
   - Click "Download" button at top of results
   - Choose format: "FASTA (canonical)"
   - Save to `downloaded_sequences/` folder
   - Name file: `Faunal_Odocoileus_virginianus_collagen.fasta`

7. **Search for other important proteins:**

   Repeat steps 2-6 for these proteins (if available):

   - **Albumin:** `organism:"Odocoileus virginianus" AND protein:albumin`
   - **Myosin:** `organism:"Odocoileus virginianus" AND protein:myosin`
   - **Hemoglobin:** `organism:"Odocoileus virginianus" AND protein:hemoglobin`

   **Note:** Not all species will have all proteins. If you find nothing after trying species and genus level, write "Not Available" in your tracker and move on.

8. **Update your tracking spreadsheet:**
   - Proteins Found: "Collagen (3), Albumin (1), Myosin (2)"
   - Download Status: "Complete"
   - Date Completed: Today's date

9. **Move to the next animal species** and repeat steps 2-8.

### Step 5: Search UniProt for Fish Proteins

**For each fish species:**

Fish have slightly different priority proteins:

1. **Search for collagen first** (same as animals):
   - `organism:"Salmo trutta" AND protein:collagen`
   - Download 2-3 collagen sequences

2. **Search for parvalbumin** (fish-specific, very stable):
   - `organism:"Salmo trutta" AND protein:parvalbumin`
   - Download 1-2 sequences if available

3. **Search for tropomyosin** (another heat-stable fish protein):
   - `organism:"Salmo trutta" AND protein:tropomyosin`
   - Download 1-2 sequences if available

4. **Optional:** Also search for albumin and myosin (same as animals)

5. Update your tracking spreadsheet

### Step 6: Search UniProt for Plant Proteins

**For each plant species:**

Plants have different priority proteins because we're looking for storage proteins in seeds/nuts/grains:

1. **For cultivated grains (corn, barley, wild rice):**

   - **Corn (Zea mays):**
     - `organism:"Zea mays" AND protein:zein` - Download 2-3
     - `organism:"Zea mays" AND protein:globulin` - Download 1-2

   - **Wild rice (Zizania):**
     - `organism:"Zizania palustris" AND protein:glutelin` - Download 2-3
     - `organism:"Zizania palustris" AND protein:oryzin` - Download 1-2

2. **For nuts (walnut, hazelnut, chestnut, acorns):**

   - `organism:"Juglans nigra" AND protein:allergen` - Download 2-3
   - `organism:"Juglans nigra" AND protein:"11S globulin"` - Download 1-2
   - `organism:"Juglans nigra" AND protein:"2S albumin"` - Download 1-2

3. **For beans/legumes (if any in your list):**

   - `organism:"Phaseolus vulgaris" AND protein:phaseolin` - Download 2-3
   - `organism:"Phaseolus vulgaris" AND protein:vicilin` - Download 1-2

4. **For berries and other plants:**

   Try these general searches (many may return 0 results):
   - `organism:"[Scientific name]" AND protein:"storage protein"`
   - `organism:"[Scientific name]" AND protein:"seed protein"`
   - `taxonomy:[Genus] AND protein:albumin`

   **Important:** Many wild plants have limited data in UniProt. If you find nothing after trying species and genus level, document this and move on.

5. **For mushrooms:**

   - `organism:"Morchella americana" AND protein:hydrophobin`
   - `organism:"Boletus edulis" AND protein:laccase`

   **Note:** Fungi are poorly represented in UniProt. You may find very few proteins.

6. Update your tracking spreadsheet

### Step 7: Handle Problem Cases

You'll encounter these issues:

**Problem:** "I can't find any proteins for this species"

**Solutions (try in order):**
1. Try genus-level search: `taxonomy:Genus AND protein:[type]`
2. Try family-level: `taxonomy:Cervidae AND protein:collagen`
3. Search for a closely related species and use those proteins as proxy
4. If still nothing, mark as "No data available" and move on

**Problem:** "Should I use reviewed or unreviewed entries?"

**Answer:**
- Always prefer "Reviewed (Swiss-Prot)" - these are manually curated
- If no reviewed entries, use unreviewed (TrEMBL) entries
- Mark in your notes which type you used

**Problem:** "The scientific name in the spreadsheet seems wrong"

**Answer:**
- Try the name as written first
- If no results, Google the species to check for:
  - Synonyms (old scientific names)
  - Spelling variations
  - Subspecies names
- Document any changes in your tracker

**Problem:** "There are hundreds of results"

**Answer:**
- Filter by "Reviewed" status
- Sort by "Annotation score" (highest first)
- Download only top 3-5 entries
- Prefer entries with complete sequences (avoid fragments)

---

## PART 3: ORGANIZING YOUR DOWNLOADS (2-3 hours)

### Step 8: Combine All FASTA Files

Once you've downloaded proteins for all species:

1. **Open your terminal/command prompt**

2. **Navigate to your downloads folder:**
   ```bash
   cd path/to/Northeast_Proteins/downloaded_sequences/
   ```

3. **Combine all FASTA files:**

   **On Mac/Linux:**
   ```bash
   cat *.fasta > ../final_output/northeast_all_proteins_raw.fasta
   ```

   **On Windows (in PowerShell):**
   ```powershell
   Get-Content *.fasta | Set-Content ../final_output/northeast_all_proteins_raw.fasta
   ```

4. **Check the combined file:**
   ```bash
   # Count how many proteins you have (each starts with >)
   grep -c "^>" ../final_output/northeast_all_proteins_raw.fasta
   ```

   You should have 500-2000 sequences total.

### Step 9: Clean Up FASTA Headers

UniProt FASTA headers are complex. We need to standardize them for PAMPA.

1. **Open** `northeast_all_proteins_raw.fasta` in a text editor

2. **FASTA format looks like this:**
   ```
   >sp|P02452|CO1A1_BOVIN Collagen alpha-1(I) chain OS=Bos taurus OX=9913 GN=COL1A1 PE=1 SV=5
   MFSFVDLRLLLLATALLTHGQEEDVDEVAGAKEAKQEVEEVVEGKQKDVEVQKGDVGVGPPGPPGPPGPP...
   ```

3. **We need to simplify to:**
   ```
   >P02452_Bos_taurus_collagen Collagen alpha-1(I) chain [Bos taurus]
   ```

4. **Create a Python script** to do this automatically:

   Save this as `clean_fasta_headers.py`:

```python
#!/usr/bin/env python3
"""
Clean and standardize FASTA headers for PAMPA
"""

import re

def clean_header(header_line):
    """
    Convert UniProt header to PAMPA format
    Input: >sp|P02452|CO1A1_BOVIN Collagen alpha-1(I) chain OS=Bos taurus OX=9913 GN=COL1A1 PE=1 SV=5
    Output: >P02452_Bos_taurus_collagen Collagen alpha-1(I) chain [Bos taurus]
    """
    # Extract accession
    acc_match = re.search(r'\|([A-Z0-9]+)\|', header_line)
    if not acc_match:
        acc_match = re.search(r'^>([A-Z0-9]+)', header_line)
    accession = acc_match.group(1) if acc_match else "UNKNOWN"

    # Extract organism name (OS=...)
    org_match = re.search(r'OS=([^=]+?)(?:OX=|\s+GN=|\s+PE=|$)', header_line)
    organism = org_match.group(1).strip() if org_match else "Unknown_organism"
    organism_clean = organism.replace(' ', '_')

    # Extract protein name (between accession and OS=)
    prot_match = re.search(r'\|[A-Z0-9_]+\s+(.+?)\s+OS=', header_line)
    if not prot_match:
        prot_match = re.search(r'^>[A-Z0-9]+\s+(.+?)\s+OS=', header_line)
    protein_name = prot_match.group(1).strip() if prot_match else "unknown_protein"

    # Determine protein type for ID
    protein_type = "unknown"
    name_lower = protein_name.lower()
    if 'collagen' in name_lower:
        protein_type = 'collagen'
    elif 'albumin' in name_lower:
        protein_type = 'albumin'
    elif 'myosin' in name_lower:
        protein_type = 'myosin'
    elif 'parvalbumin' in name_lower:
        protein_type = 'parvalbumin'
    elif 'tropomyosin' in name_lower:
        protein_type = 'tropomyosin'
    elif 'zein' in name_lower:
        protein_type = 'zein'
    elif 'globulin' in name_lower:
        protein_type = 'globulin'
    elif 'vicilin' in name_lower:
        protein_type = 'vicilin'
    elif 'legumin' in name_lower:
        protein_type = 'legumin'
    elif 'inhibitor' in name_lower:
        protein_type = 'inhibitor'
    elif 'hemoglobin' in name_lower:
        protein_type = 'hemoglobin'
    elif 'myoglobin' in name_lower:
        protein_type = 'myoglobin'

    # Create new header
    new_id = f"{accession}_{organism_clean}_{protein_type}"
    new_description = f"{protein_name} [{organism}]"

    return f">{new_id} {new_description}"

def process_fasta(input_file, output_file):
    """Process FASTA file and clean headers"""
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.startswith('>'):
                # Clean the header
                new_header = clean_header(line.strip())
                outfile.write(new_header + '\n')
            else:
                # Keep sequence lines as-is
                outfile.write(line)

    print(f"Processed {input_file}")
    print(f"Output written to {output_file}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python clean_fasta_headers.py input.fasta output.fasta")
        print("Example: python clean_fasta_headers.py northeast_all_proteins_raw.fasta northeast_reference_proteins.fasta")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    process_fasta(input_file, output_file)
```

5. **Run the cleaning script:**
   ```bash
   cd ../final_output/
   python clean_fasta_headers.py northeast_all_proteins_raw.fasta northeast_reference_proteins.fasta
   ```

6. **Verify the output:**
   ```bash
   head -20 northeast_reference_proteins.fasta
   ```

   Headers should now look clean and consistent.

---

## PART 4: CREATE TAXONOMY FILE (2-3 hours)

PAMPA needs a taxonomy file to group species by family/genus for classification.

### Step 10: Build the Taxonomy Table

1. **Create a new file** called `northeast_taxonomy.tsv` in `final_output/`

2. **Add header row:**
   ```
   species	superfamily	family	genus	species_name
   ```

   **Important:** Columns are separated by TAB characters, not spaces or commas.

3. **For each species in your database, add a row:**

   **Format:**
   ```
   [Full Scientific Name]	[Superfamily]	[Family]	[Genus]	[species epithet]
   ```

   **Examples:**
   ```
   Odocoileus virginianus	Mammalia	Cervidae	Odocoileus	virginianus
   Salmo trutta	Actinopterygii	Salmonidae	Salmo	trutta
   Zea mays	Plantae	Poaceae	Zea	mays
   Juglans nigra	Plantae	Juglandaceae	Juglans	nigra
   Morchella americana	Fungi	Morchellaceae	Morchella	americana
   ```

4. **How to find taxonomy information:**

   **Option A: Use UniProt**
   - Go back to your UniProt search results
   - Click on any entry for that species
   - Look at "Taxonomy" section on the right
   - It shows: Kingdom > Phylum > Class > Order > Family > Genus > Species

   **Option B: Use NCBI Taxonomy**
   - Go to: https://www.ncbi.nlm.nih.gov/taxonomy
   - Search for your species
   - Look at "Lineage" section

   **Option C: Use Wikipedia**
   - Search for the species
   - Look at the right sidebar info box
   - Find "Family:" and "Genus:"

5. **Superfamily guidelines:**
   - Mammals: Use "Mammalia"
   - Birds: Use "Aves"
   - Fish: Use "Actinopterygii" (or specific order like "Salmoniformes")
   - Reptiles: Use "Reptilia"
   - Plants: Use "Plantae" (or division like "Magnoliopsida")
   - Fungi: Use "Fungi"

6. **Save the file** making sure to use TAB separators (not spaces)

7. **Validate your taxonomy file:**

   Count the lines:
   ```bash
   wc -l northeast_taxonomy.tsv
   ```

   Should be one more than the number of unique species (because of header row)

---

## PART 5: QUALITY CONTROL (1-2 hours)

### Step 11: Check Your Files

1. **Verify FASTA file:**

   ```bash
   # Count sequences
   grep -c "^>" northeast_reference_proteins.fasta

   # Check for empty sequences (should return nothing)
   grep -A 1 "^>" northeast_reference_proteins.fasta | grep "^>$"

   # Look at first few entries
   head -50 northeast_reference_proteins.fasta
   ```

   **What to check:**
   - Headers start with `>` and have format: `>Accession_Organism_Type Description`
   - Sequences only contain letters (ACDEFGHIKLMNPQRSTVWY)
   - No blank lines between header and sequence
   - Sequences can span multiple lines (this is normal)

2. **Verify taxonomy file:**

   ```bash
   # Check first 10 rows
   head -10 northeast_taxonomy.tsv

   # Count entries
   wc -l northeast_taxonomy.tsv
   ```

   **What to check:**
   - All columns are tab-separated (not spaces)
   - No empty cells
   - Species names match those in FASTA file
   - Genus matches first word of species name

3. **Create a summary statistics file:**

   Make a file called `northeast_database_summary.txt`:

   ```
   NORTHEAST ARCHAEOLOGICAL PROTEIN DATABASE
   Created by: [Your Name]
   Date: [Today's Date]

   DATABASE CONTENTS:
   - Total protein sequences: [count from grep]
   - Total species represented: [count from taxonomy file - 1]
     - Faunal (mammals/birds/mussels): [count]
     - Fish: [count]
     - Reptiles: [count]
     - Plants: [count]
     - Fungi: [count]

   COVERAGE NOTES:
   - Species with good coverage (5+ proteins): [list 5-10 examples]
   - Species with limited data (<3 proteins): [list 5-10 examples]
   - Species with no UniProt data: [list any]

   PROTEIN TYPES INCLUDED:
   - Collagen: [approximate count]
   - Albumin: [approximate count]
   - Storage proteins (plants): [approximate count]
   - Other: [count]

   POTENTIAL ISSUES:
   - [Note any problems you encountered]
   - [Species that needed genus-level searches]
   - [Any concerns about data quality]
   ```

### Step 12: Submit for Review

Package your files for Dr. Lipo:

1. **Final deliverables should include:**
   - `northeast_reference_proteins.fasta` - cleaned protein sequences
   - `northeast_taxonomy.tsv` - taxonomy mapping
   - `northeast_database_summary.txt` - your summary
   - `protein_download_tracker.xlsx` - your work log
   - `NOTES.txt` - any issues or questions

2. **Compress into a zip file:**
   ```bash
   cd ..
   zip -r Northeast_Proteins_Complete.zip final_output/ working_files/
   ```

3. **Email to Dr. Lipo with:**
   - Subject: "Northeast Protein Database - Complete"
   - Attach the zip file
   - Brief summary of any issues
   - Total hours worked

---

## PART 6: NEXT STEPS (After Dr. Lipo Reviews)

Once your database is approved, you may be asked to:

### Step 13: Generate Peptide Markers (If requested)

```bash
# Navigate to PAMPA directory
cd path/to/PAMPA

# Generate all tryptic peptides from your proteins
python pampa_craft.py --allpeptides \
  -f path/to/northeast_reference_proteins.fasta \
  -o northeast_markers_raw.tsv

# Add deamidation variants (N→D, Q→E) for ancient proteins
python pampa_craft.py --deamidation \
  -p northeast_markers_raw.tsv \
  -o northeast_markers_deam.tsv

# Add taxonomy information to markers
python pampa_craft.py --fillin \
  -p northeast_markers_deam.tsv \
  -f path/to/northeast_reference_proteins.fasta \
  -t path/to/northeast_taxonomy.tsv \
  -o northeast_markers_complete.tsv
```

This creates the final peptide marker table for species identification.

### Step 14: Test Classification (If requested)

If you have test spectra to analyze:

```bash
python pampa_classify.py \
  -s path/to/test_spectra/ \
  -e 0.1 \
  -p northeast_markers_complete.tsv \
  -t path/to/northeast_taxonomy.tsv \
  --deamidation \
  -o test_results.tsv
```

---

## TROUBLESHOOTING

### Common Issues and Solutions

**"UniProt search returns 0 results"**
- Check spelling of scientific name
- Try genus level: `taxonomy:Genus`
- Try family level: `taxonomy:Family`
- Search Google Scholar for correct/current species name

**"Download button is grayed out"**
- You may not have selected any entries (click checkboxes)
- Try selecting fewer entries (max 500 at once)
- Your browser may be blocking the download

**"FASTA file looks wrong"**
- Make sure you downloaded "FASTA (canonical)" format
- Not "FASTA (isoform)" or other formats
- Check file size - should be >1KB for even one sequence

**"Tab-separated file opens weird in Excel"**
- Excel may auto-convert tabs to columns (this is OK)
- Or save as proper .tsv: File > Save As > Tab-delimited Text
- Important: Keep tabs, don't let Excel change to commas

**"Python script won't run"**
- Make sure Python 3 is installed: `python3 --version`
- Make sure you're in the right directory: `pwd` or `cd`
- Check file names match exactly (case-sensitive)

**"I'm getting overwhelmed"**
- Take breaks! This is tedious work
- Do one category at a time (all mammals, then all fish, etc.)
- Start with priority species (deer, turkey, trout, corn)
- Ask Dr. Lipo if you can skip low-priority species

---

## ESTIMATED TIME BREAKDOWN

- Setup and learning: 2 hours
- Faunal species (64 species × 15 min): 16 hours
- Fish species (41 species × 10 min): 7 hours
- Reptile species (6 species × 10 min): 1 hour
- Plant species (155 species × 8 min): 20 hours *(many will have no data)*
- File organization and cleanup: 3 hours
- Quality control: 2 hours
- **Total: 51 hours**

**Realistic estimate:** 25-35 hours because many plants will have no UniProt data

**Suggested schedule:**
- Week 1: All animals (faunal, fish, reptiles) + file setup
- Week 2: All plants + file cleanup and QC

---

## QUESTIONS?

If you encounter problems:

1. **Check the troubleshooting section above**
2. **Read** `NORTHEAST_PROTEIN_GUIDE.md` for background
3. **Document the issue** in your tracker with screenshots
4. **Email Dr. Lipo** with:
   - Specific species you're having trouble with
   - What you've tried
   - Screenshots of error or search results
   - Your question

Remember: It's OK if some species have no data. Document it and move on. The goal is to get as much coverage as possible, not 100% coverage.

---

## FINAL NOTES

**This is important work!** You're building a unique resource that will help identify what Native Americans were cooking and eating in the Northeast. Your careful work will enable:

- Identifying domesticated crops vs. wild foods
- Distinguishing between different animals in cooking pots
- Understanding seasonal subsistence patterns
- Recognizing the adoption of agriculture

Take your time, be thorough, and document everything. Good luck!

---

**Please confirm receipt of these instructions and let me know when you plan to start.**

Best regards,
Dr. Lipo
