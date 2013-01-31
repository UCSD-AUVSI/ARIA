#!/usr/bin/env python

"""
  MAVProxy default console
"""
import sys

class NoConsole():
    '''
    a message console for MAVProxy
    '''
    def __init__(self):
        pass

    def write(self, text, fg='black', bg='white'):
        pass

    def writeln(self, text, fg='black', bg='white'):
        pass

    def set_status(self, name, text='', row=0, fg='black', bg='white'):
        '''set a status value'''
        pass

    def error(self, text, fg='red', bg='white'):
        self.writeln(text, fg=fg, bg=bg)

    def close(self):
        pass

    def is_alive(self):
        '''check if we are alive'''
        return True
    
if __name__ == "__main__":
    # test the console
    import time
    console = SimpleConsole()
    while console.is_alive():
        console.write('Tick', fg='red')
        console.write(" %s " % time.asctime())
        console.writeln('tock', bg='yellow')
        time.sleep(0.5)
