import pygame, sys
from pygame.locals import *
import random

WINDOWWIDTH = 500 # Chiều dài cửa sổ
WINDOWHEIGHT = 600 # Chiều cao cửa sổ
BLOCK_SIZE = 30
COLUM = 10
ROW = 20
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLACK = (0, 0, 0)
Cubes = {
    1 :[[[1, 0, 0],
         [1, 1, 1],
         [0 ,0 ,0]],
        
        [[0, 1, 0],
         [0, 1, 0],
         [1, 1, 0]],

        [[1, 1, 1],
         [0, 0, 1],
         [0, 0, 0]],

        [[1, 1, 0],
         [1, 0, 0],
         [1, 0, 0]]],

    2: [[[0, 0, 1],
         [1, 1, 1],
         [0, 0, 0]],
          
        [[1, 1, 0],
         [0, 1, 0],
         [0, 1, 0]],
          
        [[1, 1, 1],
         [1, 0, 0],
         [0, 0, 0]],
           
        [[1, 0, 0],
         [1, 0, 0],
         [1, 1, 0]]],

    3: [[[0, 1, 1],
         [1, 1, 0],
         [0 ,0 ,0]],

        [[1, 0, 0],
         [1, 1, 0],
         [0, 1, 0]]],

    4: [[[1, 1, 0],
         [0, 1, 1],
         [0, 0, 0]],
          
        [[0, 1, 0],
         [1, 1, 0],
         [1, 0, 0]]],

    5: [[[1, 1, 1, 1],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
    
        [[0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0]]],

    6: [[[1 ,1],
         [1, 1]],
         
        [[1, 1],
         [1, 1]]],

    7: [[[0, 1, 0],
         [1, 1, 1],
         [0, 0, 0]],

        [[0, 1, 0],
         [1, 1, 0],
         [0, 1, 0]],
         
        [[1, 1, 1],
         [0, 1, 0],
         [0, 0, 0]],
         
        [[0, 1, 0],
         [0, 1, 1],
         [0, 1, 0]]]
}

GRID = []
for i in range (ROW):
    GRID.append([])
    for j in range (COLUM):
        GRID[i].append(0)

pygame.init()

### Xác định FPS ###
FPS = 120
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Tetris')
boardsurf = pygame.Surface((302, 600), SRCALPHA)
font = pygame.font.SysFont(None, 24)
active_game = False

class Score(): ## Bảng điểm
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.level = 1
        self.time = 500
    def draw_score_board(self): ## vẽ bảng điểm
        pygame.draw.rect(DISPLAYSURF, BLACK, (330, 80, 150, 100), 1)
        score_surf = font.render(f'Score: {self.score}', True, RED)
        DISPLAYSURF.blit(score_surf, (350, 130))
        highscore_surf = font.render(f'High score: {self.high_score}', True, RED)
        DISPLAYSURF.blit(highscore_surf, (350, 100))
        level_surf = font.render(f'Level: {self.level}', True, RED)
        DISPLAYSURF.blit(level_surf, (350, 150))

    def increase_level(self): ## check level
        if self.score < 10:
            self.time = 500
            self.level = 1
        elif self.score < 400:
            self.time = 100
            self.level = 2
        elif self.score < 600:
            self.time = 300
            self.level = 3
        elif score.score < 800:
            self.time = 200
            self.level = 4
        else:
            self.time = 100
            self.level = 5
        pygame.time.set_timer(automove, score.time)
score = Score()

class Board(): ## Board chơi game
    def __init__(self):
        self.grid = GRID

    def draw_line(self): ## vẽ các đường kẻ
        for i in range (COLUM+1): 
            pygame.draw.line(boardsurf, BLACK, (i*BLOCK_SIZE, 0), (i*BLOCK_SIZE, 600))
        for i in range (ROW+1):
            pygame.draw.line(boardsurf, BLACK, (0, i*BLOCK_SIZE), (300, i*BLOCK_SIZE))
        DISPLAYSURF.blit(boardsurf, (0,0))

    def draw_board(self): ## vẽ các ô của bảng
        for i in range (len(self.grid)):
            for j in range (len(self.grid[i])):
                if self.grid[i][j] == 0:
                    pygame.draw.rect(boardsurf, WHITE, (j*BLOCK_SIZE, i*BLOCK_SIZE, 30, 30))
                else :
                    pygame.draw.rect(boardsurf, RED, (j*BLOCK_SIZE, i*BLOCK_SIZE, 30, 30))

    def checkscore(self, i):
        for j in range (COLUM):
            if self.grid[i][j] == 0:
                return False
        return True

    def remove_row(self): ## xóa hàng khi đã lấp đầy
        count = 0
        for i in range (ROW):
            if self.checkscore(i):
                score.score += 10
                count += 1
        grid1 = [grid for grid in self.grid if grid != [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        grid2 = []
        for i in range (count):
            grid2.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.grid = grid2 + grid1
        score.increase_level()

    def overgame(self): ## kết thúc game
        score.high_score = max(score.score, score.high_score)
        for i in range (ROW):
            for j in range (COLUM):
                self.grid[i][j] = 0
        score.score = 0
        score.level = 1
        score.time = 500
        self.draw_board()
        score.draw_score_board()
        pygame.time.set_timer(automove, score.time)
board = Board()

class Cube(): ## Khối hình
    def __init__(self, id):
        self.id = id
        self.state = 0
        self.layout = Cubes[id] 
        self.col_pos = 4
        self.row_pos = -2

    def draw_squar(self, x, y, color):
        pygame.draw.rect(boardsurf, color, (x, y, 30, 30))

    def draw_cube(self): ## vẽ khối hình
        for i in range (len(self.layout[self.state])):
            for j in range (len(self.layout[self.state][i])):
                if self.layout[self.state][i][j] == 1:
                    self.draw_squar((self.col_pos+j)*BLOCK_SIZE, (self.row_pos+i)*BLOCK_SIZE, RED)

    def remove_cube(self): ## xóa khối hình
        for i in range (len(self.layout[self.state])):
            for j in range (len(self.layout[self.state][i])):
                if self.layout[self.state][i][j] == 1:
                    self.draw_squar((self.col_pos+j)*BLOCK_SIZE, (self.row_pos+i)*BLOCK_SIZE, WHITE)

    def moveR(self): ## dịch phải
        if self.check(self.col_pos+1, self.row_pos, self.state) :
            self.remove_cube()
            self.col_pos += 1
            self.draw_cube()

    def moveL(self): ## dịch trái
        if self.check(self.col_pos-1, self.row_pos, self.state):
            self.remove_cube()
            self.col_pos -= 1
            self.draw_cube()

    def rotate(self): ## xoay
        if self.check(self.col_pos, self.row_pos, (self.state + 1) % len(self.layout)):
            self.remove_cube()
            self.state = (self.state + 1) % len(self.layout)
            self.draw_cube

    def moveD(self): ## di chuyển xuống
        global active_game
        if self.check(self.col_pos, self.row_pos+1, self.state):
            self.remove_cube()
            self.row_pos += 1
            self.draw_cube()
            return True
        if (self.row_pos<=0):
            active_game = False
            board.overgame()
        else: 
            self.collide()
        return False

    def check(self, nextcol, nextrow, state): ## kiểm tra di chuyển
        for i in range (len(self.layout[state])):
            for j in range (len(self.layout[state][i])):
                if self.layout[state][i][j] == 1 and nextrow >=0:
                    if nextcol + j < 0 or nextcol + j + 1 > COLUM or nextrow + i + 1 > ROW or board.grid[i+nextrow][j+nextcol] == 1:
                        return False
        return True

    def collide(self): ## xử lý khi gạch chạm sàn
        global active_game
        for i in range (len(self.layout[self.state])):
            for j in range (len(self.layout[self.state][i])):
                if self.layout[self.state][i][j] == 1:
                    board.grid[i+self.row_pos][j+self.col_pos] = 1
        board.remove_row()
        board.draw_board()

nextcube_surf  = pygame.Surface((121, 61), SRCALPHA) 
class Next_cube: ## Khối hình tiếp theo
    def __init__(self) :
        self.next_cube = Cube(random.randint(1, 7))

    def draw(self):
        for i in range (5): 
            pygame.draw.line(nextcube_surf, BLACK, (i*BLOCK_SIZE, 0), (i*BLOCK_SIZE, 60))
        for i in range (3):
            pygame.draw.line(nextcube_surf, BLACK, (0, i*BLOCK_SIZE), (120, i*BLOCK_SIZE))
        DISPLAYSURF.blit(nextcube_surf, (350,400))

    def draw_cube(self):
        for i in range (2):
            for j in range (4):
                pygame.draw.rect(nextcube_surf, GREEN, (j*BLOCK_SIZE, i*BLOCK_SIZE, 30, 30))
        for i in range (len(self.next_cube.layout[self.next_cube.state])):
            for j in range (len(self.next_cube.layout[self.next_cube.state][i])):
                if self.next_cube.layout[self.next_cube.state][i][j] == 1:
                    pygame.draw.rect(nextcube_surf, RED, (j*BLOCK_SIZE, i*BLOCK_SIZE, 30, 30))
next = Next_cube()

cube = Cube(random.randint(1, 7))
automove = pygame.USEREVENT + 1
pygame.time.set_timer(automove, score.time)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if active_game == True:
            if event.type == automove:
                if not cube.moveD():
                    cube = next.next_cube
                    next.next_cube = Cube(random.randint(1, 7))

            if event.type == KEYDOWN:
                if event.key == K_LEFT: 
                    cube.moveL()
                if event.key == K_RIGHT:
                    cube.moveR()
                if event.key == K_UP:
                    cube.rotate() 
                if event.key == K_DOWN:
                    if not cube.moveD():
                        cube = next.next_cube
                        next.next_cube = Cube(random.randint(1, 7))
            next.draw_cube()

        if event.type == KEYDOWN:               
            if event.key == K_SPACE and active_game == False:
                active_game = True

    DISPLAYSURF.fill(GREEN)
    
    score.draw_score_board()
    board.draw_line()
    board.draw_board()
    cube.draw_cube()
    next.draw()
    pygame.display.update()
    fpsClock.tick(FPS)