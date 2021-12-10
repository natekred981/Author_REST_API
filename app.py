from flask import Flask, request,jsonify, Response
import aiohttp
import asyncio
from flask_caching import Cache


app = Flask(__name__)
app.config['DEBUG'] = True
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


def parse_url():
    """ 
        This function breaks down the url into the tags component,
        sortBy component, and direction component. 
    """

    if 'tags' in request.args and len(request.args['tags']) > 0: 
        tags = request.args['tags'].split(",")
    else:
        response = "{\n'error': 'Tags parameter is required'\n}"
        return Response(response, status=400,mimetype='application/json')

    sortBy, direction = "id", "asc"
    if "sortBy" in request.args: sortBy = request.args["sortBy"]
    if (sortBy != "id") and (sortBy != "reads") and \
    (sortBy != "likes") and (sortBy != "popularity"):
        response = "{\n'error': 'SortBy parameter is invalid'\n}"
        return(Response(response, status=400,mimetype='application/json'))
      
    if "direction" in request.args: direction = request.args["direction"]
    if (direction != "asc") and (direction != "desc"):
        response = "{\n'error': 'direction parameter is invalid'\n}"
        return(Response(response, status=400,mimetype='application/json'))
    return (tags,sortBy,direction)

@cache.memoize(timeout=30) 
def check_caching(tags,sortBy,direction):
    """ 
        Simply checks if function arguments have been successfuly cached or not
        by letting the user know in the terminal if it has been cached already 
        in which case nothing will be printed
    """
    print("it was cached")
    return tags, sortBy, direction


async def get_tags(session, tag):
    """ 
        This function allows the user to asynchronously load in the 
        data from however many tags they have requested in the URL
    """
    URL = f'https://api.hatchways.io/assessment/blog/posts?tag={tag}'
    async with session.get(URL) as response:
        result = await response.json()
        return result["posts"]


def organize_data(data,sortBy,direction):
    """ 
        This function is responsible for sorting the data using sortBy and direction
        into the properly formated jsons.
    """
    sorted_data = data[0]
    for unsorted_data in data[1:]:
        for dict_entry in unsorted_data:   
            if dict_entry not in sorted_data: sorted_data.append(dict_entry)
    if direction == "desc":
        sorted_data = (sorted(sorted_data, key = lambda i: i[sortBy], reverse=True))
    else:
        sorted_data = (sorted(sorted_data, key = lambda i: i[sortBy], reverse=False))
    sorted_data = {"posts": sorted_data}
    return sorted_data




@app.route('/api/ping',methods=["GET"])
def send_200_request():
    return Response("{\n'success':'True'\n}", status=200,mimetype='application/json')



@app.route('/api/posts',methods=["GET"])


async def main():
    """
        The main function accesses the above helper function to return 
        either a 200 status code with the posts json or
        400 status code error json.
    """
    check_for_error = parse_url()
    if type(check_for_error) == Response: return check_for_error
    else:
        tags,sortBy,direction = parse_url()
        tags,sortBy,direction = check_caching(tags,sortBy,direction)
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for tag in tags:
            task = asyncio.ensure_future(get_tags(session, tag))
            tasks.append(task)

        data = await asyncio.gather(*tasks)
        result = organize_data(data,sortBy,direction)
        return jsonify(result)




if __name__ == "__main__":
    app.run(port=5000)

    
    
    