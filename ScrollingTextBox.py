import pygame
from pygame.locals import *

class ScrollingTextBox:
	def __init__(self,scrn,x_min,x_max,y_min,y_max):
		self.scrn = scrn
		pygame.font.init()
		self.fontDefault = pygame.font.Font( None, 20 )
		
		self.x_min = x_min
		self.x_max = x_max
		self.xPixLength = x_max - x_min
		self.y_min = y_min
		self.y_max = y_max
		self.yPixLength = y_max - y_min
		

		(width,height) = self.fontDefault.size('A')
		self.lineHeight = height
		self.maxLines = self.yPixLength / self.lineHeight



		self.lines = []
	
	def AddLine(self,newLine):

		if len(self.lines)+1 > self.maxLines:
			self.lines.pop(0)
		self.lines.append(newLine)
	
	def Add(self,message):

		(width,height) = self.fontDefault.size(message)
		remainder = ""
		if width > self.xPixLength:
			while width > self.xPixLength:
				remainder = message[-1] + remainder
				message = message[0:-1]
				(width,height) = self.fontDefault.size(message)
		
		if len(remainder) > 0:
			if message[-1].isalnum() and remainder[0].isalnum():
				remainder = message[-1] + remainder
				message = message[0:-1] + '-'
				if message[-2] == ' ':
					message = message[0:-1]
			
		self.AddLine(message)

		if len(remainder) > 0:

			while remainder[0] == ' ':
				remainder = remainder[1:len(remainder)]
			self.Add(remainder)

		
	def Draw(self):

		x_pos = self.x_min
		y_pos = self.y_min
		color = (255,255,255)
		antialias = 1
		for line in self.lines:
			renderedLine = self.fontDefault.render(line,antialias,color)
			self.scrn.blit(renderedLine,(x_pos,y_pos))
			y_pos = y_pos + self.lineHeight
		

		

if __name__ == "__main__":

	pygame.init()
	pygame.display.init()
	screen = pygame.display.set_mode((800,500))
	screen.fill( (0,0,0) )
	x_min = 400
	x_max = 750
	y_min = 100
	y_max = 400
	textbox = ScrollingTextBox(screen,x_min,x_max,y_min,y_max)
	
	textbox.Add("Hello!!!")
	textbox.Add("When requesting fullscreen display modes, sometimes an exact match for the requested resolution cannot be made. In these situations pygame will select the closest compatable match. The returned surface will still always match the requested resolution.")
	textbox.Add("Soup for me!")
	textbox.Add("Another data structure for which a list works well in practice, as long as the structure is reasonably small, is an LRU (least-recently-used) container. The following statements moves an object to the end of the list:")
	textbox.Add("Set the current alpha value fo r the Surface. When blitting this Surface onto a destination, the pixels will be drawn slightly transparent. The alpha value is an integer from 0 to 255, 0 is fully transparent and 255 is fully opaque. If None is passed for the alpha value, then the Surface alpha will be disabled.")
	textbox.Add("All pygame functions will automatically lock and unlock the Surface data as needed. If a section of code is going to make calls that will repeatedly lock and unlock the Surface many times, it can be helpful to wrap the block inside a lock and unlock pair.")
	textbox.Draw()
	pygame.display.flip()
	
	while 1:
		for e in pygame.event.get():
			if e.type is KEYDOWN:
				pygame.quit()
				exit()
			if e.type is MOUSEBUTTONDOWN:
				(mouseX,mouseY) = pygame.mouse.get_pos()
				textbox.Add("Mouse clicked at ("+str(mouseX)+","+str(mouseY)+")")
				textbox.Draw()
				pygame.display.flip()


