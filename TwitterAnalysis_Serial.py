import sys
sys.path.append('./Model')
from MelbGrid import MelbGrid
import json
import time

startTime = time.time()

totalTweets = 0

# Load the MelbGrid json and parse the data to melbGrid
with open('Config/MelbGrid.json', encoding="utf8") as melbGridConfigFile:
    melbGridConfig = json.load(melbGridConfigFile)

# Inilialize the Melb Grid from the MelbGrid.json file data
melbGrid = MelbGrid(melbGridConfig["features"])

# Load the BigTwitter.json file and populate MelbGrid
# with open('TwitterFiles/BigTwitter.json', encoding="utf8") as twitterFileHandle:

# Load the SmallTwitter.json file and populate MelbGrid
# with open('TwitterFiles/SmallTwitter.json', encoding="utf8") as twitterFileHandle:

# Load the TinyTwitter.json file and populate MelbGrid
with open('TwitterFiles/TinyTwitter.json', encoding="utf8") as twitterFileHandle:

# Load the Sample TestTwitter.json file and populate MelbGrid
# with open('TwitterFiles/TestTwitter.json', encoding="utf8") as twitterFileHandle:
    for lineNum, line in enumerate(twitterFileHandle):
        if lineNum > 0:
            if "coordinates" in str(line):
                if str(line[-2]) == ',':
                    line = line[:-2]
                elif str(line[-3:-1]) == "]}":
                    break
                totalTweets += 1
                tweetDetails = json.loads(line)
                melbGrid.processTweet(tweetDetails)

# Print the Tweets summary in each grid
melbGrid.sortGridByTweetCountDesc()
for grid in melbGrid.grids:
    print(grid.getTweets())
print("\n")
print(melbGrid.others.getTweets())
print("\n")
print("Total tweets in file: " + str(totalTweets))
print("\n")

# Print the Hashtags summary in each grid
hashtagFrequencyLimiter = 5
for grid in melbGrid.grids:
    print(grid.getHashTags(hashtagFrequencyLimiter))

endTime = time.time()

print("\n\nExecution Time: " + str(endTime - startTime) + " s")