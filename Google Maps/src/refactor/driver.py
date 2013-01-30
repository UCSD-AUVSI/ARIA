from pygmap import PyGmap, Coordinate, Map, Polyline

if __name__=="__main__":

    center = Coordinate(latitude=0, longitude=0, altitude=0, ctype="waypoint", duration=0)

    map_options = {
        "center"    : center,
        "zoom"      : 5,
        "mapTypeId" : 'ROADMAP',
    }
    map_ = Map(options = map_options)


    path_array = [
        Coordinate(latitude=0, longitude=0, altitude=0, ctype="takeoff", duration=0),
        Coordinate(latitude=10, longitude=10, altitude=0, ctype="waypoint", duration=0),
        Coordinate(latitude=15, longitude=-15, altitude=0, ctype="loiter", duration=5),
        Coordinate(latitude=0, longitude=0, altitude=0, ctype="land", duration=0),
    ]
    path_options = {
        "path"  : path_array
    }
    path = Polyline(options = path_options)

    API_KEY = "AIzaSyDUqZDJn8yWjIKJ4nUsHQGuEAvZHar41rs"

    pygmap = PyGmap(map_, API_KEY, path)

    pygmap.write()
