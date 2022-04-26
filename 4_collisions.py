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
            print(self.blocks)


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
        #set max speed to restrict ball moving too fast
        self.speed_max = 5
        #set game_over to false/0 initially
        self.game_over = 0

    def move(self):
        #collision_threshold
        collision_thresh = 5

        #start w/ assumption that wall has been completely destroyed
        wall_destroyed = 1
        row_count = 0
        #nested for loop that will iterate through each block in master block list
        for row in wall.blocks:
            item_count = 0
            for item in row:
                #if ball(self.rect) collides w/ brick(rect(item[0]))
                if self.rect.colliderect(item[0]):
                    #if collision occurs from bottom of ball/top of block and ball is moving downwards
                    if abs(self.rect.bottom - item[0].top) < collision_thresh and self.speed_y > 0:
                        self.speed_y *= -1
                    #if collision occurs from top of ball/bottom of block and ball is moving upwards
                    if abs(self.rect.top - item[0].bottom) < collision_thresh and self.speed_y < 0:
                        self.speed_y *= -1
                    #if collision occurs from right of ball/left of block and ball is moving rightwards
                    if abs(self.rect.right - item[0].left) < collision_thresh and self.speed_x > 0:
                        self.speed_x *= -1
                    #if collision occurs from left of ball/right of block and ball is moving rightwards
                    if abs(self.rect.left - item[0].right) < collision_thresh and self.speed_x < 0:
                        self.speed_x *= -1

                    #reduce block strength upon collision
                    #use row counter and item counter for to access individual block from master block list
                    #row_count and item_count both start at 0 such that we start from the first block in the list
                    if wall.blocks[row_count][item_count][1] > 1:
                         wall.blocks[row_count][item_count][1] -= 1
                    #break block if strengh < 1
                    #instead of deleting block, we update the block's properties to be void such that it will be erased from screen
                    else:
                        wall.blocks[row_count][item_count][0] = (0, 0, 0, 0)

                #check if block still exists, in which case the wall is not destroyed
                if wall.blocks[row_count][item_count][0] != (0, 0, 0, 0):
                    wall_destroyed = 0
                #increase item counter to move on to next block/item
                item_count += 1
            #increase row counter to move on to next row
            row_count += 1
        #after iterating through all the blocks, check if the wall is destroyed
        if wall_destroyed == 1:
            #player has won if wall is destroyed
            self.game_over = 1

        
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


        #paddle collision
        if self.rect.colliderect(player_paddle):
            #check if collision occurs from top of paddle and if the ball is moving downwards
            #if we flip direction when ball is moving upwards, we could end up in a scenario where y-dur is constantly flipped
            if abs(self.rect.bottom - player_paddle.rect.top) < collision_thresh and self.speed_y > 0:
                self.speed_y *= -1
                #ball speed increases or decreases depending on paddle direction
                self.speed_x += player_paddle.direction
                #restrict ball from exceeding max speed
                if self.speed_x > self.speed_max:
                    self.speed_x = self.speed_max
                #restrict ball from exceeding max speed when moving leftwards
                elif self.speed_x < 0 and self.speed_x < -self.speed_max:
                    self.speed_x = -self.speed_max
            
            #collision occurs from left of right of paddle
            else:
                self.speed_x *= -1

        #update ball direction
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