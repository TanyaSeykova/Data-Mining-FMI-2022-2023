from dataclasses import dataclass
import math
import random

@dataclass
class Point:
    x: float
    y: float

coordinates = []

def read_input():
    with open('input.csv') as f:
        while True:
            line = f.readline()
            if not line:
                break
            coordinates.append(Point((float)(line.split(",")[0]), (float)(line.split(",")[1])))

def distance(point_a, point_b):
    return math.sqrt((point_a.x - point_b.x)**2 + (point_a.y - point_b.y)**2)

def distance_gene(gene):
    result = 0
    prev = gene[0]
    for current in gene[1:]:
        # print(coordinates[i-1], coordinates[i], distance(coordinates[i-1], coordinates[i]))
        result += distance(coordinates[prev], coordinates[current])
        prev = current
    return result

GENES_IN_POPULATION = 10
def init_first_population():
    population = []
    ind = 0
    while ind < GENES_IN_POPULATION:
        lst = list(range(len(coordinates)))
        random.shuffle(lst)
        population.append(lst)
        ind += 1

    return population

def sort_genes(genes):
    return sorted(genes, key=lambda x: distance_gene(x))

def one_point_cross(first, second):
    # print(first, second)
    first_crossed = []
    second_crossed = []
    ind = random.randint(0, len(first) - 1)
    first_crossed.extend(first[:ind])
    second_crossed.extend(second[:ind])
    i_f = 0
    while len(first_crossed) < len(first):
        if second[i_f] not in first_crossed:
            first_crossed.append(second[i_f])
        i_f += 1

    i_s = 0
    while len(second_crossed) < len(second):
        if first[i_s] not in second_crossed:
            second_crossed.append(first[i_s])
        i_s += 1

    return first_crossed, second_crossed

def reproduce(parents):
    result = []
    for first, second in zip(parents[0::2], parents[1::2]):
        result.extend(one_point_cross(first, second))
    # print("-----------------------------------------------------")
    if len(parents) % 2 != 0:
        result.append(parents[-1])
    return result

def mutate_swap(gene):
    ind1 = random.randint(0, len(gene) - 1)
    ind2 = random.randint(0, len(gene) - 1)
    gene[ind1], gene[ind2] = gene[ind2], gene[ind1]
    return gene

def mutate_reverse(gene):
    ind1 = random.randint(0, len(gene) - 2)
    ind2 = random.randint(ind1 + 1, len(gene) - 1)
    
    gene[ind1:ind2] = gene[ind1:ind2][::-1]
    return gene

def mutate_insert(gene):
    ind1 = random.randint(0, len(gene) - 1)
    ind2 = random.randint(0, len(gene) - 2)
    temp = gene[ind1]
    gene.pop(ind1)
    gene.insert(ind2, temp)
    return gene

def mutate(genes):
    result = []
    method = random.randint(0, 2)
    len_ = len(genes[0])
    if method == 0:
        for gene in genes:
            
            result.append(mutate_swap(gene))
    if method == 1:
        for gene in genes:
            result.append(mutate_reverse(gene))
    if method == 2:
        for gene in genes:
            result.append(mutate_insert(gene))
    return result
        
def genetic_algorithm(first_population):
    iteration = 1
    parents = first_population
    while iteration < 5001:
        # print("ITERATION: ", iteration)
        # print("PARENTS: ", parents)
        best_parents = sort_genes(parents)[0:int(len(parents)/2)]
        # print("BEST PARENTS: ", best_parents)
        if iteration == 1 or iteration == 10 or iteration == 100 or iteration == 500 or iteration == 1000 or iteration == 5000:
            print("Best on iteration number ", iteration, " : ", distance_gene(best_parents[0]))
        children = reproduce(best_parents)
        # print("CHILDREN: ", children)
        children = mutate(children)
        # print("MUTATED CHILDREN: ", children)
        # best_children = sort_genes(best_children)[0:len(children)/2]
        parents = best_parents + children
        iteration += 1

def main():
    read_input()
    first_population = init_first_population()
    # for gene in first_population:
    #    print(gene, distance_gene(gene))
    # print(sort_genes(first_population))
    genetic_algorithm(first_population)
    # print(mutate_insert([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))

if __name__ == "__main__":
    main()