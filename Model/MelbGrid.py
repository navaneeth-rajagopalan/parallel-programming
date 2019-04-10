from Grid import Grid
import json
import re

class MelbGrid:

    def __init__(self, gridConfigs):
        """ Initialize the grid information for each of the Grid in Melbourne City. The grid configuration is an extract of the MelbGrid.json file containing the Grid ID, xmin, xmax, ymin and ymax information """
        self.grids = []
        self.others = Grid("Others", 0, 0, 0, 0)
        for gridConfig in gridConfigs:
            properties = gridConfig["properties"]
            self.grids.append(Grid(properties["id"], properties["xmin"], properties["xmax"], properties["ymin"], properties["ymax"]))

    def consolidateMelbGrids(self, subMelbGrid):
        """ consolidate the data from subMelbGrid and add the tweet count, hashtags in the root melb grid """
        self.others.consolidateTweetCounter(subMelbGrid.others.tweetCount)
        for index, grid in enumerate(self.grids):
            # Consolidate the Tweet counts
            grid.consolidateTweetCounter(subMelbGrid.grids[index].tweetCount)
            # Consolidate the Hashtag summary
            print("TEST: ")
            print(subMelbGrid.grids[index].hashTags)
            grid.consolidateHashTagInfo(subMelbGrid.grids[index].hashTags)

    def getTweetCoordinate(self, tweet):
        """ Process the tweet dictionary to get the coordinates from any of the 3 coordinates properties that may be available """
        tweetOriginCoordinates = []
        # Check the Doc section - Coordinates - doc.coordinates.coordinates
        if ("doc" in tweet) and (type(tweet["doc"]) == dict):
            # doc exists in the tweet data and is of type dictionary. Can be iterated          
            if ("coordinates" in tweet["doc"] and (type(tweet["doc"]["coordinates"]) == dict)):
                # coordinates exists in tweets.doc and is of type dictionary. Can be iterated
                if ("coordinates" in tweet["doc"]["coordinates"] and (type(tweet["doc"]["coordinates"]["coordinates"]) == list)):
                    # Coordinates exist in tweet.doc.coordinates.coordinates and is of type list. Geo coordinates can be obtained from here
                    tweetOriginCoordinates = tweet["doc"]["coordinates"]["coordinates"]
                    if len(tweetOriginCoordinates) == 2:
                        xPos = tweetOriginCoordinates[0]
                        yPos = tweetOriginCoordinates[1]
                        return [xPos, yPos]
        
        # Check the Doc section - Geo - Coordinates - doc.geo.coordinates
        if ("doc" in tweet) and (type(tweet["doc"]) == dict):
            # doc exists in the tweet data and is of type dictionary. Can be iterated
            if ("geo" in tweet["doc"] and (type(tweet["doc"]["geo"]) == dict)):
                # geo exists in tweets.doc and is of type dictionary. Can be iterated
                if ("coordinates" in tweet["doc"]["geo"] and (type(tweet["doc"]["geo"]["coordinates"]) == list)):
                    # Coordinates exist in tweet.doc.coordinates.coordinates and is of type list. Geo coordinates can be obtained from here
                    tweetOriginCoordinates = tweet["doc"]["geo"]["coordinates"]
                    if len(tweetOriginCoordinates) == 2:
                        xPos = tweetOriginCoordinates[1]
                        yPos = tweetOriginCoordinates[0]
                        return [xPos, yPos]

        # Check the Value section - Coordinate - value.geometry.coordinates
        if ("value" in tweet) and (type(tweet["value"]) == dict):
            # Value exists in the tweet data and is of type dictionary. Can be iterated
            if ("geometry" in tweet["value"] and (type(tweet["value"]["geometry"]) == dict)):
                # Geometry exists in tweets.value and is of type dictionary. Can be iterated
                if ("coordinates" in tweet["value"]["geometry"] and (type(tweet["value"]["geometry"]["coordinates"]) == list)):
                    # Coordinates exist in tweet.value.geometry.coordinates and is of type list. Geo coordinates can be obtained from here
                    tweetOriginCoordinates = tweet["value"]["geometry"]["coordinates"]
                    if len(tweetOriginCoordinates) == 2:
                        xPos = tweetOriginCoordinates[0]
                        yPos = tweetOriginCoordinates[1]
                        return [xPos, yPos]
        
        # No proper tweet origin location details found
        return [-1, -1]

    def getHashtagsFromTweet(self, tweet):
        """ Process the tweet text to fetch the hashtags in the text as an array """
        # Check the Doc section - Coordinates - doc.coordinates.coordinates
        if ("doc" in tweet) and (type(tweet["doc"]) == dict) and ("text" in tweet["doc"]) and (type(tweet["doc"]["text"]) == str):
            tweetText = tweet["doc"]["text"]
            # https://www.hashtags.org/platforms/twitter/what-characters-can-a-hashtag-include/
            hashtags = re.findall(r" #(\w+)", tweetText)
            return hashtags
        return []

    def processTweet(self, tweet):
        """ Identify the grid from where the tweet has originated and update the grid information. Identify the hashtags associated with the tweet and update the respective grid's hashtag data """
        gridFound = False # Used to sanity check the process
        # Get the Tweet origin coordinates
        tweetOriginCoordinates = self.getTweetCoordinate(tweet)
        if tweetOriginCoordinates[0] != -1 and tweetOriginCoordinates[1] != -1:
            xPos = tweetOriginCoordinates[0]
            yPos = tweetOriginCoordinates[1]
            
            for grid in self.grids:
                # Check Latitude
                if (xPos >= grid.xmin and xPos <= grid.xmax):
                    # Check Longitude
                    if (yPos >= grid.ymin and yPos <= grid.ymax):
                        # Grid Found
                        gridFound = True
                        grid.incrementTweetCounter()
                        # Get the hashtag and update the grid
                        hashTags = self.getHashtagsFromTweet(tweet)
                        if len(hashTags) > 0:
                            for hashTag in hashTags:
                                grid.addHashTagInfo(hashTag)
                        break
            
        if not gridFound:
            self.others.incrementTweetCounter()