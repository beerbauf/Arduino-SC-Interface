#!/usr/bin/env python

##
#    Project: Arduino SC Interface - A GUI for Arduino serial comunication
#    Author: Andrea Cirillo <sabageek.blogspot.com>
#    Copyright: 2012 Andrea Cirillo
#    License: GPL-3
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

import twittPy
import serialComunication
import ConfigParser
import os

import sys
if sys.version_info < (3, 0):
    try:
        from Tkinter import *
    except ImportError:
        raise ImportError("Tkinter module not found - it is required for GUI")
else:
    try:
        from tkinter import *
    except ImportError:
        raise ImportError("tkinter module not found - it is required for GUI")

class App:

    def __init__(self):

        # Config file
        config = ConfigParser.ConfigParser()
        config.read('properties.cfg')
        
        # GUI
        master = Tk()
        master.geometry("500x600")
        master.title("Arduino SC Interface (v0.3)")

        frame = Frame(master)
        frame.pack()

        #Label
        self.portLabel = LabelFrame(master, text="Port", padx=5, pady=5)
        self.portLabel.pack(padx=10, pady=10)
 
        self.rateLabel = LabelFrame(master, text="Bauderate", padx=5, pady=5)
        self.rateLabel.pack(padx=10, pady=10)

        self.colorLabel = LabelFrame(master, text="Color", padx=5, pady=5)
        self.colorLabel.pack(padx=10, pady=10)

        self.urlLabel = LabelFrame(master, text="Feed URL/Filename", padx=5, pady=5)
        self.urlLabel.pack(padx=10, pady=10)

        #Entry text
        self.portEntry = Entry(self.portLabel)
        self.portEntry.insert(0, config.get('Arduino','port'))
        self.portEntry.pack()

        self.rateEntry = Entry(self.rateLabel)
        self.rateEntry.insert(0, config.get('Arduino','bauderate'))
        self.rateEntry.pack()

        vcmd = (master.register(self.validate), '%S')
        self.colorEntry = Entry(self.colorLabel, validate="key", validatecommand=vcmd)
        self.colorEntry.pack()

        self.urlEntry = Entry(self.urlLabel, width=300)
        self.urlEntry.insert(0, config.get('Arduino','url'))
        self.urlEntry.pack()

        #Buttons
        self.sendButton = Button(frame, text="SendToArduino", state="disable",command=self.send_func)
        self.sendButton.pack(side=LEFT)

        self.urlButton = Button(frame, text="CheckFeedArduino", command=self.feed_func)
        self.urlButton.pack(side=LEFT)

        self.clearButton = Button(frame, text="ClearColor", command=self.clear_func)
        self.clearButton.pack(side=LEFT)

        self.quitButton = Button(frame, text="Quit", bg="red", command=self.close_func)
        self.quitButton.pack(side=LEFT)

        #Text area
        self.text = Text(master)
        self.text.insert("insert", "Arduino SC interface (v0.3)\n--")
        self.text.pack()
        
        master.mainloop()

    #validate entry color (make active the SendToArduino button)
    def validate(self, S):
        if len(S) is not 0:
            self.sendButton.configure(state="active")
        return all(S)

    #send to Arduino function
    def send_func(self):
        serialResponse = serialComunication.send_serial(self.colorEntry.get()[1:], self.portEntry.get(), self.rateEntry.get())
        self.text.insert("end", "\n%s --> %s"%(self.colorEntry.get(),serialResponse))

    #implement feed class for twitter
    def feed_func(self):
        try:
            feed = twittPy.TwittFeed(self.urlEntry.get())
            self.colorEntry.insert(0,feed.colorArduino(feed.readFeed('text')))
        except Exception:
            import sys
            self.text.insert("end", "\n%s"%(sys.exc_info()[2]))

    #clear and close button
    def clear_func(self):
        self.colorEntry.delete(0,END)
        serialResponse = serialComunication.send_serial('000000', self.portEntry.get(), self.rateEntry.get())
        self.sendButton.configure(state="disable")

    def close_func(self):
        self.write_to_config()
        sys.exit(0)

    #write in properties file
    def write_to_config(self):
        config = ConfigParser.RawConfigParser()
        config.add_section('Arduino')
        config.set('Arduino', 'port', self.portEntry.get())
        config.set('Arduino', 'bauderate', self.rateEntry.get())
        config.set('Arduino', 'url', self.urlEntry.get())
        with open('properties.cfg', 'wb') as configfile:
            config.write(configfile)
