import pygame

pygame.init() # 초기화 (반드시 필요)

bg = (234, 218, 184)


# 화면 크기 설정
screen_width = 800 # 가로 크기
screen_height = 600 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Brick Game") # 게임 이름

# 배경색 생성
bg = (234, 218, 184)

#벽돌색 생성
block_red = (242, 85, 96)
block_green = (86, 174, 87)
block_blue = (69, 177, 232)


#캐릭터 이미지 불러오기
character = pygame.image.load("/Users/franciskim/Desktop/Web_Development/Sparta/projects/brickgame/images/character.png")
character_size = character.get_rect().size # 캐릭터 크기를 구해옴
character_width = character_size[0] # 캐릭터의 가로 크기
character_height = character_size[1] # 캐릭터의 세로 크기
character_x_pos = (screen_width / 2) - (character_width / 2) # 화면 가로의 절반 크기에 해당하는 곳에 위치 (가로)
character_y_pos = screen_height - character_height # 화면 세로 크기 가장 아래에 해당하는 곳에 위치 (세로)

#defines number of cols and rows for creating a grid system
cols = 6
rows = 6

#brick wall class
class wall():
    def __init__(self):
        self.width = screen_width // cols
        self.height = 50

    def create_wall(self):
        #define an empty list that will be used as full list of blocks
        self.blocks = []
        #define an empty list for an individual block
        block_individual = []
        for row in range(rows):
            #reset the block row list for each iteration
            block_row = []
            #iterate through each column in that row
            for col in range(cols):
                #generate x and y positions for each block and create a rectangle from that
                block_x_pos = col * self.width #x_pos shift by width value for each iteration
                block_y_pos = row * self.height #y_pos maintains constant
                rect = pygame.Rect(block_x_pos, block_y_pos, self.width, self.height)
                #assign block strength based on row
                #blocks closer to player will be more durable
                if row < 2:
                    strength = 3
                elif row < 4:
                    strength = 2
                elif row < 6:
                    strength = 1
                #store the rect and color data
                block_individual = [rect, strength]
                #append that individual block to the block row
                block_row.append(block_individual)
            #append the row to the full list of blocks
            self.blocks.append(block_row)


    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                #assign color based on strength value
                if block[1] == 3:
                    block_col = block_blue
                elif block[1] == 2:
                    block_col = block_green
                elif block[1] == 1:
                    block_col = block_red
                pygame.draw.rect(screen, block_col, block[0])
                pygame.draw.rect(screen, bg, (block[0]), 2)



#create an instance of class wall
wall = wall()
wall.create_wall()


# 이벤트 루프
running = True # 게임이 진행중인가?
while running:

    #draw wall
    screen.fill(bg)  # 배경 그리기
    screen.blit(character, (character_x_pos, character_y_pos))  # 캐릭터 그리기

    wall.draw_wall()

    for event in pygame.event.get(): # 어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생하였는가?
            running = False # 게임이 진행중이 아님

    pygame.display.update() # 게임화면을 다시 그리기!

# pygame 종료
pygame.quit()