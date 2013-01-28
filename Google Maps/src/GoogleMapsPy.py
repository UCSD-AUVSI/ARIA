from GoogleMapsObjects import Coordinate, Polygon, PolyLine

class GoogleMapsPy(object):
    # showPath - flag to allow lines to be drawn on map
    def __init__(self, center, zoom, typeId, path=None):
        self.__center = center
        self.__zoom = zoom
        self.__mapTypeId = typeId
        self.__polygonCount = 0
        self.__polygonList = []
        self.__polyLine = PolyLine()
        self.__showPath = True
        self.__path = path

    def createPolygon(self, polygon):
        self.__polygonList.append(polygon)
        self.__polygonCount += 1

    def createPolyLine(self, polyLine):
        self.__polyLine = polyLine

    # drawPath draws predefined path based on list of coordinates passed in
    def setPath(self, path):
        if not self.__showPath:
            self.__showPath = True
        self.__path = path

    # change the state of __showPath
    def togglePath(self, bool):
        self.__showPath = bool

    def __getJs(self):
        self.__jsCode = """
            var map;
            var poly;
            var infoWindow;
            var marker;
            var isContextMenuOpen;
            var isInfoWindowOpen;
            var currentPosition;
            var altitudeArray;
            var typeArray;
            var durArray;

            function initialize() {
                var mapCenter = new google.maps.LatLng(%d,%d);

                var mapOptions = {
                    zoom: %i,
                    mapTypeId: google.maps.MapTypeId.%s,
                    center: mapCenter,
                    disableDefaultUI: true
                };
                map = new google.maps.Map(document.getElementById('map_canvas'),mapOptions);

                altitudeArray = [];
                typeArray = [];
                durArray = [];

                currentPosition = mapCenter;

                var markerOptions = {
                    position: currentPosition
                };
                marker = new google.maps.Marker(markerOptions);
                marker.setMap(map);

                infoWindow = new google.maps.InfoWindow();
                isContextMenuOpen = false;
        """ % (self.__center.latitude, self.__center.longitude, self.__zoom, self.__mapTypeId)

        if self.__polygonCount > 0:
            i = 1
            for polygon in self.__polygonList:
                self.__jsCode += """
                var coordinates%i = [""" % (i)

                for coord in polygon.path:
                    self.__jsCode += """
                    new google.maps.LatLng(%d,%d),""" % (coord.latitude, coord.longitude)

                self.__jsCode += """
                ];
                """

                self.__jsCode += """
                var polygon%i = new google.maps.Polygon({
                    path: coordinates%i,
                    fillColor: '%s',
                    fillOpacity: %s,
                    strokeColor: '%s',
                    strokeOpacity: %s,
                    strokeWeight: %s
                });
                polygon%i.setMap(map);
                google.maps.event.addListener(polygon%i, 'rightclick', showContextMenu);
                """ % (i, i, polygon.fillColor, polygon.fillOpacity,
                       polygon.strokeColor, polygon.strokeOpacity, polygon.strokeWeight, i, i)
                i += 1


        if self.__showPath:
            if self.__path is not None:
                self.__jsCode += """
                var pathArray = ["""

                for coordinate in self.__path:
                    self.__jsCode += """
                    new google.maps.LatLng(%d,%d),""" % (coordinate.latitude, coordinate.longitude)

                self.__jsCode += """
                ];
                """

            self.__jsCode += """
                var polyOptions = {
            """

            if self.__path is not None:
                self.__jsCode += """
                    path: pathArray,
                """

            self.__jsCode += """
                    strokeColor: '%s',
                    strokeWeight: %s,
                    strokeOpacity: %s
                };
                poly = new google.maps.Polyline(polyOptions);
                poly.setEditable(%s);
                poly.setMap(map);

                // initialize altitude array if path is preset
                for(var i = 0; i < poly.getPath().getLength(); i++) {
                    altitudeArray.push(i)       // TODO: properly set altitude
                }
                // initialize type array if path is preset
                for(var i = 0; i < poly.getPath().getLength(); i++) {
                    if(i == 0)
                        typeArray.push("Takeoff");
                    else if(i == (poly.getPath().getLength() - 1))
                        typeArray.push("Land");
                    else
                        typeArray.push("Waypoint");
                }
                // initialize duration array if path is preset
                for(var i = 0; i < poly.getPath().getLength(); i++) {
                    durArray.push(0);
                }

                // TODO: binder may not be needed
                poly.binder = new MVCArrayBinder(poly.getPath());
            """ % (self.__polyLine.strokeColor, self.__polyLine.strokeWeight,
                   self.__polyLine.strokeOpacity, str(self.__polyLine.editable).lower())

        self.__jsCode += """
                // Makes sure altitdue array and path array are in sync
                google.maps.event.addListener(poly.getPath(), 'insert_at', function(index) {
                    if(index == 0) {
                        altitudeArray.push(index);      // TODO: properly set altitude
                        durArray.push(0);
                        typeArray.push("Takeoff");  // set to Takeoff if first element
                    }
                    else if(index == (poly.getPath().getLength() - 1)) {
                        altitudeArray.push(index);      // TODO: properly set altitude
                        durArray.push(0);
                        typeArray.push("Land"); // set to Land if last element
                        // set 2nd to last element to Waypoint
                        if((typeArray.length-2) > 0)
                            if(typeArray[typeArray.length-2] == "Land")
                                typeArray[typeArray.length-2] = "Waypoint";
                    }
                    else {
                        var aTmp = [];
                        var tTmp = [];
                        var dTmp = [];

                        // Altitude Array
                        for(var i = 0; i < index; i++)
                            aTmp[i] = altitudeArray[i];
                        aTmp[index] = index;        // TODO: properly set altitude
                        for(var i = index+1; i <= altitudeArray.length; i++)
                            aTmp[i] = altitudeArray[i-1];
                        altitudeArray = aTmp;

                        // Type Array
                        for(var i = 0; i < index; i++)
                            tTmp[i] = typeArray[i];
                        tTmp[index] = "Waypoint";
                        for(var i = index+1; i <= typeArray.length; i++)
                            tTmp[i] = typeArray[i-1];
                        typeArray = tTmp;

                        // Duration Array
                        for(var i = 0; i < index; i++)
                            dTmp[i] = durArray[i];
                        dTmp[index] = 0;
                        for(var i = index+1; i <= durArray.length; i++)
                            dTmp[i] = durArray[i-1];
                        durArray = tTmp;
                    }
                });
                /*
                ** NOTE: google maps api decreases length of mvc array before 'remove_at' event gets called
                */
                google.maps.event.addListener(poly.getPath(), 'remove_at', function(index) {
                    if(index == 0) {
                        altitudeArray.shift();  // remove first element
                        durArray.shift();
                        typeArray.shift();  // remove first element
                        typeArray[0] = "Takeoff";   // set first element to Takeoff
                    }
                    else if(index == poly.getPath().getLength()) {
                        altitudeArray.pop(); // remove last element
                        durArray.pop();
                        typeArray.pop();    // remove last element
                        typeArray[typeArray.length-1] = "Land"; // set last element to Land
                    }
                    else {
                        var aTmp = [];
                        var tTmp = [];
                        var dTmp = [];

                        // Altitude Array
                        for(var i = 0; i < index; i++)
                            aTmp[i] = altitudeArray[i];
                        for(var i = index+1; i < altitudeArray.length; i++)
                            aTmp[i-1] = altitudeArray[i];
                        altitudeArray = aTmp;

                        // Type Array
                        for(var i = 0; i < index; i++)
                            tTmp[i] = typeArray[i];
                        for(var i = index+1; i < typeArray.length; i++)
                            tTmp[i-1] = typeArray[i];
                        typeArray = tTmp;

                        // Duration Array
                        for(var i = 0; i < index; i++)
                            dTmp[i] = durArray[i];
                        for(var i = index+1; i < durArray.length; i++)
                            dTmp[i-1] = durArray[i];
                        durArray = dTmp;
                    }
                });
                google.maps.event.addListener(poly.getPath(), 'set_at', function(event) {
                    /*
                    ** THIS EVENT IS CALLED WHEN THE UNDO BUTTON IS PRESSED
                    ** PLACE HOLDER
                    ** CODE HERE
                    */
                });

                google.maps.event.addListener(map, 'click', addPoint);
                google.maps.event.addListener(map, 'rightclick', showContextMenu);
                google.maps.event.addListener(map, 'mousemove', statusBarCoordinate);
                google.maps.event.addListener(poly, 'click', showCoordinate);
                google.maps.event.addListener(poly, 'rightclick', showContextMenu);
                google.maps.event.addListener(marker, 'rightclick', showContextMenu);
            } // end of initialize()

            function showCoordinate(event) {
                var index = poly.getPath().getArray().indexOf(event.latLng);
                var message = "<label>Longitude:</label><input id=\\"latBox\\" class=\\"inputBox\\" type=\\"text\\" value=\\"" + event.latLng.lat() + "\\"/><br />";
                message += "<label>Latitude:</label><input id=\\"lngBox\\" class=\\"inputBox\\" type=\\"text\\" value=\\"" + event.latLng.lng() + "\\"/><br />";
                message += "<label>Altitude:</label><input id=\\"altBox\\" class=\\"inputBox\\" type=\\"text\\" value=\\"" + altitudeArray[index] + "\\"/><br />";

                if(typeArray[index] == "Takeoff")
                    message = message + "<label>Type:</label>" + 
                            "<select>" + 
                            "<option value=\\"takeoff\\" selected=\\"selected\\">Takeoff</option>" + 
                            "<option value=\\"waypoint\\">Waypoint</option>" + 
                            "<option value=\\"loiter\\">Loiter</option>" + 
                            "<option value=\\"land\\">Land</option></select><br />";
                else if(typeArray[index] == "Waypoint")
                    message = message + "<label>Type:</label>" + 
                            "<select>" + 
                            "<option value=\\"takeoff\\">Takeoff</option>" + 
                            "<option value=\\"waypoint\\" selected=\\"selected\\">Waypoint</option>" + 
                            "<option value=\\"loiter\\">Loiter</option>" + 
                            "<option value=\\"land\\">Land</option></select><br />";
                else if(typeArray[index] == "Loiter")
                    message = message + "<label>Type:</label>" + 
                            "<select>" + 
                            "<option value=\\"takeoff\\">Takeoff</option>" + 
                            "<option value=\\"waypoint\\">Waypoint</option>" + 
                            "<option value=\\"loiter\\" selected=\\"selected\\">Loiter</option>" + 
                            "<option value=\\"land\\">Land</option></select><br />" + 
                            "<label>Duration:</label>" +
                            "<input id=\\"durBox\\" class=\\"inputBox\\" type=\\"text\\" value=\\"" + durArray[index] + "\\" /><br />";
                else if(typeArray[index] == "Land")
                    message = message + "<label>Type:</label>" + 
                            "<select>" + 
                            "<option value=\\"takeoff\\">Takeoff</option>" + 
                            "<option value=\\"waypoint\\">Waypoint</option>" + 
                            "<option value=\\"loiter\\">Loiter</option>" + 
                            "<option value=\\"land\\" selected=\\"selected\\">Land</option></select><br />";

                infoWindow.setContent(message);
                infoWindow.setPosition(event.latLng);
                infoWindow.open(map);

                $('.inputBox').bind('keypress', function(event) {
                    // enter key is pressed
                    if(event.keyCode == 13) {
                        var newPos = new google.maps.LatLng($('#latBox').val(), $('#lngBox').val())
                        poly.getPath().setAt(index, newPos);
                        altitudeArray[index] = $('#altBox').val();
                        if(typeArray[index] == "Loiter")
                            durArray[index] = $('#durBox').val();
                        infoWindow.setPosition(newPos);
                        alert("values updated");
                    }
                });

                $('select').change(function() {
                    var optionSelected = "";
                    $('select option:selected').each(function() {
                        optionSelected += $(this).text();
                    });
                    if(optionSelected == "Loiter") {
                        infoWindow.close();
                        message = "<label>Longitude:</label>" + 
                                "<input id=\\"latBox\\" class=\\"inputBox\\" type=\\"text\\" value=\\"" + event.latLng.lat() + "\\"/><br />";
                        message = message + "<label>Latitude:</label>" + 
                                "<input id=\\"lngBox\\" class=\\"inputBox\\" type=\\"text\\" value=\\"" + event.latLng.lng() + "\\"/><br />";
                        message = message + "<label>Altitude:</label>" + 
                                "<input id=\\"altBox\\" class=\\"inputBox\\" type=\\"text\\" value=\\"" + altitudeArray[index] + "\\"/><br />";
                        message = message + "<label>Type:</label>" + 
                                "<select>" + 
                                "<option value=\\"takeoff\\">Takeoff</option>" + 
                                "<option value=\\"waypoint\\">Waypoint</option>" + 
                                "<option value=\\"loiter\\" selected=\\"selected\\">Loiter</option>" + 
                                "<option value=\\"land\\">Land</option></select><br />" + 
                                "<label>Duration:</label>" +
                                "<input id=\\"durBox\\" class=\\"inputBox\\" type=\\"text\\" value=\\"" + durArray[index] + "\\" /><br />";
                        infoWindow.setContent(message);
                        infoWindow.open(map);
                        $('.inputBox').bind('keypress', function(event) {
                            // enter key is pressed
                            if(event.keyCode == 13) {
                                var newPos = new google.maps.LatLng($('#latBox').val(), $('#lngBox').val())
                                poly.getPath().setAt(index, newPos);
                                altitudeArray[index] = $('#altBox').val();
                                if(typeArray[index] == "Loiter")
                                    durArray[index] = $('#durBox').val();
                                infoWindow.setPosition(newPos);
                                alert("values updated");
                            }
                        });
                    }
                    typeArray[index] = optionSelected;
                    durArray[index] = 0;
                });

                isInfoWindowOpen = true;
            }

            function addPoint(event) {
                if(isContextMenuOpen) {
                    $('.contextmenu').remove();
                    isContextMenuOpen = false;
                    return;
                }
                if(isInfoWindowOpen) {
                    infoWindow.close();
                    isInfoWindowOpen = false;
                    return;
                }
                // All arrays are passed by reference in js
                var path = poly.getPath();
                path.push(event.latLng);
            }

            function statusBarCoordinate(event) {
                $('span.message').html(event.latLng.lat() + ", " + event.latLng.lng());
            }

            function showContextMenu(event) {
                $('.contextmenu').remove(); // remove existing menu when right clicked again
                var contextmenu;
                var position = event.latLng;
                contextmenu = document.createElement('div');
                contextmenu.className = 'contextmenu';
                contextmenu.innerHTML = "<button type=\\"button\\" id=\\"item1\\" class=\\"btn\\">Send Coordinates</button>";
                contextmenu.innerHTML += "<button type=\\"button\\" id=\\"item2\\" class=\\"btn\\">Circle Here</button>";
                contextmenu.innerHTML += "<button type=\\"button\\" id=\\"item3\\" class=\\"btn\\">Refresh</button>";
                contextmenu.innerHTML += "<button type=\\"button\\" id=\\"item4\\" class=\\"btn\\">Remove point</button>";
                contextmenu.innerHTML += "<button type=\\"button\\" id=\\"item5\\" class=\\"btn\\">Loiter Here</button>";
                contextmenu.innerHTML += "<button type=\\"button\\" id=\\"item6\\" class=\\"btn\\">Clear all waypoints</button>";

                $(map.getDiv()).append(contextmenu);

                var clickedPosition = latLngToXY(position);
                $('.contextmenu').css('left', clickedPosition.x);
                $('.contextmenu').css('top', clickedPosition.y);

                contextmenu.style.visibility = "visible";

                isContextMenuOpen = true;

                // add event listeners
                // SEND COORDINATES
                $('#item1').click(function() {
                    var coordArray = [];
                    for(var i = 0; i < poly.getPath().getLength(); i++) {
                        coordArray.push({
                            lat: poly.getPath().getAt(i).lat(),
                            lng: poly.getPath().getAt(i).lng(),
                            alt: altitudeArray[i],
                            type: typeArray[i],
                            dur: durArray[i]
                        });
                    }
                    $.post("http://localhost:5000",
                    {
                        "data": coordArray
                    });
                    contextmenu.style.visibility = "hidden";
                }); // end item1 event handler

                // CIRCLE HERE
                $('#item2').click(function() {
                    var scale = 1.5
                    var circlePathCoord = [
                        // current position
                        new google.maps.LatLng(currentPosition.lat(), currentPosition.lng()),

                        // top right corner
                        new google.maps.LatLng(position.lat()+scale, position.lng()+scale),

                        // top left corner
                        new google.maps.LatLng(position.lat()+scale, position.lng()-scale),

                        // middle left corner
                        new google.maps.LatLng(position.lat(), position.lng()-scale),

                        // bottom left corner
                        new google.maps.LatLng(position.lat()-scale, position.lng()-scale),

                        // bottom right corner
                        new google.maps.LatLng(position.lat()-scale, position.lng()+scale),

                        // middle right corner
                        new google.maps.LatLng(position.lat(), position.lng()+scale),

                        // connect line to first point
                        new google.maps.LatLng(position.lat()+scale, position.lng()+scale)
                    ];
                    poly.setPath(circlePathCoord);
                    currentPosition = circlePathCoord[1];
                    marker.setPosition(circlePathCoord[1]);

                    contextmenu.style.visibility = "hidden";
                }); // end #item2 event handler

                // REFRESH PAGE
                $('#item3').click(function() {
                    location.reload();
                }); // end #item3 event handler

                // DELETE POINT
                $('#item4').click(function() {
                    var path = poly.getPath();
                    var index = path.getArray().indexOf(position);
                    if(index != -1)
                        path.removeAt(index);
                    else
                        alert('point not in path');
                    contextmenu.style.visibility = "hidden";
                }); // end of #item4 event handler

                // LOITER HERE
                $('#item5').click(function() {
                    if(position.equals(currentPosition)) {
                        marker.setPosition(position);
                        currentPosition = position;
                    }
                    else {
                        var tmpPath = [
                            new google.maps.LatLng(currentPosition.lat(), currentPosition.lng()),
                            new google.maps.LatLng(position.lat(), position.lng())
                        ];
                        poly.setPath(tmpPath);
                        marker.setPosition(position);
                        currentPosition = position;
                    }
                    contextmenu.style.visibility = "hidden";
                }); //  end of #item5 event handler
				
                // CLEAR ALL WAYPOINTS
                $('#item6').click(function() {
                    poly.getPath().clear();
                    contextmenu.style.visibility = "hidden";
                }); // end of #item6 event handler

                contextmenu.style.visibility = "visible";
            }

            function latLngToXY(latlng) {
                var scale = Math.pow(2, map.getZoom());
                var nwLatLng = new google.maps.LatLng(
                    map.getBounds().getNorthEast().lat(),
                    map.getBounds().getSouthWest().lng()
                );
                var nwPoint = map.getProjection().fromLatLngToPoint(nwLatLng);
                var clickPoint = map.getProjection().fromLatLngToPoint(latlng);
                var offset = new google.maps.Point(
                    (clickPoint.x - nwPoint.x) * scale,
                    (clickPoint.y - nwPoint.y) * scale
                );

                return offset;
            }

            // TODO: binder may not be needed
            function MVCArrayBinder(pathArray) {
                this.array_ = pathArray;
            }
            MVCArrayBinder.prototype = new google.maps.MVCObject();
            MVCArrayBinder.prototype.get = function(key) {
                if(!isNaN(parseInt(key)))
                    return this.array_.getAt(parseInt(key));
                else
                    return this.array_.get(key);
            }
            MVCArrayBinder.prototype.set = function(key, val) {
                if(!isNan(parseInt(key)))
                    this.array_.setAt(parseInt(key), val);
                else
                    this.array_.set(key, val);
            }
            """

        return self.__jsCode

    def getHtml(self):
        self.__html = """
<!DOCTYPE html>
<html>
    <head>
        <meta name="viewport" content="initial-scale=1.0, user-scalable=no"/>
        <meta charset="utf-8">
        <style type="text/css">
            html { height: 100%% }
            body { height: 100%%; margin: 0; padding: 0 }
            .status_bar {
                position: absolute;
                bottom: 0;
                height: 18px;
                width: 100%%;
                background: #FAFAFA;
                border-top: 1px solid #F0F0F0;
                z-index: 10;
            }
            .status_bar span.message { float: right; }
            .contextmenu {
                visibility: hidden;
                background: #FEFEFE;
                border: 2px solid #FAFAFA;
                z-index: 10;
                position: relative;
                width: 140px
            }
            .btn {
                width: 100%%;
                height: 100%%;
                border: none;
                background: #FEFEFE;
                outline: 0;
                text-align: left;
            }
            .btn:hover { background: #F0F0F0; }
            #map_canvas { height: 100%% }
        </style>
        <script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDUqZDJn8yWjIKJ4nUsHQGuEAvZHar41rs&sensor=false"></script>
        <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
        <script type="text/javascript">%s</script>
    </head>
    <body onload="initialize()">
        <div id="map_canvas" style="width: 100%%; height: 100%%;"></div>
        <div class="status_bar">
            <span class="message"></span>
        </div>
    </body>
</html>
        """ % (self.__getJs())

        return self.__html
