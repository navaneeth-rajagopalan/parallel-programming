from Grid import Grid

class MelbGrid:

    def __init__(self, gridConfigs):
        """ Initialize the grid information for each of the Grid in Melbourne City. The grid configuration is an extract of the MelbGrid.json file containing the Grid ID, xmin, xmax, ymin and ymax information """
        self.grids = {}
        self.others = Grid("Others", 0, 0, 0, 0)
        for gridConfig in gridConfigs:
            properties = gridConfig["properties"]
            self.grids[properties["id"]] = Grid(properties["id"], properties["xmin"], properties["xmax"], properties["ymin"], properties["ymax"])

    def processTweet(self, tweet):
        """ Identify the grid from where the tweet has originated and update the grid information. Identify the hashtags associated with the tweet and update the respective grid's hashtag data """
        # Get the Tweet origin coordinates
        #TODO Check if Geolocation data is available
        coordinates = tweet["value"]["geometry"]["coordinates"]
        xPos = coordinates[0]
        yPos = coordinates[1]

        gridFound = False # Used to sanity check the process

        for gridId in self.grids:
            # Check Latitude
            if (xPos >= self.grids[gridId].xmin and xPos <= self.grids[gridId].xmax):
                # Check Longitude
                if (yPos >= self.grids[gridId].ymin and yPos <= self.grids[gridId].ymax):
                    # Grid Found
                    gridFound = True
                    self.grids[gridId].incrementTweetCounter()
                    # Get the hashtag and update the grid
                    hashTags = tweet["doc"]["entities"]["hashtags"]
                    if len(hashTags) > 0:
                        for hashTag in hashTags:
                            self.grids[gridId].addHashTagInfo(hashTag["text"])
                    break
        
        if not gridFound:
            self.others.incrementTweetCounter()