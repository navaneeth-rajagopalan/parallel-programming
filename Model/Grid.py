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
        hashTag = hashTag.lower()
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
        topFiveHashtags = []
        counter = 0
        totalHashtagsRecorded = len(sortedHashTags)
        for index in range(limit):
            if counter >= totalHashtagsRecorded:
                break
            topFiveHashtags.append(sortedHashTags[index])
            counter += 1            
        while counter < totalHashtagsRecorded and topFiveHashtags[-1][1] == sortedHashTags[counter][1]: # Add the Hashtags that are as frequent as the 5th most frequent hashtag and check to not run out of array index
            topFiveHashtags.append(sortedHashTags[counter])
            counter += 1
        return self.id + ": " + str(tuple(topFiveHashtags[:]))

    def consolidateHashTagInfo(self, hashTagSummaryList):
        """ Add hash tag information to the grid. If a new hash tag is encountered create a new property with hash tag and set count to 1. If hashtag exists in grid, increment counter by the count in the list """
        for hashTag in hashTagSummaryList:
            hashTag = hashTag.lower()
            if hashTag in self.hashTags:
                self.hashTags[hashTag] += hashTagSummaryList[hashTag]
            else:
                self.hashTags[hashTag] = hashTagSummaryList[hashTag]

    def consolidateTweetCounter(self, additionalTweetCount):
        """ Increments the tweet counter for the grid by the number of additional tweets recorded """
        self.tweetCount += additionalTweetCount