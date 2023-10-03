#from tkinter import S
import pygame_menu
import chess
import chess.engine
import os
import pygame

#stockfish_path = ( "stockfish_15_win_x64_avx2\stockfish_15_win_x64_avx2\stockfish_15_x64_avx2.exe")
stockfish_path = ("/opt/homebrew/opt/stockfish/bin/stockfish")
#kodomo_path = "komodo-13\komodo-13_201fd6\Windows\komodo-13.02-64bit.exe"
komodo_path = "komodo-14/OSX/komodo-14.1-64-osx"
GREEN = (118, 150, 86)
WHITE = (220, 220, 220)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()
engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
time_for_move = 0.1

pygame.init()
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Chess")
pygame.display.set_icon(pygame.image.load("images/chess-board.png"))


def set_engine(value, _):
    global engine
    print(value[0][1])
    l = [stockfish_path, komodo_path]
    engine = chess.engine.SimpleEngine.popen_uci(str(l[int(value[0][1])]))


def show_menu():
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    menu = pygame_menu.Menu(
        "Chess", WINDOW_WIDTH, WINDOW_HEIGHT, theme=pygame_menu.themes.THEME_GREEN
    )
    menu.add.button("Play", main)
    menu.add.selector(
        "Engine :", [("Stockfish 15", 0), ("Komodo 13", 1)], onchange=set_engine
    )
    menu.add.button("Quit", pygame_menu.events.EXIT)

    menu.mainloop(surface)


def main():
    global SCREEN, CLOCK, engine
    pygame.init()

    board = chess.Board()
    while not board.is_game_over():
        blockSize = 50
        i = 0
        j = 0
        for y in range(0, WINDOW_HEIGHT, blockSize):
            for x in range(0, WINDOW_WIDTH, blockSize):
                rect = pygame.Rect(y, x, blockSize, blockSize)
                if i % 2 == 0:
                    if j % 2 == 0:
                        pygame.draw.rect(SCREEN, WHITE, rect)
                    else:
                        pygame.draw.rect(SCREEN, GREEN, rect)
                else:
                    if j % 2 == 0:
                        pygame.draw.rect(SCREEN, GREEN, rect)
                    else:
                        pygame.draw.rect(SCREEN, WHITE, rect)
                j += 1
            i += 1

        result = engine.play(board, chess.engine.Limit(time=time_for_move))
        board.push(result.move)
        # print(board)

        pgn = board.epd()
        pieces = []
        pieces_ = pgn.split(" ", 1)[0]
        rows = pieces_.split("/")
        for row in rows:
            for thing in row:
                if thing.isdigit():
                    for i in range(0, int(thing)):
                        pieces.append(".")
                else:
                    pieces.append(thing)

        i = 0
        for y in range(0, WINDOW_HEIGHT, blockSize):
            for x in range(0, WINDOW_WIDTH, blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                if pieces[i] != ".":
                    if pieces[i].isupper():
                        img = "images/Chess_" + str(pieces[i]) + "dt60.png"
                    else:
                        img = "images/Chess_" + str(pieces[i]) + "lt60.png"
                    auto = pygame.image.load(img)
                    SCREEN.blit(auto, (x - 5, y - 5))
                i += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(0)

        pygame.display.update()

    print(str(board.outcome()))
    if board.outcome().winner != None:
        winner = "White win" if not board.outcome().winner else "Black win"
    else:
        winner = "tie"
    print(winner)
    i = 0
    for y in range(0, WINDOW_HEIGHT, blockSize):
        for x in range(0, WINDOW_WIDTH, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            if pieces[i] != ".":
                if pieces[i].isupper():
                    img = "images/Chess_" + str(pieces[i]) + "dt60.png"
                else:
                    img = "images/Chess_" + str(pieces[i]) + "lt60.png"
                auto = pygame.image.load(img)
                SCREEN.blit(auto, (x - 5, y - 5))
            i += 1
    pygame.image.save(surface, "image.jpg")
    show_winner(winner)


def show_winner(winner):
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT + 100))
    font = pygame.font.Font("college.ttf", 35)
    img = pygame.image.load(r"image.jpg")
    while True:
        text = font.render(winner, True, GREEN)
        text_rect = text.get_rect(center=(WINDOW_WIDTH / 4, WINDOW_HEIGHT / 8))
        SCREEN.blit(text, text_rect)
        SCREEN.blit(img, (0, 100))

        mouse = pygame.mouse.get_pos()
        if (
            WINDOW_WIDTH / 1.3 - 40 <= mouse[0] <= WINDOW_WIDTH / 1.3 + 40
            and WINDOW_HEIGHT / 8 - 10 <= mouse[1] <= WINDOW_HEIGHT / 8 + 10
        ):
            pygame.draw.rect(
                screen, WHITE, [WINDOW_WIDTH / 1.55, WINDOW_HEIGHT / 12.7, 97, 40]
            )
            txt = font.render("MENU", True, GREEN)
            txt_rect = txt.get_rect(center=(WINDOW_WIDTH / 1.3, WINDOW_HEIGHT / 8))
            screen.blit(txt, txt_rect)
        else:
            pygame.draw.rect(
                screen, (0, 0, 0), [WINDOW_WIDTH / 1.55, WINDOW_HEIGHT / 12.7, 97, 40]
            )
            txt = font.render("MENU", True, GREEN)
            txt_rect = txt.get_rect(center=(WINDOW_WIDTH / 1.3, WINDOW_HEIGHT / 8))
            screen.blit(txt, txt_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(mouse[0])
                print(mouse[1])
                if (
                    WINDOW_WIDTH / 1.3 - 40 <= mouse[0] <= WINDOW_WIDTH / 1.3 + 40
                    and WINDOW_HEIGHT / 8 - 10 <= mouse[1] <= WINDOW_HEIGHT / 8 + 10
                ):
                    show_menu()

        pygame.display.update()


show_menu()
# show_winner('sd')
