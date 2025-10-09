# Northeast Archaeological Protein Database - Quick Start Guide

## Summary

I've created a comprehensive framework for building a protein database for 266 Northeast species from your Excel file:
- **64 Faunal species** (mammals, birds, mussels)
- **41 Fish species**
- **6 Reptile species**
- **155 Plant species** (cultivated crops, nuts, berries, mushrooms)

## Files Created

1. **`fetch_northeast_proteins.py`** - Main fetching script (needs UniProt API syntax fix)
2. **`NORTHEAST_PROTEIN_GUIDE.md`** - Comprehensive 20-page guide with:
   - Protein targets (heat-stable, cooking-resistant)
   - Archaeological interpretation
   - PAMPA workflow integration
   - Troubleshooting tips

3. **`test_northeast_fetch.py`** - Test script for 9 representative species

## Recommended Approach: Manual Curation with UniProt Web Interface

Given the complexity of the UniProt REST API, I recommend this practical approach:

### Step 1: Use UniProt Web Interface for Key Species

**For Animals** (focus on diagnostic collagen):
```
1. Go to https://www.uniprot.org/
2. Search: organism:"Odocoileus virginianus" AND protein:collagen
3. Filter: Reviewed (Swiss-Prot) entries
4. Download FASTA for top 3-5 entries
5. Repeat for each animal species
```

**For Plants** (focus on storage proteins):
```
1. Search: organism:"Zea mays" AND protein:(zein OR storage)
2. Filter: Reviewed entries
3. Download FASTA
```

**Protein Priorities by Type:**
- **Mammals/Birds**: Collagen (col1a1, col1a2), Albumin, Myosin
- **Fish**: Collagen, Parvalbumin, Tropomyosin
- **Reptiles**: Collagen
- **Plants**: Storage proteins (globulins, albumins), Zeins (corn), Inhibitors
- **Mushrooms**: Often limited data - use genus level

### Step 2: Organize Downloaded Sequences

```bash
# Combine all downloaded FASTA files
cat faunal_*.fasta fish_*.fasta reptile_*.fasta plant_*.fasta > northeast_combined.fasta

# Clean up headers to match PAMPA format
# Format: >Accession_Organism_ProteinType Description
```

### Step 3: Create Taxonomy File

Create `northeast_taxonomy.tsv` with columns:
```
species	superfamily	family	genus	species_name
Odocoileus virginianus	Mammalia	Cervidae	Odocoileus	virginianus
Salmo trutta	Actinopterygii	Salmonidae	Salmo	trutta
Zea mays	Plantae	Poaceae	Zea	mays
...
```

### Step 4: Generate Peptide Markers

```bash
# Generate all tryptic peptides
python pampa_craft.py --allpeptides \
  -f northeast_combined.fasta \
  -o northeast_markers.tsv

# Add deamidation variants (for ancient proteins)
python pampa_craft.py --deamidation \
  -p northeast_markers.tsv \
  -o northeast_markers_deam.tsv

# Fill in taxonomy
python pampa_craft.py --fillin \
  -p northeast_markers_deam.tsv \
  -f northeast_combined.fasta \
  -t northeast_taxonomy.tsv \
  -o northeast_markers_complete.tsv
```

### Step 5: Run Classification

```bash
python pampa_classify.py \
  -s your_spectra_directory/ \
  -e 0.1 \
  -p northeast_markers_complete.tsv \
  -t northeast_taxonomy.tsv \
  --deamidation \
  -o results.tsv
```

## Alternative: Use Existing PAMPA Mammal Database + Add Plants

Since PAMPA includes a `--mammals` option, you might:

```bash
# Use existing mammal database for fauna
python pampa_classify.py --mammals \
  -s spectra/ -e 0.1 -o fauna_results.tsv

# Build separate plant database
# (manually fetch plant proteins as above)
python pampa_classify.py \
  -s spectra/ -e 0.1 \
  -p plant_markers.tsv \
  -t plant_taxonomy.tsv \
  -o plant_results.tsv
```

## Key Proteins to Prioritize

### Animals (ZooMS Standard):
1. **Collagen Type I** (COL1A1, COL1A2) - ESSENTIAL
   - Best species discrimination
   - Survives cooking and burial
   - Available for most vertebrates

2. **Collagen Type II** (COL2A1) - cartilage
3. **Albumin** (ALB) - blood protein
4. **Myoglobin** (MB) - muscle
5. **Parvalbumin** (PVALB) - fish-specific

### Plants (Archaeological Residues):
1. **Zeins** - Corn/maize specific
2. **11S Globulins** (legumins) - beans, nuts
3. **2S Albumins** - nuts, seeds
4. **Trypsin Inhibitors** - very heat-stable
5. **RuBisCO** - abundant in leaves

## Expected Coverage

**Good UniProt Coverage:**
- Domestic mammals (deer, dog, cattle relatives)
- Common fish (trout, bass, salmon family)
- Major crops (corn, beans)
- Tree nuts (walnut, hazelnut)

**Limited Coverage:**
- Wild berries
- Many mushroom species
- Regional fish species
- Freshwater mussels

**Solution for Limited Coverage:**
- Use genus-level searches
- Include related species as proxies
- Manual literature curation

## Quick Reference: UniProt Search Syntax

```
# Species-specific
organism:"Odocoileus virginianus" AND protein:collagen

# Genus-level
taxonomy:Odocoileus AND protein:collagen

# With gene name
organism:"Salmo trutta" AND gene:col1a1

# Reviewed only (higher quality)
organism:"Zea mays" AND protein:zein AND reviewed:true

# Protein family
taxonomy:Cervidae AND protein:collagen AND reviewed:true
```

## Troubleshooting

### "No sequences found"
- Try genus-level: `taxonomy:Genus`
- Remove `AND reviewed:true` filter
- Use family level: `taxonomy:Cervidae`
- Check species name spelling

### "Wrong species identified"
- Check for contamination
- Verify spectra quality
- Adjust mass tolerance (`-e` parameter)
- Consider that similar species may be indistinguishable

### "Script takes too long"
- Focus on high-priority species first
- Do mammals, then fish, then plants separately
- Use batch downloads from UniProt web interface

## Next Steps

1. ✅ **Start Small**: Download proteins for 5-10 key species manually
2. ✅ **Test Workflow**: Run through PAMPA pipeline with test data
3. ✅ **Expand Gradually**: Add more species as needed
4. ✅ **Validate**: Compare results with known archaeological samples

## Archaeological Context

Your Northeast database covers key subsistence resources:
- **Eastern Agricultural Complex**: Chenopodium, sunflower, squash
- **Three Sisters**: Corn, beans, squash
- **Tree Nuts**: Walnut, hazelnut, acorns, beech
- **Wild Foods**: Berries, tubers, wild rice
- **Game**: Deer, elk, turkey, waterfowl
- **Fish**: Trout, bass, perch, pike

This comprehensive coverage will help identify:
- Cooking activities (mixed residues)
- Storage practices (single-species residues)
- Seasonal patterns (fish vs. plant remains)
- Agricultural vs. foraging (domestic vs. wild)

## References

See `NORTHEAST_PROTEIN_GUIDE.md` for:
- Detailed protein selection rationale
- Heat stability information
- Archaeological interpretation guidelines
- Troubleshooting details
- Literature references

---

**Contact**: For PAMPA-specific questions, see main PAMPA documentation in this repository.
