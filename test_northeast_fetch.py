#!/usr/bin/env python3
"""
Test script - fetch proteins for a small subset of species
Tests the UniProt fetching workflow before running the full database build
"""

import sys
sys.path.insert(0, '.')
from fetch_northeast_proteins import NortheastProteinFetcher

class TestFetcher(NortheastProteinFetcher):
    """Test with just a few representative species"""

    def load_species_data(self):
        """Load only test species"""
        return {
            'Faunal': [
                {'common': 'White Tailed Deer', 'scientific': 'Odocoileus virginianus', 'category': 'Faunal'},
                {'common': 'Wild Turkey', 'scientific': 'Meleagris gallopavo', 'category': 'Faunal'},
                {'common': 'Virginia Opossum', 'scientific': 'Didelphis virginiana', 'category': 'Faunal'},
            ],
            'Fish': [
                {'common': 'Brown Trout', 'scientific': 'Salmo trutta', 'category': 'Fish'},
                {'common': 'Yellow Perch', 'scientific': 'Perca flavescens', 'category': 'Fish'},
            ],
            'Reptile': [
                {'common': 'Snapping Turtle', 'scientific': 'Chelydra serpentina', 'category': 'Reptile'},
            ],
            'Floral': [
                {'common': 'Corn', 'scientific': 'Zea mays', 'category': 'Floral'},
                {'common': 'Black walnut', 'scientific': 'Juglans nigra', 'category': 'Floral'},
                {'common': 'Common morel', 'scientific': 'Morchella americana', 'category': 'Floral'},
            ]
        }

def main():
    print("=" * 80)
    print("NORTHEAST DATABASE TEST - Small subset of species")
    print("=" * 80)
    print("\nThis will fetch proteins for 9 test species to verify the workflow")
    print("Expected time: 2-3 minutes\n")

    fetcher = TestFetcher("plant_animal data by site.xlsx")
    fetcher.run()

    print("\n✓ Test complete!")
    print("\nTo fetch the full database (266 species, ~30-45 minutes):")
    print("  python3 fetch_northeast_proteins.py 'plant_animal data by site.xlsx'")

if __name__ == "__main__":
    main()
