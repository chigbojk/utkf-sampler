import json
import os

# Input list of file names
# Output json file. [ file name: {age, gender, race, [landmarks]}]

# get Asian data (to reclassify into E. Asian and S. Asian)
# get Other data (to reclassify into Middle Eastern (and Other?))

IMG_DIRS = ["utkf/part{0}/".format(x) for x in range(1, 4)]
LANDMARK_FILES = ["utkf/landmark_list_part{0}.txt".format(x) for x in range(1, 4)]
OUTPUT_FILE = 'out.json'

genderDict = {"0": "Male", "1": "Female"}
raceDict = {"0": "White", "1": "Black", "2": "Asian", "3": "Indian", "4": "Others"}

def main():
    res = []

    for i, dir in enumerate(IMG_DIRS):
        for fileName in os.listdir(dir)[:50]:
            metadata = {}
            values = fileName.split("_")
            
            if len(values) == 4 and all(x for x in values):
                age = str(values[0])
                gender = genderDict[values[1]]
                race = raceDict[values[2]]

                metadata["age"] = age
                metadata["gender"] = gender
                metadata["race"] = race

                with open(LANDMARK_FILES[i], 'r') as f:
                    for line in f:
                        key, val = line.split(" ")[0], line.split(" ")[1:-1]
                        
                        if key == fileName:
                            landmarks = val
                            metadata["landmarks"] = landmarks

                res.append((fileName, metadata))
    return res

def filterJSON(key, val):
    res = []

    with open(OUTPUT_FILE, 'r') as f:
        data = json.loads(f.read())
        
        for entry in data:
            imgName, imgData = entry[0], entry[1]
            if imgData[key] == val:
                res.append((imgName, imgData))

    return res

def saveJSON(res, file=OUTPUT_FILE):
    with open(file, "w") as f:
        json.dump(res, f)

def saveFilteredJSON(key="race", val="Others"):
    res = filterJSON(key, val)
    OUT_FILE = "out-{0}-{1}.json".format(key, val)
    saveJSON(res, OUT_FILE)

if __name__ == "__main__":
    saveFilteredJSON("race", "Indian")
