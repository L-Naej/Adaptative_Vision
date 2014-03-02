#NOTE : Ne pas mettre d'accents dans les commentaires sinon ca ne marche pas
# glLoadIdentity(), glPopMatrix(), glPushMatrix() permettent de reinitialiser les positions ou les rotations

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Image import *
import time
import sys
from math import *

#Code Ascii de la touche echap
ESCAPE = '\033'

# Number of the glut window. 
# (Initialisation de variables)
window = 0
blend = 0
texture = 0

def LoadTextures():
    # Chargement de l'image
    timage = open("target_256x256.bmp")
	
    ix = timage.size[0]
    iy = timage.size[1]
    image = timage.tostring("raw", "RGBX", 0, -1)
	
    # Creation de la texture	
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

# A general OpenGL initialization function.  Sets all of the initial parameters. 
def InitGL(Width, Height):				# We call this right after our OpenGL window is created.
    LoadTextures()

    glBlendFunc(GL_SRC_ALPHA, GL_ONE) # Active la fonction blend afin de jouer avec la transparence
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.0, 1.0, 0.0, 0.0)	# This Will Clear The Background Color To Black
    glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)				# The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)				# Enables Depth Testing
    #glShadeModel(GL_SMOOTH)				# Enables Smooth Color Shading
	
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()					# Reset The Projection Matrix
										# Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)

# Fonction qui permet de redimensionner la fenetre
def ReSizeGLScene(Width, Height):
    if Height == 0:						# Prevent A Divide By Zero If The Window Is Too Small 
	    Height = 1

    glViewport(0, 0, Width, Height)		# Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

# Fonction principale de dessin 
def DrawGLScene():

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)	# Nettoie l'ecran et le buffer de profondeur
	glLoadIdentity()					

	glPushMatrix()
	glTranslatef(0.0, 0.0, -6.0) #On place le point de depart du premier carre	
	glBegin(GL_QUADS)			   #CARRE 1 
	
	glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  -5.0)	# Bas gauche
	glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  -5.0)	# Bas droite
	glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  -5.0)	# Haut droit
	glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0,  -5.0)	# Haut gauche
	glEnd()
	

	glPopMatrix()
	glPushMatrix()
	
	glTranslatef(1.0, 0.0, -6.0)
	
	glBegin(GL_QUADS)			    #CARRE 2
	
	glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  0.0)	# Bas gauche
	glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  0.0)	# Bas droite
	glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  0.0)	# Haut droit
	glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0,  0.0)	# Haut gauche
	glEnd()
	
	glPopMatrix()
	glPushMatrix()
	
	glTranslatef(-2.0, 0.0, -6.0)
	
	
	glBegin(GL_QUADS)			    #CARRE 3
	
	glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  2.0)	# Bas gauche
	glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  2.0)	# Bas droite
	glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  2.0)	# Haut droit
	glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0,  2.0)	# Haut gauche
	glEnd()
	
	dessineLigne()
	glPopMatrix()
	
	
	#  since this is double buffered, swap the buffers to display what just got drawn. 
	glutSwapBuffers()

	
def dessineLigne() :
	# repere en x : -3 a 7
	# repere en y : -2,5 a 2,5
	glLineWidth(2)
	glColor(1.0, 1.0, 1.0)
	
        glBegin(GL_LINES)

	i=0
        #1er rectangle illusion
	while i <= 50 : 
		#verticale gauche
		glVertex3f(-5,-4, -i)
		glVertex3f(-5, 5, -i)
		#verticale droite
		glVertex3f(10, -4, -i)
		glVertex3f(10, 5, -i)
		#horizontale bas
		glVertex3f(-5, -4, -i)
		glVertex3f(10, -4, -i)
		#horizontale haut
		glVertex3f(-5, 5, -i)
		glVertex3f(10, 5, -i)
		i+=4
	i=-5
	while (i <= 10)  : 
		glVertex(i, 5, 0)
		glVertex(i, 5, -50)
		glVertex(i, -4, 0)
		glVertex(i, -4, -50)
		i=i+1

        i=-4
	while (i <= 5) :
		glVertex(10, i, 0)
		glVertex(10, i, -50)
		glVertex(-5, i, 0)
		glVertex(-5, i, -50)
		i=i+1
	#fin quadrillage
	glEnd()


	glLineWidth(4)
	glColor(1.0, 1.0, 1.0)
	
        glBegin(GL_LINES)
	#traces des cibles
	#cible 1 : la plus grosse
	glVertex(-1, 0, 2)
	glVertex(-1, 0, -50)
	#cible2 : la plus petite
	glVertex(2, 0, -5)
	glVertex( 2, 0, -50)
	#cible3 : la moyenne
	glVertex(3, 0, 0)
	glVertex(3, 0, -50)
	glEnd()
	
	
	
# Fonction appelee lorsqu'une touche est pressee 
def keyPressed(key, x, y):
	global blend
	#time.sleep(0.1) Aucune idee d'a quoi sert ce timer mais semblait utile
	if ord(key) == 27:
		sys.exit()
		
	# Si on appuie sur la touche b, on active ou desactive la transparence
	elif key == 'B' or key == 'b': 
		print("B/b pressed; blending is: %d\n"%(blend))
		if blend:		
			blend = 0
		else:
			blend = 1    
		
		if (blend):
		    glEnable(GL_BLEND)
		    glDisable(GL_DEPTH_TEST)
		else:
		    glDisable(GL_BLEND)
		    glEnable(GL_DEPTH_TEST)



def main():
	global window
	#glBlendFunc(GL_ZERO,GL_ZERO)
	# For now we just pass glutInit one empty argument. I wasn't sure what should or could be passed in (tuple, list, ...)
	# Once I find out the right stuff based on reading the PyOpenGL source, I'll address this.
	glutInit("")

	# Select type of Display mode:   
	#  Double buffer 
	#  RGBA color
	# Alpha components supported 
	# Depth buffer
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
	
	# On choisit la taille de la fenetre
	glutInitWindowSize(640, 480)
	
	# the window starts at the upper left corner of the screen 
	glutInitWindowPosition(0, 0)
	
	# Okay, like the C version we retain the window id to use when closing, but for those of you new
	# to Python (like myself), remember this assignment would make the variable local and not global
	# if it weren't for the global declaration at the start of main.
	window = glutCreateWindow("Scene numero 2")

   	# Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
	# set the function pointer and invoke a function to actually register the callback, otherwise it
	# would be very much like the C version of the code.	
	
	glutDisplayFunc(DrawGLScene)
	
	# Uncomment this line to get full screen.
	# glutFullScreen()

	# When we are doing nothing, redraw the scene.
	glutIdleFunc(DrawGLScene)
	
	# Register the function called when our window is resized.
	glutReshapeFunc(ReSizeGLScene)
	
	# Fonction qui s'execute si une touche est pressee  
	glutKeyboardFunc(keyPressed)
	
	# Initialisation de la fenetre
	InitGL(640, 480)
	
	# Start Event Processing Engine	
	glutMainLoop()

# Print message to console, and kick off the main to get it rolling.
print "Hit ESC key to quit."
main()
    	