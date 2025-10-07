#!/usr/bin/env python3
"""
Fetch plant proteins from UniProt for archaeological pottery residue analysis.
Focuses on proteins from Native American cultivated and wild plants.
"""

import requests
import time
from pathlib import Path
from typing import List, Dict, Tuple
import sys

# Plant protein database organized by species and protein types
PLANT_PROTEINS = {
    # BEANS (Phaseolus)
    "Phaseolus_vulgaris": {
        "common_name": "Common bean",
        "proteins": {
            "phaseolin": ["P02853", "P04405", "P19329", "P13744", "P21569"],
            "phytohemagglutinin": ["P05087", "P05088"],
            "arcelin": ["P19330", "P19331", "P19332"],
            "alpha_amylase_inhibitor": ["P01060", "P02873", "P80404"],
            "storage_globulins": ["Q43629"],
            "protease_inhibitors": ["P01055", "P01056"],
            "lipoxygenase": ["P27480"],
            "urease": ["P42655"]
        }
    },
    "Phaseolus_lunatus": {
        "common_name": "Lima bean",
        "proteins": {
            "phaseolin": ["P04404"],
            "storage_proteins": ["Q43477"]
        }
    },

    # MAIZE (Zea mays)
    "Zea_mays": {
        "common_name": "Maize",
        "proteins": {
            "alpha_zeins": ["P04700", "P04701", "P04702", "P04703"],
            "beta_zein": ["P04705"],
            "gamma_zein": ["P06673"],
            "globulins": ["P15590"],
            "glutelins": ["Q7SIC8"],
            "prolamins": ["P06674"]
        }
    },

    # SUNFLOWER (Helianthus annuus)
    "Helianthus_annuus": {
        "common_name": "Sunflower",
        "proteins": {
            "helianthinin_11S": ["P19084"],
            "albumin_2S": ["P15461"],
            "storage_globulins": ["Q6VA02", "Q6VA03"]
        }
    },

    # CHENOPODIUM/QUINOA
    "Chenopodium_quinoa": {
        "common_name": "Quinoa (proxy for C. berlandieri)",
        "proteins": {
            "chenopodin_11S": ["Q84V37"],
            "albumin_2S": ["A0A1D5RZE4", "A0A1D5SIS4"],
            "storage_globulins": ["A0A1D5RZK6"]
        }
    },

    # SQUASH/GOURD (Cucurbita)
    "Cucurbita_pepo": {
        "common_name": "Squash/pumpkin",
        "proteins": {
            "cucurbitin": ["P26654"],
            "cucumisin": ["P25776"],
            "albumin_2S": ["Q39639", "Q39640"],
            "storage_proteins": ["Q9SRZ8"]
        }
    },
    "Cucurbita_maxima": {
        "common_name": "Winter squash",
        "proteins": {
            "storage_proteins": ["Q9XGS6"]
        }
    },

    # AMARANTH
    "Amaranthus_hypochondriacus": {
        "common_name": "Amaranth",
        "proteins": {
            "amarantin_11S": ["P16349"],
            "albumins": ["A0A140JWP2", "P11828"],
            "globulins": ["Q43652"]
        }
    },

    # WILD RICE
    "Zizania_palustris": {
        "common_name": "Wild rice",
        "proteins": {
            "glutelins": ["Q5QKU4"],
            "storage_proteins": ["Q5QKU5"]
        }
    },

    # TREE NUTS - limited UniProt entries but included where available
    "Juglans_nigra": {
        "common_name": "Black walnut",
        "proteins": {
            "albumin_2S": ["Q2TPW5"],
            "storage_proteins": ["A0A2P6PAH8"]
        }
    },
    "Carya_illinoinensis": {
        "common_name": "Pecan (proxy for hickory)",
        "proteins": {
            "albumins": ["B6CGA9"],
            "storage_proteins": ["A0A2P6QY45"]
        }
    },

    # ADDITIONAL SPECIES (using general searches if specific accessions unavailable)
    "Apios_americana": {
        "common_name": "Groundnut",
        "proteins": {
            # Will search by organism name if no specific accessions
        }
    },
    "Helianthus_tuberosus": {
        "common_name": "Jerusalem artichoke",
        "proteins": {
            # Will search by organism name
        }
    }
}


