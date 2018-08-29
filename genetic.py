import random
import operator
from operator import itemgetter

def fitness (password, test_word):
    if (len(test_word) != len(password)):
        print("taille incompatible")
        return
    else:
        score = 0
        for i in range(len(password)):
            if (password[i] == test_word[i]):
                score+=1
        return score * 100 / len(password)

def generateANumber(genelength, numberRange):
    result = ""
    for i in range(genelength):
        number = str(random.randrange(0, numberRange+1))
        result += number  
    return result

def generateFirstPopulation(sizePopulation, genelength, numberRange):
    population = []
    for i in range(sizePopulation):
        aNumber = generateANumber(genelength, numberRange)
        population.append(aNumber)
    return population

def computePerfPopulation(population, password):
    populationPerf = []
    for i in range(len(population)):
            populationPerf.append((population[i], fitness(password, population[i])))
    populationPerf.sort(key=itemgetter(1), reverse = True)
    return populationPerf
        
def selectFromPopulation(populationSorted, best_sample, lucky_few):
    selectedParents = []
    for i in range(best_sample):
        selectedParents.append(populationSorted[i][0])
    for i in range(lucky_few):
        selectedParents.append(random.choice(populationSorted)[0])
        random.shuffle(selectedParents)
    return selectedParents

def createChild(parents):
    n = random.randrange(0,len(parents))
    m = random.randrange(0,len(parents))
    while(n==m):
        m = random.randrange(0,len(parents))
    individual1 = parents[n]
    individual2 = parents[m]
    child = ''
    for i in range(len(individual1)):
        if (int(100 * random.random()) <50):
            child += individual1[i]
        else:
            child += individual2[i]
    return child

def createChildren(parents, populationSize):
    nextPopulation = []
    for i in range(populationSize):
        nextPopulation.append(createChild(parents))
    return nextPopulation

def mutateNumber(number, length, numberRange):
    location = random.randrange(0,length)
    mutatedNumber = number[:location]+str(random.randrange(0,numberRange))+number[location+1:]
    return mutatedNumber
def mutatePopulation(population, chance_of_mutation, length, numberRange):
    for i in range(len(population)):
        if random.random() * 100 <chance_of_mutation:
            population[i] = mutateNumber(population[i], length, numberRange)
    return population

#Setting options
length = 10
numberRange = 9
sizePopulation = 20
numberofGeneration = 100
chance_of_mutation = 10
number_of_parents = int(sizePopulation*(40/100))
best_sample = int(number_of_parents/2)
lucky_few = int(number_of_parents/2)
numberofParents = best_sample + lucky_few
datalist = []

#Generate solution
password = generateANumber(length, numberRange)

#Generate first population
Population = generateFirstPopulation(sizePopulation, length, numberRange)

#Compute fitness
populationSorted = computePerfPopulation(Population, password)

#Save data
datalist.append(populationSorted[0][1])

#Informations
print('Gene length : {}'.format(length))
print('Gene range : 0 ~ {}'.format(numberRange))
print('Population size : {}'.format(sizePopulation))
print('Number of generation : {}'.format(numberofGeneration))
print('Chance of mutation : {}%'.format(chance_of_mutation))
print('Number of parents : {} (best {}, lucky {})\n'.format(number_of_parents, best_sample, lucky_few))
print('Password : {}'.format(password))
print('           {} {}'.format(populationSorted[0][0], populationSorted[0][1]))

perfectcount = 1
firstPerfect = 0

for i in range(2, numberofGeneration+1):
    #Select parents
    parents = selectFromPopulation(populationSorted, best_sample, lucky_few)

    #Create next generation
    nextGeneration_vanilla = createChildren(parents, sizePopulation)

    #Mutation
    nextGeneration_mutated = mutatePopulation(nextGeneration_vanilla, chance_of_mutation, length, numberRange)
    Population = nextGeneration_mutated

    #Compute fitness
    populationSorted = computePerfPopulation(nextGeneration_mutated, password)
    print('           {} {}'.format(populationSorted[0][0], populationSorted[0][1]))
    if populationSorted[0][1] == 100:
        if perfectcount != 0:
            firstPerfect = i
            perfectcount -= 1

    #Save data
    datalist.append(populationSorted[0][1])

#Print 100% generation
if(firstPerfect==0):
    print('\n\n           No 100%\n\n')
else:
    print('\n\n           Generation {}\n\n'.format(firstPerfect))
