"""
File: snakeGame.py
Goal: To Create the Snake Game Using OOP
"""

import pygame

from enum import Enum 

import random 

pygame.init()


"""
	Things Todo: 
	- Link the Head Fruit and Body Together (BUG TAIL POSITION IS THE SAME AS PLAYER POSITION )
	- Make it so that if the head touches the body game over 
	- Game is Done 

"""


#Used to Detect Collisions Between Two Entities 
class Collision:
	

	def __init__(self, first, second):
		
		#Saving the Entities Used to check for collision 
		self.first = first 
		self.second = second 		

		#Getting Half Sizes of the Entities 
		self.firstHalfSize = (self.first.image.get_width() /2 , self.first.image.get_height() / 2)
		self.secondHalfSize = (self.second.image.get_width() /2 , self.second.image.get_height() / 2)

	def isColliding(self):

		entitiesColliding = False #initially False 

		#Dont Need to Saving it since it will constantly be changing 
		#Getting the Positions Of the two entities 
		firstPos = self.first.pos
		secondPos = self.second.pos 

		#Getting the Center of the Surfaces 
		firstCenter = (firstPos[0] - self.firstHalfSize[0], firstPos[1] - self.firstHalfSize[1])
		secondCenter = (secondPos[0] - self.secondHalfSize[0], secondPos[1] - self.secondHalfSize[1])


		#Calculating the Distance Between Both Centers 
		deltaX = abs(firstCenter[0] - secondCenter[0])
		deltaY = abs(firstCenter[1] - secondCenter[1])

		#Seeing if the Entities are intersecting 
		intersectX = deltaX - (self.firstHalfSize[0] + self.secondHalfSize[0])
		intersectY = deltaY - (self.firstHalfSize[1] + self.secondHalfSize[1])

		if intersectX < 0 and intersectY < 0:
			entitiesColliding = True 

		return entitiesColliding



class Entity:

	def __init__(self, pos = [0,0], imageFile = "temp.png", width = 20, height = 20):

		#Saving the Position of the Entity 
		self.pos = pos 
		self.image = pygame.image.load(imageFile)
		#Ensuring Entity is to the correct Dimensions 
		self.image = pygame.transform.scale(self.image, (width, height))

		self.colliding = False #Initially the entity is not colliding with anything 

	#All Entities Will have Different Update Methods 
	def update(self, keys, dt):
		pass

	#Drawing the Image on to the screen 
	def draw(self, screen):
		screen.blit(self.image, (self.pos[0], self.pos[1]))

	#Updates the Collision Variable of the entity 
	def setColliding(self, newValue):
		self.colliding = newValue


#Helps With Player Class
class Dir(Enum):
	UP = 1
	DOWN = 2
	RIGHT = 3
	LEFT = 4


class Player(Entity):

	def __init__(self, speed, pos, imageFile, screenD, width = 20, height = 20):
		
		super().__init__(pos, imageFile, width, height)
		self.speed = speed 

		self.dir = Dir.RIGHT #Initially Direction is to the Right 

		self.screenW = screenD[0]
		self.screenH = screenD[1]

		#Initially Empty 
		self.body = []

		#Stopping the Players From Moving 
		self.gameOver = False
	#Updates the Player 
	def update(self, keys, dt):

		if not self.gameOver: 
			if self.__checkBorder() == True: 
				#Constantly Moving the Player 
				self.__changeDir(keys) 
				self.__movePlayer(dt)

			#Updating Body
			self.__updateBody()



	#Moves the Body with the Player 
	def __updateBody(self):


		if len(self.body) > 0: 

			#Starting at the back
			for i in range(len(self.body) -1, 0, -1):
				self.body[i].pos = self.body[i-1].pos[:]

			tempPos = self.pos[:]
			self.body[0].pos = tempPos

	#Overriding the Draw Method So that it Draws the Body as well 
	def draw(self, screen):

		#Drawing the Body 
		for i in range(len(self.body)):
			screen.blit(self.body[i].image, (self.body[i].pos[0], self.body[i].pos[1]))
		
		#Drawing the Player 
		screen.blit(self.image, (self.pos[0], self.pos[1]))

	def growBody(self):

		#Checking if its the first element in the list 
		if len(self.body) == 0:
			#pos = [0,0], imageFile = "temp.png", width = 20, height = 20)
			tempPos = self.pos[:]
			for i in range(self.speed):
				self.body.append(Entity(tempPos, "body.png", self.image.get_width(), self.image.get_height()))	
		else:
			for i in range(self.speed):
				self.body.append(Entity(self.body[len(self.body) -1].pos, "body.png", self.image.get_width(), self.image.get_height()))
			pass

	#Updates the Direction of the Player 
	def __changeDir(self, keys):

		if keys[pygame.K_w] == True:
			self.dir = Dir.UP

		if keys[pygame.K_s] == True:
			self.dir = Dir.DOWN

		if keys[pygame.K_d] == True:
			self.dir = Dir.RIGHT

		if keys[pygame.K_a] == True:
			self.dir = Dir.LEFT

	#Constantly Moves the Player 
	def __movePlayer(self, dt):

		if self.dir == Dir.UP:
			#self.pos[1] += dt * self.speed * -1 
			self.pos[1] -= self.image.get_height() / self.speed

		if self.dir == Dir.DOWN: 
			#self.pos[1] += dt * self.speed 
			self.pos[1] += self.image.get_height() / self.speed

		if self.dir == Dir.RIGHT:
			#self.pos[0] += dt * self.speed 
			self.pos[0] += self.image.get_width() / self.speed

		if self.dir == Dir.LEFT:
			#self.pos[0] += dt * self.speed * -1 
			self.pos[0] -= self.image.get_width() / self.speed

	#Limits the Snake from going outside the border 
	def __checkBorder(self):

		#Checking X position 
		if self.pos[0] + self.image.get_width() < self.screenW and self.pos[0] > 0: 
			#Checking Y position 
			if self.pos[1] + self.image.get_height() < self.screenH and self.pos[1] > 0: 
				return True 
		#Else 
		return False 


