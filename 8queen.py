import random

# Define the problem parameters
POPULATION_SIZE = 20 #The population size is small because of small search space size 
MUTATION_RATE = 0.05 #To avoid large changes in the population.
BOARD_SIZE = 8  #8 Queens and 8*8 chess board 

# Define the fitness function
#it will return lower value for a good solution and higher value for a worst solution 
def fitness(chromosome):
    conflicts = 0
    for i in range(len(chromosome)):
        for j in range(i + 1, len(chromosome)):
            if chromosome[i] == chromosome[j]:
                conflicts += 1
            elif abs(chromosome[i] - chromosome[j]) == j - i:
                conflicts += 1
    return conflicts

# Define the selection method
#this is basically selecting the fittest parent 
def tournament_selection(population, tournament_size):
    selected = []
    for i in range(len(population)):
        tournament = random.sample(population, tournament_size)
        winner = min(tournament, key=lambda x: fitness(x))
        selected.append(winner)
    return selected

# Define the crossover method
#it basically creates new chromosomes 
def one_point_crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

# Define the mutation method
# randomly change some of the genes in the offspring chromosome to introduce new genetic info
def mutation(chromosome):
    mutated_chromosome = chromosome[:]
    if random.random() < MUTATION_RATE:
        idx = random.randint(0, len(chromosome) - 1)
        mutated_chromosome[idx] = random.randint(0, BOARD_SIZE - 1)
    return mutated_chromosome

# Generate the initial population
population = []
for i in range(POPULATION_SIZE):
    chromosome = [random.randint(0, BOARD_SIZE - 1) for _ in range(BOARD_SIZE)]
    while fitness(chromosome) > 0:
        chromosome = [random.randint(0, BOARD_SIZE - 1) for _ in range(BOARD_SIZE)]
    population.append(chromosome)

# Run the genetic algorithm
for generation in range(100):
    # Select the parents
    parents = tournament_selection(population, 2)

    # Create the offspring
    offspring1, offspring2 = one_point_crossover(parents[0], parents[1])

    # Apply mutation to the offspring
    offspring1 = mutation(offspring1)
    offspring2 = mutation(offspring2)

    # Evaluate the fitness of the offspring
    offspring1_fitness = fitness(offspring1)
    offspring2_fitness = fitness(offspring2)

    # Replace the worst chromosome with the best offspring
    #The size of the next generation should be equal to the size of the current generation
    worst_fitness = max([fitness(chromosome) for chromosome in population])
    if offspring1_fitness < offspring2_fitness:
        if offspring1_fitness < worst_fitness:
            population.remove(max(population, key=lambda x: fitness(x)))
            population.append(offspring1)
    else:
        if offspring2_fitness < worst_fitness:
            population.remove(max(population, key=lambda x: fitness(x)))
            population.append(offspring2)

    # Check if the solution is found
    #Return the chromosome with the lowest number of conflicts as the best solution to the problem.
    if 0 in [fitness(chromosome) for chromosome in population]:
        solution = [chromosome for chromosome in population if fitness(chromosome) == 0][0]
        break

# Print the solution
if solution:
    print(solution)
else:
    print("Solution not found.")
