#!/usr/bin/env python
# -*- coding: utf8 -*-
# Prototype de serveur qui reçoit d'un client les coordonnées des yeux de l'utilisateur
# et à partir de là calcule une scène 3D.
#
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import Image
#from math import *
import liblo, sys, time

from numpy import *


ESCAPE = '\033'
window = 0

#Variables de configuration (conf.cgf)
screenW = screenH = port = 0
Debug = False

# ------------------------------------------------------------------
#| Définition de la position des yeux au démarrage de l'application |
# ------------------------------------------------------------------
#	En face de l'écran à 360mm de distance
ex,ey,ez = (0.0,0.0,400.0)

#Gestion des FPS et du fullscreen
currentTime = previousTime = glutGet(GLUT_ELAPSED_TIME)
frameCount = fps = 0
fullscreen = 0

#gestion du temps pour affichage de debug
newTime = 0.0
oldTime = time.time()
# ------------------------------------------------------------------
#| Définition de la position de la scène au démarrage de l'application |
# ------------------------------------------------------------------
posx,posy,posz=(0.0,0.0,0.0)

#Charge le fichier de config et initialise les variables adéquates
def initConfig():
	global screenW,screenH,port, Debug
	arg = {}
	try:
		config = open('conf.cfg', 'rb')
	except IOError, err:
		print "Le fichier de configuration [conf.cfg] n'a pas été trouvé."
		print str(err)
		sys.exit(1)
	lignes = config.readlines()
	
	for lig in lignes:
		sp = lig.split('#')[0]
		sp = sp.split('=')
		if len(sp) == 2:
			arg[sp[0].strip()]=sp[1].strip()
	config.close()

	screenW = float(arg['screenwidth'])
	screenH = float(arg['screenheight'])
	port = int(arg['port'])
	Debug = int(arg['Debug'])
	
def calculeFPS():
	global frameCount, currentTime, previousTime, fps
	
	frameCount = frameCount + 1
	
	currentTime = glutGet(GLUT_ELAPSED_TIME)
	
	timeInterval = currentTime - previousTime
	
	if timeInterval > 1000:
		fps = frameCount / (timeInterval / 1000.0)
		
		previousTime = currentTime
		
		frameCount = 0

#------------Calcule la matrice de projection selon la position des yeux---------
def calcProjection():
	global ex,ey,ez, scale
	global oldTime, newTime
	global screenW, screenH
	global Debug
	#--------ALGO CALCUL MATHEMATIQUE DE LA MATRICE DE PROJECTION-------
	
	#Profondeur de vue (f=>far)
	f = 15.0
	
	#Distance minimale de vue (n => near)
	n = 1.0
	

	#RAPPEL : le centre de l'écran est l'origine du repère
	pa=array([-screenW/2.0,-screenH/2.0,0.0])#le bord gauche de l'écran 
	pb=array([screenW/2.0,-screenH/2.0,0.0])#le bord droit
	pc=array([-screenW/2.0,+screenH/2.0,0.0])#le bord haut gauche
	
	pe=array([ex,ey,ez])
	
	vr = subtract(pb,pa)
	
	vu=subtract(pc, pa)
	
	
	normvr = linalg.norm(vr)
	vr = dot(vr,1.0/normvr)
	
	normvu = linalg.norm(vu)
	vu = dot(vu, 1.0/normvu)
	
	vn = cross(vr,vu)
	normvn=linalg.norm(vn)
	vn=dot(vn, 1.0/normvn)
	
	va=subtract(pa,pe)
	
	vb=subtract(pb,pe)
	
	vc=subtract(pc,pe)
	
	d=-dot(va,vn)
	
	l = dot(vr,va) * (n / d)
	r = dot(vr,vb)*(n/d)
	b = dot(vu, va) * (n / d)
	t = dot(vu, vc) * (n / d) 
	
	#DEBUG, affiche la position des yeux toutes les 1/2 secondes
	if Debug == 1:
		newTime = time.time()
		if (newTime - oldTime) > 0.5:
			print "\n-------- DEBUG --------"
			print "Coordonnées des yeux : (" + str(ex) +", "+ str(ey) + ", " + str(ez) + ")"
			print "Distance yeux/écran : " + str(d) + "mm"
			print "FPS : " + str(fps) + " longueur = " + str(len(str(fps)))+"\n"
			oldTime = newTime
	
	M=(vr[0],vu[0],vn[0],0,vr[1],vu[1],vn[1],0,vr[2],vu[2],vn[2],0,0,0,0,1.0)
	glFrustum(l,r,b,t,n,f)
	glMultMatrixf(M)
	glTranslatef(-pe[0], -pe[1], -pe[2])		
		
#Reçoit les messages du client contenant les coordonnées des yeux
def coordonnee_callback(path, args):
	global ex,ey,ez
	ex,ey,ez = args

