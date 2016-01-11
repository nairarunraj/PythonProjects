'''
                            -- breadth --
                   20         30         50        150
    ||     30     FS1        FS2        FS3        FS4
length     20     FS5        FS6        FS7        FS8
    ||     50     FS9        FS10       FS11       FS12
   
Input -
    length, breadth, numberOfHorizontalAirlifts, 1..numberOfHorizontalAirlifts, numberOfVerticalAirlifts, 1..numberOfVerticalAirlifts
    100, 250, 2, 30, 50, 3, 20, 50, 100
'''
from itertools import product
import sys

(hallLength, hallBreadth, airliftDetails) = sys.argv[1].split(",", 2)
hallLength = int(hallLength)
hallBreadth = int(hallBreadth)
airliftDetails = list(map(int, airliftDetails.split(",")))
numberOfHorizontalAirlifts = airliftDetails[0]
numberOfVerticalAirlifts = airliftDetails[numberOfHorizontalAirlifts + 1]

##########################################################################
# Find the lengths of individual blocks created by airlifts
def get_divisions(hallDimension, airliftDetails, startIndex, endIndex):
    divisions = list(map(int, []))
    previousLength = hallDimension
    for distance in reversed(airliftDetails[startIndex:endIndex]):
        # print(distance)
        divisions.append(previousLength - distance)
        previousLength = distance
    # Add the first airlift's dimension
    divisions.append(airliftDetails[startIndex] - 0)
    divisions = list(reversed(divisions))
    return(divisions)
##########################################################################

##########################################################################   
# Find the lengths of individual blocks created by horizontal airlifts
lengthWiseDivisions = get_divisions(hallLength, airliftDetails, 1, numberOfHorizontalAirlifts + 1)
# print(lengthWiseDivisions)
##########################################################################
##########################################################################
# Find the breadths of individual blocks created by vertical airlifts
breadthWiseDivisions = get_divisions(hallBreadth, airliftDetails, numberOfHorizontalAirlifts + 2, numberOfHorizontalAirlifts + 2 + numberOfVerticalAirlifts + 1)
# print(breadthWiseDivisions)
##########################################################################   
##########################################################################
# Use the individual length-wise and breadth-wise divisions to map atomic functional spaces
atomicFunctionalSpaceArea = {}
functionalSpaceIndex = 1
for length in lengthWiseDivisions:
    for breadth in breadthWiseDivisions:
        atomicFunctionalSpaceArea[functionalSpaceIndex] = length * breadth
        functionalSpaceIndex += 1
# print(functionalSpaceIndex)
numberOfAtomicFunctionalSpaces = functionalSpaceIndex - 1
# print(atomicFunctionalSpaceArea)
##########################################################################
##########################################################################
# Find adjacent atomic functional spaces
adjacencyList = {}
for functionalSpaceIndex in range(1, numberOfAtomicFunctionalSpaces + 1):
    # print(functionalSpaceIndex)
    adjacencyList[functionalSpaceIndex] = set()
   
    # North element
    if(1 <= functionalSpaceIndex - numberOfVerticalAirlifts - 1 <= numberOfAtomicFunctionalSpaces):
        adjacencyList[functionalSpaceIndex].add(functionalSpaceIndex - numberOfVerticalAirlifts - 1)
   
    # South element
    if(1 <= functionalSpaceIndex + numberOfVerticalAirlifts + 1 <= numberOfAtomicFunctionalSpaces):
        adjacencyList[functionalSpaceIndex].add(functionalSpaceIndex + numberOfVerticalAirlifts + 1)
   
    # East element
    if((functionalSpaceIndex - 1) % (numberOfVerticalAirlifts + 1) != 0 and 1 <= functionalSpaceIndex - 1 <= numberOfAtomicFunctionalSpaces):
        adjacencyList[functionalSpaceIndex].add(functionalSpaceIndex - 1)
    # West element
    if((functionalSpaceIndex + 1) % (numberOfVerticalAirlifts + 1) != 1 and 1 <= functionalSpaceIndex + 1 <= numberOfAtomicFunctionalSpaces):
        adjacencyList[functionalSpaceIndex].add(functionalSpaceIndex + 1)
   
print(adjacencyList)

##########################################################################
##########################################################################
def dfs(graph, start, maxdegree, finalListOfFunctionalSpaces, path=None):
    if path is None:
        path = [start]
       
    if (maxdegree == 1):
        path.sort()
        # print ("Path at maxdegree 1 : ", path)
        if path not in finalListOfFunctionalSpaces:
            finalListOfFunctionalSpaces.append(path)
    else:
        '''
        print()
        print(start)
        print(path)
        print(graph[start])
        print(graph[start] - set(path))
        '''
        for nextFS in graph[start] - set(path):
            if (maxdegree != 1):
                intermediatePath = path
                intermediatePath.sort()
                if intermediatePath not in finalListOfFunctionalSpaces:
                    finalListOfFunctionalSpaces.append(intermediatePath)
                # print ("Intermediate", path)
                dfs(graph, nextFS, maxdegree - 1, finalListOfFunctionalSpaces, path + [nextFS])
