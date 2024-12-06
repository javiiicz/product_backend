import numpy as np
import random as r
import math as m
from config import ATTRIBUTE_ORDER, ATTRIBUTES as attributes

# Reproduction: select the s fittest vectors from the population to survive
    # Assuming 2D array is sorted by decreasing score, we just return top proportion of the array 
    
# Returns the top p * 100 % fittest products
# array A: Matrix containing all products sorted by decreasing score
# float p: Proportion of products kept ( 0 <= p <= 1 )
def reproducion(A, p):
    
    print("Reproduction: saving the top", p* 100, "% of products")
    
    n = len(A)
    end = m.ceil(n * p)
    return A[:end]


# Crossover: randomly picked pairs exchange genetic material to produce offspring

# Returns the 2m offspring that occured by selecting m pairs out of the products in A
# array A: Matrix of products where the pairs will be selected
# int m: Number of pairs going to crossover
# float p: Probalility of a given attribute to crossover ( 0 <= p <= 1)
def crossover(A, m, p):
    
    print("Crossover with", m, "pairs and", p, "probability of change.")
    
    res = []
    
    # Ensure m is not larger than the population size divided by 2
    m = min(m, len(A) // 2)
    
    # Pick m distinct pairs for crossover
    pairs = [r.sample(range(len(A)), 2) for _ in range(m)]
    
    for index1, index2 in pairs:
        product1, product2 = A[index1], A[index2]
        
        offspring1, offspring2 = product1.copy(), product2.copy()
        
        # Vectorized crossover based on probability
        mask = np.random.rand(len(product1)) <= p
        offspring1[mask], offspring2[mask] = offspring2[mask], offspring1[mask]
        
        res.append(offspring1)
        res.append(offspring2)
    
    return np.array(res)


# Mutation: every vector has a chanve m to mutate an attribute


# Given a 2D array A of products returns an array with the same amout of products but each product has a probability p of changing an attribute.
# Only one attribute will be changed per mutation
# array A: Matrix of products
# float p: probability of mutation occuring
def mutation(population, mutation_chance):
    print(population)
    num_individuals, num_attributes = population.shape
    print(f"Number of individuals: {num_individuals}, Number of attributes: {num_attributes}")
    print(f"Length of ATTRIBUTE_ORDER: {len(ATTRIBUTE_ORDER)}")
    
    mutated_products = np.copy(population)
    
    for i in range(num_individuals):
        if np.random.rand() < mutation_chance:
            attribute_index = np.random.randint(0, num_attributes)
            if attribute_index >= len(ATTRIBUTE_ORDER):
                print(f"Error: attribute_index {attribute_index} out of range for ATTRIBUTE_ORDER")
                continue  # Skip this mutation or handle it appropriately
            
            attribute_name = ATTRIBUTE_ORDER[attribute_index]
            current_value = mutated_products[i, attribute_index]
            mutated_value = mutate_value(current_value, attribute_index)
            mutated_products[i, attribute_index] = mutated_value
            print(f"Mutated individual {i}: Changed {attribute_name} from {current_value} to {mutated_value}")
    return mutated_products


def mutate_value(current_value, attribute_index):
    attribute_name = ATTRIBUTE_ORDER[attribute_index]
    possible_values = attributes[attribute_name]
    # Optionally exclude the current value
    possible_values = [value for value in possible_values if value != current_value]
    if possible_values:
        return np.random.choice(possible_values)
    else:
        return current_value  # No other possible values to choose from


if __name__ == "__main__":
    X = []
    for _ in range(60):
        product = []
        # For each attribute in the attributes dictionary, randomly choose a value
        for attribute, values in attributes.items():
            random_value = r.choice(values)
            product.append(random_value)
        X.append(product)

    X = np.array(X)
    print((X), len(X))
    print()

    Y = reproducion(X, 0.5)
    print(Y, len(Y))
    print()

    Z = crossover(Y, len(Y)//2, 0.5)
    print(Z, len(Z))
    print()

    W = mutation(X, 0.02)
    print(W, len(W))
    print()