#ne devrait jamais être appelée
def fallback(path, args, types, src):
	print "Message inconnu '%s' depuis '%s'" % (path, src.get_url())
	for a, t in zip(args, types):
		print "arguments de type '%s': %s" % (t, a)
		
		
def LoadTextures():
    # Chargement de l'image
    try:
    	timage = Image.open("target_256x256.png")
    except IOError, err:
    	print "Impossible de charger le fichier !" + str(err)
    	sys.exit(1)

    ix = timage.size[0]
    iy = timage.size[1]
    image = timage.tostring("raw", "RGBA", 0, -1)

    # Paramètres de la texture	
    glTexImage2D(GL_TEXTURE_2D, 0, 4, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
   

def InitGL(Width, Height):
	#glViewport(0,0, Width, Height)
	LoadTextures()
    
	glClearAccum(0.0,0.0,0.0,0.0)
	glClearColor(0.0, 0.0, 0.0, 0.0)	# Repeint l'arrière plan en noir à chaque nouvelle frame
	glClearDepth(1.0)					
	glDepthFunc(GL_LESS)				
	glEnable(GL_DEPTH_TEST)					
	

#Fonction principale de dessin 
def DrawGLScene():
	#Permet de modifier facilement la position de la scène (pour tests)
	global posx,posy,posz
	global server
	server.recv(0)
	
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	
	#Calcul matrice projection en fonction position tête
	calcProjection()
	
	glMatrixMode(GL_MODELVIEW)

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_ACCUM_BUFFER_BIT);	# Vide l'écran et le tampon de profondeur
	
	glLoadIdentity()				
	glTranslate(posx,posy,posz)
	
	#drawRepere()
		
	#--------------INSERER ICI DESSIN DE LA SCENE-------------------------	
	
		
	#dessine le tunnel de ligne	
	xg,xd,yb,yh,z,maxz = dessineTunnel()
	
	#dessineCible()
	
	#Cube de debug
	glPushMatrix()
	#glScale(scaling,scaling,scaling)
	glTranslate((xg+xd)/2.0,(yh+yb)/2.0,z - abs(z-maxz) / 2.0)
	print str(maxz)
	
	
	dessineCube(0.1)
	glPopMatrix()
	"""
	glPushMatrix()
	glTranslate(-10.0,10.0,20.0)
	dessineCube(10.0)
	glPopMatrix()

	glPushMatrix()
	glTranslate(10.0,0.0,60.0)
	dessineCube(15.0)
	glPopMatrix()"""
	
	
	#  since this is double buffered, swap the buffers to display what just got drawn. 
	glutSwapBuffers()
	calculeFPS()
	

def drawRepere() :
	glBegin(GL_LINES)	# Start Drawing The Cube
	glColor3ub(142,179,206)
	glVertex3f(0.0,0.0,0.0)
	glVertex3f(100.0,0.0,0.0)
	
	glColor3f(0.0,1.0,0.0)
	glVertex3f(0.0,0.0,0.0)
	glVertex3f(0.0,100.0,0.0)
	
	glColor3f(0.0,0.0,1.0)
	glVertex3f(0.0,0.0,0.0)
	glVertex3f(0.0,0.0,100.0)
	glEnd()	

def dessineCube(size):
	glBegin(GL_QUADS)			# Start Drawing The Cube
	
	glColor3f(0.0,1.0,0.0)			# Set The Color To Blue
	glVertex3f( size, size,-size)		# Top Right Of The Quad (Top)
	glVertex3f(-size, size,-size)		# Top Left Of The Quad (Top)
	glVertex3f(-size, size, size)		# Bottom Left Of The Quad (Top)
	glVertex3f( size, size, size)		# Bottom Right Of The Quad (Top)
	
	glColor3f(1.0,0.5,0.0)			# Set The Color To Orange
	glVertex3f( size,-size, size)		# Top Right Of The Quad (Bottom)
	glVertex3f(-size,-size, size)		# Top Left Of The Quad (Bottom)
	glVertex3f(-size,-size,-size)		# Bottom Left Of The Quad (Bottom)
	glVertex3f( size,-size,-size)		# Bottom Right Of The Quad (Bottom)
	
	glColor3f(1.0,0.0,0.0)			# Set The Color To Red
	glVertex3f( size, size, size)		# Top Right Of The Quad (Front)
	glVertex3f(-size, size, size)		# Top Left Of The Quad (Front)
	glVertex3f(-size,-size, size)		# Bottom Left Of The Quad (Front)
	glVertex3f( size,-size, size)		# Bottom Right Of The Quad (Front)
	
	glColor3f(1.0,1.0,0.0)			# Set The Color To Yellow
	glVertex3f( size,-size,-size)		# Bottom Left Of The Quad (Back)
	glVertex3f(-size,-size,-size)		# Bottom Right Of The Quad (Back)
	glVertex3f(-size, size,-size)		# Top Right Of The Quad (Back)
	glVertex3f( size, size,-size)		# Top Left Of The Quad (Back)
	
	glColor3f(0.0,0.0,1.0)			# Set The Color To Blue
	glVertex3f(-size, size, size)		# Top Right Of The Quad (Left)
	glVertex3f(-size, size,-size)		# Top Left Of The Quad (Left)
	glVertex3f(-size,-size,-size)		# Bottom Left Of The Quad (Left)
	glVertex3f(-size,-size, size)		# Bottom Right Of The Quad (Left)
	
	glColor3f(1.0,0.0,1.0)			# Set The Color To Violet
	glVertex3f( size, size,-size)		# Top Right Of The Quad (Right)
	glVertex3f( size, size, size)		# Top Left Of The Quad (Right)
	glVertex3f( size,-size, size)		# Bottom Left Of The Quad (Right)
	glVertex3f( size,-size,-size)		# Bottom Right Of The Quad (Right)
	glEnd()				# Done Drawing The Quad

