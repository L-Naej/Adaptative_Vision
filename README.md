Adaptative_Vision
=================

The goal of this project was to reproduce the experiment of Mr. Johnny Lee (https://www.youtube.com/watch?v=Jd3-eiid-Uw) but with a camera instead of a Wiimote. The user sees the virtual scene as if it was behind a virtual window which would perfectly match the screen. Thanks to this method, the user has a perception of depth, "3D", and is more immersed in the virtual universe.

The project was entirely coded in Python, and sadly I lost all the source code so I cannot give a link to it. It used a client/server paradigm where the client was the computer vision program tracking the head and the server the 3D scene receiving the head coordinates in order to calculate the correct projection matrix.
Technologies used

* Python 2.7
* pyOpenGL (to draw the scene)
* pyOpenCV (computer vision, to track the user's head)
* pyLiblo (OSC protocol implementation) 
