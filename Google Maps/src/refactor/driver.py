from pygmap import PyGmap, Coordinate, Map

if __name__=="__main__":

    center = Coordinate(latitude=0, longitude=0, altitude=0, ctype="waypoint", duration=0)

    map_options = {
        "center"    : center,
        "zoom"      : 5,
        "mapTypeId" : Map.ROADMAP,
        "something" : "something else"
    }

    pygmap = PyGmap(Map(map_options))

    pygmap.write()