translat = 1.0
sens = 1.0
oTAnim = time.time()
def dessineCible():
	global translat, sens, nTAnim, oTAnim
#Définit les coordonnées des vertex
	x = (-70.0, -7.0, -80.0, 50.0,40.0, -150.0, -40.0, 0.0, 75.0,40.0, 0.0, 75.0,-70.0, -7.0, -80.0, -60.0, -30.0)
	y = (5.0, -2.0, 40.0, 45.0, 5.0, 8.0, 0.0, 10.0, -10.0, 45.0, 5.0, 8.0, -40, -20, -10, 40.0, 45.0)
	z = (550.0, 620.0, 460.0, 390.0, 470.0, 560.0, 470.0, 500.8, 470.0, 10.0, 59.0, 100.0,20.0,75.0,150.0, 300.0, 350.0)
	
	for i in range(len(x)):
		glPushMatrix()
		scaling = 1
		glTranslatef(x[i], y[i], z[i]-50 + translat) 
		glScale(scaling, scaling, scaling)
		glColor3ub(255,250,254)	
		glLineWidth(0.1)	
		glBegin(GL_LINES)
		glVertex3f(0.0,0.0,0.0)
		glVertex3f(0.0,0.0, -500)
		glEnd()
		glColor3f(1.0,1.0,1.0)
		glEnable(GL_TEXTURE_2D)
		#Ces deux lignes suppriment les pixels transparents de la texture
		glEnable(GL_ALPHA_TEST)
		glAlphaFunc(GL_GREATER, 0.0) 
		#Les carrés contenant la texture de la cible
		glBegin(GL_QUADS)			  
		glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  0.0)	# Bas gauche
		glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  0.0)	# Bas droite
		glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  0.0)	# Haut droit
		glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0,  0.0)	# Haut gauche
		glEnd()
		glDisable(GL_ALPHA_TEST)
		glDisable(GL_TEXTURE_2D)
		
		nTAnim = time.time()
		if (nTAnim - oTAnim) > 0.01: 
			if translat >= 99 or translat < 1.0: sens = -sens
			translat = (translat + sens*0.01) % 10
			otAnim = nTAnim
		glPopMatrix()	
		
	
def dessineTunnel() :
	global screenW, screenH
	
	modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
	projection = glGetDoublev(GL_PROJECTION_MATRIX)
	viewport = glGetIntegerv(GL_VIEWPORT)
	
	winxg = float(viewport[0]) 
	winyb = float(viewport[1])
	
	#Bas | Gauche
	coord = gluUnProject(winxg,winyb,0.0,modelview,projection,viewport)
	xg = coord[0]
	yb = coord[1]
	z = coord[2]
	
	#Haut
	winyh = float(viewport[3])
	coord = gluUnProject(winxg,winyh,0.0,modelview,projection,viewport)
	yh = coord[1]
		
	#Droit
	winxd = float(viewport[2])
	coord = gluUnProject(winxd,winyb,0.0,modelview,projection,viewport)
	xd = coord[0]
		
	maxz = z - 5
	
	glColor3f(1.0,0.0,0.0)

	glBegin(GL_LINES)
	
	largeur = abs(xd-xg)
	nbLignes = 10
	espacementX = largeur / nbLignes
	i = xg
	while i <= xd:
		#sol
		glVertex3f(i,yb,z)
		glVertex3f(i,yb,maxz)
		
		#plafond
		glVertex3f(i,yh,z)
		glVertex3f(i,yh,maxz)
		
		i = i + espacementX
	
	hauteur = abs(yh-yb)
	nbLignes = 10
	espacementY = hauteur / nbLignes
	i = yb
	#Parralèles au sol
	while i <= yh:
		#Mur gauche
		glVertex3f(xg, i, z)
		glVertex3f(xg,i,maxz)
		#Mur droit
		glVertex3f(xd,i,z)
		glVertex3f(xd,i,maxz)
		i = i + espacementY
	#Colonnes	
	i = z
	espacementZ = 0.3
	while i >= maxz:
		#Mur gauche
		glVertex3f(xg,yb,i)
		glVertex3f(xg,yh,i)
		#Mur droit
		glVertex3f(xd,yb,i)
		glVertex3f(xd,yh,i)
		
		#Sol
		glVertex3f(xg,yb,i)
		glVertex3f(xd,yb,i)
		
		#Plafond
		glVertex3f(xg,yh,i)
		glVertex3f(xd,yh,i)
		
		i = i - espacementZ
		
	glEnd()
	return(xg,xd,yb,yh,z,maxz)

