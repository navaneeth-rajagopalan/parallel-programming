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

hashtagFrequencyLimiter = 5

totalTweets = 0
startTime = time.time()

melbGridConfig = None

def processTwitterFile(mySummary, rank, cores):
    # Load the BigTwitter.json file and populate MelbGrid
    #with open('TwitterFiles/bigTwitter.json', encoding="utf8") as twitterFileHandle:

    # Load the SmallTwitter.json file and populate MelbGrid
    #with open('TwitterFiles/smallTwitter.json', encoding="utf8") as twitterFileHandle:

    # Load the TinyTwitter.json file and populate MelbGrid
    with open('TwitterFiles/tinyTwitter.json', encoding="utf8") as twitterFileHandle:

    # Load the SampleBigTwitter.json file and populate MelbGrid
    #with open('TwitterFiles/SampleBigTwitter.json', encoding="utf8") as twitterFileHandle:
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
                        mySummary.rank = rank
    
    return mySummary

if rank == 0:
    # Load the MelbGrid json and parse the data to melbGrid
    with open('Config/MelbGrid.json', encoding="utf8") as melbGridConfigFile:
        melbGridConfig = json.load(melbGridConfigFile)
    summaryList = []
    for i in range(size):
        # Create the array with the data strucutre to populate the information by processing the file
        # Inilialize the Melb Grid from the MelbGrid.json file data
        summaryList.append(Summary(MelbGrid(melbGridConfig["features"])))
else:
    summaryList = None

mySummary = comm.scatter(summaryList, root = 0)

print("Data place holders scattered")

mySummary = processTwitterFile(mySummary, rank, size)

endTime = time.time()

mySummary.executionTime = endTime - startTime

processedList = comm.gather(mySummary, root = 0)

if rank == 0:
    print("Received Data")
    finalMelbGrid = MelbGrid(melbGridConfig["features"])
    for processedMelbGridSummary in processedList:
        processedMelbGrid = processedMelbGridSummary.melbGrid
        print("Summary from processor #" + str(processedMelbGridSummary.rank))
        for grid in processedMelbGrid.grids:
            print(grid.getTweets())
        print("\n")
        print(processedMelbGrid.others.getTweets())
        print("\n")
        totalTweets += processedMelbGridSummary.totalTweetsProcessed
        print("Total tweets in file: " + str(processedMelbGridSummary.totalTweetsProcessed))
        # print("\n")

        # # Print the Hashtags summary in each grid
        # hashtagFrequencyLimiter = 5
        # for grid in processedMelbGrid.grids:
        #     print(grid.getHashTags(hashtagFrequencyLimiter))

        print("\nExecution Time: " + str(processedMelbGridSummary.executionTime) + " s")

        print("\n########################################################################################################################################################\n")

        finalMelbGrid.consolidateMelbGrids(processedMelbGrid)
    
    for finalGrid in finalMelbGrid.grids:
        print(finalGrid.getTweets())
    print("\n")
    print(finalMelbGrid.others.getTweets())
    print("\n")
    print("Total tweets in file: " + str(totalTweets))
    print("\n")

    # Print the Hashtags summary in each grid
    for finalGrid in finalMelbGrid.grids:
        print(finalGrid.getHashTags(hashtagFrequencyLimiter))

    endTime = time.time()

    print("\nExecution Time: " + str(endTime - startTime) + " s")