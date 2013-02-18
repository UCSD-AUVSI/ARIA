from flask import Flask, url_for, request
from MAVProxy import mavproxy_headless, mavproxy

app = Flask(__name__)

app.config["SERVER_NAME"] = "localhost:5000"

@app.route("/flightplan", methods=['POST'])
def setFlightPlan():
    plan = []
    index = 0

    while True:

        lat = "data[" + str(index) +"][latitude]"
        lng = "data["+ str(index) +"][longitude]"
        typeField = "data[" + str(index) + "][type]"
        altitude = "data[" + str(index) + "][altitude]"
        duration = "data[" + str(index) + "][duration]"
        if lat in request.form.keys():
            plan += [{
                "latitude": request.form[lat],
                "longitude": request.form[lng],
                "altitude" : request.form[altitude],
                "type": request.form[typeField],
                "duration": request.form[duration]
            }]
        else:
            break
        index += 1

    for coordDict in plan:
        print "latitude: " + str(coordDict["latitude"])
        print "longitude: " + str(coordDict["longitude"])
        print "altitude: " + str(coordDict["altitude"])
        print "type: " + str(coordDict["type"])
        print "duration: " + str(coordDict["duration"])
        print

    print "before loading waypoints"
    mavproxy_headless.load_waypoints_from_array(plan)
    print "after loading from waypoints"

    mavproxy_headless.save_waypoints("output.txt")

    return "OK"

@app.route("/home", methods=['POST'])
def setHome():
    lat=float(request.form["lat"])
    lng=float(request.form["lng"])
    alt=float(request.form["alt"])

    mavproxy_headless.master().command_long_send(mpstate.status.target_system, 
                                                mpstate.status.target_component,
                                                MAV_CMD_DO_SET_HOME,
                                                1, #comfirmation
                                                lat, lng, alt)