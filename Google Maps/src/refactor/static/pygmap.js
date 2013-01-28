
            function initialize() {
        
            var mapOptions = {
        
                    mapTypeId : google.maps.MapTypeId.ROADMAP,
                
                    center : new google.maps.LatLng(0,0),
                
                    zoom : 5,
                
            };  // end mapOptions
            window.map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);
        
                    var pathArray = [
                
                        new google.maps.LatLng(0, 0),
                    
                        new google.maps.LatLng(10, 10),
                    
                        new google.maps.LatLng(15, -15),
                    
                        new google.maps.LatLng(0, 0),
                    
                    ]; // end path array
                
                var pathOptions = { 
            
                    path: pathArray,
                
                strokeColor: '#000000',
                strokeWeight: 2,
                strokeOpacity: 1,
                editable: true,
                map: window.map
                }; // end pathOptions
                window.path = new google.maps.Polyline(pathOptions);
            
            google.maps.event.addListener(window.map, 'click', function(event) {
                if(window.isContextMenuOpen) {
                    $('.contextmenu').remove();
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
        
            google.maps.event.addListener(window.map, 'rightclick', showContextMenu);
        
            google.maps.event.addListener(window.path, 'rightclick', showContextMenu);
        
            google.maps.event.addListener(window.path, 'click', showCoordinate);
        
            } // end initialize()
        
            function showCoordinate(event) {
                window.infowindow = new google.maps.InfoWindow();
                var index = window.path.getPath().getArray().indexOf(event.latLng);

                var message = "";
                message += "<div class=\'infodiv\'><label class=\'name\'>Latitude:</label><input id=\'latbox\' class=\'inputbox\' type=\'text\' value=\'" + event.latLng.lat() + "\'/></div><br />";
                message += "<div class=\'infodiv\'><label class=\'name\'>Longitude:</label><input id=\'lngbox\' class=\'inputbox\' type=\'text\' value=\'" + event.latLng.lng() + "\'/></div><br />";
                message += "<div class=\'infodiv\'><label class=\'name\'>Altitude:</label><input id=\'altbox\' class=\'inputbox\' type=\'text\' value=\'" + 0 + "\'/></div><br />";
                message += "<div class=\'infodiv\'><label class=\'name\'>Type:</label><select class=\'inputbox\' name=\'types\'><option value=\'takeoff\'>Takeoff</option><option value=\'waypoint\'>Waypoint</option><option value=\'loiter\'>Loiter</option><option value=\'land\'>Land</option></select></div><br />";
                

                window.infowindow.setContent(message);
                window.infowindow.setPosition(event.latLng);
                window.infowindow.open(map);
                window.isInfoWindowOpen = true;
            }
        
            function showContextMenu(event) {
                // first remove existing context menu
                $('.contextmenu').remove();

                var contextmenu;
                var position = event.latLng;
                contextmenu = document.createElement('div');
                contextmenu.className = 'contextmenu';
                contextmenu.innerHTML = "<button type=\'button\' id=\'sendCoord\' class=\'btn\'>Send Coordinates</button>";
                contextmenu.innerHTML += "<button type=\'button\' id=\'refresh\' class=\'btn\'>Refresh</button>";
                contextmenu.innerHTML += "<button type=\'button\' id=\'delPoint\' class=\'btn\'>Delete Waypoint</button>";
                contextmenu.innerHTML += "<button type=\'button\' id=\'delAllPoints\' class=\'btn\'>Delete All Waypoints</button>";
                $(window.map.getDiv()).append(contextmenu);

                var clickedPosition = latlngToXY(position);
                $('.contextmenu').css('left', clickedPosition.x);
                $('.contextmenu').css('top', clickedPosition.y);

                contextmenu.style.visibility = "visible";

                window.isContextMenuOpen = true;

                $('#sendCoord').click(sendCoordinates);
                $('#refresh').click(refresh);
                $('#delPoint').click({param1: position},deletePoint);
                $('#delAllPoints').click(deleteAllPoints);

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
               // $('.contextmenu').remove();
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
                    alert('point not in path');
                $('.contextmenu').remove();
            } // end deletePoints()

            function deleteAllPoints() {
                // TODO: complete function
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
            }
        