class Fruit(Entity):

	def __init__(self, imageFile, screenD):
		
		super().__init__([0,0], imageFile)

		#Fruit will spawn randomly 
		randX = random.randint(0 + self.image.get_width(), screenD[0] - self.image.get_width())
		randY = random.randint(0 + self.image.get_height(), screenD[1] - self.image.get_height())
		pos = [randX, randY]
		self.pos = pos

		self.screenD = screenD.copy()


	#Overriding the update method 
	def update(self, keys, dt):
		
		if self.colliding == True: 
			#Moving position of Fruit 
			randX = random.randint(0 + self.image.get_width(), self.screenD[0] - self.image.get_width())
			randY = random.randint(0 + self.image.get_height(), self.screenD[1] - self.image.get_height())
			self.pos = [randX, randY]
			self.colliding = False #Resetting 

		pass




#Main Game Class
class Game:

	def __init__(self, screenW = 800, screenH = 800):

		#Creating a Screen to draw everything on 
		self.screen = pygame.display.set_mode((screenW, screenH))

		#speedReduction, position , imageFile
		self.player = Player(6, [400,400], "head.png", [screenW, screenH], 40,40)

		pygame.display.set_caption("Jc Snake Game")

		#Fruit 
		#ImageFile, screenD
		self.fruit = Fruit("temp.png", [screenW, screenH])

		#Used to Control Amount of Collisions that can occur 
		self.counter = 0 #Initially Zero 

		#First Entity, Second Entitiy
		self.collisionChecker = Collision(self.player, self.fruit)

	def start(self):
		self.__gameLoop()

	#Main Game Loop
	def __gameLoop(self):

		isOver = False #Initially False 

		#RGB
		SCREEN_COLOR = (100, 100, 200) 

		clock = pygame.time.Clock()

		#Main Game Loop 	
		while not isOver:

			#Controls Game Speed 
			dt = clock.tick(60)

			#Event Loop Handler 
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					isOver = True

			#Constantly updating the screen with this color 
			self.screen.fill(SCREEN_COLOR)

			keys = pygame.key.get_pressed()

			self.__updateComponents(keys, dt)

			self.__drawComponents()
			#Updating the Display 
			pygame.display.update()

		#Quitting Pygame 
		pygame.quit()

	#Updates all the Components of the Game 
	def __updateComponents(self, keys, dt):

		#Updating Collision First
		self.__updateCollision(dt)

		self.player.update(keys,dt)
		self.fruit.update(keys,dt)
		

	#Updates All Collisions of the game 
	def __updateCollision(self, dt):

		self.counter +=  dt

		# One Collision per 5 Frames 
		if self.counter > (dt * 4):

			#Player and Fruit are Colliding 
			if self.collisionChecker.isColliding() == True: 

				#Telling the Player to Grow a Tail 
				self.player.growBody()
				#Telling the Fruit to Move to a different location 
				self.fruit.colliding = True 
			#Resetting Counter 
			self.counter = 0 

		pass

	#Draws all the components of the Game 
	def __drawComponents(self):
		self.player.draw(self.screen)
		self.fruit.draw(self.screen)

def main():

	snakeGame = Game()

	snakeGame.start()

	pass

if __name__ == "__main__":
	main()