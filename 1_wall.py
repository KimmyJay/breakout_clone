import pygame

#initialize game
pygame.init()

#set screen width and height
screen_width = 600
screen_height = 600

#display screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Breakout Clone')

#background color
bg = (20, 20, 20)

#block colors
block_red = (242, 85, 96)
block_green = (86, 174, 87)
block_blue = (69, 177, 232)

#define columns and rows for grid
cols = 6
rows = 6

#create wall class
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
                rect = pygame.Rect(block_x, block_y, self.width, self.height) #create rect value based on x,y coordinates and width and heigh value
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

                #create borders
                pygame.draw.rect(screen, bg, (block[0]), 2)

#create a wall instance
wall = wall()
#call create_wall method
wall.create_wall()

run = True
while run:

    #create background
    screen.fill(bg)

    #draw wall
    wall.draw_wall()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    pygame.display.update()

pygame.quit()