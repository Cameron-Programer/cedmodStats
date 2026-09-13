import requests
import devEnv

# TODO: Write tests

# Setting global vars.

domain = "freyasfortress.cmod.app"
banlist = "26091"
apiKey = devEnv.apiKey
maxDefault = "10"


def validate_query(max, q, page):
    if max is not None:
        if max <= 100:
            max = str(int(max))
        else:
            # Making a request for more than 100 items will invalidate API key.
            max = maxDefault
    else:
        max = maxDefault

    if page is not None:
        page = str(int(page))
    else:
        page = "0"

    if q is not None:
        q = str(q)
    else:
        q = "none@custom"

    return (max, q, page)


def make_request(endpoint, queryDict=None):
    print("API: Making request to endpoint: " + endpoint)
    # Endpoint validation
    if str(endpoint).lower().endswith("user"):
        # Making a request for a user endpoint will also result in the key being invalidated.
        print("Forbidden Request: It is forbidden to access endpoints ending with 'user' ")
        return ("ERROR: Forbidden endpoint")

    # Setting header
    header = {
        "authorization": "Bearer " + apiKey,
        "Accept": "*/*"
    }

    # Checking if a query dictionary has been passed in, if it has the request will include it.
    if queryDict is not None:
        response = requests.get("https://" + domain + endpoint, params=queryDict, headers=header)
    else:
        response = requests.get("https://" + domain + endpoint, headers=header)

    responseJson = response.json()

    # Returning the Json response object
    print("API: Finished request to endpoint: " + endpoint)
    return responseJson


# Note: Get functions are very similar as such I will only explain the first one.
def get_bans(max=None, q=None, page=None):
    # Checking that the params are valid and if not setting them to defaults.
    max, q, page = validate_query(max=max, q=q, page=page)

    # Setting the query using a dict to ensure that the user cannot inject text to change the location of the call.
    queryDict = {
        "q": str(q),
        "banList": str(banlist),
        "page": str(page),
        "max": str(max)
    }

    # Making the request, this returns a JSON object. this is the returned.
    return make_request(endpoint="/Api/BanLog/Query", queryDict=queryDict)


def get_warns(max=None, q=None, page=None):
    max, q, page = validate_query(max=max, q=q, page=page)

    queryDict = {
        "q": str(q),
        "banList": str(banlist),
        "page": str(page),
        "max": str(max)
    }

    return make_request(endpoint="/Api/Warn/Query", queryDict=queryDict)


def get_reports(max=None, q=None, page=None):
    max, q, page = validate_query(max=max, q=q, page=page)

    queryDict = {
        "q": str(q),
        "page": str(page),
        "max": str(max)
    }

    return make_request(endpoint="/Api/Report/Query", queryDict=queryDict)


def get_activity(max=25, q=None, page=None, staffOnly=True, activityMin=30):
    max, q, page = validate_query(max=max, q=q, page=page)

    queryDict = {
        "q": str(q),
        "create": "false",
        "moderationData": "true",
        "staffOnly": str(staffOnly),
        "max": str(max),
        "page": str(page),
        "sortLabel": "id_field",
        "sortDirection": "None",
        "activityMin": str(activityMin)
    }

    return make_request(endpoint="/Api/Player/Query", queryDict=queryDict)
