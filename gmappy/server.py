from flask import Flask, url_for, request
from MAVProxy import mavproxy_headless, mavlinkv10

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

    home_lat = request.form["home[latitude]"]
    home_lng = request.form["home[longitude]"]
    home_alt = request.form["home[altitude]"]
    home_type = request.form["home[type]"]
    home_dur = request.form["home[duration]"]

    print "Home Location"
    print "Home latitude: " + home_lat
    print "Home longitude: " + home_lng
    print "Home altitude: " + home_alt
    print "Home type: " + home_type
    print "Home duration: " + home_dur
    print "\n"

    print "asdf"
    try:
        mavproxy_headless.master().command_long_send(mpstate.status.target_system, 
                                                mpstate.status.target_component,
                                                MAV_CMD_DO_SET_HOME,
                                                1, #comfirmation
                                                home_lat, home_lng, home_alt)
    except:
        print "except"
        print sys.exec_info()[0]

    print "1234"