def showFPS(x,y,z):
	global fps
	fpsArrondi = int(fps)
	ch_fps = [int(nbr) for nbr in str(fpsArrondi)]
	
	glTranslate(-x,-y,-z)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glEnable(GL_BLEND)
	glEnable(GL_LINE_SMOOTH)
	glLineWidth(2.0)
	glutBitmapCharacter(GLUT_BITMAP_8_BY_13, 'A')
	glDisable(GL_BLEND)
	glDisable(GL_LINE_SMOOTH)
	
	
	
pas = 1
# DEBUG au clavier 
def keyPressed(*args):
	global ex,ey,ez,posx,posy,posz
	global thread, fullscreen, pas, Debug
	#pas = 10#le pas de déplacement
	touche = args[0]
	if pas <= 0 : pas = 1
	#Simulation du deplacement des yeux
	if touche == GLUT_KEY_UP:		
		ez -= pas
	elif touche == GLUT_KEY_DOWN:
		ez += pas 
	elif touche == GLUT_KEY_RIGHT:
		ex += pas
	elif touche == GLUT_KEY_LEFT:
		ex -= pas
	elif touche == 'w':
		pas = pas + 2
	elif touche == 'x':
		pas = pas - 2
	elif touche == 'z':
		ey += pas
	elif touche == 's':
		ey -= pas
	elif touche == 'i':
		posy += pas
	elif touche == 'k':
		posy -= pas
	elif touche =='j':
		posx -= pas
	elif touche == 'l':
		posx += pas
	elif touche == 'y':
		posz += pas*3.0
	elif touche == 'h':
		posz -= pas
	elif touche == 'd':
		if Debug == 0: Debug = 1
		else : Debug = 0
	elif touche == 'f':
		if fullscreen == 0:
			glutFullScreen()
			fullscreen = 1
		elif fullscreen == 1:
			glutReshapeWindow(640,480)
			fullscreen = 0
	if touche == ESCAPE:
	    glutDestroyWindow(window)
	    #thread.join(0.1)
	    sys.exit()


#rafraichit l'affichage    
def refresh(argInutile):
	global FIX_60_FPS, FIX_30_FPS
	glutTimerFunc(FIX_30_FPS, refresh,FIX_30_FPS)
	glutPostRedisplay()
	
def main():
	global window
	global server
	global FIX_60_FPS 
	global FIX_30_FPS
	FIX_60_FPS = int(1000.0/60.0)
	FIX_30_FPS = int(1000.0/30.0)
	glutInit()

	# Select type of Display mode:   
	#  Double buffer 
	#  RGBA color
	# Alpha components supported 
	# Depth buffer
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_ACCUM)
	
	glutInitWindowSize(640, 480)
	
	glutInitWindowPosition(0, 0)
	
	window = glutCreateWindow("Scene")

	#Enregistre la fonction appelée pour dessiner la scène (callback)	
	glutDisplayFunc(DrawGLScene)
	glutTimerFunc(FIX_60_FPS, refresh,FIX_60_FPS)
		
	glutReshapeFunc(InitGL)
	
	#permet du debug au clavier 
	glutKeyboardFunc(keyPressed)
	glutSpecialFunc(keyPressed)
	
	# Initialise la fenêtre OpenGL
	InitGL(640, 480)
	


print "Appuyez sur ECHAP pour quitter"

if __name__ == '__main__':

	initConfig()
	print "Appuyez sur F pour activer/désactiver le mode plein écran"
	#---------MISE EN ROUTE SERVEUR LIBLO----------
	try:
		server = liblo.Server(port)
	except liblo.ServerError, err:
		print str(err)
		sys.exit()
		
	#Définit les méthodes appelées quand le serveur liblo reçoit des données
	#la méthode qui reçoit les coordonnées des yeux
	server.add_method("/coordonnees/", 'fff', coordonnee_callback)
	#la méthode par défaut si des données non formatées sont reçues(ne devrait pas arriver)
	server.add_method(None, None, fallback)
	
	main()

	glutMainLoop()


	
    	