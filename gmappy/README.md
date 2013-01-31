Gmappy
======

To run:
    
    python driver.py

Gmappy contains a simple Python interface for Google Maps. The Python interface allows:

* the creation and editing (only some options are supported) of the map itself
* the creation of an editable path (can be preset)

The Javascript code produced by Gmappy can:

* track position of plane
* send information of path over local server to Python interface using Flask and from there send to MavLink
* reset map to its default (default is the map produced by Python interface)
* deleting specific points on the path
* editing position, altitude, and type of each point on the path

TODO
* send data from python to javascript over server
* send data from python to mavlink
* retrieve data from python to mavlink

Dependencies 
------------

Python 2.7 

Flask v.0.9 

PyQt 4.9.5-1 
