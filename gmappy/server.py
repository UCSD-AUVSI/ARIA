from flask import Flask, url_for, request
#from MAVProxy import mavproxy_headless, mavproxy

app = Flask(__name__)

app.config["SERVER_NAME"] = "localhost:5000"

@app.route("/", methods=['GET', 'POST'])
def getFlightPlan():
    list = []
    index = 0

    while True:

        lat = "data[" + str(index) +"][latitude]"
        lng = "data["+ str(index) +"][longitude]"
        typeField = "data[" + str(index) + "][type]"
        altitude = "data[" + str(index) + "][altitude]"
        duration = "data[" + str(index) + "][duration]"
        if lat in request.form.keys():
            list += [{
                "latitude": request.form[lat],
                "longitude": request.form[lng],
                "altitude" : request.form[altitude],
                "type": request.form[typeField],
                "duration": request.form[duration]
            }]
        else:
            break
        index += 1

    for coordDict in list:
        print "latitude: " + str(coordDict["latitude"])
        print "longitude: " + str(coordDict["longitude"])
        print "altitude: " + str(coordDict["altitude"])
        print "type: " + str(coordDict["type"])
        print "duration: " + str(coordDict["duration"])
        print

    #print "before loading waypoints"
    #mavproxy_headless.load_waypoints_from_array(list)
    #print "after loading from waypoints"

    return list
