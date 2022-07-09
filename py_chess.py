import pygame_menu
import chess
import chess.engine
import os
import pygame
import pyautogui
import time

GREEN = (118,150,86)
WHITE = (220, 220, 220)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()

pygame.init()
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Chess')
pygame.display.set_icon(pygame.image.load("images/chess-board.png"))

def main():
    global SCREEN, CLOCK
    pygame.init()

    engine = chess.engine.SimpleEngine.popen_uci(r"D:\py projects\chess\stockfish_15_win_x64_avx2\stockfish_15_win_x64_avx2\stockfish_15_x64_avx2.exe")
    board = chess.Board()
    while not board.is_game_over():
        blockSize = 50 
        i = 0
        j = 0
        for y in range(0, WINDOW_HEIGHT, blockSize):
            for x in range(0, WINDOW_WIDTH, blockSize):
                rect = pygame.Rect(y, x, blockSize, blockSize)
                if i%2==0:
                    if j%2==0:pygame.draw.rect(SCREEN, WHITE, rect)
                    else:
                        pygame.draw.rect(SCREEN, GREEN, rect)
                else:
                    if j%2==0:pygame.draw.rect(SCREEN, GREEN, rect)
                    else:
                        pygame.draw.rect(SCREEN, WHITE, rect)
                j+=1
            i+=1

        result = engine.play(board, chess.engine.Limit(time=0.1))
        board.push(result.move)
        print(board)
    
        pgn = board.epd()
        pieces = [] 
        pieces_ = pgn.split(" ", 1)[0]
        rows = pieces_.split("/")
        for row in rows:
            for thing in row:
                if thing.isdigit():
                    for i in range(0, int(thing)):
                        pieces.append('.')
                else:
                    pieces.append(thing)
        

        i=0
        for y in range(0, WINDOW_HEIGHT, blockSize):
            for x in range(0, WINDOW_WIDTH, blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                if pieces[i]!='.':
                    if pieces[i].isupper(): 
                        img = 'images/Chess_'+str(pieces[i])+'dt60.png'
                    else:
                        img = 'images/Chess_'+str(pieces[i])+'lt60.png'
                    auto=pygame.image.load(img)
                    #auto=pygame.transform.scale(auto,(50, 50))
                    SCREEN.blit(auto, (x-5,y-5))
                i+=1
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(0)

        pygame.display.update()
    

    print(str(board.outcome()))
    if board.outcome().winner!=None:
        winner = "White win" if not board.outcome().winner else "Black win"
    else:
        winner = "tie"
    print(winner)
    #pyautogui.alert(winner)
    i=0
    for y in range(0, WINDOW_HEIGHT, blockSize):
        for x in range(0, WINDOW_WIDTH, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            if pieces[i]!='.':
                if pieces[i].isupper(): 
                    img = 'images/Chess_'+str(pieces[i])+'dt60.png'
                else:
                    img = 'images/Chess_'+str(pieces[i])+'lt60.png'
                auto=pygame.image.load(img)
                #auto=pygame.transform.scale(auto,(50, 50))
                SCREEN.blit(auto, (x-5,y-5))
            i+=1
    #data = pygame.image.tostring(surface, 'RGBA')
    show_winner(winner)

def show_winner(winner):
    global SCREEN
    while True:
        font = pygame.font.Font("college.ttf", 50)
        text = font.render(winner, True, (255,153,51))
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        SCREEN.blit(text, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(0)
    
        pygame.display.update()


def show_menu():
    menu = pygame_menu.Menu('Chess', WINDOW_WIDTH, WINDOW_HEIGHT,
                        theme=pygame_menu.themes.THEME_GREEN)
    menu.add.button('Play', main)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    
    menu.mainloop(surface)

show_menu()
#show_winner("black win")