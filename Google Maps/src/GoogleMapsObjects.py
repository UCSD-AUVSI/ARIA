class Coordinate(object):
    def __init__(self, latitude, longitude):
        self.__latitude = latitude
        self.__longitude = longitude

    def latitude():
        def fget(self):
            return self.__latitude

        def fset(self, value):
            self.__latitude = value

        def fdel(self):
            del self.__latitude
        return locals()
    latitude = property(**latitude())

    def longitude():
        def fget(self):
            return self.__longitude

        def fset(self, value):
            self.__longitude = value

        def fdel(self):
            del self.__longitude
        return locals()
    longitude = property(**longitude())


class Polygon(object):
    # path is a list of coordinate objects
    def __init__(self, path):
        self.__path = path
        self.__fillColor = '#FFFFFF'
        self.__fillOpacity = 0.5
        self.__strokeColor = '#000000'
        self.__strokeWeight = 3
        self.__strokeOpacity = 1

    def path():
        def fget(self):
            return self.__path

        def fset(self, value):
            self.__path = value

        def fdel(self):
            del self.__path
        return locals()
    path = property(**path())

    def fillColor():
        def fget(self):
            return self.__fillColor

        def fset(self, value):
            self. __fillColor = value

        def fdel(self):
            del self.__fillColor
        return locals()
    fillColor = property(**fillColor())

    def fillOpacity():
        def fget(self):
            return self.__fillOpacity

        def fset(self, value):
            self.__fillOpacity = value

        def fdel(self):
            del self.__fillOpacity
        return locals()
    fillOpacity = property(**fillOpacity())

    def strokeColor():
        def fget(self):
            return self.__strokeColor

        def fset(self, value):
            self.__strokeColor = value

        def fdel(self):
            del self.__strokeColor
        return locals()
    strokeColor = property(**strokeColor())

    def strokeWeight():
        def fget(self):
            return self.__strokeWeight

        def fset(self, value):
            self.__strokeWeight = value

        def fdel(self):
            del self.__strokeWeight
        return locals()
    strokeWeight = property(**strokeWeight())

    def strokeOpacity():
        def fget(self):
            return self.__strokeOpacity

        def fset(self, value):
            self.__strokeOpacity = value

        def fdel(self):
            del self.__strokeOpacity
        return locals()
    strokeOpacity = property(**strokeOpacity())


class PolyLine(object):
    def __init__(self):
        self.__strokeColor = '#000000'
        self.__strokeOpacity = 1.0
        self.__strokeWeight = 3
        self.__editable = True

    def strokeColor():
        def fget(self):
            return self.__strokeColor

        def fset(self, value):
            self.__strokeColor = value

        def fdel(self):
            del self.__strokeColor
        return locals()
    strokeColor = property(**strokeColor())

    def strokeOpacity():
        def fget(self):
            return self.__strokeOpacity

        def fset(self, value):
            self.__strokeOpacity = value

        def fdel(self):
            del self.__strokeOpacity
        return locals()
    strokeOpacity = property(**strokeOpacity())

    def strokeWeight():
        def fget(self):
            return self.__strokeWeight

        def fset(self, value):
            self.__strokeWeight = value

        def fdel(self):
            del self.__strokeWeight
        return locals()
    strokeWeight = property(**strokeWeight())

    def editable():
        def fget(self):
            return self.__editable

        def fset(self, value):
            self.__editable = value

        def fdel(self):
            del self.__editable
        return locals()
    editable = property(**editable())
