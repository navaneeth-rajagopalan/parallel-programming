class Summary:

    """ Summary stores the Grid Summary Total Tweet Count and the Hashtag Information along with the execution time """

    def __init__(self, melbGrid):
        """ Initialize the Summary - initialized melbGrid obj """
        # Initialize the Grid - ID, Latitute min and max, Longitute min and max
        self.melbGrid = melbGrid
        self.executionTime = 0
        self.totalTweetsProcessed = 0
        self.rank = -1