import pygame
import math 

def Load_Sprites(spritesheet, rectangle, colorkey = None):
    rect = pygame.Rect(rectangle) #Create rectangle 
    frame = pygame.Surface(rect.size) #Create surface from rectangle size
    frame.blit(spritesheet, (0,0), rect) #Draws frame onto surface
    if colorkey is not None:
        frame.set_colorkey(colorkey, pygame.RLEACCEL) #Set transparency
    return frame

class Characters(object):
	def __init__(self, x, y, width, height, color):
		self.x = x
		self.y = y
		self.width = width
		self.height = height		
		self.color = color

		self.bullets=[]
		self.cooldown = 0
		self.invul = 0 
		self.health = 1

		#Load Sprites
		self.frame = 0
		self.spritesheet = pygame.image.load("Bulbasaur.png").convert() 
		self.sprites = []
		for y in range(2):
			for x in range(15):
				self.sprites.append(Load_Sprites(self.spritesheet, (x*30,y*30,30,30), colorkey=(0,128,192)))
		#Animation States
		self.direction = 'Left'
		self.flip = 0
		self.walk = False
		self.attack = False 
		self.hit = False
		self.knocked = False
		self.frame_dictionary = {'Down': {'Hit': 25, 'Attack': 15, 'Walk':0}, 
								'Down Left': {'Hit': 26, 'Attack': 17, 'Walk':3},  
								'Left': {'Hit': 27, 'Attack': 19, 'Walk':6},
								'Up Left': {'Hit': 28, 'Attack': 21, 'Walk':9},
								'Up': {'Hit': 29, 'Attack': 23, 'Walk':12},
								'Down Right': {'Hit': 26, 'Attack': 17, 'Walk':3},  
								'Right': {'Hit': 27, 'Attack': 19, 'Walk':6},
								'Up Right': {'Hit': 28, 'Attack': 21, 'Walk':9},
								}

	def frames(self):
		if self.walk or self.attack:
			self.frame += 0.25 

		if self.hit:
			self.frame = self.frame_dictionary[self.direction]['Hit'] #Hit frame
		elif self.attack:
			if self.frame<self.frame_dictionary[self.direction]['Attack'] or self.frame>self.frame_dictionary[self.direction]['Attack']+1.75:
				self.frame = self.frame_dictionary[self.direction]['Attack'] #Set to attack frame
		elif self.walk:
			if self.frame<self.frame_dictionary[self.direction]['Walk'] or self.frame>self.frame_dictionary[self.direction]['Walk']+2.75:
				self.frame = self.frame_dictionary[self.direction]['Walk']
		else: #Standing still 
			self.frame = self.frame_dictionary[self.direction]['Walk']
				
		if self.frame>self.frame_dictionary[self.direction]['Attack']+1:
			self.attack = False #Toggles "Attack" state
		
		if not self.invul:
			self.hit = False #Once invulnerability ends, toggle "Hit" state

		if self.direction == 'Down Right' or self.direction == 'Right' or self.direction == 'Up Right':
			self.flip = 1
		else:
			self.flip = 0

		print(self.frame)

