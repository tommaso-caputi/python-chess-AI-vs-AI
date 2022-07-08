import pygame_menu
import chess
import chess.engine
import os
import pygame
import pyautogui
import time

pygame.init()
surface = pygame.display.set_mode((400, 400))

def main():
    GREEN = (118,150,86)
    WHITE = (200, 200, 200)
    WINDOW_HEIGHT = 400
    WINDOW_WIDTH = 400
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(GREEN)

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
                    auto=pygame.transform.scale(auto,(50, 50))
                    SCREEN.blit(auto, (x,y))
                i+=1
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(0)

        pygame.display.update()
    

    print(str(board.outcome()))
    if board.outcome().winner!=None:
        winner = "White win" if not board.outcome().winner else "GREEN win"
    else:
        winner = "tie"
    print(winner)
    pyautogui.alert(winner)
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
                auto=pygame.transform.scale(auto,(50, 50))
                SCREEN.blit(auto, (x,y))
            i+=1
    show_menu()


def show_menu():
    menu = pygame_menu.Menu('Chess', 400, 400,
                        theme=pygame_menu.themes.THEME_DEFAULT)
    menu.add.button('Play', main)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(surface)

show_menu()