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
    
    def write(self, html_file="pygmap.html", js_file="pygmap.js"):
        """
        writes javascript and html to files
        file names can be passed in as parameters
        """
        cwd = os.curdir
        with open(cwd+"/static/"+html_file, "w") as file:
            file.write(self._get_html())
        with open(cwd+"/static/"+js_file, "w") as file:
            file.write(self._get_js())

    def toggle_display_path(self, switch):
        """
        turns path on/off using SHOW_PATH/HIDE_PATH constants
        """
        self._display_polyline = switch

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
        self._js += self._setup_marker()

        self._js += self._setup_add_point_event()
        self._js += self._setup_insert_event()
        self._js += self._setup_delete_event()
        self._js += self._setup_show_coordinate_event()

        self._js += self._end_initialize()

        self._js += self._setup_context_menu_event()

        return self._js

    def _start_initialize(self):
        js = """
            function initialize() {
                window.durationArray = []
                window.altitudeArray = []
                window.typeArray = []
                window.infowindow = new google.maps.InfoWindow();
        """
        return js

    def _end_initialize(self):
        js = """
            google.maps.event.addListener(window.map, "rightclick", showContextMenu);
            google.maps.event.addListener(window.path, "rightclick", showContextMenu);
            } // end initialize()
        """
        return js

    def _setup_map(self):
        js = """
            var mapOptions = {
        """

        for key,value in self._map.options.items():
            
            if key == "mapTypeId":
                js += """
                    %s : google.maps.MapTypeId.%s,
                """ % (key, value)

            elif type(value) is Coordinate:
                js += """
                    %s : new google.maps.LatLng(%d,%d),
                """ % (key, value.longitude, value.latitude)

            elif type(value) is str:
                js += """
                    %s : "%s",
                """ % (key, value)

            else:
                js += """
                    %s : %s,
                """ % (key, value)

        js += """
            };  // end mapOptions
            window.map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
        """
        return js

    def _setup_path(self):
        js = ""
        if self._display_polyline:
            if self._polyline is not None:
                js = """
                    var pathArray = [
                """

                for point in self._polyline.options["path"]:
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
                strokeColor: "#000000",
                strokeWeight: 2,
                strokeOpacity: 1,
                editable: true,
                map: window.map
                }; // end pathOptions
                window.path = new google.maps.Polyline(pathOptions);
            """

            if self._polyline is not None:
                for point in self._polyline.options["path"]:
                    js += """
                        altitudeArray.push(%i);
                        typeArray.push("%s");
                        durationArray.push(%i);
                    """ % (point.altitude, point.ctype, point.duration)
            return js
        else:
            pass

    def _setup_marker(self):
        js = """
            var markerOptions = {
        """

        for key,value in self._marker.options.items():
            if key is "position":
                js += """
                    %s : new google.maps.LatLng(%d,%d),
                """ % (key, value.latitude, value.longitude)
                continue

            if type(value) is str:
                js += """
                    %s : '%s',
                """ % (key, value)
                continue

            js += """
                %s : %s,
            """ (key, value)

        js += """
            }; // end markerOptions
            window.marker = new google.maps.Marker(markerOptions);
            window.marker.setMap(window.map);
        """
        return js

    def _setup_show_coordinate_event(self):
        js = """
            google.maps.event.addListener(window.path, "click", function(event) {
                    var index = window.path.getPath().getArray().indexOf(event.latLng);

                    var message = "";
                    message += "<div class=\\"infodiv\\"><label class=\\"name\\">Latitude:</label><input id=\\"latbox\\" class=\\"inputbox\\" type=\\"text\\" value=\\"" + event.latLng.lat() + "\\"/></div><br />";
                    message += "<div class=\\"infodiv\\"><label class=\\"name\\">Longitude:</label><input id=\\"lngbox\\" class=\\"inputbox\\" type=\\"text\\" value=\\"" + event.latLng.lng() + "\\"/></div><br />";
                    message += "<div class=\\"infodiv\\"><label class=\\"name\\">Altitude:</label><input id=\\"altbox\\" class=\\"inputbox\\" type=\\"text\\" value=\\"" + 0 + "\\"/></div><br />";
                    if(window.typeArray[index] == "Takeoff") {
                        message += "<div class=\\"infodiv\\"><label class=\\"name\\">Type:</label><select class=\\"inputbox\\" name=\\"types\\"><option value=\\"takeoff\\" selected=\\"selected\\">Takeoff</option><option value=\\"waypoint\\">Waypoint</option><option value=\\"loiter\\">Loiter</option><option value=\\"land\\">Land</option></select></div><br />";
                    }
                    else if(window.typeArray[index] == "Waypoint") {
                        message += "<div class=\\"infodiv\\"><label class=\\"name\\">Type:</label><select class=\\"inputbox\\" name=\\"types\\"><option value=\\"takeoff\\">Takeoff</option><option value=\\"waypoint\\" selected=\\"selected\\">Waypoint</option><option value=\\"loiter\\">Loiter</option><option value=\\"land\\">Land</option></select></div><br />";
                    }
                    else if(window.typeArray[index] == "Loiter") {
                        message += "<div class=\\"infodiv\\"><label class=\\"name\\">Type:</label><select class=\\"inputbox\\" name=\\"types\\"><option value=\\"takeoff\\" >Takeoff</option><option value=\\"waypoint\\">Waypoint</option><option value=\\"loiter\\" selected=\\"selected\\">Loiter</option><option value=\\"land\\">Land</option></select></div><br />";
                        message += "<div class=\\"infodiv\\"><label class=\\"name\\">Duration:</label><input id=\\"durbox\\" class=\\"inputbox\\" type=\\"text\\" value=\\"" + window.durationArray[index] + "\\" /><br />";
                    }
                    else {
                        message += "<div class=\\"infodiv\\"><label class=\\"name\\">Type:</label><select class=\\"inputbox\\" name=\\"types\\"><option value=\\"takeoff\\" >Takeoff</option><option value=\\"waypoint\\">Waypoint</option><option value=\\"loiter\\">Loiter</option><option value=\\"land\\" selected=\\"selected\\">Land</option></select></div><br />";
                    }
                    
                    window.infowindow.setContent(message);
                    window.infowindow.setPosition(event.latLng);
                    window.infowindow.open(map);
                    window.isInfoWindowOpen = true;

                    $(".infodiv > .inputbox").keyup(function(event) {
                        // enter key is pressed
                        if(event.keyCode == 13) {
                            var newpos = new google.maps.LatLng($("#latbox").val(), $("#lngbox").val());
                            window.path.getPath().setAt(index, newpos);
                            window.altitudeArray[index] = $("#altbox").val();
                            if(window.typeArray[index] == "Loiter")
                                window.durationArray[index] = $("#durbox").val();
                            window.infowindow.setPosition(newpos);
                            alert("values updatd");
                        }
                    }); //  inputbox event handler

                    $(".infodiv > select").change(function() {
                        var optionSelected = "";
                        $('select option:selected').each(function() {
                            optionSelected += $(this).text();
                        });
                        if(optionSelected == "Loiter") {
                            window.infowindow.close();

                            var message = "";
                            message += "<div class=\\"infodiv\\"><label class=\\"name\\">Latitude:</label><input id=\\"latbox\\" class=\\"inputbox\\" type=\\"text\\" value=\\"" + event.latLng.lat() + "\\"/></div><br />";
                            message += "<div class=\\"infodiv\\"><label class=\\"name\\">Longitude:</label><input id=\\"lngbox\\" class=\\"inputbox\\" type=\\"text\\" value=\\"" + event.latLng.lng() + "\\"/></div><br />";
                            message += "<div class=\\"infodiv\\"><label class=\\"name\\">Altitude:</label><input id=\\"altbox\\" class=\\"inputbox\\" type=\\"text\\" value=\\"" + 0 + "\\"/></div><br />";
                            message += "<div class=\\"infodiv\\"><label class=\\"name\\">Type:</label><select class=\\"inputbox\\" name=\\"types\\"><option value=\\"takeoff\\" >Takeoff</option><option value=\\"waypoint\\">Waypoint</option><option value=\\"loiter\\" selected=\\"selected\\">Loiter</option><option value=\\"land\\">Land</option></select></div><br />";
                            message += "<div class=\\"infodiv\\"><label class=\\"name\\">Duration:</label><input id=\\"durbox\\" class=\\"inputbox\\" type=\\"text\\" value=\\"" + window.durationArray[index] + "\\" /><br />";

                            window.infowindow.setContent(message);
                            window.infowindow.open(window.map);

                            $(".infodiv > .inputbox").keyup(function(event) {
                                // enter key is pressed
                                if(event.keyCode == 13) {
                                    var newpos = new google.maps.LatLng($("#latbox").val(), $("#lngbox").val());
                                    window.path.getPath().setAt(index, newpos);
                                    window.altitudeArray[index] = $("#altbox").val();
                                    if(window.typeArray[index] == "Loiter")
                                        window.durationArray[index] = $("#durbox").val();
                                    window.infowindow.setPosition(newpos);
                                    alert("values updatd");
                                }
                            }); // end inputbox event handler
                        } // end select box event handler

                        window.typeArray[index] = optionSelected;
                        window.durationArray[index] = 0;
                    });
            }); // end show coordinate event listener
        """
        return js

    def _setup_add_point_event(self):
        js = """
            google.maps.event.addListener(window.map, "click", function(event) {
                if(window.isContextMenuOpen) {
                    $(".contextmenu").remove();
                    window.isContextMenuOpen = false;
                    return;
                }
                if(window.isInfoWindowOpen) {
                    window.infowindow.close();
                    window.isInfoWindowOpen = false;
                    return;
                }
                window.path.getPath().push(event.latLng);                
            });
               
        """

        return js

    def _setup_insert_event(self):
        js = """
            google.maps.event.addListener(window.path.getPath(), "insert_at", function(index) {
                // insert at beginning of path
                if(index == 0) {
                    window.altitudeArray.push(index);   // TODO: properly set altitude
                    window.typeArray.push("Takeoff");
                    window.durationArray.push(0);
                }
                // insert at end of path
                else if(index == (window.path.getPath().getLength() - 1)) {
                    window.altitudeArray.push(index);   // TODO: properly set altitude
                    window.typeArray.push("Land");
                    window.durationArray.push(0);
                }
                // insert at middle of path
                else {
                    var atmp = [];
                    var ttmp = [];
                    var dtmp = [];

                    // Altitude array
                    for(var i = 0; i < index; i++)
                        atmp[i] = window.altitudeArray[i];
                    atmp[index] = index;                // TODO: properly set altitude
                    for(var i = index+1; i <= window.altitudeArray.length; i++)
                        atmp[i] = window.altitudeArray[i-1];
                    window.altitudeArray = atmp;

                    // Type array
                    for(var i = 0; i < index; i++)
                        ttmp[i] = window.typeArray[i];
                    ttmp[index] = "Waypoint";
                    for(var i = index+1; i <= window.typeArray.length; i++)
                        ttmp[i] = window.typeArray[i-1];
                    window.typeArray = ttmp;

                    // Duratino array
                    for(var i = 0; i < index; i++)
                        dtmp[i] = window.durationArray[i];
                    dtmp[index] = 0;
                    for(var i = index+1; i <= window.durationArray.length; i++)
                        dtmp[i] = window.durationArray[i-1];
                    window.durationArray = dtmp;
                }
            });
        """
        return js

    def _setup_delete_event(self):
        js = """
            /*
            * NOTE: google maps api decreases length of mvc array beore "remove_at" event gets called
            */
            google.maps.event.addListener(window.path.getPath(), "remove_at", function(index) {
                // remove first waypoint in path
                if(index == 0) {
                    window.altitudeArray.shift();
                    window.durationArray.shift();
                    window.typeArray.shift();
                }
                // remove last waypoint in path
                else if(index == window.path.getPath().getLength()) {
                    window.altitudeArray.pop();
                    window.durationArray.pop();
                    window.typeArray.pop();
                }
                // remove waypoint from middle of path
                else {
                    var atmp = [];
                    var ttmp = [];
                    var dtmp = [];

                    // Altitude array
                    for(var i = 0; i < index; i++)
                        atmp[i] = window.altitudeArray[i];
                    for(var i = index+1; i < window.altitudeArray.length; i++)
                        atmp[i-1] = window.altitudeArray[i];
                    window.altitudeArray = atmp;

                    // Type array
                    for(var i = 0; i < index; i++)
                        ttmp[i] = window.durationArray[i];
                    for(var i = index+1; i < window.typeArray.length; i++)
                        ttmp[i-1] = window.durationArray[i];
                    window.typeArray = ttmp;

                    // Duration array
                    for(var i = 0; i < index; i++)
                        dtmp[i] = window.durationArray[i];
                    for(var i = index+1; i < window.durationArray.length; i++)
                        dtmp[i-1] = window.durationArray[i];
                    window.durationArray = dtmp;
                }
            });
        """
        return js

    def _setup_context_menu_event(self):
        js = """
            function showContextMenu(event) {
                // first remove existing context menu
                $(".contextmenu").remove();

                var contextmenu;
                var position = event.latLng;
                contextmenu = document.createElement("div");
                contextmenu.className = "contextmenu";
                contextmenu.innerHTML = "<button type=\\"button\\" id=\\"sendCoord\\" class=\\"btn\\">Send Coordinates</button>";
                contextmenu.innerHTML += "<button type=\\"button\\" id=\\"refresh\\" class=\\"btn\\">Refresh</button>";
                contextmenu.innerHTML += "<button type=\\"button\\" id=\\"delPoint\\" class=\\"btn\\">Delete Waypoint</button>";
                contextmenu.innerHTML += "<button type=\\"button\\" id=\\"delAllPoints\\" class=\\"btn\\">Delete All Waypoints</button>";
                $(window.map.getDiv()).append(contextmenu);

                var clickedPosition = latlngToXY(position);
                $(".contextmenu").css("left", clickedPosition.x);
                $(".contextmenu").css("top", clickedPosition.y);

                contextmenu.style.visibility = "visible";

                window.isContextMenuOpen = true;

                $("#sendCoord").click(sendCoordinates);
                $("#refresh").click(refresh);
                $("#delPoint").click({param1: position},deletePoint);
                $("#delAllPoints").click(deleteAllPoints);

                //TODO: is this necessary?
                //contextmenu.style.visibility = "visible";
            } // end showContext menu()

            function sendCoordinates() {
               // var coordArray = [];
               // for(var i = 0; i  < window.path.getPath().getLength(); i++) {
               //     coordArray.push({
               //         latitude: window.path.getPath().getAt(i).lat(),
               //         longitude: window.path.getPath().getAt(i).lng(),
               //         altitude: altitudeArray[i],
               //         type: typeArray[i],
               //         duration: durationArray[i]
               //     });
               // }
               // $.post("http://localhost:5000",
               // {
               //     "data" : coordArray
               // });
               // $(".contextmenu").remove();
            } // end sendCoordinates()

            function refresh() {
                location.reload();
            } // end refresh()

            function deletePoint(event) {
                var position = event.data.param1;
                var index = window.path.getPath().getArray().indexOf(position);
                if(index != -1)
                    window.path.getPath().removeAt(index);
                else
                    alert("point not in path");
                $(".contextmenu").remove();
            } // end deletePoints()

            function deleteAllPoints() {
                window.path.getPath().clear();
                window.altitudeArray = [];
                window.typeArray = [];
                window.durationArray = [];
                $(".contextmenu").remove();
            } // end deleteAllPoints()

            function latlngToXY(latlng) {
                var scale = Math.pow(2, window.map.getZoom());
                var nwlatlng = new google.maps.LatLng(
                    window.map.getBounds().getNorthEast().lat(),
                    window.map.getBounds().getSouthWest().lng()
                );
                var nwpoint = window.map.getProjection().fromLatLngToPoint(nwlatlng);
                var clickpoint = window.map.getProjection().fromLatLngToPoint(latlng);
                var offset = new google.maps.Point(
                    (clickpoint.x - nwpoint.x) * scale,
                    (clickpoint.y - nwpoint.y) * scale
                );
                
                return offset;
            } // end latlngToXY()
        """
        return js

    #----------------------------------------------------------SET UP HTML---------

    def _get_html(self):
        self._html = """
        <!DOCTYPE html>
        <html>
            <head>
                <meta name="viewport" content="initial-scale=1.0, user-scalable=no"/>
                <meta charset="utf-8">
                <style text="text/css">
                    html {height: 100%%;}
                    body {height: 100%%; margin: 0, padding: 0}
                    #map_canvas {height: 100%%}
                    .contextmenu {
                        visibility: hidden;
                        background: #FEFEFE;
                        border: 2px solid #FAFAFA;
                        z-index: 10;
                        position: relative;
                        width: 180px;
                    }
                    .btn {
                        width: 100%%;
                        height: 100%%;
                        border: none;
                        background: #FEFEFE;
                        outline: 0;
                        text-align: left;
                    }
                    .btn:hover {
                        background: #F0F0F0;
                    }
                    .infodiv {
                        height: 10px;
                        margin: 2px 0;
                    }
                    .name {
                        float: left;
                        text-align: left;
                        margin: 4px 0;
                    }
                    .inputbox {
                        float: right;
                        margin: 1px 0 1px 3px;
                        width: 200px;
                    }
                    select.inputbox {
                        width: 206px;
                    }
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

