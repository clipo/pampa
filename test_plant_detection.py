#!/usr/bin/env python3
"""
Test script to validate plant protein detection system.
Checks that database files are properly formatted and PAMPA can read them.
"""

import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and report size."""
    path = Path(filepath)
    if path.exists():
        size = path.stat().st_size
        print(f"✓ {description}: {filepath} ({size:,} bytes)")
        return True
    else:
        print(f"✗ MISSING {description}: {filepath}")
        return False

def check_fasta_format(filepath):
    """Validate FASTA file format."""
    try:
        with open(filepath) as f:
            lines = f.readlines()

        if not lines:
            print(f"✗ FASTA file is empty: {filepath}")
            return False

        header_count = sum(1 for line in lines if line.startswith('>'))
        if header_count == 0:
            print(f"✗ No FASTA headers found in {filepath}")
            return False

        print(f"✓ FASTA format valid: {header_count} sequences")
        return True
    except Exception as e:
        print(f"✗ Error reading FASTA: {e}")
        return False

def check_tsv_format(filepath, expected_columns=None):
    """Validate TSV file format."""
    try:
        with open(filepath) as f:
            header = f.readline().strip().split('\t')
            line_count = sum(1 for _ in f)

        print(f"✓ TSV format valid: {len(header)} columns, {line_count:,} data rows")

        if expected_columns:
            missing = set(expected_columns) - set(header)
            if missing:
                print(f"  ⚠ Missing expected columns: {missing}")

        print(f"  Columns: {', '.join(header[:5])}..." if len(header) > 5 else f"  Columns: {', '.join(header)}")
        return True
    except Exception as e:
        print(f"✗ Error reading TSV: {e}")
        return False

def test_pampa_modules():
    """Test that PAMPA modules can be imported."""
    print("\n=== Testing PAMPA Module Imports ===")

    try:
        sys.path.insert(0, str(Path(__file__).parent / "src"))

        modules = [
            "config",
            "sequences",
            "markers",
            "peptide_table",
            "fasta_parsing",
            "taxonomy",
            "compute_masses"
        ]

        for module_name in modules:
            try:
                __import__(module_name)
                print(f"✓ Successfully imported: {module_name}")
            except ImportError as e:
                print(f"✗ Failed to import {module_name}: {e}")
                return False

        return True
    except Exception as e:
        print(f"✗ Error testing imports: {e}")
        return False

def main():
    """Run all validation tests."""
    print("=" * 60)
    print("Plant Protein Detection System Validation")
    print("=" * 60)

    all_tests_passed = True

    # Check essential files
    print("\n=== Checking Essential Files ===")
    files_to_check = [
        ("native_american_plants.fasta", "Protein sequence database"),
        ("plant_markers.tsv", "Peptide markers (no PTMs)"),
        ("plant_markers_deamidation.tsv", "Peptide markers (with deamidation)"),
        ("plant_taxonomy.tsv", "Taxonomy file"),
        ("fetch_plant_proteins.py", "Database fetching script"),
        ("PLANT_PROTEIN_GUIDE.md", "User guide"),
        ("PLANT_WORKFLOW.md", "Quick workflow guide")
    ]

    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_tests_passed = False

    # Validate FASTA format
    print("\n=== Validating FASTA Format ===")
    if not check_fasta_format("native_american_plants.fasta"):
        all_tests_passed = False

    # Validate TSV formats
    print("\n=== Validating Peptide Marker Tables ===")
    expected_columns = ["Rank", "TaxID", "Taxon name", "Sequence", "PTM", "Mass", "Marker"]

    print("\nBase markers (plant_markers.tsv):")
    if not check_tsv_format("plant_markers.tsv", expected_columns):
        all_tests_passed = False

    print("\nDeamidated markers (plant_markers_deamidation.tsv):")
    if not check_tsv_format("plant_markers_deamidation.tsv", expected_columns):
        all_tests_passed = False

    # Validate taxonomy file
    print("\n=== Validating Taxonomy File ===")
    if not check_tsv_format("plant_taxonomy.tsv"):
        all_tests_passed = False

    # Test PAMPA imports
    if not test_pampa_modules():
        all_tests_passed = False

    # Count proteins and peptides
    print("\n=== Database Statistics ===")
    try:
        with open("native_american_plants.fasta") as f:
            protein_count = sum(1 for line in f if line.startswith('>'))

        with open("plant_markers.tsv") as f:
            base_peptide_count = sum(1 for _ in f) - 1  # Subtract header

        with open("plant_markers_deamidation.tsv") as f:
            deam_peptide_count = sum(1 for _ in f) - 1

        print(f"Total proteins: {protein_count}")
        print(f"Peptides (base): {base_peptide_count:,}")
        print(f"Peptides (with deamidation): {deam_peptide_count:,}")
        print(f"Deamidation variants added: {deam_peptide_count - base_peptide_count:,}")
    except Exception as e:
        print(f"✗ Error counting statistics: {e}")
        all_tests_passed = False

    # Species coverage
    print("\n=== Species Coverage ===")
    species_list = [
        "Phaseolus vulgaris (Common bean)",
        "Zea mays (Maize)",
        "Helianthus annuus (Sunflower)",
        "Chenopodium quinoa (Quinoa/goosefoot)",
        "Cucurbita pepo (Squash)",
        "Amaranthus hypochondriacus (Amaranth)",
        "Zizania palustris (Wild rice)",
        "Juglans nigra (Black walnut)",
        "Carya illinoinensis (Pecan/hickory)",
        "Helianthus tuberosus (Jerusalem artichoke)"
    ]

    for species in species_list:
        print(f"  • {species}")

    # Final summary
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("✓ ALL TESTS PASSED")
        print("\nSystem is ready for plant protein detection!")
        print("\nNext steps:")
        print("  1. Prepare your MS/MS spectra (MGF, mzML, or CSV format)")
        print("  2. Run: python pampa_classify.py -s spectra_dir/ -e 0.1 \\")
        print("          -p plant_markers_deamidation.tsv -t plant_taxonomy.tsv \\")
        print("          --deamidation -o results.tsv")
        print("\nSee PLANT_WORKFLOW.md for detailed instructions.")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        print("\nPlease regenerate the database:")
        print("  python fetch_plant_proteins.py")
        return 1

if __name__ == "__main__":
    sys.exit(main())
