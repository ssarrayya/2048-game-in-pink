import pygame
import random
import sys
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'  # centers the window
pygame.init()

# setting up paths
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except AttributeError:
        base_path = os.path.abspath(".")  # Development
    return os.path.join(base_path, relative_path)

font_path = resource_path(os.path.join("assets", "OpenDyslexic3-Bold.ttf"))
my_font = pygame.font.Font(font_path, 24)

high_score_path = resource_path(os.path.join("assets", "high_score"))

# initial set-up
WIDTH=550
HEIGHT=700
screen=pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption('Accessible 2048')
timer=pygame.time.Clock()
fps=60
font=my_font
previous_board=None
previous_score=0

# 2048 game color library
colors={0: (250,224,228),
          2: (247,202,208),
          4: (249,190,199),
          8: (251,177,189),
          16: (255,153,172),
          32: (255,133,161),
          64: (255,112,150),
          128: (255,107,149),
          256: (255,77,109),
          512: (255,10,84),
          1024: (201,24,74),
          2048: (164,19,60),
          'light text': (255, 255, 255),
          'dark text': (11, 11, 11),
          'other': (0, 0, 0),
          'bg': (187, 173, 160)}

# game variables initialize
board_values=[[0 for _ in range(4)] for _ in range(4)]
game_over=False
spawn_new=True
init_count=0
direction=''
score=0
file=open(high_score_path, 'r')
init_high=int(file.readline())
file.close()
high_score=init_high

# draw game over and restart text
def draw_over():
    pygame.draw.rect(screen, 'black', [50, 50, 300, 100], 0, 10)
    game_over_text1=font.render('Game Over!', True, 'white')
    game_over_text2=font.render('Press Enter to Restart', True, 'white')
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))

# take your turn based on direction
def take_turn(direc, board):
    global score
    merged=[[False for _ in range(4)] for _ in range(4)]
    if direc=='UP':
        for i in range(4):
            for j in range(4):
                shift=0
                if i > 0:
                    for q in range(i):
                        if board[q][j]==0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j]=board[i][j]
                        board[i][j]=0
                    if board[i - shift - 1][j]==board[i - shift][j] and not merged[i - shift][j] \
                            and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] *= 2
                        score += board[i - shift - 1][j]
                        board[i - shift][j]=0
                        merged[i - shift - 1][j]=True

    elif direc=='DOWN':
        for i in range(3):
            for j in range(4):
                shift=0
                for q in range(i + 1):
                    if board[3 - q][j]==0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j]=board[2 - i][j]
                    board[2 - i][j]=0
                if 3 - i + shift <= 3:
                    if board[2 - i + shift][j]==board[3 - i + shift][j] and not merged[3 - i + shift][j] \
                            and not merged[2 - i + shift][j]:
                        board[3 - i + shift][j] *= 2
                        score += board[3 - i + shift][j]
                        board[2 - i + shift][j]=0
                        merged[3 - i + shift][j]=True

    elif direc=='LEFT':
        for i in range(4):
            for j in range(4):
                shift=0
                for q in range(j):
                    if board[i][q]==0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift]=board[i][j]
                    board[i][j]=0
                if board[i][j - shift]==board[i][j - shift - 1] and not merged[i][j - shift - 1] \
                        and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift]=0
                    merged[i][j - shift - 1]=True

    elif direc=='RIGHT':
        for i in range(4):
            for j in range(4):
                shift=0
                for q in range(j):
                    if board[i][3 - q]==0:
                        shift += 1
                if shift > 0:
                    board[i][3 - j + shift]=board[i][3 - j]
                    board[i][3 - j]=0
                if 4 - j + shift <= 3:
                    if board[i][4 - j + shift]==board[i][3 - j + shift] and not merged[i][4 - j + shift] \
                            and not merged[i][3 - j + shift]:
                        board[i][4 - j + shift] *= 2
                        score += board[i][4 - j + shift]
                        board[i][3 - j + shift]=0
                        merged[i][4 - j + shift]=True
    return board


