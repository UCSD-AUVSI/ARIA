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
            var currentPosition;

            function initialize() {
                var mapCenter = new google.maps.LatLng(%d,%d);

                var mapOptions = {
                    zoom: %i,
                    mapTypeId: google.maps.MapTypeId.%s,
                    center: mapCenter,
                    disableDefaultUI: true
                };
                map = new google.maps.Map(document.getElementById('map_canvas'),mapOptions);

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
            """ % (self.__polyLine.strokeColor, self.__polyLine.strokeWeight,
                   self.__polyLine.strokeOpacity, str(self.__polyLine.editable).lower())

        self.__jsCode += """
                google.maps.event.addListener(map, 'click', addPoint);
                google.maps.event.addListener(map, 'rightclick', showContextMenu);
                google.maps.event.addListener(map, 'mousemove', statusBarCoordinate);
                google.maps.event.addListener(poly, 'click', showCoordinate);
                google.maps.event.addListener(poly, 'rightclick', showContextMenu);
                google.maps.event.addListener(marker, 'rightclick', showContextMenu);
            } // end of initialize()

            function showCoordinate(event) {
                var message = "Longitude: " + event.latLng.lat() + "<br />";
                message += "Latitude: " + event.latLng.lng() + "<br />";
                infoWindow.setContent(message);
                infoWindow.setPosition(event.latLng);
                infoWindow.open(map);
            }

            function addPoint(event) {
                if(isContextMenuOpen) {
                    $('.contextmenu').remove();
                    isContextMenuOpen = false;
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
                $(map.getDiv()).append(contextmenu);

                var clickedPosition = latLngToXY(position);
                $('.contextmenu').css('left', clickedPosition.x);
                $('.contextmenu').css('top', clickedPosition.y);

                contextmenu.style.visibility = "visible";

                isContextMenuOpen = true;

                // add event listeners
                // SEND COORDINATES
                $('#item1').click(function() {
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