class Enemies(object):
	def __init__(self,x,y, width, height, color):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.color = color
		self.invul = False
		self.health = 1
		self.speed = 0.50

		#Load Frames
		self.frame = 0
		self.spritesheet = pygame.image.load("Grimer.png").convert() 
		self.sprites = []
		for y in range(2):
			for x in range(15):
				self.sprites.append(Load_Sprites(self.spritesheet, (x*30,y*30,30,30), colorkey=(0,128,192)))

		#Animation States
		self.direction = 'Left'
		self.flip = 0
		self.hit = False 
		self.attack = False 
		self.walk = True
		self.knocked = False
		self.frame_dictionary = {'Down': {'Hit': 25, 'Attack': 15, 'Walk':0}, 
								'Down Left': {'Hit': 26, 'Attack': 17, 'Walk':3},  
								'Left': {'Hit': 27, 'Attack': 19, 'Walk':6},
								'Up Left': {'Hit': 28, 'Attack': 21, 'Walk':9},
								'Up': {'Hit': 29, 'Attack': 23, 'Walk':12},
								'Down Right': {'Hit': 26, 'Attack': 17, 'Walk':3},  
								'Right': {'Hit': 27, 'Attack': 19, 'Walk':6},
								'Up Right': {'Hit': 28, 'Attack': 21, 'Walk':9},
								}

	def frames(self):
		if self.hit:
			self.frame = self.frame_dictionary[self.direction]['Hit'] #Hit frame
		elif self.attack:
			if self.frame<self.frame_dictionary[self.direction]['Attack'] or self.frame>self.frame_dictionary[self.direction]['Attack']+1:
				self.frame = self.frame_dictionary[self.direction]['Attack'] #Set to attack frame
		elif self.walk:
			if self.frame<self.frame_dictionary[self.direction]['Walk'] or self.frame>self.frame_dictionary[self.direction]['Walk']+2:
				self.frame = self.frame_dictionary[self.direction]['Walk']
		else: #Standing still 
			self.frame = self.frame_dictionary[self.direction]['Walk']
		
		if self.walk or self.attack:
			self.frame += 0.25 
		
		if self.frame>self.frame_dictionary[self.direction]['Attack']+1:
			self.attack = False #Toggles "Attack" state
		
		if not self.invul:
			self.hit = False #Once invulnerability ends, toggle "Hit" state

		if self.direction == 'Down Right' or self.direction == 'Right' or self.direction == 'Up Right':
			self.flip = 1
		else:
			self.flip = 0

def Move_Object(obj):
	speed = 1
	if pygame.key.get_pressed()[pygame.K_w]:
		if pygame.key.get_pressed()[pygame.K_a]: #Move Up-Left
			obj.x -= speed * 0.707
			obj.y -= speed * 0.707
			obj.direction = 'Up Left'
			obj.walk = True
		elif pygame.key.get_pressed()[pygame.K_d]: #Move Up-Right
			obj.x += speed * 0.707
			obj.y -= speed * 0.707
			obj.direction = 'Up Right'
			obj.walk = True
		else: #Move Up 
			obj.y -= speed
			obj.direction = 'Up' 
			obj.walk = True
	elif pygame.key.get_pressed()[pygame.K_s]:
		if pygame.key.get_pressed()[pygame.K_a]: #Move Down-Left
			obj.x -= speed * 0.707 
			obj.y += speed * 0.707
			obj.direction = 'Down Left' 
			obj.walk = True
		elif pygame.key.get_pressed()[pygame.K_d]: #Move Down-Right
			obj.x += speed * 0.707
			obj.y += speed * 0.707
			obj.direction = 'Down Right' 
			obj.walk = True
		else: #Move Down
			obj.y += speed 
			obj.direction = 'Down' 
			obj.walk = True
	elif pygame.key.get_pressed()[pygame.K_a]: #Move Left
		obj.x -= speed
		obj.direction = 'Left' 
		obj.walk = True
	elif pygame.key.get_pressed()[pygame.K_d]: #Move Right
		obj.x += speed
		obj.direction = 'Right'
		obj.walk = True
	else:
		obj.walk = False

	if obj.x < 0: #If object exceeds left boundary
		obj.x = 0
	elif obj.x > 400-5: #If object exceeds right boundary
		obj.x = 400-5

	if obj.y < 0: #If object exceeds top boundary
		obj.y = 0
	elif obj.y > 300-10: #If object exceeds bottom boundary
		obj.y = 300-10	

class Projectiles(object):
	def __init__(self, x, y, direction, color, speed):
		self.x = x
		self.y = y
		self.color = color
		self.direction = direction
		self.speed = speed
		self.radius = 3
	def Move(self, win):
		if self.direction == 'Up Left':
			self.x -= self.speed * 0.707
			self.y -= self.speed * 0.707
		elif self.direction == 'Up':
			self.y -= self.speed
		elif self.direction == 'Up Right':
			self.x += self.speed * 0.707
			self.y -= self.speed * 0.707
		elif self.direction == 'Right':
			self.x += self.speed
		elif self.direction == 'Down Right':
			self.x += self.speed * 0.707
			self.y += self.speed * 0.707
		elif self.direction == 'Down':
			self.y += self.speed
		elif self.direction == 'Down Left':
			self.x -= self.speed * 0.707
			self.y += self.speed * 0.707
		elif self.direction == 'Left':
			self.x -= self.speed

		pygame.draw.circle(win, self.color, (round(self.x), round(self.y)), self.radius)

