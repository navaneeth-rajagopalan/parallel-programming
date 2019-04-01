import sys
sys.path.append('./Model')
from MelbGrid import MelbGrid
import json
import time

startTime = time.time()

# Load the MelbGrid json and parse the data to melbGrid
with open('Config/MelbGrid.json', encoding="utf8") as melbGridConfigFile:
    melbGridConfig = json.load(melbGridConfigFile)

# Inilialize the Melb Grid from the MelbGrid.json file data
melbGrid = MelbGrid(melbGridConfig["features"])

# Load the SmallTwitter.json file and populate MelbGrid
with open('TwitterFiles/SmallTwitter.json', encoding="utf8") as tweetFile:

# Load the TinyTwitter.json file and populate MelbGrid
# with open('TwitterFiles/TinyTwitter.json', encoding="utf8") as tweetFile:

# Load the Sample TestTwitter.json file and populate MelbGrid
# with open('TwitterFiles/TestTwitter.json', encoding="utf8") as tweetFile:
    tweets = json.load(tweetFile)
    for tweet in tweets["rows"]:
        melbGrid.processTweet(tweet)

# Print the Tweets summary in each grid
for grid in melbGrid.grids:
    print(melbGrid.grids[grid].getTweets())

# Print the Hashtags summary in each grid
hashtagFrequencyLimiter = 5
for grid in melbGrid.grids:
    print(melbGrid.grids[grid].getHashTags(hashtagFrequencyLimiter))

endTime = time.time()

print("\n\nExecution Time: " + str(endTime - startTime) + " s")