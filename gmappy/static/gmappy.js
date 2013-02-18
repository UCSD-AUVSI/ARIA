
            function initialize() {
                window.durationArray = []
                window.altitudeArray = []
                window.typeArray = []
                window.infowindow = new google.maps.InfoWindow();
        
            var mapOptions = {
        
                    mapTypeId : google.maps.MapTypeId.ROADMAP,
                
                    center : new google.maps.LatLng(0,0),
                
                    zoom : 5,
                
            };  // end mapOptions
            window.map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
        
                    var pathArray = [
                
                        new google.maps.LatLng(0, 0),
                    
                        new google.maps.LatLng(10, 10),
                    
                        new google.maps.LatLng(15, -15),
                    
                        new google.maps.LatLng(0, 0),
                    
                    ]; // end path array
                
                var pathOptions = { 
            
                    path: pathArray,
                
                strokeColor: "#000000",
                strokeWeight: 2,
                strokeOpacity: 1,
                editable: true,
                map: window.map
                }; // end pathOptions
                window.path = new google.maps.Polyline(pathOptions);
            
                        altitudeArray.push(0);
                        typeArray.push("Takeoff");
                        durationArray.push(0);
                    
                        altitudeArray.push(0);
                        typeArray.push("Waypoint");
                        durationArray.push(0);
                    
                        altitudeArray.push(0);
                        typeArray.push("Loiter");
                        durationArray.push(5);
                    
                        altitudeArray.push(0);
                        typeArray.push("Land");
                        durationArray.push(0);
                    
            var markerOptions = {
        
                    position : new google.maps.LatLng(0,0),
                
                    title : 'current location',
                
            }; // end markerOptions
            window.marker = new google.maps.Marker(markerOptions);
            window.marker.setMap(window.map);
        
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
        
            google.maps.event.addListener(window.path, "click", function(event) {
                    var index = window.path.getPath().getArray().indexOf(event.latLng);

                    var message = "";
                    message += "<div class=\"infodiv\"><label class=\"name\">Latitude:</label><input id=\"latbox\" class=\"inputbox\" type=\"text\" value=\"" + event.latLng.lat() + "\"/></div><br />";
                    message += "<div class=\"infodiv\"><label class=\"name\">Longitude:</label><input id=\"lngbox\" class=\"inputbox\" type=\"text\" value=\"" + event.latLng.lng() + "\"/></div><br />";
                    message += "<div class=\"infodiv\"><label class=\"name\">Altitude:</label><input id=\"altbox\" class=\"inputbox\" type=\"text\" value=\"" + 0 + "\"/></div><br />";
                    if(window.typeArray[index] == "Takeoff") {
                        message += "<div class=\"infodiv\"><label class=\"name\">Type:</label><select class=\"inputbox\" name=\"types\"><option value=\"takeoff\" selected=\"selected\">Takeoff</option><option value=\"waypoint\">Waypoint</option><option value=\"loiter\">Loiter</option><option value=\"land\">Land</option></select></div><br />";
                    }
                    else if(window.typeArray[index] == "Waypoint") {
                        message += "<div class=\"infodiv\"><label class=\"name\">Type:</label><select class=\"inputbox\" name=\"types\"><option value=\"takeoff\">Takeoff</option><option value=\"waypoint\" selected=\"selected\">Waypoint</option><option value=\"loiter\">Loiter</option><option value=\"land\">Land</option></select></div><br />";
                    }
                    else if(window.typeArray[index] == "Loiter") {
                        message += "<div class=\"infodiv\"><label class=\"name\">Type:</label><select class=\"inputbox\" name=\"types\"><option value=\"takeoff\" >Takeoff</option><option value=\"waypoint\">Waypoint</option><option value=\"loiter\" selected=\"selected\">Loiter</option><option value=\"land\">Land</option></select></div><br />";
                        message += "<div class=\"infodiv\"><label class=\"name\">Duration (s):</label><input id=\"durbox\" class=\"inputbox\" type=\"text\" value=\"" + window.durationArray[index] + "\" /><br />";
                    }
                    else {
                        message += "<div class=\"infodiv\"><label class=\"name\">Type:</label><select class=\"inputbox\" name=\"types\"><option value=\"takeoff\" >Takeoff</option><option value=\"waypoint\">Waypoint</option><option value=\"loiter\">Loiter</option><option value=\"land\" selected=\"selected\">Land</option></select></div><br />";
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
                            message += "<div class=\"infodiv\"><label class=\"name\">Latitude:</label><input id=\"latbox\" class=\"inputbox\" type=\"text\" value=\"" + event.latLng.lat() + "\"/></div><br />";
                            message += "<div class=\"infodiv\"><label class=\"name\">Longitude:</label><input id=\"lngbox\" class=\"inputbox\" type=\"text\" value=\"" + event.latLng.lng() + "\"/></div><br />";
                            message += "<div class=\"infodiv\"><label class=\"name\">Altitude:</label><input id=\"altbox\" class=\"inputbox\" type=\"text\" value=\"" + 0 + "\"/></div><br />";
                            message += "<div class=\"infodiv\"><label class=\"name\">Type:</label><select class=\"inputbox\" name=\"types\"><option value=\"takeoff\" >Takeoff</option><option value=\"waypoint\">Waypoint</option><option value=\"loiter\" selected=\"selected\">Loiter</option><option value=\"land\">Land</option></select></div><br />";
                            message += "<div class=\"infodiv\"><label class=\"name\">Duration (s):</label><input id=\"durbox\" class=\"inputbox\" type=\"text\" value=\"" + window.durationArray[index] + "\" /><br />";

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
        
            google.maps.event.addListener(window.map, "rightclick", showContextMenu);
            google.maps.event.addListener(window.path, "rightclick", showContextMenu);
            } // end initialize()
        
            function showContextMenu(event) {
                // first remove existing context menu
                $(".contextmenu").remove();

                var contextmenu;
                var position = event.latLng;
                contextmenu = document.createElement("div");
                contextmenu.className = "contextmenu";
                contextmenu.innerHTML =  "<button type=\"button\" id=\"setHome\" class=\"btn\">Set Home Location</button>";
                contextmenu.innerHTML += "<button type=\"button\" id=\"sendCoord\" class=\"btn\">Send Coordinates</button>";
                contextmenu.innerHTML += "<button type=\"button\" id=\"refresh\" class=\"btn\">Refresh</button>";
                contextmenu.innerHTML += "<button type=\"button\" id=\"delPoint\" class=\"btn\">Delete Waypoint</button>";
                contextmenu.innerHTML += "<button type=\"button\" id=\"delAllPoints\" class=\"btn\">Delete All Waypoints</button>";
                $(window.map.getDiv()).append(contextmenu);

                var clickedPosition = latlngToXY(position);
                $(".contextmenu").css("left", clickedPosition.x);
                $(".contextmenu").css("top", clickedPosition.y);

                contextmenu.style.visibility = "visible";

                window.isContextMenuOpen = true;

                $("#setHome").click({param1: position},setHome);
                $("#sendCoord").click(sendCoordinates);
                $("#refresh").click(refresh);
                $("#delPoint").click({param1: position},deletePoint);
                $("#delAllPoints").click(deleteAllPoints);

                //TODO: is this necessary?
                //contextmenu.style.visibility = "visible";
            } // end showContext menu()

            function setHome(event) {
                var position = event.data.param1;
                window.home = position;

                window.homeMarker = new google.maps.Marker({
                    map: window.map,
                    position: new google.maps.LatLng(position.lat(), position.lng()),
                    title: "Home"
                });

                $('.contextmenu').remove();
            }

            function sendCoordinates() {
                if(window.path.getPath().getLength() == 0) {
                    alert("You do not have a path to send!");
                    $('.contextmenu').remove();
                    return;
                }
                var coordArray = [];
                for(var i = 0; i  < window.path.getPath().getLength(); i++) {
                    coordArray.push({
                        latitude: window.path.getPath().getAt(i).lat(),
                        longitude: window.path.getPath().getAt(i).lng(),
                        altitude: altitudeArray[i],
                        type: typeArray[i],
                        duration: durationArray[i]
                    });
                }

                var homeloc = {
                    latitude: window.home.lat(),
                    longitude: window.home.lng(),
                    altitude: 0,
                    type: "Land",
                    duration: 0
                };

                $.post("http://localhost:5000",
                {
                    "data" : coordArray,
                    "home" : homeloc
                });
                $(".contextmenu").remove();
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
        