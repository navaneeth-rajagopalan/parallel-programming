import sys
sys.path.append('./Model')
from MelbGrid import MelbGrid
from Summary import Summary
import json
import time
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size

totalTweets = 0
startTime = time.time()

def processTwitterFile(mySummary, rank, cores):
    # Load the BigTwitter.json file and populate MelbGrid
    #with open('TwitterFiles/BigTwitter.json', encoding="utf8") as twitterFileHandle:

    # Load the SmallTwitter.json file and populate MelbGrid
    #with open('TwitterFiles/SmallTwitter.json', encoding="utf8") as twitterFileHandle:

    # Load the TinyTwitter.json file and populate MelbGrid
    # with open('TwitterFiles/TinyTwitter.json', encoding="utf8") as twitterFileHandle:

    # Load the SampleBigTwitter.json file and populate MelbGrid
    with open('TwitterFiles/SampleBigTwitter.json', encoding="utf8") as twitterFileHandle:
        for lineNum, line in enumerate(twitterFileHandle):
            if lineNum > 0:
                if lineNum % cores == rank:
                    if "coordinates" in str(line):
                        if str(line[-2]) == ',':
                            line = line[:-2]
                        elif str(line[-3:-1]) == "]}":
                            break
                        mySummary.totalTweetsProcessed += 1
                        tweetDetails = json.loads(line)
                        mySummary.melbGrid.processTweet(tweetDetails)


# Create an empty list of size = number of cores
summaryList = [None] * comm.size

# Load the MelbGrid json and parse the data to melbGrid
with open('Config/MelbGrid.json', encoding="utf8") as melbGridConfigFile:
    melbGridConfig = json.load(melbGridConfigFile)

# Inilialize the Melb Grid from the MelbGrid.json file data
melbGrid = MelbGrid(melbGridConfig["features"])
finalMelbGrid = MelbGrid(melbGridConfig["features"])


if rank == 0:
    summaryList = []
    for i in range(size):
        summaryList.append(Summary(melbGrid))
else:
    summaryList = None

mySummary = comm.scatter(summaryList, root = 0)

print("After Scatter")

processTwitterFile(mySummary, rank, size)

endTime = time.time()

mySummary.executionTime = endTime - startTime

processedList = comm.gather(mySummary, root = 0)

if rank == 0:
    print("Received Data")
    for processedMelbGridSummary in processedList:
        processedMelbGrid = processedMelbGridSummary.melbGrid
        print("Summary from 1 core")
        processedMelbGrid.grids = sorted(processedMelbGrid.grids.items())
        print(processedMelbGrid.grids)
        for grid in processedMelbGrid.grids:
            print(grid)
            print(processedMelbGrid.grids[grid].getTweets())
        print("\n")
        print(processedMelbGrid.others.getTweets())
        print("\n")
        totalTweets += processedMelbGridSummary.totalTweetsProcessed
        print("Total tweets in file: " + str(processedMelbGridSummary.totalTweetsProcessed))
        print("\n")

        # Print the Hashtags summary in each grid
        hashtagFrequencyLimiter = 5
        for grid in melbGrid.grids:
            print(melbGrid.grids[grid].getHashTags(hashtagFrequencyLimiter))

        print("\nExecution Time: " + str(processedMelbGridSummary.executionTime) + " s")

        print("\n########################################################################################################################################################\n")

        melbGrid.consolidateMelbGrids(processedMelbGrid)
    
    for grid in melbGrid.grids:
        print(melbGrid.grids[grid].getTweets())
    print("\n")
    print(melbGrid.others.getTweets())
    print("\n")
    print("Total tweets in file: " + str(totalTweets))
    print("\n")

    # Print the Hashtags summary in each grid
    hashtagFrequencyLimiter = 5
    for grid in melbGrid.grids:
        print(melbGrid.grids[grid].getHashTags(hashtagFrequencyLimiter))

    endTime = time.time()

    print("\nExecution Time: " + str(endTime - startTime) + " s")