def fetch_from_uniprot(accessions: List[str], organism_name: str = None) -> str:
    """
    Fetch protein sequences from UniProt by accession numbers or organism name.

    Args:
        accessions: List of UniProt accession numbers
        organism_name: Organism name for broader search if accessions empty

    Returns:
        FASTA formatted sequences
    """
    sequences = []

    if accessions:
        # Fetch by specific accessions
        for acc in accessions:
            url = f"https://rest.uniprot.org/uniprotkb/{acc}.fasta"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    sequences.append(response.text.strip())
                    print(f"  ✓ Fetched {acc}")
                else:
                    print(f"  ✗ Failed to fetch {acc}: HTTP {response.status_code}", file=sys.stderr)
                time.sleep(0.2)  # Rate limiting
            except Exception as e:
                print(f"  ✗ Error fetching {acc}: {e}", file=sys.stderr)

    elif organism_name:
        # Broader search by organism
        print(f"  Searching UniProt for {organism_name}...")
        query = f"organism_name:\"{organism_name}\" AND reviewed:true"
        url = f"https://rest.uniprot.org/uniprotkb/search?query={query}&format=fasta&size=100"
        try:
            response = requests.get(url)
            if response.status_code == 200 and response.text.strip():
                sequences.append(response.text.strip())
                print(f"  ✓ Fetched proteins from {organism_name}")
            else:
                print(f"  ✗ No reviewed proteins found for {organism_name}", file=sys.stderr)
            time.sleep(0.5)
        except Exception as e:
            print(f"  ✗ Error searching {organism_name}: {e}", file=sys.stderr)

    return "\n".join(sequences)


def build_plant_database(output_dir: Path = Path(".")):
    """
    Build comprehensive plant protein reference database.

    Args:
        output_dir: Directory to save output files
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    all_sequences = []
    taxonomy_data = []

    print("\n=== Fetching Plant Proteins from UniProt ===\n")

    for species, data in PLANT_PROTEINS.items():
        common_name = data.get("common_name", species)
        print(f"\n{species} ({common_name}):")

        species_sequences = []

        if data["proteins"]:
            for protein_type, accessions in data["proteins"].items():
                if accessions:
                    print(f"  {protein_type}:")
                    seqs = fetch_from_uniprot(accessions)
                    if seqs:
                        species_sequences.append(seqs)
        else:
            # No specific accessions, try organism search
            seqs = fetch_from_uniprot([], organism_name=species.replace("_", " "))
            if seqs:
                species_sequences.append(seqs)

        if species_sequences:
            all_sequences.extend(species_sequences)

            # Add to taxonomy (simplified)
            genus = species.split("_")[0]
            taxonomy_data.append(f"{species}\t{genus}\t{common_name}")

    # Write combined FASTA
    fasta_path = output_dir / "native_american_plants.fasta"
    with open(fasta_path, 'w') as f:
        f.write("\n".join(all_sequences))
    print(f"\n✓ Wrote {fasta_path}")

    # Write taxonomy file
    taxonomy_path = output_dir / "plant_taxonomy.tsv"
    with open(taxonomy_path, 'w') as f:
        f.write("Species\tGenus\tCommon_Name\n")
        f.write("\n".join(taxonomy_data))
    print(f"✓ Wrote {taxonomy_path}")

    # Write metadata
    metadata_path = output_dir / "plant_database_info.txt"
    with open(metadata_path, 'w') as f:
        f.write("Native American Plant Protein Database\n")
        f.write("=" * 50 + "\n\n")
        f.write("Species included:\n")
        for species, data in PLANT_PROTEINS.items():
            f.write(f"\n{species} ({data.get('common_name', 'N/A')})\n")
            if data['proteins']:
                for ptype, accs in data['proteins'].items():
                    f.write(f"  - {ptype}: {len(accs)} accessions\n")
    print(f"✓ Wrote {metadata_path}")

    print(f"\n=== Database Build Complete ===")
    print(f"Total species: {len(PLANT_PROTEINS)}")
    print(f"\nNext steps:")
    print(f"  1. Generate peptide markers:")
    print(f"     python pampa_craft.py --allpeptides -f {fasta_path} -o plant_markers.tsv")
    print(f"  2. Add deamidation:")
    print(f"     python pampa_craft.py --deamidation -p plant_markers.tsv -o plant_markers_deam.tsv")
    print(f"  3. Classify your spectra:")
    print(f"     python pampa_classify.py -s spectra_dir/ -e 0.1 -p plant_markers_deam.tsv -t {taxonomy_path} -o results.tsv")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Fetch Native American plant proteins from UniProt for archaeological analysis"
    )
    parser.add_argument(
        "-o", "--output-dir",
        default=".",
        help="Output directory for database files (default: current directory)"
    )

    args = parser.parse_args()

    build_plant_database(Path(args.output_dir))
