import json

#ricordarsi di far vedere le costanti da usare qui dentro
# controllare che richiamando queste funzioni, posso avere accesso al self.configValues della classe super Bot


# metodo della classe bot e non delle api
# def buildSearchParams(self):
#     print "Check search params..."
#     if "searchParams" in self.configValues:
#         print "Found search params: building"
#         searchParams = []
#         for tag in self.configValues["searchParams"]["tags"]:
#             sort = ""
#             categories = []
#             typeSearch = "fresh"

#             if "sort" in self.configValues["searchParams"]:
#                 sort = self.configValues["searchParams"]["sort"]

#             if "type" in self.configValues["searchParams"]:
#                 typeSearch = self.configValues["searchParams"]["type"]

#             if "categories" in self.configValues["searchParams"]:
#                 categories = self.configValues["searchParams"]["categories"]

#             searchParams.append({"term": tag, "typeSearch": typeSearch, "sort": sort, "categories": categories})
    
#     print "DEBUG: we have " + str(len(searchParams)) + " search criteria"

#     print "DEBUG: Append data in " + self.constants["SEARCH_FILE"]
#     appendToFile(searchParams, self.constants["SEARCH_FILE"])


def search(self, term="",typeSearch="photos",sort="",categories=[], exclude_nude=True, page=1):
    # endpoin GET https://api.500px.com/v1/photos/search
    # params
    # type:photos
    # term:london
    # sort:highest_rating|pulse|created_at default: revelance
    # only:Aerial|Animals,Celebrities multiple
    # image_size[]:1
    # image_size[]:2
    # image_size[]:32
    # image_size[]:31
    # image_size[]:33
    # image_size[]:34
    # image_size[]:35
    # image_size[]:36
    # image_size[]:2048
    # image_size[]:4
    # image_size[]:14
    # include_states:true
    # formats:jpeg,lytro
    # include_tags:true
    # exclude_nude:true
    # page:1
    # rpp:50

    params = {
        "term": term,
        "type": typeSearch,
        "image_size": [1,2,32,31,33,34,35,36,2048,4,14],
        "include_states": True,
        "formats": "jpeg,lytro",
        "exclude_nude": exclude_nude,
        "page": page,
        "rpp": 50
    }

    if sort != "":
        params["sort"] = sort

    if categories != "":
        params["only"] = ",".join(categories) #working?


    search = []
    try:
        search = self.enviroment_variables["userSession"].get(self.constants["API_DOMAIN"] + '/photos/search', params=params, headers = self.enviroment_variables["configValues"]["csrfHeaders"])
        if search.status_code == 200:
            search = json.loads(search.text)
        elif search.status_code == 404:
            print "404 - photo not exists"
        else:
            print search.status_code

        pass
    except Exception, e:
        print "exception search: " + str(e)
        pass

    return search