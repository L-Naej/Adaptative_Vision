Adaptative Vision
=================

The goal of this project was to reproduce the experiment of Mr. Johnny Lee (https://www.youtube.com/watch?v=Jd3-eiid-Uw) but with a camera instead of a Wiimote. The user sees the virtual scene as if it was behind a virtual window which would perfectly match the screen. Thanks to this method, the user has a perception of depth, "3D", and is more immersed in the virtual universe.

The project is entirely coded in Python. It uses a client/server paradigm where the client is the computer vision program tracking the head and the server the 3D scene receiving the head coordinates in order to calculate the correct projection matrix.
Technologies used

* Python 2.7
* pyOpenGL (to draw the scene)
* pyOpenCV (computer vision, to track the user's head)
* pyLiblo (OSC protocol implementation) 
 

Usage
==
To start the program, symply run in console the script "./tp.sh".

You have to configure the program in order to make it work on your computer. The configuration is in conf.cfg (plain text). The most important thing to configure is your screen dimensions (in millimeters).

Parameters :
* screenwidth : width of your screen in millimeters
* screenheight height of your screen in millimeters
* ip : server IP (generally, localhost), ie. the machine where server.py is being executed
* port : port the server is listening to
* treshold : value to tweak to improve stability of the head tracking. Higher the value, more stable is the detection, but a value too high will result in no more detection of the movement (head considered as still).
* haarfile : cascading files containing statistics value used to detect a head in the camera stream. If you want to use an other file, change this value (see the haarcascades directory). See http://en.wikipedia.org/wiki/Haar-like_features for more information.
* webcamId : ID used by OpenCV to choose the webcam to use. If you have just one webcam, don't touch the value.
* Debug : 0 = no debug, 1 = print debug values in console each 1/2 second
* showCamera : 1 = a window with what the camera see is opened. 0 = no window (better performance)

