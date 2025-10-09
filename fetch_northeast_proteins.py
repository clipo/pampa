#!/usr/bin/env python3
"""
Fetch Northeast Archaeological Protein Database from UniProt

This script fetches protein sequences from UniProt for fauna and flora found in
Northeast North American archaeological sites. It targets proteins that can survive
cooking and archaeological preservation, including:

ANIMAL PROTEINS (heat-stable and diagnostic):
- Collagen (Type I, II, III) - most abundant, heat-stable
- Keratin - highly stable
- Albumin - survives some cooking
- Myoglobin, Hemoglobin - blood proteins
- Actin, Myosin - muscle proteins (partially stable)
- Tropomyosin - allergen marker, heat-stable
- Parvalbumin - fish-specific, heat-stable

PLANT PROTEINS (cooking-resistant):
- Storage proteins: albumins, globulins, prolamins, glutelins
- Seed storage proteins (legumins, vicilins)
- Grain proteins (zeins, gliadins, glutenins)
- Heat shock proteins (HSPs)
- Enzyme inhibitors (protease, amylase inhibitors)

Author: Archaeological Proteomics Analysis
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import time
import sys
import pandas as pd
from typing import List, Dict, Set, Tuple
import re

class NortheastProteinFetcher:
    """Fetch and organize proteins for Northeast archaeological database"""

    def __init__(self, excel_file: str):
        self.excel_file = excel_file
        self.base_url = "https://rest.uniprot.org/uniprotkb/search"
        self.sequences = {}
        self.taxonomy_data = []
        self.failed_queries = []

        # Protein targets by category
        self.animal_proteins = [
            # Collagen - most important for ZooMS
            ("collagen", "COL1A1 OR COL1A2 OR COL2A1 OR COL3A1"),
            # Muscle proteins
            ("myosin", "MYH1 OR MYH2 OR MYH4 OR MYH7"),
            ("actin", "ACTA1 OR ACTB OR ACTG1"),
            ("tropomyosin", "TPM1 OR TPM2 OR TPM3"),
            # Blood proteins
            ("hemoglobin", "HBA OR HBB OR HBD"),
            ("myoglobin", "MB"),
            # Serum proteins
            ("albumin", "ALB"),
            ("transferrin", "TF"),
            # Keratin (for feathers, hair)
            ("keratin", "KRT1 OR KRT5 OR KRT10"),
            # Fish-specific
            ("parvalbumin", "PVALB"),
        ]

        self.plant_proteins = [
            # Storage proteins (seeds, nuts, grains)
            ("storage_globulin", "11S globulin OR legumin OR glycinin"),
            ("storage_albumin", "2S albumin OR napin"),
            ("vicilin", "7S globulin OR vicilin"),
            # Grain-specific
            ("zein", "zein"),  # Corn
            ("gliadin", "gliadin OR glutenin"),  # Wheat family
            ("avenin", "avenin"),  # Oats
            ("hordein", "hordein"),  # Barley
            # Enzyme inhibitors (very stable)
            ("protease_inhibitor", "trypsin inhibitor OR protease inhibitor"),
            ("amylase_inhibitor", "amylase inhibitor"),
            # Other abundant proteins
            ("ribulose", "RuBisCO OR ribulose"),
            ("heat_shock", "HSP70 OR heat shock protein"),
        ]

        self.fungal_proteins = [
            ("hydrophobin", "hydrophobin"),
            ("laccase", "laccase"),
            ("chitin", "chitin synthase OR chitinase"),
        ]

    def load_species_data(self):
        """Load all species from Excel file"""
        xl = pd.ExcelFile(self.excel_file)

        species_data = {
            'Faunal': [],
            'Fish': [],
            'Reptile': [],
            'Floral': []
        }

        for sheet_name in species_data.keys():
            if sheet_name in xl.sheet_names:
                df = pd.read_excel(xl, sheet_name=sheet_name)
                for _, row in df.iterrows():
                    if pd.notna(row['Scientific name']):
                        species_data[sheet_name].append({
                            'common': row['Common name'] if pd.notna(row['Common name']) else 'Unknown',
                            'scientific': row['Scientific name'],
                            'category': sheet_name
                        })

        return species_data

    def clean_scientific_name(self, name: str) -> Tuple[str, bool]:
        """
        Clean scientific name and determine if it needs family-level search
        Returns: (cleaned_name, is_family_level)
        """
        name = name.strip()

        # Handle special cases
        if ' sp.' in name or ' ssp.' in name:
            # Extract genus for family-level search
            genus = name.split()[0]
            return (genus, True)

        if '×' in name or ' × ' in name:
            # Hybrid - use first parent species
            parts = re.split(r'[×=]', name)
            if parts:
                parent = parts[0].strip()
                return (parent, False)

        if ' var.' in name:
            # Variety - use species level
            parts = name.split(' var.')
            return (parts[0].strip(), False)

        return (name, False)

    def query_uniprot(self, query: str, max_results: int = 5) -> List[Dict]:
        """Query UniProt REST API with rate limiting"""
        params = {
            'query': query,
            'format': 'json',
            'size': max_results,
            'fields': 'accession,id,protein_name,organism_name,organism_id,sequence,gene_names,reviewed'
        }

        url = f"{self.base_url}?{urllib.parse.urlencode(params)}"

        try:
            time.sleep(0.5)  # Rate limiting
            with urllib.request.urlopen(url, timeout=30) as response:
                data = response.read()
                result = eval(data.decode('utf-8'))  # Parse JSON
                return result.get('results', [])
        except Exception as e:
            print(f"  ⚠️  Query failed: {query[:100]}... | Error: {e}")
            self.failed_queries.append(query)
            return []

    def fetch_animal_proteins(self, species: Dict) -> int:
        """Fetch diagnostic proteins for animal species"""
        scientific = species['scientific']
        common = species['common']
        category = species['category']

        clean_name, is_family = self.clean_scientific_name(scientific)

        print(f"\n🔍 Fetching {category}: {common} ({scientific})")

        count = 0
        for protein_type, gene_query in self.animal_proteins:
            # Build query
            if is_family:
                query = f"(taxonomy:{clean_name}) AND ({gene_query}) AND reviewed:true"
            else:
                query = f'(organism:"{clean_name}") AND ({gene_query})'

            # Try reviewed first, then expand if needed
            results = self.query_uniprot(query + " AND reviewed:true", max_results=3)
            if not results and not is_family:
                # Try family level if species fails
                genus = clean_name.split()[0]
                query = f"(taxonomy:{genus}) AND ({gene_query}) AND reviewed:true"
                results = self.query_uniprot(query, max_results=2)

            for entry in results:
                accession = entry.get('primaryAccession', '')
                protein_name = entry.get('proteinDescription', {}).get('recommendedName', {}).get('fullName', {}).get('value', protein_type)
                organism = entry.get('organism', {}).get('scientificName', scientific)
                taxid = entry.get('organism', {}).get('taxonId', '')
                sequence = entry.get('sequence', {}).get('value', '')

                if sequence:
                    seq_id = f"{accession}_{organism.replace(' ', '_')}_{protein_type}"
                    self.sequences[seq_id] = {
                        'sequence': sequence,
                        'description': f"{protein_name} [{organism}]",
                        'accession': accession,
                        'organism': organism,
                        'protein_type': protein_type,
                        'category': category,
                        'taxid': taxid
                    }
                    count += 1

        if count > 0:
            print(f"  ✓ Found {count} proteins")
        else:
            print(f"  ⚠️  No proteins found")

        return count

    def fetch_plant_proteins(self, species: Dict) -> int:
        """Fetch storage and cooking-resistant proteins for plants"""
        scientific = species['scientific']
        common = species['common']

        clean_name, is_family = self.clean_scientific_name(scientific)

        print(f"\n🌱 Fetching Plant: {common} ({scientific})")

        count = 0

        # Determine protein targets based on plant type
        protein_targets = self.plant_proteins.copy()

        # Add specific proteins for certain plant types
        if 'Zea mays' in scientific:
            protein_targets.append(("zein", "zein"))
        elif any(nut in common.lower() for nut in ['walnut', 'hazelnut', 'chestnut', 'beech']):
            protein_targets.append(("allergen", "allergen"))
        elif 'rice' in common.lower():
            protein_targets.append(("oryzin", "oryzin OR glutelin"))

        for protein_type, search_term in protein_targets:
            if is_family:
                query = f"(taxonomy:{clean_name}) AND ({search_term}) AND reviewed:true"
            else:
                query = f'(organism:"{clean_name}") AND ({search_term})'

            results = self.query_uniprot(query + " AND reviewed:true", max_results=2)

            if not results and not is_family:
                # Try genus level
                genus = clean_name.split()[0]
                query = f"(taxonomy:{genus}) AND ({search_term}) AND reviewed:true"
                results = self.query_uniprot(query, max_results=2)

            for entry in results:
                accession = entry.get('primaryAccession', '')
                protein_name = entry.get('proteinDescription', {}).get('recommendedName', {}).get('fullName', {}).get('value', protein_type)
                organism = entry.get('organism', {}).get('scientificName', scientific)
                taxid = entry.get('organism', {}).get('taxonId', '')
                sequence = entry.get('sequence', {}).get('value', '')

                if sequence:
                    seq_id = f"{accession}_{organism.replace(' ', '_')}_{protein_type}"
                    self.sequences[seq_id] = {
                        'sequence': sequence,
                        'description': f"{protein_name} [{organism}]",
                        'accession': accession,
                        'organism': organism,
                        'protein_type': protein_type,
                        'category': 'Floral',
                        'taxid': taxid
                    }
                    count += 1

        if count > 0:
            print(f"  ✓ Found {count} proteins")
        else:
            print(f"  ⚠️  No proteins found")

        return count

    def fetch_fungal_proteins(self, species: Dict) -> int:
        """Fetch fungal proteins (mushrooms)"""
        scientific = species['scientific']
        common = species['common']

        print(f"\n🍄 Fetching Fungus: {common} ({scientific})")

        count = 0
        for protein_type, search_term in self.fungal_proteins:
            query = f'(organism:"{scientific}") AND ({search_term})'
            results = self.query_uniprot(query, max_results=2)

            if not results:
                # Try genus
                genus = scientific.split()[0]
                query = f"(taxonomy:{genus}) AND ({search_term}) AND reviewed:true"
                results = self.query_uniprot(query, max_results=2)

            for entry in results:
                accession = entry.get('primaryAccession', '')
                protein_name = entry.get('proteinDescription', {}).get('recommendedName', {}).get('fullName', {}).get('value', protein_type)
                organism = entry.get('organism', {}).get('scientificName', scientific)
                taxid = entry.get('organism', {}).get('taxonId', '')
                sequence = entry.get('sequence', {}).get('value', '')

                if sequence:
                    seq_id = f"{accession}_{organism.replace(' ', '_')}_{protein_type}"
                    self.sequences[seq_id] = {
                        'sequence': sequence,
                        'description': f"{protein_name} [{organism}]",
                        'accession': accession,
                        'organism': organism,
                        'protein_type': protein_type,
                        'category': 'Floral',
                        'taxid': taxid
                    }
                    count += 1

        if count > 0:
            print(f"  ✓ Found {count} proteins")

        return count

    def write_fasta(self, filename: str):
        """Write sequences to FASTA file"""
        with open(filename, 'w') as f:
            for seq_id, data in sorted(self.sequences.items()):
                f.write(f">{seq_id} {data['description']}\n")
                # Write sequence in 60-character lines
                seq = data['sequence']
                for i in range(0, len(seq), 60):
                    f.write(f"{seq[i:i+60]}\n")

        print(f"\n✓ Wrote {len(self.sequences)} sequences to {filename}")

    def write_taxonomy(self, filename: str):
        """Write taxonomy file for PAMPA"""
        taxonomy_entries = {}

        for seq_id, data in self.sequences.items():
            organism = data['organism']
            if organism not in taxonomy_entries:
                taxonomy_entries[organism] = {
                    'category': data['category'],
                    'taxid': data['taxid'],
                    'sequences': []
                }
            taxonomy_entries[organism]['sequences'].append(seq_id)

        with open(filename, 'w') as f:
            # Write header
            f.write("species\tsuperfamily\tfamily\tgenus\tspecies_name\n")

            for organism, info in sorted(taxonomy_entries.items()):
                parts = organism.split()
                genus = parts[0] if parts else organism
                species_name = ' '.join(parts[1:]) if len(parts) > 1 else ''

                # Map category to taxonomic group
                superfamily = ""
                family = ""

                if info['category'] == 'Faunal':
                    superfamily = "Mammalia/Aves"
                    family = genus
                elif info['category'] == 'Fish':
                    superfamily = "Actinopterygii"
                    family = genus
                elif info['category'] == 'Reptile':
                    superfamily = "Reptilia"
                    family = genus
                elif info['category'] == 'Floral':
                    superfamily = "Plantae"
                    family = genus

                f.write(f"{organism}\t{superfamily}\t{family}\t{genus}\t{species_name}\n")

        print(f"✓ Wrote taxonomy for {len(taxonomy_entries)} organisms to {filename}")

    def generate_report(self, filename: str):
        """Generate summary report"""
        categories = {}
        proteins = {}

        for seq_id, data in self.sequences.items():
            cat = data['category']
            prot = data['protein_type']

            categories[cat] = categories.get(cat, 0) + 1
            proteins[prot] = proteins.get(prot, 0) + 1

        with open(filename, 'w') as f:
            f.write("NORTHEAST ARCHAEOLOGICAL PROTEIN DATABASE\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Total sequences: {len(self.sequences)}\n\n")

            f.write("Sequences by Category:\n")
            f.write("-" * 40 + "\n")
            for cat, count in sorted(categories.items()):
                f.write(f"{cat:20s}: {count:4d}\n")

            f.write("\nSequences by Protein Type:\n")
            f.write("-" * 40 + "\n")
            for prot, count in sorted(proteins.items()):
                f.write(f"{prot:25s}: {count:4d}\n")

            if self.failed_queries:
                f.write(f"\n\nFailed queries: {len(self.failed_queries)}\n")
                f.write("-" * 40 + "\n")
                for query in self.failed_queries[:20]:
                    f.write(f"{query[:100]}...\n")

        print(f"✓ Wrote report to {filename}")

    def run(self):
        """Main execution"""
        print("=" * 80)
        print("NORTHEAST ARCHAEOLOGICAL PROTEIN DATABASE BUILDER")
        print("=" * 80)

        # Load species data
        print("\n📖 Loading species data from Excel...")
        species_data = self.load_species_data()

        total_species = sum(len(spp) for spp in species_data.values())
        print(f"✓ Loaded {total_species} species:")
        for category, species_list in species_data.items():
            print(f"  • {category}: {len(species_list)} species")

        # Process animals (fauna, fish, reptiles)
        print("\n" + "=" * 80)
        print("FETCHING ANIMAL PROTEINS")
        print("=" * 80)

        for category in ['Faunal', 'Fish', 'Reptile']:
            for species in species_data.get(category, []):
                self.fetch_animal_proteins(species)

        # Process plants
        print("\n" + "=" * 80)
        print("FETCHING PLANT PROTEINS")
        print("=" * 80)

        for species in species_data.get('Floral', []):
            # Check if it's a fungus
            if any(fungus in species['common'].lower() for fungus in ['mushroom', 'morel', 'bolete', 'puffball']):
                self.fetch_fungal_proteins(species)
            else:
                self.fetch_plant_proteins(species)

        # Write outputs
        print("\n" + "=" * 80)
        print("WRITING OUTPUT FILES")
        print("=" * 80)

        self.write_fasta("northeast_reference_proteins.fasta")
        self.write_taxonomy("northeast_taxonomy.tsv")
        self.generate_report("northeast_protein_report.txt")

        print("\n" + "=" * 80)
        print("COMPLETE!")
        print("=" * 80)
        print("\nNext steps:")
        print("1. Review northeast_protein_report.txt for coverage summary")
        print("2. Generate peptide markers:")
        print("   python pampa_craft.py --allpeptides -f northeast_reference_proteins.fasta -o northeast_markers.tsv")
        print("3. Add taxonomy information:")
        print("   python pampa_craft.py --fillin -p northeast_markers.tsv -f northeast_reference_proteins.fasta -t northeast_taxonomy.tsv -o northeast_markers_complete.tsv")
        print("4. Run classification:")
        print("   python pampa_classify.py -s spectra_dir/ -e 0.1 -p northeast_markers_complete.tsv -t northeast_taxonomy.tsv -o results.tsv")

def main():
    if len(sys.argv) < 2:
        print("Usage: python fetch_northeast_proteins.py <excel_file>")
        print("Example: python fetch_northeast_proteins.py 'plant_animal data by site.xlsx'")
        sys.exit(1)

    excel_file = sys.argv[1]
    fetcher = NortheastProteinFetcher(excel_file)
    fetcher.run()

if __name__ == "__main__":
    main()
