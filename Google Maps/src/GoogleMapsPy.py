class Coordinate(object):
    def __init__(self, latitude, longitude):
        self.__latitude = latitude
        self.__longitude = longitude

    def latitude():
        def fget(self):
            return self.__latitude

        def fset(self, value):
            self.__latitude = value

        def fdel(self):
            del self.__latitude
        return locals()
    latitude = property(**latitude())

    def longitude():
        def fget(self):
            return self.__longitude

        def fset(self, value):
            self.__longitude = value

        def fdel(self):
            del self.__longitude
        return locals()
    longitude = property(**longitude())


class Polygon(object):
    # path is a list of coordinate objects
    def __init__(self, path):
        self.__path = path
        self.__fillColor = '#FFFFFF'
        self.__fillOpacity = 0.5
        self.__strokeColor = '#000000'
        self.__strokeWeight = 3
        self.__strokeOpacity = 1

    def path():
        def fget(self):
            return self.__path

        def fset(self, value):
            self.__path = value

        def fdel(self):
            del self.__path
        return locals()
    path = property(**path())

    def fillColor():
        def fget(self):
            return self.__fillColor

        def fset(self, value):
            self. __fillColor = value

        def fdel(self):
            del self.__fillColor
        return locals()
    fillColor = property(**fillColor())

    def fillOpacity():
        def fget(self):
            return self.__fillOpacity

        def fset(self, value):
            self.__fillOpacity = value

        def fdel(self):
            del self.__fillOpacity
        return locals()
    fillOpacity = property(**fillOpacity())

    def strokeColor():
        def fget(self):
            return self.__strokeColor

        def fset(self, value):
            self.__strokeColor = value

        def fdel(self):
            del self.__strokeColor
        return locals()
    strokeColor = property(**strokeColor())

    def strokeWeight():
        def fget(self):
            return self.__strokeWeight

        def fset(self, value):
            self.__strokeWeight = value

        def fdel(self):
            del self.__strokeWeight
        return locals()
    strokeWeight = property(**strokeWeight())

    def strokeOpacity():
        def fget(self):
            return self.__strokeOpacity

        def fset(self, value):
            self.__strokeOpacity = value

        def fdel(self):
            del self.__strokeOpacity
        return locals()
    strokeOpacity = property(**strokeOpacity())


class PolyLine(object):
    def __init__(self):
        self.__strokeColor = '#000000'
        self.__strokeOpacity = 1.0
        self.__strokeWeight = 3
        self.__editable = True

    def strokeColor():
        def fget(self):
            return self.__strokeColor

        def fset(self, value):
            self.__strokeColor = value

        def fdel(self):
            del self.__strokeColor
        return locals()
    strokeColor = property(**strokeColor())

    def strokeOpacity():
        def fget(self):
            return self.__strokeOpacity

        def fset(self, value):
            self.__strokeOpacity = value

        def fdel(self):
            del self.__strokeOpacity
        return locals()
    strokeOpacity = property(**strokeOpacity())

    def strokeWeight():
        def fget(self):
            return self.__strokeWeight

        def fset(self, value):
            self.__strokeWeight = value

        def fdel(self):
            del self.__strokeWeight
        return locals()
    strokeWeight = property(**strokeWeight())

    def editable():
        def fget(self):
            return self.__editable

        def fset(self, value):
            self.__editable = value

        def fdel(self):
            del self.__editable
        return locals()
    editable = property(**editable())


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

            function initialize() {
                var mapOptions = {
                    zoom: %i,
                    mapTypeId: google.maps.MapTypeId.%s,
                    center: new google.maps.LatLng(%d,%d)
                };
                map = new google.maps.Map(document.getElementById('map_canvas'),mapOptions);
        """ % (self.__zoom, self.__mapTypeId, self.__center.latitude,
               self.__center.longitude)

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
                """ % (i, i, polygon.fillColor, polygon.fillOpacity,
                       polygon.strokeColor, polygon.strokeOpacity, polygon.strokeWeight, i)
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
                infoWindow = new google.maps.InfoWindow();
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
            """ % (self.__polyLine.strokeColor, self.__polyLine.strokeWeight,
                   self.__polyLine.strokeOpacity, str(self.__polyLine.editable).lower())

            self.__jsCode += """
                var markerOptions = {
                    position: coordinates1[0]
                }
                var marker = new google.maps.Marker(markerOptions);
                marker.setMap(map);

                google.maps.event.addListener(map, 'click', addPoint);
                google.maps.event.addListener(poly, 'click', showCoordinate);
                $("#coordButton").click(function(event){
                  var data = poly.getPath().getArray();
                  var coordArray = $.map(data, function(coord){
                    return {
                              lat: coord.lat(),
                              lng: coord.lng()
                            }
                  });
                  console.log(poly.getPath().getArray());
                  $.post("http://localhost:5000",
                  {
                    "path": coordArray
                  });
                });

                var i = 1;
                $('#testButton').click(function(event) {
                    if(i < poly.getPath().getArray().length) {
                        console.log("coordinates " + i + " = [" + poly.getPath().getArray()[i].lat() + "," + poly.getPath().getArray()[i].lng() + "]");
                        marker.setPosition(poly.getPath().getArray()[i]);
                        i++;
                    }
                    else {
                        console.log("coordinates 0 = [" + poly.getPath().getArray()[0].lat() + "," + poly.getPath().getArray()[0].lng() + "]");
                        marker.setPosition(poly.getPath().getArray()[0]);
                        i = 1;
                    }
                });
            }

            function showCoordinate(event) {
                var message = "Longitude: " + event.latLng.lat() + "<br />";
                message += "Latitude: " + event.latLng.lng() + "<br />";
                infoWindow.setContent(message);
                infoWindow.setPosition(event.latLng);
                infoWindow.open(map);
            }

            function addPoint(event) {
                // All arrays are passed by reference in js
                var path = poly.getPath();
                path.push(event.latLng);
            }
            """

            return self.__jsCode

        return self.__jsCode + """
            }
            """

    def getHtml(self):
        self.__html = """
        <html>
            <head>
                <meta name="viewport" content="initial-scale=1.0, user-scalable=no"/>
                <meta charset="utf-8">
                <script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDUqZDJn8yWjIKJ4nUsHQGuEAvZHar41rs&sensor=false"></script>
                <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
                <script type="text/javascript">
                    %s
                </script>
            </head>
            <body onload="initialize()">
                <button type="button" id="coordButton">Send Coordinates</button>
                <button type="button" id="testButton">Something</button>
                <div id="map_canvas" style="width: 100%%; height: 100%%;"></div>
            </body>
        </html>
        """ % (self.__getJs())

        return self.__html