def Shoot(obj):
	if pygame.key.get_pressed()[pygame.K_j]:
		if obj.cooldown == 0:
			obj.attack = True 
			obj.bullets.append(Projectiles(obj.x, obj.y, obj.direction, (255,255,255), 5))
			obj.cooldown = 10
	if obj.cooldown>0:
		obj.cooldown -= 1
def Collision(obj, proj, enemy):
	if proj.x < 0: #If object exceeds left boundary
		obj.bullets.pop(obj.bullets.index(proj)) 
	elif proj.x > 400-proj.radius: #If object exceeds right boundary
		obj.bullets.pop(obj.bullets.index(proj)) 
	if proj.y < 0: #If object exceeds top boundary
		obj.bullets.pop(obj.bullets.index(proj)) 
	elif proj.y > 300-proj.radius: #If object exceeds bottom boundary
		obj.bullets.pop(obj.bullets.index(proj)) 

	if enemy.health>0:
		if proj.x > enemy.x and proj.x < enemy.x+enemy.width:
			if proj.y > enemy.y and proj.y < enemy.y+enemy.height: 
				obj.bullets.pop(obj.bullets.index(proj)) 
				enemy.hit = True
				enemy.health -= 1
def Object_Collision(hunter, target):
	knock_back = 10
	if not target.invul:
		if hunter.x+hunter.width>target.x and hunter.x<target.x: #Right boundary
			if hunter.y<target.y+target.height and hunter.y+hunter.height>target.y+target.height: 
				target.knocked = True
				target.hit = True #Hit from bottom left
			elif hunter.y+hunter.height>target.y and hunter.y<target.y:
				target.knocked = True
				target.hit = True #Hit from top left
			elif hunter.y == target.y or hunter.y+hunter.height == target.y+target.height:
				target.knocked = True
				target.hit = True #Hit from left 
		elif hunter.x+hunter.width>target.x+target.width and hunter.x<target.x+target.width: #Left boundary
			if hunter.y<target.y+target.height and hunter.y+hunter.height>target.y+target.height: 
				target.knocked = True
				target.hit = True #Hit from bottom right
			elif hunter.y+hunter.height>target.y and hunter.y<target.y:
				target.knocked = True
				target.hit = True #Hit from top right
			elif hunter.y == target.y or hunter.y+hunter.height == target.y+target.height:
				target.knocked = True
				target.hit = True #Hit from right
		elif hunter.y+hunter.height>target.y+target.height and hunter.y<target.y+target.height:
			if hunter.x == target.x or hunter.x+hunter.width == target.x+target.width:
				target.knocked = True
				target.hit = True #Hit from bottom
		elif hunter.y+hunter.height>target.y and hunter.y<target.y: #Bottom boundary
			if hunter.x == target.x or hunter.x+hunter.width == target.x+target.width:
				target.knocked = True
				target.hit = True #Hit from top 
		else:
			target.knocked = False
			target.hit = False

	if target.knocked:
		target.invul = 10
		target.health -= 1

		if hunter.x - target.x > 5: #Knock left
			if hunter.y - target.y > 5: #Knock up left
				target.x -= knock_back *.707
				target.y -= knock_back *.707
			elif target.y - hunter.y > 5: #Knock down left
				target.x -= knock_back *.707
				target.y += knock_back *.707				
			else:
				target.x -= knock_back
		elif target.x - hunter.x > 5: #Knock right
			if hunter.y - target.y > 5: #Knock up right
				target.x += knock_back *.707
				target.y -= knock_back *.707
			elif target.y - hunter.y > 5: #Knock down right
				target.x += knock_back *.707
				target.y += knock_back *.707				
			else:
				target.x += knock_back
		elif hunter.y - target.y > 5: #Knock up
			target.y -= knock_back
		elif target.y - hunter.y > 5:  #Knock down
			target.y += knock_back
		else:
			target.y += knock_back	
		target.knocked = False	


