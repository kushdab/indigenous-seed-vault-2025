import json
import os
from datetime import datetime
from tabulate import tabulate

class SeedVault:
    def __init__(self, db_path='seed_archive.json'):
        self.db_path = db_path
        self.seeds = self._load_data()

    def _load_data(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                return json.load(f)
        return []

    def _save_data(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.seeds, f, indent=4)

    def add_seed(self, name, local_name, scientific_name, county, traits, maturity):
        seed_entry = {
            "id": len(self.seeds) + 1,
            "common_name": name,
            "indigenous_name": local_name,
            "scientific_name": scientific_name,
            "origin_county": county,
            "genetic_traits": [t.strip() for t in traits.split(',')],
            "maturity_period_days": maturity,
            "date_cataloged": datetime.now().strftime("%Y-%m-%d")
        }
        self.seeds.append(seed_entry)
        self._save_data()
        print(f"\n[SUCCESS] Cataloged: {name} ({local_name})")

    def list_seeds(self):
        if not self.seeds:
            print("\nVault is currently empty.")
            return
        
        headers = ["ID", "Name", "Indigenous Name", "County", "Traits", "Maturity (Days)"]
        table = [[s['id'], s['common_name'], s['indigenous_name'], s['origin_county'], ", ".join(s['genetic_traits']), s['maturity_period_days']] for s in self.seeds]
        print("\n--- INDIGENOUS KENYAN SEED ARCHIVE 2025 ---")
        print(tabulate(table, headers=headers, tablefmt="grid"))

    def search_by_trait(self, trait):
        results = [s for s in self.seeds if any(trait.lower() in t.lower() for t in s['genetic_traits'])]
        if results:
            headers = ["Name", "County", "Traits"]
            table = [[s['common_name'], s['origin_county'], ", ".join(s['genetic_traits'])] for s in results]
            print(f"\nResults for trait: {trait}")
            print(tabulate(table, headers=headers, tablefmt="simple"))
        else:
            print(f"\nNo seeds found with trait: {trait}")

def main():
    vault = SeedVault()
    while True:
        print("\n1. Add Seed Variety")
        print("2. View Vault")
        print("3. Search by Genetic Trait")
        print("4. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            name = input("Common Name: ")
            local = input("Indigenous Name (e.g., Kikamba, Dholuo): ")
            sci = input("Scientific Name: ")
            county = input("County of Origin: ")
            traits = input("Traits (comma-separated, e.g., drought-resistant, pest-hardy): ")
            try:
                maturity = int(input("Maturity Period (days): "))
                vault.add_seed(name, local, sci, county, traits, maturity)
            except ValueError:
                print("Invalid maturity period.")
        elif choice == '2':
            vault.list_seeds()
        elif choice == '3':
            trait = input("Enter trait to search: ")
            vault.search_by_trait(trait)
        elif choice == '4':
            break

if __name__ == "__main__":
    main()