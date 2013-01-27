
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
                window.path.getPath().push(event.latLng);                
            });
        
            google.maps.event.addListener(window.map, 'rightclick', showContextMenu);
        
            } // end initialize()
        
            function showContextMenu(event) {
                // first remove existing context menu
                $('.contextmenu').remove();

                var contextmenu;
                var position = event.latLng;
                contextmenu = document.createElement('div');
                contextmenu.className = 'contextmenu';
                contextmenu.innerHTML = "<button type=\'button\' id=\'sendCoord\' class=\'btn\'>Send Coordinates</button>";
                contextmenu.innerHTML += "<button type=\'button\' id=\'refresh\' class=\'btn\'>Refresh</button>";
                contextmenu.innerHTML += "<button type=\'button\' id=\'delPoint\' class=\'btn\'>Delete Point</button>";
                $(window.map.getDiv()).append(contextmenu);

                var clickedPosition = latlngToXY(position);
                $('.contextmenu').css('left', clickedPosition.x);
                $('.contextmenu').css('top', clickedPosition.y);

                contextmenu.style.visibility = "visible";

                window.isContextMenuOpen = true;

                $('#sendCoord').click(sendCoordinates);
                $('#refresh').click(refresh);
                $('#delPoint').click(deletePoint);

                //TODO: is this necessary?
                //contextmenu.style.visibility = "visible";
            } // end showContext menu()

            function sendCoordinates() {} // end sendCoordinates()
            function refresh() {
                location.reload();
            } // end refresh()
            function deletePoint() {} // end deletePoints()

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
        