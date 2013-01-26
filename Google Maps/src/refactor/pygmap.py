import os
import collections

#
# THIS CLASS NEEDS TO BE REFACTORED
#
class PyGmap(object):
    """
    simple python wrapper for google maps api
    """

    SHOW_PATH = True
    HIDE_PATH = False

    def __init__(self, map_, api_key, path=None):
        """
        options is dict of mapOptions (should work for most mapOptions from api)
        path is array of LatLng for preset path
        """
        self._api_key = api_key
        self._map = map_
        self._polyline = path
        self._display_polyline = True
        self._polygon_count = 0
        self._polygon_list = []
    
    def write(self, html_file="pygmap.html", js_file="pygmap.js"):
        """
        writes javascript and html to files
        file names can be passed in as parameters
        """
        cwd = os.curdir
        with open(cwd+'/static/'+html_file, 'w') as file:
            file.write(self._get_html())
        with open(cwd+'/static/'+js_file, 'w') as file:
            file.write(self._get_js())

    def toggle_display_path(self, switch):
        """
        turns path on/off using SHOW_PATH/HIDE_PATH constants
        """
        self._display_polyline = switch

    def add_polygon(self, polygon):
        """
        adds polygon to list to be displayed on map
        """
        self._polygon_count += 1
        self._polygon_list.append(polygon)
    
    def add_marker(self, marker):
        """
        add marker to be displayed on map
        only 1 marker can be on the map at any time
        """
        self._marker = marker

    def add_polyline(self, polyline):
        """
        """
        self._polyline = polyline

    #----------------------------------------------------------SET UP JAVASCRIPT---

    def _get_js(self):
        self._js = self._start_initialize()

        self._js += self._setup_map()
        self._js += self._setup_path()
        self._js += self._setup_event_listeners()
        self._js += self._end_initialize()

        return self._js

    def _start_initialize(self):
        js = """
            function initialize() {
        """
        return js

    def _end_initialize(self):
        js = """
            } // end initialize()
        """
        return js

    def _setup_map(self):
        js = """
            var mapOptions = {
        """

        for key,value in self._map.map_options.items():
            
            if key == "mapTypeId":
                js += """
                    %s : google.maps.MapTypeId.%s,
                """ % (key, value)

            elif type(value) is Coordinate:
                js += """
                    %s : new google.maps.LatLng(%d,%d),
                """ % (key,value.longitude, value.latitude)

            elif type(value) is str:
                js += """
                    %s : '%s',
                """ % (key, value)

            else:
                js += """
                    %s : %s,
                """ % (key, value)

        js += """
            };  // end mapOptions
            window.map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);
        """
        return js

    def _setup_path(self):
        js = ""
        if self._display_polyline:
            if self._polyline is not None:
                js = """
                    var pathArray = [
                """

                for point in self._polyline.polyline_options["path"]:
                    js += """
                        new google.maps.LatLng(%s, %s),
                    """ % (point.latitude, point.longitude)

                js += """
                    ]; // end path array
                """
            js += """
                var pathOptions = { 
            """
            
            if self._polyline is not None:
                js += """
                    path: pathArray,
                """
            js += """
                strokeColor: '#000000',
                strokeWeight: 2,
                strokeOpacity: 1,
                editable: true,
                map: window.map
                }; // end pathOptions
                window.path = new google.maps.Polyline(pathOptions);
            """

            return js
        else:
            pass

    def _setup_polygon(self):
        js = ""
        return js
    
    def _setup_context_menu(self):
        js = ""
        return js

    def _setup_event_listeners(self):
        js = """
            google.maps.event.addListener(window.map, 'click', function(event) {
                window.path.getPath().push(event.latLng);                
            });
        """
        return js

    #----------------------------------------------------------SET UP HTML---------

    def _get_html(self):
        self._html = """
        <!DOCTYPE html>
        <html>
            <head>
                <style text="text/css">
                    html {height: 100%%;}
                    body {height: 100%%; margin: 0, padding: 0}
                    #map_canvas {height: 100%%}
                </style>
                <script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?key=%s&sensor=false"></script>
                <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
                <script type="text/javascript" src="pygmap.js"></script>
            </head>
            <body onload="initialize()">
                <div id="map_canvas" style="width: 100%%; height: 100%%;"></div>
            </body>
        </html>
        """ % (self._api_key)
        return self._html

#------------------------------------------------------GOOGLE MAPS API OBJECTS-------

Coordinate = collections.namedtuple('Coordinate', 'latitude longitude altitude ctype duration')

class Map(object):
    
    ROADMAP = "ROADMAP"
    HYBRID = "HYBRID"
    SATELLITE = "SATELLITE"
    TERRAIN = "TERRAIN"

    def __init__(self,options):
        self._options = options
    
    def get_map_options(self):
        return self._options
    def set_map_options(self, options):
        self._options = options
    def del_map_options(self):
        del self._options
    map_options = property(get_map_options, set_map_options, del_map_options)

    def update_options(self, options):
        self._options.update(options)

class Polygon(object):
    def __init__(self, options):
        self._options

    def get_polygon_options(self):
        return self._options
    def set_polygon_options(self, options):
        self._options = options
    def del_polygon_options(self):
        del self._options
    polygon_options = property(get_polygon_options, set_polygon_options, del_polygon_options)

    def update_options(self, options):
        self._options.update(options)

class PolyLine(object):
    def __init__(self, options):
        self._options = options
    
    def get_polyline_options(self):
        return self._options
    def set_polyline_options(self, options):
        self._options = options
    def del_polyline_options(self):
        del self._options
    polyline_options = property(get_polyline_options, set_polyline_options, del_polyline_options)

    def update_options(self, options):
        self._options.update(options)

class Marker(object):
    def __init__(self, options):
        self._options

    def get_marker_options(self):
        return self._options
    def set_marker_options(self, options):
        self._options = options
    def del_marker_options(self):
        del self._options
    marker_options = property(get_marker_options, set_marker_options, del_marker_options)

    def update_options(self, options):
        self._options.update(options)