def Invulnerable(obj):
	if obj.invul > 0:
		obj.invul -= 1

def Hunt(hunter, target):
	if not target.invul: 
		if hunter.y>target.y:
			if hunter.x>target.x: #Move Up-Left
				hunter.x -= hunter.speed * 0.707
				hunter.y -= hunter.speed * 0.707
			elif hunter.x<target.x: #Move Up-Right
				hunter.x += hunter.speed * 0.707
				hunter.y -= hunter.speed * 0.707
			else: #Move Up 
				hunter.y -= hunter.speed
		elif hunter.y<target.y:
			if hunter.x>target.x: #Move Down-Left
				hunter.x -= hunter.speed * 0.707 
				hunter.y += hunter.speed * 0.707
			elif hunter.x<target.x: #Move Down-Right
				hunter.x += hunter.speed * 0.707
				hunter.y += hunter.speed * 0.707
			else: #Move Down
				hunter.y += hunter.speed
		elif hunter.x>target.x: #Move Left
			hunter.x -= hunter.speed
		elif hunter.x<target.x: #Move Right
			hunter.x += hunter.speed

		if hunter.x - target.x > 5: #Knock left
			if hunter.y - target.y > 5: #Knock up left
				hunter.direction = 'Up Left'
			elif target.y - hunter.y > 5: #Knock down left
				hunter.direction = 'Down Left'
			else:
				hunter.direction = 'Left'
		elif target.x - hunter.x > 5: #Knock right
			if hunter.y - target.y > 5: #Knock up right
				hunter.direction = 'Up Right'
			elif target.y - hunter.y > 5: #Knock down right
				hunter.direction = 'Down Right'
			else:
				hunter.direction = 'Right'
		elif hunter.y - target.y > 5: #Knock up
			hunter.direction = 'Up'
		elif target.y - hunter.y > 5:  #Knock down
			hunter.direction = 'Down'

def main():
	win = pygame.display.set_mode((400, 300))
	pygame.init()

	Red_Guy = Characters(100, 100, 10, 20,  (255, 0, 0))
	Blue_Guy = Enemies(200, 100, 10, 20, (0, 0, 255))

	bullets = []

	while True:
		frames = 30
		clock=pygame.time.Clock()
		clock.tick(frames)

		for event in pygame.event.get(): #Exit game on red button
			if event.type == pygame.QUIT:
				return
		win.fill((0,0,0))
		
		Move_Object(Red_Guy)
		pygame.draw.rect(win, Red_Guy.color, (Red_Guy.x, Red_Guy.y, Red_Guy.width, Red_Guy.height))
		#win.blit(Red_Guy.sprites[0], (Red_Guy.x-8, Red_Guy.y-9)) #Draw sprite

		Red_Guy.frames()
		win.blit(pygame.transform.flip(Red_Guy.sprites[math.floor(Red_Guy.frame)],Red_Guy.flip,0),(Red_Guy.x-11,Red_Guy.y-9))

		Shoot(Red_Guy) 

		
		for bullet in Red_Guy.bullets:
			bullet.Move(win)
			Collision(Red_Guy, bullet, Blue_Guy)
		
		if Blue_Guy.health>0:
			pygame.draw.rect(win, Blue_Guy.color, (Blue_Guy.x, Blue_Guy.y, Blue_Guy.width, Blue_Guy.height))
			Hunt(Blue_Guy, Red_Guy)
			Object_Collision(Blue_Guy, Red_Guy)
			Blue_Guy.frames()
			win.blit(pygame.transform.flip(Blue_Guy.sprites[math.floor(Blue_Guy.frame)],Blue_Guy.flip,0),(Blue_Guy.x-11,Blue_Guy.y-9))

		Invulnerable(Red_Guy)

		pygame.display.flip()

main()
