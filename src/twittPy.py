#!/bin/env python

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

import os
import urllib2, unicodedata
from xml.dom.minidom import parseString


class TwittFeed: 
    def __init__(self, fileName):
        if os.path.isfile(fileName):
            try:
                file = open(fileName,'r')
            except Exception, e:
                raise Exception(e.printStack())
                                
        else:
            try:
                file = urllib2.urlopen(fileName)
            except:
                raise Exception

        #convert to string:
        data = file.read()
        file.close()
        
        #parse the xml you got from the file
        self.dom = parseString(data)

        
    def readFeed(self,tagName):
        xmlList = []
        
        for i in xrange(len(self.dom.getElementsByTagName(tagName))):
            xmlTag = self.dom.getElementsByTagName(tagName)
            xmlList.append(" ".join(t.nodeValue for t in xmlTag[i].childNodes if t.nodeType == t.TEXT_NODE))
        return xmlList

    def colorArduino(self, xmlList):
        for i in xrange(len(xmlList)):
            #convert unicode to string
            xmlString = unicodedata.normalize('NFKD', xmlList[i]).encode('ascii','ignore')
            if xmlString[0:8] == '#Arduino':
                return xmlString[9:]

