from flask import Flask, url_for, request
from MAVProxy import mavproxy_headless, mavlinkv10

app = Flask(__name__)

app.config["SERVER_NAME"] = "localhost:5000"

@app.route("/", methods=['GET', 'POST'])
def getFlightPlan():
    waypoint_list = []
    index = 0

    home_lat = "home[latitude]"
    home_lng = "home[longitude]"
    home_alt = "home[altitude]"
    home_type = "home[type]"
    home_dur = "home[duration]"

    print "Home Location"
    print "Home latitude: " + str(request.form[home_lat])
    print "Home longitude: " + str(request.form[home_lng])
    print "Home altitude: " + str(request.form[home_alt])
    print "Home type: " + str(request.form[home_type])
    print "Home duration: " + str(request.form[home_dur])
    print "\n"

    while True:

        lat = "data[" + str(index) +"][latitude]"
        lng = "data["+ str(index) +"][longitude]"
        typeField = "data[" + str(index) + "][type]"
        altitude = "data[" + str(index) + "][altitude]"
        duration = "data[" + str(index) + "][duration]"
        if lat in request.form.keys():
            waypoint_list += [{
                "latitude": request.form[lat],
                "longitude": request.form[lng],
                "altitude" : request.form[altitude],
                "type": request.form[typeField],
                "duration": request.form[duration]
            }]
        else:
            break
        index += 1

    for coordDict in waypoint_list:
        print "latitude: " + str(coordDict["latitude"])
        print "longitude: " + str(coordDict["longitude"])
        print "altitude: " + str(coordDict["altitude"])
        print "type: " + str(coordDict["type"])
        print "duration: " + str(coordDict["duration"])
        print

    print "before loading waypoints"
    mavproxy_headless.load_waypoints_from_array(waypoint_list)
    print "after loading from waypoints"

    mavproxy_headless.save_waypoints("output.txt")

    return "OK"
