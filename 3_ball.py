import pygame
from pygame.locals import *

#initialize game
pygame.init()

#set screen width and height
screen_width = 600
screen_height = 600

#set screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Breakout Clone')

#background color
bg = (20, 20, 20)
#block colors
block_red = (242, 85, 96)
block_green = (86, 174, 87)
block_blue = (69, 177, 232)
#paddle colors
paddle_col = (77, 77, 77)
paddle_outline = (100, 100, 100)

#define columns and rows for grid
cols = 6
rows = 6

#set framerate
clock = pygame.time.Clock()
fps = 60

#wall class
class wall():
    #constructor method
    def __init__(self):
        #instance variables for setting width and height
        self.width = screen_width // cols # // yields an integer
        self.height = 50

    def create_wall(self):
        #list for collection of final blocks
        self.blocks = []
        #define an empty list for an individual block
        block_individual = []
        for row in range(rows):
            #reset the block row list for each row iteration
            block_row = []
            for col in range(cols):
                #generate x and y positions for each block and create a rectangle from that
                block_x = col * self.width #x_pos is updated for each col iteration
                block_y = row * self.height #y_pos remains constant as it is dependent on row value
                rect = pygame.Rect(block_x, block_y, self.width, self.height) #create rect value based on x,y coordinates and width and height value
                #assign block strength value based on row position
                #the closer the block is to the paddle, the more durable
                if row < 2:
                    strength = 3
                elif row < 4:
                    strength = 2
                elif row < 6:
                    strength = 1
                #create a list to store the rect and color data
                block_individual = [rect, strength]

                #append that individual block to the block row
                block_row.append(block_individual)

            #append the row to the full list of blocks
            self.blocks.append(block_row)


    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                #assign color based on block strength
                if block[1] == 3:
                    block_col = block_blue
                elif block[1] == 2:
                    block_col = block_green
                elif block[1] == 1:
                    block_col = block_red
                pygame.draw.rect(screen, block_col, block[0])
                pygame.draw.rect(screen, bg, (block[0]), 2) #creates a border effect

#paddle class
class paddle():
    def __init__(self):
        #1. define paddle variables: height, width, x and y coordinates
        #2. use rectangle function to create paddle based on those variables

        self.height = 20
        self.width = 80
        self.x = int((screen_width / 2) - (self.width / 2)) # x_coordinate: middle of screen
        self.y = screen_height - (self.height * 2)
        self.speed = 10
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.direction = 0 #tracks direction movement

        #1. reset movement direction
        #2. store key value pressed
        #3. set restrictions
    def move(self):
        self.direction = 0
        key = pygame.key.get_pressed()
        #if left key has been pressed...
        if key[pygame.K_LEFT] and self.rect.left > 0: #restrict paddle from moving off-screen
            #update paddle x coordinate
            self.rect.x -= self.speed
            #assign direction
            self.direction = -1

        if key[pygame.K_RIGHT] and self.rect.right < screen_width: #restrict paddle from moving off-screen
            #update paddle x coordinate
            self.rect.x += self.speed
            #assign direction
            self.direction = 1

    def draw(self):
        pygame.draw.rect(screen, paddle_col, self.rect)
        pygame.draw.rect(screen, paddle_outline, self.rect, 3) #creates a border effect

#ball class
class game_ball():
    #constructor method
    #an instance of a ball will have x, y coordinates ---> will later be used for draw()
    def __init__(self, x, y):
        #declare instance variables: radius, x and y position
        self.ball_rad = 10
        #remember we are working in a coordinate system where top left corner of screen is (0, 0)
        self.x = x - self.ball_rad #centralizes the ball position for later use
        self.y = y
        #create rectangle for hitbox purposes
        #Rect() takes in x, y coordinates, height, width
        self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2) #width and height for a ball is radius*2

        #ball initially moves northeast
        self.speed_x = 4
        self.speed_y = -4
        #set game_over to false/0 initially
        self.game_over = 0

    def move(self):
        
        #reverse direction of ball when it hits the sides of the screen
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *= -1

        #reverse direction of ball when it hits top of scren
        if self.rect.top < 0:
            self.speed_y *= -1

        #game ends if ball hits bottom of screen
        if self.rect.bottom > screen_height:
            #set game_over to -1 for later usage
            self.game_over = -1

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.game_over

    def draw(self):
        #draws a circle on surface = screen, color = paddle_col, center position and radius
        pygame.draw.circle(screen, paddle_col, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)
        #draws border for ball
        pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), 3)


#create a wall
wall = wall()
wall.create_wall()

#create a paddle
player_paddle = paddle()

#create a ball in relative position to paddle
ball = game_ball(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
run = True
while run:

    #set framerate
    clock.tick(fps)

    #create background
    screen.fill(bg)

    #draw wall
    wall.draw_wall()

    #draw paddle
    player_paddle.draw()
    player_paddle.move()

    #draw ball
    ball.draw()
    ball.move()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    pygame.display.update()

pygame.quit()