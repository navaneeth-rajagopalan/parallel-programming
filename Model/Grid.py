import operator

class Grid:

    """ Grid stores the grid configuration details - ID, Latitude, Longitude boundary details, Total Tweet Count and the Hashtag Information """

    def __init__(self, id, xmin, xmax, ymin, ymax):
        """ Initialize the Grid - ID, Coordinate, Tweet count """
        # Initialize the Grid - ID, Latitute min and max, Longitute min and max
        self.id = id
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        # Initialize the Grid's Tweet Count to 0
        self.tweetCount = 0
        # Initialize the Grid's Hashtag information
        self.hashTags = {}
    
    def addHashTagInfo(self, hashTag):
        """ Add hash tag information to the grid. If a new hash tag is encountered create a new property with hash tag and set count to 1. If hashtag exists in grid, increment counter by 1 """
        hashTag = "#" + hashTag.lower()
        if hashTag in self.hashTags:
            self.hashTags[hashTag] += 1
        else:
            self.hashTags[hashTag] = 1

    def incrementTweetCounter(self):
        """ Increments the tweet counter for the grid by 1 """
        self.tweetCount += 1

    def getTweets(self):
        """ Return the total tweets in the Grid """
        return self.id.upper() + ": " + str(self.tweetCount) + " posts"
    
    def getHashTags(self, limit):
        """ Get all the Hashtag frequency. Sorted in descending order. The results are limited by the limit parameter """
        sortedHashTags = sorted(self.hashTags.items(), key=operator.itemgetter(1), reverse=True)
        return self.id + ": " + str(tuple(sortedHashTags[:limit]))

    def consolidateHashTagInfo(self, hashTagSummaryList):
        """ Add hash tag information to the grid. If a new hash tag is encountered create a new property with hash tag and set count to 1. If hashtag exists in grid, increment counter by the count in the list """
        for hashTag in hashTagSummaryList:
            if hashTag in self.hashTags:
                self.hashTags[hashTag] += hashTagSummaryList[hashTag]
            else:
                self.hashTags[hashTag] = 1

    def consolidateTweetCounter(self, additionalTweetCount):
        """ Increments the tweet counter for the grid by the number of additional tweets recorded """
        self.tweetCount += additionalTweetCount