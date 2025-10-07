#!/usr/bin/env python3
"""
Comprehensive protein fetching for Northeast North American archaeological analysis.
Includes animals, fish, birds, shellfish, reptiles, and plants.
"""

import requests
import time
from pathlib import Path
from typing import List, Dict
import sys

# Complete protein database for Northeast North American archaeology
NE_PROTEINS = {
    # ============================================================================
    # MAMMALS - COLLAGEN (Primary structural proteins)
    # ============================================================================
    "Odocoileus_virginianus": {
        "common_name": "White-tailed deer",
        "category": "Mammal - Ungulate",
        "proteins": {
            "COL1A1": ["P02453"],
            "COL1A2": ["P02465"],
            "Hemoglobin_alpha": ["P68228"],
            "Hemoglobin_beta": ["P68229"],
            "Serum_albumin": ["P19121"],
            "LDH_A": ["Q29550"],
            "LDH_B": ["Q29551"],
            "GAPDH": ["Q28554"]
        }
    },

    "Ursus_americanus": {
        "common_name": "Black bear",
        "category": "Mammal - Carnivore",
        "proteins": {
            "COL1A1": ["A0A6J0WK64"],
            "COL1A2": ["A0A6J0Z288"],
            "Hemoglobin_alpha": ["P60522"],
            "Hemoglobin_beta": ["P68084"]
        }
    },

    "Alces_alces": {
        "common_name": "Moose",
        "category": "Mammal - Ungulate",
        "proteins": {
            "COL1A1_proxy": ["P02453"],  # Using Bos taurus
            "COL1A2_proxy": ["P02465"],  # Using Bos taurus
            "Hemoglobin_alpha": ["P01958"],
            "Hemoglobin_beta": ["P21627"]
        }
    },

    "Cervus_elaphus": {
        "common_name": "Elk/Red deer (proxy for wapiti)",
        "category": "Mammal - Ungulate",
        "proteins": {
            "COL1A1": ["O46392"],
            "COL1A2": ["O46393"]
        }
    },

    "Canis_lupus": {
        "common_name": "Wolf/Dog",
        "category": "Mammal - Carnivore",
        "proteins": {
            "COL1A1": ["P22202"],
            "COL1A2": ["P30754"],
            "Serum_albumin": ["P49822"]
        }
    },

    "Felis_catus": {
        "common_name": "Cat (proxy for lynx)",
        "category": "Mammal - Carnivore",
        "proteins": {
            "COL1A1": ["O97767"],
            "COL1A2": ["O97768"],
            "Serum_albumin": ["P49064"]
        }
    },

    "Oryctolagus_cuniculus": {
        "common_name": "Rabbit (proxy for hare/cottontail)",
        "category": "Mammal - Small game",
        "proteins": {
            "COL1A1": ["P02452"],
            "COL1A2": ["Q28668"],
            "Serum_albumin": ["P49065"],
            "Creatine_kinase": ["P00563"]
        }
    },

    "Rattus_norvegicus": {
        "common_name": "Rat (proxy for rodents: beaver, muskrat, squirrel, etc.)",
        "category": "Mammal - Rodent",
        "proteins": {
            "COL1A1": ["P02454"],
            "COL1A2": ["P02466"],
            "Hemoglobin_alpha": ["P01946"],
            "Hemoglobin_beta": ["P02091"],
            "Serum_albumin": ["P02770"]
        }
    },

    "Bos_taurus": {
        "common_name": "Cattle (general ungulate proxy)",
        "category": "Mammal - Ungulate proxy",
        "proteins": {
            "COL1A1": ["P02453"],
            "COL1A2": ["P02465"],
            "Myosin_heavy_1": ["Q3T145"],
            "Myosin_heavy_2": ["Q3T134"],
            "Myosin_heavy_7": ["Q29079"],
            "Actin_beta": ["P60712"],
            "Actin_alpha": ["P68138"],
            "Tropomyosin_1": ["P42639"],
            "Tropomyosin_2": ["Q5E956"],
            "Serum_albumin": ["P02769"],
            "Ferritin_H": ["F1MNW4"],
            "Ferritin_L": ["F1N757"],
            "Transferrin": ["Q29443"],
            "LDH_A": ["P19858"],
            "LDH_B": ["P30929"],
            "Creatine_kinase": ["Q9XSC6"],
            "GAPDH": ["P10096"]
        }
    },

    "Sus_scrofa": {
        "common_name": "Pig (general omnivore proxy)",
        "category": "Mammal - Omnivore proxy",
        "proteins": {
            "Myosin_heavy_1": ["Q9TV61"],
            "Myosin_heavy_2": ["Q9TV62"],
            "Myosin_heavy_7": ["Q28706"],
            "Actin_beta": ["P60711"],
            "Actin_alpha": ["P68137"],
            "Tropomyosin_1": ["P42634"],
            "Tropomyosin_2": ["P58775"],
            "Serum_albumin": ["P08835"],
            "Ferritin_H": ["P25914"],
            "Ferritin_L": ["P02793"],
            "Transferrin": ["P09571"],
            "LDH_A": ["P00339"],
            "LDH_B": ["P00336"],
            "Creatine_kinase": ["P62708"],
            "GAPDH": ["P00355"]
        }
    },

    # Marine mammals
    "Phoca_vitulina": {
        "common_name": "Harbor seal",
        "category": "Mammal - Marine",
        "proteins": {
            "COL1A1": ["A0A2U3WFE8"],
            "COL1A2": ["A0A2U3WKC3"]
        }
    },

    # ============================================================================
    # BIRDS
    # ============================================================================
    "Meleagris_gallopavo": {
        "common_name": "Wild turkey",
        "category": "Bird - Galliforme",
        "proteins": {
            "COL1A1": ["F1NHI0"],
            "COL1A2": ["F1NWD0"],
            "Hemoglobin_alpha": ["P01993"],
            "Hemoglobin_beta": ["P83123"],
            "Lysozyme": ["P00703"],
            "Ovalbumin": ["P01014"],
            "Ovotransferrin": ["P43165"]
        }
    },

    "Gallus_gallus": {
        "common_name": "Chicken (general bird proxy)",
        "category": "Bird - Galliforme proxy",
        "proteins": {
            "COL1A1": ["P02457"],
            "COL1A2": ["P02467"],
            "Myosin_heavy_1": ["P02563"],
            "Myosin_heavy_2": ["P02564"],
            "Myosin_heavy_7": ["P02566"],
            "Actin_beta": ["P60706"],
            "Actin_alpha": ["P68139"],
            "Tropomyosin_1": ["P04268"],
            "Tropomyosin_2": ["P04269"],
            "Hemoglobin_alpha": ["P01994"],
            "Hemoglobin_beta": ["P02112"],
            "Serum_albumin": ["P19121"],
            "Ferritin_H": ["P08267"],
            "Ferritin_L": ["P02794"],
            "Transferrin": ["P02789"],
            "LDH_A": ["P00337"],
            "LDH_B": ["P52503"],
            "Creatine_kinase": ["P00565"],
            "GAPDH": ["P00356"],
            "Lysozyme": ["P00698"],
            "Ovalbumin": ["P01012"]
        }
    },

    "Anas_platyrhynchos": {
        "common_name": "Mallard (waterfowl proxy)",
        "category": "Bird - Waterfowl",
        "proteins": {
            "COL1A1": ["A0A8C0T6I9"],
            "COL1A2": ["R0K4U3"],
            "Hemoglobin_alpha": ["P01986"],
            "Hemoglobin_beta": ["P02113"],
            "Serum_albumin": ["P85107"],
            "Lysozyme": ["P04421"],
            "Ovalbumin": ["P01013"]
        }
    },

    "Branta_canadensis": {
        "common_name": "Canada goose",
        "category": "Bird - Waterfowl",
        "proteins": {
            "COL1A1": ["A0A6J3FIA1"]
        }
    },

    "Anser_anser": {
        "common_name": "Goose (proxy for waterfowl COL1A2)",
        "category": "Bird - Waterfowl",
        "proteins": {
            "COL1A2": ["A0A8D0UJ42"]
        }
    },

    "Cygnus_columbianus": {
        "common_name": "Tundra swan",
        "category": "Bird - Waterfowl",
        "proteins": {
            "COL1A1": ["A0A674HT17"],
            "COL1A2": ["A0A674I288"]
        }
    },

    "Columba_livia": {
        "common_name": "Rock pigeon (proxy for passenger pigeon)",
        "category": "Bird - Other",
        "proteins": {
            "COL1A1": ["F1NVR4"],
            "COL1A2": ["F1P2I0"]
        }
    },

    # ============================================================================
    # FISH - ANADROMOUS
    # ============================================================================
    "Salmo_salar": {
        "common_name": "Atlantic salmon",
        "category": "Fish - Anadromous",
        "proteins": {
            "COL1A1": ["B5X2Y1"],
            "COL1A2": ["B5DG59"],
            "Myosin_heavy_1": ["B5DGF1"],
            "Myosin_heavy_2": ["B5X0W3"],
            "Actin_beta": ["A0A1S3R3D6"],
            "Tropomyosin_1": ["B5X372"],
            "Hemoglobin_alpha": ["P02018"],
            "Hemoglobin_beta": ["P02019"],
            "Ferritin_H": ["B5XCV7"],
            "Ferritin_L": ["B5X893"],
            "Transferrin": ["P79815"],
            "LDH_A": ["P00338"],
            "LDH_B": ["Q91474"],
            "GAPDH": ["B5X247"],
            "Vitellogenin": ["P87498"]
        }
    },

    "Clupea_harengus": {
        "common_name": "Atlantic herring (proxy for shad/alewife)",
        "category": "Fish - Anadromous",
        "proteins": {
            "COL1A1": ["A0A060Y1J8"]
        }
    },

    "Acipenser_ruthenus": {
        "common_name": "Sterlet (proxy for Atlantic sturgeon)",
        "category": "Fish - Anadromous",
        "proteins": {
            "COL1A1": ["A0A8C9JHD1"],
            "COL1A2": ["A0A8C9JG52"]
        }
    },

    "Acipenser_transmontanus": {
        "common_name": "White sturgeon (sturgeon roe proxy)",
        "category": "Fish - Anadromous",
        "proteins": {
            "Vitellogenin": ["P87000"]
        }
    },

    "Anguilla_anguilla": {
        "common_name": "European eel (proxy for American eel)",
        "category": "Fish - Anadromous",
        "proteins": {
            "COL1A1": ["A0A2P4VHE4"],
            "COL1A2": ["A0A2P4W8F8"]
        }
    },

    # ============================================================================
    # FISH - FRESHWATER
    # ============================================================================
    "Esox_lucius": {
        "common_name": "Northern pike",
        "category": "Fish - Freshwater",
        "proteins": {
            "COL1A1": ["A0A8C7PBL0"],
            "COL1A2": ["A0A8C7P9M9"]
        }
    },

    "Micropterus_salmoides": {
        "common_name": "Largemouth bass",
        "category": "Fish - Freshwater",
        "proteins": {
            "COL1A1": ["A0A8C5Y5K9"]
        }
    },

    "Perca_fluviatilis": {
        "common_name": "European perch (proxy for yellow perch/walleye)",
        "category": "Fish - Freshwater",
        "proteins": {
            "COL1A1": ["A0A8C7I7F2"],
            "COL1A2": ["A0A8C7HUA6"]
        }
    },

    "Ictalurus_punctatus": {
        "common_name": "Channel catfish",
        "category": "Fish - Freshwater",
        "proteins": {
            "COL1A1": ["A0A8C6JM76"],
            "COL1A2": ["A0A8C6JLY8"]
        }
    },

    "Lepomis_macrochirus": {
        "common_name": "Bluegill (proxy for sunfish/crappie)",
        "category": "Fish - Freshwater",
        "proteins": {
            "COL1A1": ["A0A8C5VQB8"]
        }
    },

    # ============================================================================
    # FISH - MARINE (COASTAL)
    # ============================================================================
    "Gadus_morhua": {
        "common_name": "Atlantic cod",
        "category": "Fish - Marine",
        "proteins": {
            "COL1A1": ["Q90512"],
            "COL1A2": ["Q90513"]
        }
    },

    "Platichthys_flesus": {
        "common_name": "European flounder (proxy for winter flounder)",
        "category": "Fish - Marine",
        "proteins": {
            "COL1A1": ["A0A8C9HAU2"],
            "COL1A2": ["A0A8C9H9Z0"]
        }
    },

    "Labrus_bergylta": {
        "common_name": "Ballan wrasse (proxy for cunner)",
        "category": "Fish - Marine",
        "proteins": {
            "COL1A1": ["A0A8C9P9R2"],
            "COL1A2": ["A0A8C9PCB0"]
        }
    },

    # ============================================================================
    # REPTILES AND AMPHIBIANS
    # ============================================================================
    "Trachemys_scripta": {
        "common_name": "Red-eared slider (proxy for turtles)",
        "category": "Reptile",
        "proteins": {
            "COL1A1": ["A0A674JPF2"]
        }
    },

    "Python_bivittatus": {
        "common_name": "Burmese python (proxy for water snake)",
        "category": "Reptile",
        "proteins": {
            "COL1A1": ["A0A6J0WQF0"],
            "COL1A2": ["A0A6J0U8E3"]
        }
    },

    "Xenopus_laevis": {
        "common_name": "African clawed frog (proxy for bullfrog)",
        "category": "Amphibian",
        "proteins": {
            "COL1A1": ["F6WBU2"],
            "COL1A2": ["Q6INZ4"]
        }
    },

    # ============================================================================
    # SHELLFISH (ATLANTIC COAST)
    # ============================================================================
    "Homarus_americanus": {
        "common_name": "American lobster",
        "category": "Shellfish - Crustacean",
        "proteins": {
            "Tropomyosin": ["G8XZJ5"],
            "Arginine_kinase": ["B3TUF5"]
        }
    },

    "Crassostrea_virginica": {
        "common_name": "Eastern oyster",
        "category": "Shellfish - Bivalve",
        "proteins": {
            "Tropomyosin": ["P84856"],
            "Arginine_kinase": ["K1QBR0"]
        }
    },

    "Mercenaria_mercenaria": {
        "common_name": "Hard clam/Quahog",
        "category": "Shellfish - Bivalve",
        "proteins": {
            "Tropomyosin": ["Q95W94"]
        }
    },

    "Mytilus_edulis": {
        "common_name": "Blue mussel",
        "category": "Shellfish - Bivalve",
        "proteins": {
            "Tropomyosin": ["P51111"]
        }
    },

    # ============================================================================
    # CONTAMINATION CONTROLS
    # ============================================================================
    "Homo_sapiens": {
        "common_name": "Human (contamination control)",
        "category": "Contamination",
        "proteins": {
            "COL1A1": ["P02452"],
            "COL1A2": ["P08123"],
            "Keratin_1": ["P04264"],
            "Keratin_10": ["P13645"],
            "Serum_albumin": ["P02768"]
        }
    },

    # ============================================================================
    # PLANTS (from previous plant database)
    # ============================================================================
    "Phaseolus_vulgaris": {
        "common_name": "Common bean",
        "category": "Plant - Domesticated",
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

    "Zea_mays": {
        "common_name": "Maize",
        "category": "Plant - Domesticated",
        "proteins": {
            "alpha_zeins": ["P04700", "P04701", "P04702", "P04703"],
            "beta_zein": ["P04705"],
            "gamma_zein": ["P06673"],
            "globulins": ["P15590"],
            "glutelins": ["Q7SIC8"],
            "prolamins": ["P06674"]
        }
    },

    "Helianthus_annuus": {
        "common_name": "Sunflower",
        "category": "Plant - Domesticated",
        "proteins": {
            "helianthinin_11S": ["P19084"],
            "albumin_2S": ["P15461"],
            "storage_globulins": ["Q6VA02", "Q6VA03"]
        }
    },

    "Chenopodium_quinoa": {
        "common_name": "Quinoa (proxy for C. berlandieri)",
        "category": "Plant - Domesticated",
        "proteins": {
            "chenopodin_11S": ["Q84V37"]
        }
    },

    "Cucurbita_pepo": {
        "common_name": "Squash/pumpkin",
        "category": "Plant - Domesticated",
        "proteins": {
            "cucurbitin": ["P26654"],
            "cucumisin": ["P25776"],
            "albumin_2S": ["Q39639", "Q39640"],
            "storage_proteins": ["Q9SRZ8"]
        }
    },

    "Cucurbita_maxima": {
        "common_name": "Winter squash",
        "category": "Plant - Domesticated",
        "proteins": {
            "storage_proteins": ["Q9XGS6"]
        }
    },

    "Amaranthus_hypochondriacus": {
        "common_name": "Amaranth",
        "category": "Plant - Domesticated",
        "proteins": {
            "amarantin_11S": ["P16349"],
            "albumins": ["A0A140JWP2", "P11828"],
            "globulins": ["Q43652"]
        }
    },

    "Zizania_palustris": {
        "common_name": "Wild rice",
        "category": "Plant - Wild",
        "proteins": {
            "glutelins": ["Q5QKU4"],
            "storage_proteins": ["Q5QKU5"]
        }
    },

    "Juglans_nigra": {
        "common_name": "Black walnut",
        "category": "Plant - Wild",
        "proteins": {
            "albumin_2S": ["Q2TPW5"],
            "storage_proteins": ["A0A2P6PAH8"]
        }
    },

    "Carya_illinoinensis": {
        "common_name": "Pecan (proxy for hickory)",
        "category": "Plant - Wild",
        "proteins": {
            "storage_proteins": ["A0A2P6QY45"]
        }
    },

    "Helianthus_tuberosus": {
        "common_name": "Jerusalem artichoke",
        "category": "Plant - Wild",
        "proteins": {}  # Will search by organism
    }
}


def fetch_from_uniprot(accessions: List[str], organism_name: str = None) -> str:
    """Fetch protein sequences from UniProt."""
    sequences = []

    if accessions:
        for acc in accessions:
            url = f"https://rest.uniprot.org/uniprotkb/{acc}.fasta"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    sequences.append(response.text.strip())
                    print(f"    ✓ {acc}")
                else:
                    print(f"    ✗ Failed: {acc} (HTTP {response.status_code})", file=sys.stderr)
                time.sleep(0.2)
            except Exception as e:
                print(f"    ✗ Error: {acc} - {e}", file=sys.stderr)

    elif organism_name:
        print(f"    Searching for {organism_name}...")
        query = f"organism_name:\"{organism_name}\" AND reviewed:true"
        url = f"https://rest.uniprot.org/uniprotkb/search?query={query}&format=fasta&size=100"
        try:
            response = requests.get(url)
            if response.status_code == 200 and response.text.strip():
                sequences.append(response.text.strip())
                print(f"    ✓ Found proteins")
            time.sleep(0.5)
        except Exception as e:
            print(f"    ✗ Error searching: {e}", file=sys.stderr)

    return "\n".join(sequences)


def build_complete_database(output_dir: Path = Path(".")):
    """Build comprehensive Northeast archaeological reference database."""
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    all_sequences = []
    taxonomy_data = []
    category_summary = {}

    print("\n" + "=" * 70)
    print("NORTHEAST NORTH AMERICAN ARCHAEOLOGICAL PROTEIN DATABASE")
    print("=" * 70 + "\n")

    for species, data in NE_PROTEINS.items():
        common_name = data.get("common_name", species)
        category = data.get("category", "Unknown")

        print(f"\n{species}")
        print(f"  Common: {common_name}")
        print(f"  Category: {category}")

        # Track categories
        if category not in category_summary:
            category_summary[category] = 0
        category_summary[category] += 1

        species_sequences = []

        if data["proteins"]:
            for protein_type, accessions in data["proteins"].items():
                if accessions:
                    print(f"  {protein_type}:")
                    seqs = fetch_from_uniprot(accessions)
                    if seqs:
                        species_sequences.append(seqs)
        else:
            # Try organism search
            seqs = fetch_from_uniprot([], organism_name=species.replace("_", " "))
            if seqs:
                species_sequences.append(seqs)

        if species_sequences:
            all_sequences.extend(species_sequences)
            genus = species.split("_")[0]
            taxonomy_data.append(f"{species}\t{genus}\t{category}\t{common_name}")

    # Write combined FASTA
    fasta_path = output_dir / "northeast_complete.fasta"
    with open(fasta_path, 'w') as f:
        f.write("\n".join(all_sequences))
    print(f"\n✓ Wrote {fasta_path}")

    # Write taxonomy
    taxonomy_path = output_dir / "northeast_taxonomy.tsv"
    with open(taxonomy_path, 'w') as f:
        f.write("Species\tGenus\tCategory\tCommon_Name\n")
        f.write("\n".join(taxonomy_data))
    print(f"✓ Wrote {taxonomy_path}")

    # Write comprehensive metadata
    metadata_path = output_dir / "northeast_database_info.txt"
    with open(metadata_path, 'w') as f:
        f.write("NORTHEAST NORTH AMERICAN ARCHAEOLOGICAL PROTEIN DATABASE\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Total species/proxies: {len(NE_PROTEINS)}\n\n")

        f.write("CATEGORY SUMMARY:\n")
        f.write("-" * 70 + "\n")
        for category, count in sorted(category_summary.items()):
            f.write(f"{category:.<50} {count:>3} species\n")

        f.write("\n\nSPECIES DETAILS:\n")
        f.write("-" * 70 + "\n")

        current_category = None
        for species, data in NE_PROTEINS.items():
            category = data.get("category", "Unknown")
            if category != current_category:
                f.write(f"\n{category}:\n")
                current_category = category

            common_name = data.get("common_name", species)
            f.write(f"\n  {species} ({common_name})\n")

            if data['proteins']:
                for ptype, accs in data['proteins'].items():
                    f.write(f"    - {ptype}: {len(accs)} accessions\n")

    print(f"✓ Wrote {metadata_path}")

    # Print summary
    print("\n" + "=" * 70)
    print("DATABASE BUILD COMPLETE")
    print("=" * 70)
    print(f"\nTotal species/proxies: {len(NE_PROTEINS)}")
    print("\nCategory breakdown:")
    for category, count in sorted(category_summary.items()):
        print(f"  {category}: {count}")

    print(f"\n\nNext steps:")
    print(f"  1. Generate peptide markers:")
    print(f"     python pampa_craft.py --allpeptides -f {fasta_path} -o northeast_markers.tsv")
    print(f"  2. Add deamidation (CRITICAL for ancient proteins!):")
    print(f"     python pampa_craft.py --deamidation -p northeast_markers.tsv -o northeast_markers_deam.tsv")
    print(f"  3. Analyze your samples:")
    print(f"     python pampa_classify.py -s spectra/ -e 0.1 -p northeast_markers_deam.tsv -t {taxonomy_path} --deamidation -o results.tsv")
    print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Build comprehensive Northeast North American archaeological protein database"
    )
    parser.add_argument(
        "-o", "--output-dir",
        default=".",
        help="Output directory (default: current directory)"
    )

    args = parser.parse_args()
    build_complete_database(Path(args.output_dir))
