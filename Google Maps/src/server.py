from flask import Flask, url_for, request
from werkzeug.contrib.cache import SimpleCache
from MAVProxy import mavproxy_headless
app = Flask(__name__)
cache = SimpleCache()

app.config["SERVER_NAME"] = "localhost:5000"

@app.route("/", methods=['GET', 'POST'])
def getFlightPlan():
    list = []
    index = 0

    while True:

        lat = "data[" + str(index) +"][lat]"
        lng = "data["+ str(index) +"][lng]"
        typeField = "data[" + str(index) + "][type]"
        altitude = "data[" + str(index) + "][alt]"
        duration = "data[" + str(index) + "][dur]"
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

    load_waypoints_from_array(list)
    return list

with app.app_context():
    url_for('static', filename='gmaps.html')
if __name__ == "__main__":
    app.run()
