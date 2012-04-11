'''
    Project: Arduino SC Interface - A GUI for Arduino serial comunication
    @author: Andrea Cirillo <sabageek.blogspot.com>
    @copyright: 2012 Andrea Cirillo
    @license: GPL-3
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

   This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import serial
 
def send_serial(word, *args):
    port = '/dev/ttyACM0'
    baudrate = 115200
    if len(args) < 2:
        port = args[0]
        if len(args) == 2:
            baudrate = int(args[1])
            ser = serial.Serial(port, baudrate)
            ser.write(str(word))
            return args[0]