##########################################################################
##########################################################################
finalListOfFunctionalSpaces = []
for i in range(1, numberOfAtomicFunctionalSpaces + 1):
        dfs(adjacencyList, i, numberOfAtomicFunctionalSpaces, finalListOfFunctionalSpaces)

#print(finalListOfFunctionalSpaces)

'''
count = 0
for i in finalListOfFunctionalSpaces:
    if(len(i)==12): count += 1
    if(len(i)==12): print(i)
   
print(count)
'''
##########################################################################
##########################################################################
functionalSpaceAreas = {}
# FS functionalSpaceNumber comprises of atomic FS's listed in blocksList
for (functionalSpaceNumber, blocksList) in enumerate(finalListOfFunctionalSpaces):
    #print(blocksList)
    functionalSpaceAreas[functionalSpaceNumber] = sum(atomicFunctionalSpaceArea[x] for x in blocksList)
   
# print(functionalSpaceAreas)
##########################################################################
##########################################################################
# The allocation must be done in a way such that no two requests end up sharing the same space
def check_for_overlap(allocationBlocks):
    if(len(allocationBlocks) != len(set(allocationBlocks))):
        return False
    firstPossibleFunctionalSpaceNumber = allocationBlocks[0]
    previousFunctionalSpaceBlockList = set(finalListOfFunctionalSpaces[firstPossibleFunctionalSpaceNumber])
    for functionalSpaceNumber in allocationBlocks[1:]:
        # print(finalListOfFunctionalSpaces[previousFunctionalSpaceNumber])
        currentFunctionalSpaceBlockList = frozenset(finalListOfFunctionalSpaces[functionalSpaceNumber])
        if(not currentFunctionalSpaceBlockList.isdisjoint(previousFunctionalSpaceBlockList)):
            return False
        previousFunctionalSpaceBlockList = previousFunctionalSpaceBlockList.union(currentFunctionalSpaceBlockList)
   
    return True
##########################################################################
##########################################################################
# No functional space must be allocated to a request that is a superset for an existing allocation
def is_not_a_superset(functionalSpaceNumber, spaceAllocation, currentRequestPossibleAllocations):
    atomicBlocksList = frozenset(finalListOfFunctionalSpaces[functionalSpaceNumber])
    for currentAllocation in currentRequestPossibleAllocations:
        currentAllocationBlocksList = frozenset(finalListOfFunctionalSpaces[currentAllocation])
        if(atomicBlocksList.issuperset(currentAllocationBlocksList)):
            break
    else:
        return True
##########################################################################
##########################################################################
def get_functional_space_allocation(requests, functionalSpaceAreas):
    print(requests)
    print(functionalSpaceAreas)
    # spaceAllocation = [[] for x in length(requests)]
    spaceAllocation = []
    for requestedArea in requests:
        currentRequestPossibleAllocations = []
        for functionalSpaceNumber in functionalSpaceAreas:
            # print(functionalSpaceNumber, functionalSpaceArea)
            if(requestedArea <= functionalSpaceAreas[functionalSpaceNumber] and is_not_a_superset(functionalSpaceNumber, spaceAllocation, currentRequestPossibleAllocations)):
                currentRequestPossibleAllocations.append(functionalSpaceNumber)
        spaceAllocation.append(currentRequestPossibleAllocations)
    # print(spaceAllocation)
   
    for allocationPossibility in filter(check_for_overlap, product(*spaceAllocation)):               
        print("possibility " , allocationPossibility)
        for i in allocationPossibility:
            print(finalListOfFunctionalSpaces[i])
            
    for allocationPossibility in filter(check_for_overlap, product(*spaceAllocation)):               
        print("possibility " , allocationPossibility)
        for i in allocationPossibility:
            print(finalListOfFunctionalSpaces[i])
##########################################################################
##########################################################################
while(1):
    print("Number of requests? (Q for exit)")
    inputRequest = input()
    if(inputRequest.lower() == 'q'): exit(0)
    requests = []
    for i in range(int(inputRequest)):
        requests.append(int(input()))
    '''
    requests.append(1500)
    requests.append(22000)
    requests.append(24)
    requests.append(1000)
    '''
    get_functional_space_allocation(requests, functionalSpaceAreas)
##########################################################################
