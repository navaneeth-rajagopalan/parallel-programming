import json
from pprint import pprint



# with open('TwitterFiles/TinyTwitter.json', encoding="utf8") as f:
with open('TwitterFiles/SmallTwitter.json', encoding="utf8") as f:
    data = json.load(f)

count = {}

count["value"] = 0
count["value_geometry_coordinates"] = 0
count["hashtags"] = 0
count["hashtags.count"] = 0
count["hashtags.empty"] = 0

for row in data["rows"]:
    if "value" in row:
        count["value"] += 1
    if "coordinates" in row["value"]["geometry"]:
        if len(row["value"]["geometry"]["coordinates"]) == 2:
            count["value_geometry_coordinates"] += 1
    if "hashtags" in row["doc"]["entities"]:
        count["hashtags"] += 1
        for hashtag in row["doc"]["entities"]["hashtags"]:
            count["hashtags.count"] += 1
            if hashtag["text"] == '':
                count["hashtags.empty"] += 1

pprint(count)