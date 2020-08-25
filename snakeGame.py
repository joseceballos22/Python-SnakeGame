"""
File: snakeGame.py
Goal: To Create the Snake Game Using OOP
"""

import pygame

from enum import Enum 

import random 

pygame.init()



class Entity:

	def __init__(self, pos = [0,0], imageFile = "temp.png", width = 20, height = 20):

		#Saving the Position of the Entity 
		self.pos = pos 
		self.image = pygame.image.load(imageFile)
		#Ensuring Entity is to the correct Dimensions 
		self.image = pygame.transform.scale(self.image, (width, height))

	#All Entities Will have Different Update Methods 
	def update(self, keys, dt):
		pass

	#Drawing the Image on to the screen 
	def draw(self, screen):
		screen.blit(self.image, (self.pos[0], self.pos[1]))


#Helps With Player Class
class Dir(Enum):
	UP = 1
	DOWN = 2
	RIGHT = 3
	LEFT = 4


class Player(Entity):

	def __init__(self, speed, pos, imageFile, screenD):
		
		super().__init__(pos, imageFile)
		self.speed = speed 

		self.dir = Dir.RIGHT #Initially Direction is to the Right 

		self.screenW = screenD[0]
		self.screenH = screenD[1]

	#Updates the Player 
	def update(self, keys, dt):

		if self.__checkBorder() == True: 
			#Constantly Moving the Player 
			self.__movePlayer(dt)
		
		#Updating the Direction of the Player 
		self.__changeDir(keys) 




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
			self.pos[1] += dt * self.speed * -1 

		if self.dir == Dir.DOWN: 
			self.pos[1] += dt * self.speed 

		if self.dir == Dir.RIGHT:
			self.pos[0] += dt * self.speed 

		if self.dir == Dir.LEFT:
			self.pos[0] += dt * self.speed * -1 

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

		#Initially the Position of the Fruit will be random 

		randX = random.randint(0, screenD[0])
		randY = random.randint(0, screenD[1])
		pos = [randX, randY]
		
		super().__init__(pos, imageFile)



	#Overriding the update method 
	def update(self, keys, dt):
		pass




#Main Game Class
class Game:

	def __init__(self, screenW = 800, screenH = 800):

		#Creating a Screen to draw everything on 
		self.screen = pygame.display.set_mode((screenW, screenH))

		#speed, position , imageFile
		self.player = Player(0.5, [400,400], "head.png", [screenW, screenH])

		pygame.display.set_caption("Jc Snake Game")

		#Fruit 
		#ImageFile, screenD
		self.fruit = Fruit("temp.png", [screenW, screenH])

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
		self.player.update(keys,dt)

		self.fruit.update(keys,dt)

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