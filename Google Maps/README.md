Google Maps
============

To run on windows just run the batch file otherwise run RunUI.py 

GoogleMapsPy contains a simple Python interface for Google Maps. The Python interface allows:

* the creation and editing (only some options are supported) of the map itself
* the creation of an editable path (can be preset)
* the creation of multiple polygons of different fill options, and stroke options (preset only)

The Javascript code produced by GoogleMapsPy can:

* track position of plane
* send information of path over local server to Python interface using Flask and from there send to MavLink
* reset map to its default (default is the map produced by Python interface)
* deleting specific points on the path
* editing position, altitude, and type of each point on the path
* display GPS coordinate of position of mouse in status bar

TODO
* Add "Send Data" to Python interface
  * will send data received from Javascript to Mavlink

Dependencies 
------------

Python 2.7 

Flask v.0.9 

PyQt 4.9.5-1 
