import pygame
import time
from threading import Thread
import socket
import math

TCP_IP = '127.0.0.1'
TCP_PORT = 2311
BUFFER_SIZE = 1024

WHITE =(255,255,255)

UP = False
DOWN = False
LEFT = False
RIGHT = False

EXIT = False

def CheckInput():
	global UP
	global DOWN
	global LEFT
	global RIGHT
	global EXIT
	pressed = pygame.key.get_pressed()
	if pressed[pygame.K_UP] or pressed[pygame.K_w]:
		UP =True
	else:
		UP =False
	if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
		DOWN =True
	else:
		DOWN =False
	if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
		LEFT =True
	else:
		LEFT =False
	if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
		RIGHT =True
	else:
		RIGHT =False
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			EXIT = True
		

def ShowText(text, poz, col):
	global screen
	global myfont
	label = mainFont.render(text, 1, col)
	screen.blit(label, poz)

def DrawEverything():
	screen.fill((0,0,0))
	screen.blit(gameMap,(-player.x,-player.y))
	i=1
	while i<len(otherPlayers):
		temp=pygame.transform.rotate(enemyImage,float(otherPlayers[i+1]));	
		screen.blit(temp,(float(otherPlayers[i-1])-player.x+(screenSize[0]//2),float(otherPlayers[i])-player.y+(screenSize[0]//2)))
		i+=3
	#pygame.draw.rect(screen, WHITE, pygame.Rect(characterPos[0],characterPos[1],10,10))
	temp=pygame.transform.rotate(player.image,player.rotation);	
	screen.blit(temp,(screenSize[0]//2,screenSize[1]//2))
	
	


def KeepReciving():
	global otherPlayers
	while not EXIT:
		data = s.recv(BUFFER_SIZE)
		data = data.decode()
		if data[0]=='p':
			data=data[1:]
			otherPlayers = data.split(',')

class Character:
	rotation=0
	speed=0
	def __init__(self,x,y):
		self.x=x
		self.y=y
		self.image = pygame.image.load("./desertArrow.png")
		self.rect = self.image.get_rect()
	
	def isCollidedWith(self, sprite):
		return self.rect.colliderect(sprite.rect)

otherPlayers =[]

pygame.init()

mainFont = pygame.font.Font("./upheavtt.ttf", 30)
screenSize =(700,700)
screen =pygame.display.set_mode(screenSize)
pygame.display.set_caption("Game")


player = Character(350, 350)


deg2Rad = 3.1415/180

lastTime = time.time()

enemyImage = pygame.image.load("./desertArrowEnemy.png")
gameMap = pygame.image.load("./map.png")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
timeToSendData=0;
reciving =  Thread(target=KeepReciving, args=())
reciving.start()
while not EXIT:
	deltaTime = time.time() -lastTime
	lastTime = time.time()
	if timeToSendData <=0:		
		timeToSendData = 0.01
		s.send(str.encode('p'+str(int(player.x))+','+str(int(player.y))+','+str(int(player.rotation))))
	else:
		timeToSendData-=deltaTime;
	CheckInput()
	if UP:
		if player.speed<150:
			player.speed+=deltaTime*100
		else:
			player.speed=150
	else:
		if player.speed>0:
			player.speed-=deltaTime*50
		if player.speed<0:
			player.speed+=deltaTime*50
	if DOWN:
		if player.speed>(-50):
			player.speed-=deltaTime*150
		else:
			player.speed = ( -50)
	if LEFT and player.speed!= 0:
		player.rotation+=deltaTime*(200-player.speed)*(player.speed/150)*2
	if RIGHT and player.speed!= 0:
		player.rotation-=deltaTime*(200-player.speed)*(player.speed/150)*2
	player.x -= math.sin(player.rotation*deg2Rad)*player.speed*deltaTime*2;
	player.y -= math.cos(player.rotation*deg2Rad)*player.speed*deltaTime*2;
	#ClampPosition()
	player.rect.x=player.x
	player.rect.y=player.y
	DrawEverything()
	pygame.display.flip()
s.close()
reciving.join()
