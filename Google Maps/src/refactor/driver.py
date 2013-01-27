from pygmap import PyGmap, Coordinate, Map, PolyLine

if __name__=="__main__":

    center = Coordinate(latitude=0, longitude=0, altitude=0, ctype="waypoint", duration=0)

    map_options = {
        "center"    : center,
        "zoom"      : 5,
        "mapTypeId" : Map.ROADMAP,
    }

    API_KEY = "AIzaSyDUqZDJn8yWjIKJ4nUsHQGuEAvZHar41rs"

    path_array = [
        Coordinate(latitude=0, longitude=0, altitude=0, ctype="takeoff", duration=0),
        Coordinate(latitude=10, longitude=10, altitude=0, ctype="waypoint", duration=0),
        Coordinate(latitude=15, longitude=-15, altitude=0, ctype="loiter", duration=5),
        Coordinate(latitude=0, longitude=0, altitude=0, ctype="land", duration=0),
    ]

    path_options = {
        "path"  : path_array
    }

    pygmap = PyGmap(Map(map_options), API_KEY, PolyLine(path_options))

    pygmap.write()