Coordinate = collections.namedtuple("Coordinate", "latitude longitude altitude ctype duration")
Map = collections.namedtuple("Map", "options")
Marker = collections.namedtuple("Marker", "options")
Polyline = collections.namedtuple("Polyline", "options")

#class Map(object):
    
    #ROADMAP = "ROADMAP"
    #HYBRID = "HYBRID"
    #SATELLITE = "SATELLITE"
    #TERRAIN = "TERRAIN"

    #def __init__(self,options):
        #self._options = options
    
    #def get_map_options(self):
        #return self._options
    #def set_map_options(self, options):
        #self._options = options
    #def del_map_options(self):
        #del self._options
    #map_options = property(get_map_options, set_map_options, del_map_options)

    #def update_options(self, options):
        #self._options.update(options)

#class Polygon(object):
    #def __init__(self, options):
        #self._options

    #def get_polygon_options(self):
        #return self._options
    #def set_polygon_options(self, options):
        #self._options = options
    #def del_polygon_options(self):
        #del self._options
    #polygon_options = property(get_polygon_options, set_polygon_options, del_polygon_options)

    #def update_options(self, options):
        #self._options.update(options)

#class PolyLine(object):
    #def __init__(self, options):
        #self._options = options
    
    #def get_polyline_options(self):
        #return self._options
    #def set_polyline_options(self, options):
        #self._options = options
    #def del_polyline_options(self):
        #del self._options
    #polyline_options = property(get_polyline_options, set_polyline_options, del_polyline_options)

    #def update_options(self, options):
        #self._options.update(options)

#class Marker(object):
    #def __init__(self, options):
        #self._options

    #def get_marker_options(self):
        #return self._options
    #def set_marker_options(self, options):
        #self._options = options
    #def del_marker_options(self):
        #del self._options
    #marker_options = property(get_marker_options, set_marker_options, del_marker_options)

    #def update_options(self, options):
        #self._options.update(options)
