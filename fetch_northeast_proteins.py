#!/usr/bin/env python3
"""
Fetch Northeast Archaeological Protein Database from UniProt (FIXED VERSION)

This script fetches protein sequences from UniProt for fauna and flora found in
Northeast North American archaeological sites using the CORRECT UniProt REST API syntax.

Author: Archaeological Proteomics Analysis
Version: 2.0 - Fixed API queries
"""

import urllib.request
import urllib.parse
import json
import time
import sys
import pandas as pd
from typing import List, Dict, Tuple
import re

class NortheastProteinFetcher:
    """Fetch and organize proteins for Northeast archaeological database"""

    def __init__(self, excel_file: str):
        self.excel_file = excel_file
        self.base_url = "https://rest.uniprot.org/uniprotkb/search"
        self.sequences = {}
        self.taxonomy_data = []
        self.failed_queries = []
        self.query_count = 0

        # Protein targets - using keywords and protein_name (not gene symbols)
        self.animal_proteins = [
            ("collagen", "keyword:collagen"),
            ("myosin", "protein_name:myosin"),
            ("actin", "protein_name:actin"),
            ("tropomyosin", "protein_name:tropomyosin"),
            ("hemoglobin", "protein_name:hemoglobin"),
            ("myoglobin", "protein_name:myoglobin"),
            ("albumin", "protein_name:albumin"),
            ("parvalbumin", "protein_name:parvalbumin"),
        ]

        self.plant_proteins = [
            ("globulin", "protein_name:globulin"),
            ("albumin", "protein_name:albumin"),
            ("vicilin", "protein_name:vicilin"),
            ("zein", "protein_name:zein"),
            ("glutelin", "protein_name:glutelin"),
            ("inhibitor", "protein_name:inhibitor"),
        ]

        self.fungal_proteins = [
            ("hydrophobin", "protein_name:hydrophobin"),
            ("laccase", "protein_name:laccase"),
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
        Returns: (cleaned_name, is_genus_level)
        """
        name = name.strip()

        # Handle special cases
        if ' sp.' in name or ' ssp.' in name:
            genus = name.split()[0]
            return (genus, True)

        if '×' in name or ' × ' in name:
            parts = re.split(r'[×=]', name)
            if parts:
                parent = parts[0].strip()
                return (parent, False)

        if ' var.' in name:
            parts = name.split(' var.')
            return (parts[0].strip(), False)

        return (name, False)

    def query_uniprot(self, query: str, max_results: int = 5) -> List[Dict]:
        """Query UniProt REST API with CORRECT syntax and rate limiting"""
        params = {
            'query': query,
            'format': 'json',
            'size': str(max_results),
            'fields': 'accession,id,protein_name,organism_name,organism_id,sequence,gene_names,reviewed'
        }

        url = f"{self.base_url}?{urllib.parse.urlencode(params, quote_via=urllib.parse.quote)}"

        try:
            self.query_count += 1
            time.sleep(0.35)  # Rate limiting - ~3 queries/second

            with urllib.request.urlopen(url, timeout=30) as response:
                data = response.read()
                result = json.loads(data.decode('utf-8'))
                return result.get('results', [])
        except Exception as e:
            print(f"  ⚠️  Query failed: {query[:80]}... | {e}")
            self.failed_queries.append((query, str(e)))
            return []

    def fetch_animal_proteins(self, species: Dict) -> int:
        """Fetch diagnostic proteins for animal species"""
        scientific = species['scientific']
        common = species['common']
        category = species['category']

        clean_name, is_genus = self.clean_scientific_name(scientific)

        print(f"\n🔍 {category}: {common} ({scientific})", end="", flush=True)

        count = 0
        for protein_type, protein_query in self.animal_proteins:
            # Build query with correct syntax
            if is_genus:
                # Genus-level search
                query = f'taxonomy_name:"{clean_name}" AND {protein_query} AND reviewed:true'
            else:
                # Species-level search
                query = f'organism_name:"{clean_name}" AND {protein_query}'

            # Try species/genus level first
            results = self.query_uniprot(query, max_results=2)

            # If no results, try broader genus search
            if not results and not is_genus:
                genus = clean_name.split()[0]
                query = f'taxonomy_name:"{genus}" AND {protein_query} AND reviewed:true'
                results = self.query_uniprot(query, max_results=1)

            for entry in results:
                accession = entry.get('primaryAccession', '')

                # Get protein name
                prot_desc = entry.get('proteinDescription', {})
                rec_name = prot_desc.get('recommendedName', {})
                protein_name = rec_name.get('fullName', {}).get('value', '') if rec_name else ''

                if not protein_name:
                    sub_names = prot_desc.get('submissionNames', [])
                    if sub_names:
                        protein_name = sub_names[0].get('fullName', {}).get('value', protein_type)
                    else:
                        protein_name = protein_type

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
            print(f" ✓ {count} proteins")
        else:
            print(f" ⚠️  No proteins")

        return count

    def fetch_plant_proteins(self, species: Dict) -> int:
        """Fetch storage and cooking-resistant proteins for plants"""
        scientific = species['scientific']
        common = species['common']

        clean_name, is_genus = self.clean_scientific_name(scientific)

        print(f"\n🌱 Plant: {common} ({scientific})", end="", flush=True)

        count = 0

        # Determine protein targets
        protein_targets = self.plant_proteins.copy()

        # Add specific proteins for certain types
        if 'Zea mays' in scientific or 'corn' in common.lower() or 'maize' in common.lower():
            protein_targets = [("zein", "protein_name:zein"), ("globulin", "protein_name:globulin")]
        elif any(nut in common.lower() for nut in ['walnut', 'hazelnut', 'chestnut', 'hickory', 'pecan', 'beech']):
            protein_targets = [("allergen", "protein_name:allergen"), ("albumin", "protein_name:albumin")]
        elif 'rice' in common.lower():
            protein_targets = [("glutelin", "protein_name:glutelin"), ("globulin", "protein_name:globulin")]

        for protein_type, protein_query in protein_targets:
            if is_genus:
                query = f'taxonomy_name:"{clean_name}" AND {protein_query} AND reviewed:true'
            else:
                query = f'organism_name:"{clean_name}" AND {protein_query}'

            results = self.query_uniprot(query, max_results=2)

            if not results and not is_genus:
                genus = clean_name.split()[0]
                query = f'taxonomy_name:"{genus}" AND {protein_query} AND reviewed:true'
                results = self.query_uniprot(query, max_results=1)

            for entry in results:
                accession = entry.get('primaryAccession', '')

                prot_desc = entry.get('proteinDescription', {})
                rec_name = prot_desc.get('recommendedName', {})
                protein_name = rec_name.get('fullName', {}).get('value', '') if rec_name else ''

                if not protein_name:
                    sub_names = prot_desc.get('submissionNames', [])
                    if sub_names:
                        protein_name = sub_names[0].get('fullName', {}).get('value', protein_type)
                    else:
                        protein_name = protein_type

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
            print(f" ✓ {count} proteins")
        else:
            print(f" ⚠️  No proteins")

        return count

    def fetch_fungal_proteins(self, species: Dict) -> int:
        """Fetch fungal proteins (mushrooms)"""
        scientific = species['scientific']
        common = species['common']

        print(f"\n🍄 Fungus: {common} ({scientific})", end="", flush=True)

        count = 0
        for protein_type, protein_query in self.fungal_proteins:
            query = f'organism_name:"{scientific}" AND {protein_query}'
            results = self.query_uniprot(query, max_results=2)

            if not results:
                genus = scientific.split()[0]
                query = f'taxonomy_name:"{genus}" AND {protein_query}'
                results = self.query_uniprot(query, max_results=1)

            for entry in results:
                accession = entry.get('primaryAccession', '')

                prot_desc = entry.get('proteinDescription', {})
                rec_name = prot_desc.get('recommendedName', {})
                protein_name = rec_name.get('fullName', {}).get('value', '') if rec_name else ''

                if not protein_name:
                    sub_names = prot_desc.get('submissionNames', [])
                    if sub_names:
                        protein_name = sub_names[0].get('fullName', {}).get('value', protein_type)
                    else:
                        protein_name = protein_type

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
            print(f" ✓ {count} proteins")
        else:
            print(f" ⚠️  No proteins")

        return count

    def write_fasta(self, filename: str):
        """Write sequences to FASTA file"""
        with open(filename, 'w') as f:
            for seq_id, data in sorted(self.sequences.items()):
                f.write(f">{seq_id} {data['description']}\n")
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
            f.write("species\tsuperfamily\tfamily\tgenus\tspecies_name\n")

            for organism, info in sorted(taxonomy_entries.items()):
                parts = organism.split()
                genus = parts[0] if parts else organism
                species_name = ' '.join(parts[1:]) if len(parts) > 1 else ''

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
                else:
                    superfamily = "Unknown"
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
            f.write(f"Total sequences fetched: {len(self.sequences)}\n")
            f.write(f"Total UniProt queries: {self.query_count}\n")
            f.write(f"Failed queries: {len(self.failed_queries)}\n\n")

            f.write("Sequences by Category:\n")
            f.write("-" * 40 + "\n")
            for cat, count in sorted(categories.items()):
                f.write(f"{cat:20s}: {count:4d}\n")

            f.write("\nSequences by Protein Type:\n")
            f.write("-" * 40 + "\n")
            for prot, count in sorted(proteins.items()):
                f.write(f"{prot:25s}: {count:4d}\n")

            if self.failed_queries:
                f.write(f"\n\nFailed Queries ({len(self.failed_queries)}):\n")
                f.write("-" * 40 + "\n")
                for query, error in self.failed_queries[:30]:
                    f.write(f"Query: {query[:80]}...\n")
                    f.write(f"Error: {error}\n\n")

        print(f"✓ Wrote report to {filename}")

    def run(self):
        """Main execution"""
        print("=" * 80)
        print("NORTHEAST ARCHAEOLOGICAL PROTEIN DATABASE BUILDER v2.0")
        print("=" * 80)

        # Load species data
        print("\n📖 Loading species data from Excel...")
        species_data = self.load_species_data()

        total_species = sum(len(spp) for spp in species_data.values())
        print(f"✓ Loaded {total_species} species:")
        for category, species_list in species_data.items():
            print(f"  • {category}: {len(species_list)} species")

        print(f"\n⏱️  Estimated time: ~{total_species * 0.4:.0f} minutes ({total_species * 8 * 0.35:.0f}s queries + processing)")
        print("=" * 80)

        # Process animals
        print("\nFETCHING ANIMAL PROTEINS")
        print("=" * 80)

        for category in ['Faunal', 'Fish', 'Reptile']:
            for species in species_data.get(category, []):
                self.fetch_animal_proteins(species)

        # Process plants
        print("\n" + "=" * 80)
        print("FETCHING PLANT PROTEINS")
        print("=" * 80)

        for species in species_data.get('Floral', []):
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
        print(f"\nFetched {len(self.sequences)} protein sequences from {self.query_count} UniProt queries")
        print("\nNext steps:")
        print("1. Review northeast_protein_report.txt")
        print("2. Generate peptide markers:")
        print("   python pampa_craft.py --allpeptides -f northeast_reference_proteins.fasta -o northeast_markers.tsv")
        print("3. Add deamidation and taxonomy:")
        print("   python pampa_craft.py --deamidation -p northeast_markers.tsv -o northeast_markers_deam.tsv")
        print("   python pampa_craft.py --fillin -p northeast_markers_deam.tsv -f northeast_reference_proteins.fasta -t northeast_taxonomy.tsv -o northeast_markers_complete.tsv")
        print("4. Analyze samples:")
        print("   python pampa_classify.py -s spectra/ -e 0.1 -p northeast_markers_complete.tsv -t northeast_taxonomy.tsv --deamidation -o results.tsv")

def main():
    if len(sys.argv) < 2:
        print("Usage: python fetch_northeast_proteins_v2.py <excel_file>")
        print("Example: python fetch_northeast_proteins_v2.py 'plant_animal data by site.xlsx'")
        sys.exit(1)

    excel_file = sys.argv[1]
    fetcher = NortheastProteinFetcher(excel_file)
    fetcher.run()

if __name__ == "__main__":
    main()
