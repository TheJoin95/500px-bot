import json
import os

# uitls files
def appendToFile(data, filename="output.json"):
    feeds = []
    with open(filename, mode='r+') as feedsjson:
        feeds = json.load(feedsjson)

    with open(filename, mode='w') as feedsjson:
        if type(data) == type([]):
            feeds = data
        else:
            feeds.append(data)
        
        feeds = list(set(feeds))
        json.dump(feeds, feedsjson)


def getJsonFile(filename):
    fileContent = []
    if filename != '':
        f = open(filename)
        try:
            fileContent = json.load(f)
            pass
        except Exception, e:
            print e
            print 'error: filename - invalid json'
            pass
        
        f.close()

    return fileContent


def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z