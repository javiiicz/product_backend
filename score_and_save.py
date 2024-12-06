import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import hashlib
from reproduction import *
from population_builder import *
from config import ATTRIBUTE_ORDER, ATTRIBUTES as attributes

PROPORTION_KEPT = 1/2
CROSSOVER_CHANCE = 1/2
MUTATION_CHANCE = 2/100
TRACKING_FILE = "product_tracking.json"

# 1. Get scores from sessions and keep rank
def load_scores():
    scores = {}
    score_list = []
    folder_path = 'sessions'

    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, 'r') as json_file:
                data = json.load(json_file)

                for i in range(len(data["individuals"])):
                    individual = data["individuals"][i]
                    score = data["scores"].get(str(i), None)
                    if score is None:
                        continue

                    attributes = individual.values()
                    key = tuple(attributes)

                    if key in scores:
                        old_score = -scores[key][0]
                        old_N = scores[key][2]
                        new_score = (old_score * old_N + score) / (old_N + 1)
                        scores[key] = (-new_score, key, old_N + 1)
                    else:
                        scores[key] = (-score, key, 1)

    for product in scores:
        score_list.append(scores[product])

    score_list.sort(key=lambda x: x[0])
    X = [product[1] for product in score_list]
    return np.array(X)

# 2. Create new Generation
def populate(X):
    X = reproducion(X, PROPORTION_KEPT)

    if len(X) < 2:
        return X

    num_pairs = min(len(X) // 2, 50)
    if num_pairs == 0:
        return X

    Y = crossover(X, num_pairs, CROSSOVER_CHANCE)
    X = np.concatenate((X, Y))
    X = mutation(X, MUTATION_CHANCE)
    return X

# 3. Update Product Tracking (Ordered by Count)
def update_tracking(X, generation):
    # Load existing tracking data or initialize a new dictionary
    if os.path.exists(TRACKING_FILE):
        with open(TRACKING_FILE, 'r') as file:
            tracking_data = json.load(file)
    else:
        tracking_data = {}

    # Convert current generation to a DataFrame for easier processing
    current_df = pd.DataFrame(X, columns=ATTRIBUTE_ORDER)

    # Track counts for the current generation
    for _, row in current_df.iterrows():
        product_key = tuple(row.values)
        product_hash = hashlib.md5(str(product_key).encode()).hexdigest()

        # Initialize tracking entry if not present
        if product_hash not in tracking_data:
            tracking_data[product_hash] = {
                "attributes": list(product_key),
                "counts": []
            }

        # Extend the counts list to the current generation if necessary
        while len(tracking_data[product_hash]["counts"]) < generation:
            tracking_data[product_hash]["counts"].append(0)

        # Update the count for this product in the current generation
        if len(tracking_data[product_hash]["counts"]) == generation:
            tracking_data[product_hash]["counts"].append(1)
        else:
            tracking_data[product_hash]["counts"][generation] += 1

    # Sort the tracking data by total count (decreasing order)
    tracking_data = dict(sorted(tracking_data.items(), key=lambda item: sum(item[1]["counts"]), reverse=True))

    # Save the updated and sorted tracking data
    with open(TRACKING_FILE, 'w') as file:
        json.dump(tracking_data, file, indent=4)

# 4. Create new population JSON
def create_population_json(A):
    population = []
    attributes = ATTRIBUTE_ORDER
    for product in A:
        phone = {}
        for i in range(len(product)):
            phone[attributes[i]] = str(product[i])
        population.append(phone)
    save_population_to_file(population, 'new_population.json')

# 5. Attribute Analysis
def attribute_analysis():
    file_path = "new_population.json"
    with open(file_path, 'r') as file:
        data = json.load(file)

    df = pd.DataFrame(data)
    output_dir = "graph-individual attribute frequency"
    os.makedirs(output_dir, exist_ok=True)

    for column in df.columns:
        value_counts = df[column].value_counts()
        plt.figure(figsize=(10, 6))
        value_counts.plot(kind='bar', color='skyblue', edgecolor='black')
        plt.title(f'Count of Each Value for Attribute: {column}')
        plt.xlabel('Values')
        plt.ylabel('Count')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plot_path = os.path.join(output_dir, f"{column}_count.png")
        plt.savefig(plot_path)
        # plt.show(block=True)

# 6. Product Analysis
def product_analysis():
    file_path = "new_population.json"
    with open(file_path, 'r') as file:
        data = json.load(file)

    df = pd.DataFrame(data)
    product_combinations = df.apply(lambda row: tuple(row.items()), axis=1)
    combination_counts = product_combinations.value_counts(normalize=False)

    top_combinations = combination_counts.head(10)
    short_labels = []
    label_mapping = {}
    for combination in top_combinations.index:
        combination_str = str(combination)
        hash_label = hashlib.md5(combination_str.encode()).hexdigest()[:8]
        short_labels.append(hash_label)
        label_mapping[hash_label] = combination_str

    plots_dir = "graph-product frequency"
    os.makedirs(plots_dir, exist_ok=True)

    plt.figure(figsize=(15, 8))
    plt.bar(short_labels, top_combinations.values, color='skyblue', edgecolor='black')
    plt.title('Frequency of Top 10 Most Common Product Combinations', fontsize=18)
    plt.xlabel('Product Combinations (Hashed Labels)', fontsize=14)
    plt.ylabel('Count', fontsize=14)
    plt.xticks(rotation=30, ha='right', fontsize=12)
    plt.tight_layout()
    output_path = os.path.join(plots_dir, "top_product_combinations_hashed.png")
    plt.savefig(output_path, bbox_inches='tight')

    mapping_path = os.path.join(plots_dir, "label_mapping.txt")
    with open(mapping_path, 'w') as mapping_file:
        for hash_label, combination_str in label_mapping.items():
            mapping_file.write(f"{hash_label}: {combination_str}\n")

# 7. Plot Product Tracking Data (Ordered by Count)
def plot_tracking_data():
    if not os.path.exists(TRACKING_FILE):
        print("No tracking data found.")
        return

    with open(TRACKING_FILE, 'r') as file:
        tracking_data = json.load(file)

    # Prepare sorted data based on total counts (decreasing order)
    sorted_items = sorted(tracking_data.items(), key=lambda item: sum(item[1]["counts"]), reverse=True)
    
    plt.figure(figsize=(15, 10))
    for product_hash, data in sorted_items:
        product_label = " | ".join(data["attributes"])
        counts = data["counts"]
        plt.plot(counts, label=product_label[:50])  # Truncate label for readability

    plt.xlabel("Generation")
    plt.ylabel("Count")
    plt.title("Product Counts Across Generations (Sorted by Decreasing Total Count)")
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    # plt.show()

# Main Execution
if __name__ == "__main__":
    generation = 0
    if os.path.exists(TRACKING_FILE):
        with open(TRACKING_FILE, 'r') as file:
            tracking_data = json.load(file)
            generation = max(len(data["counts"]) for data in tracking_data.values())

    X = load_scores()
    X = populate(X)
    update_tracking(X, generation)
    create_population_json(X)

    # Perform analysis
    print("Starting attribute analysis...")
    attribute_analysis()

    print("Starting product analysis...")
    product_analysis()

    print("Plotting tracking data...")
    plot_tracking_data()

    print("Analysis complete.")
