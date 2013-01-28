
            function initialize() {
        
            window.durationArray = []
            window.altitudeArray = []
            window.typeArray = []
        
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
            
                        altitudeArray.push(0);
                        typeArray.push('takeoff');
                        durationArray.push(0);
                    
                        altitudeArray.push(0);
                        typeArray.push('waypoint');
                        durationArray.push(0);
                    
                        altitudeArray.push(0);
                        typeArray.push('loiter');
                        durationArray.push(5);
                    
                        altitudeArray.push(0);
                        typeArray.push('land');
                        durationArray.push(0);
                    
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
        
            google.maps.event.addListener(window.path.getPath(), 'insert_at', function(index) {
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
        
            /*
            * NOTE: google maps api decreases length of mvc array beore 'remove_at' event gets called
            */
            google.maps.event.addListener(window.path.getPath(), 'remove_at', function(index) {
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
        