# spawn in new pieces randomly when turns start
def new_pieces(board):
    count=0
    full=False
    while any(0 in row for row in board) and count < 1:
        row=random.randint(0, 3)
        col=random.randint(0, 3)
        if board[row][col]==0:
            count+=1
            if random.randint(1, 10)==10:
                board[row][col]=4
            else:
                board[row][col]=2
    if count < 1:
        full=True
    return board, full


# draw background for the board
def draw_board():
    board_size = 400
    board_x = (WIDTH - board_size) // 2
    board_y = (HEIGHT - board_size) // 2

    pygame.draw.rect(screen, colors['bg'], [board_x, board_y, board_size, board_size], 0, 10)

    score_text = font.render(f'Score: {score}', True, 'white')
    high_score_text = font.render(f'High Score: {high_score}', True, 'white')
    score_rect = score_text.get_rect(topleft=(board_x, board_y + board_size + 12))
    screen.blit(score_text, score_rect)

    # Position high score just to the right of the score
    high_score_text = font.render(f'High Score: {high_score}', True, 'white')
    high_score_rect = high_score_text.get_rect(topleft=(board_x, score_rect.bottom + 10))
    screen.blit(high_score_text, high_score_rect)

# draw tiles for game
def draw_pieces(board):
    # tile / spacing settings (matches your previous sizes) 
    tile_size = 75 
    gap = 20 
    cols = 4 
    # total width occupied by tiles and internal gaps (no extra outer padding) 
    grid_width = cols * tile_size + (cols - 1) * gap 

    board_size = 400
    board_x = (WIDTH - board_size) // 2
    board_y = (HEIGHT - board_size) // 2

    # start positions: center the tile-grid inside the board rectangle
    start_x = board_x + (board_size - grid_width) // 2
    start_y = board_y + (board_size - grid_width) // 2

    for i in range(4):
        for j in range(4):
            value = board[i][j]
            value_color = colors['light text'] if value > 8 else colors['dark text']
            color = colors[value] if value <= 2048 else colors['other']

            # Centered tile positions
            tile_x = board_x + j * 95 + 20
            tile_y = board_y + i * 95 + 20

            pygame.draw.rect(screen, color, [tile_x, tile_y, 75, 75], 0, 5)

            if value > 0:
                value_len = len(str(value))
                font_tile = pygame.font.Font(font_path, 48 - (5 * value_len))
                value_text = font_tile.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(tile_x + 37, tile_y + 37))
                screen.blit(value_text, text_rect)

            pygame.draw.rect(screen, 'black', [tile_x, tile_y, 75, 75], 2, 5)


# main game loop
run=True
while run:
    timer.tick(fps)
    screen.fill('#494955')
    draw_board()
    draw_pieces(board_values)
    if spawn_new or init_count < 2:
        board_values, game_over=new_pieces(board_values)
        spawn_new=False
        init_count+=1
    if direction!='':
        import copy
        previous_board = copy.deepcopy(board_values)
        previous_score = score
        # Then make the move
        board_values=take_turn(direction, board_values)
        direction=''
        spawn_new=True
    if game_over:
        draw_over()
        if high_score > init_high:
            file=open(high_score_path, 'w')
            file.write(f'{high_score}')
            file.close()
            init_high=high_score

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_UP:
                direction='UP'
            elif event.key==pygame.K_DOWN:
                direction='DOWN'
            elif event.key==pygame.K_LEFT:
                direction='LEFT'
            elif event.key==pygame.K_RIGHT:
                direction='RIGHT'
            elif event.key == pygame.K_u:
                if previous_board is not None:
                    board_values = [row[:] for row in previous_board]
                    score = previous_score
                    spawn_new = False  # Don’t spawn a new tile after undo

            if game_over:
                if event.key==pygame.K_RETURN:
                    board_values=[[0 for _ in range(4)] for _ in range(4)]
                    spawn_new=True
                    init_count=0
                    score=0
                    direction=''
                    game_over=False

    if score > high_score:
        high_score=score

    pygame.display.flip()
pygame.quit()