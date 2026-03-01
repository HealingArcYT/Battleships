import datetime
import time

import player as p
import pygame


if __name__ == "__main__":
    playerA = p.Player()
    playerB = p.Player()

    playerA.board.randomize_ships()

    for x in playerA.board.board:
        for y in x:
            print("X" if y.ship else "-", end=" ")
        print()
    print()
    for x in playerB.board.board:
        for y in x:
            print("X" if y.ship else "-", end=" ")
        print()

    pygame.init()
    screen = pygame.display.set_mode((404, 798))
    clock = pygame.time.Clock()
    running = True

    dt = 0

    state = "menu"

    pygame.font.init()

    font = pygame.font.SysFont("Arial", 20)

    AInotImplementedToast = -2000

    while running:
        print(state, dt)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.dict)
                if event.button == 1:
                    if (screen.get_width() / 2 - playPVP.get_width() / 2) <= event.pos[0] <= (
                            screen.get_width() / 2 + playPVP.get_width() / 2):
                        if (screen.get_height() / 2 - 40 - playPVP.get_height()) <= event.pos[1] <= (
                                screen.get_height() / 2 - 40):
                            state = "test"

                        if (screen.get_height() / 2 + 40) <= event.pos[1] <= (
                                screen.get_height() / 2 + 40 + playAI.get_height()):
                            print("ainotimplemented")
                            AInotImplementedToast = pygame.time.get_ticks()

        screen.fill("#005aff")

        pygame.draw.rect(screen, "#796596", pygame.Rect(10, 10, 384, 384))
        pygame.draw.rect(screen, "#796596", pygame.Rect(10, 404, 384, 384))

        for x in range(10):
            for y in range(10):
                width = 380 / 10

                # upper field
                pygame.draw.rect(screen, "#b0a8ba", pygame.Rect(10 + y * width + 4, 10 + x * width + 4, width - 4, width - 4))

                # lower field
                pygame.draw.rect(screen, "#b0a8ba", pygame.Rect(10 + y * width + 4, 404 + x * width + 4, width - 4, width - 4))

        if state == "menu":
            menu = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            menu.fill((0, 0, 0, 200))

            playPVP = pygame.Surface((200, 50))
            playPVP.fill("#ffb93b")
            pygame.draw.rect(playPVP, "#ff6b42", pygame.Rect(10, 10, 180, 30))
            playPVPtext = font.render("Player vs Player", True, "#1e1926")
            playPVP.blit(playPVPtext, ((playPVP.get_width() - playPVPtext.get_width()) / 2, (playPVP.get_height() - playPVPtext.get_height()) / 2))

            playAI = pygame.Surface((200, 50))
            playAI.set_alpha(80)
            playAI.fill("#ffb93b")
            pygame.draw.rect(playAI, "#ff6b42", pygame.Rect(10, 10, 180, 30))
            playAItext = font.render("Player vs Computer", True, "#1e1926")
            playAI.blit(playAItext, ((playAI.get_width() - playAItext.get_width()) / 2,
                                       (playAI.get_height() - playAItext.get_height()) / 2))

            menu.blit(playPVP,
                      (
                          menu.get_width() / 2 - playPVP.get_width() / 2,
                          menu.get_height() / 2 - 40 - playPVP.get_height())
                      )

            menu.blit(playAI,
                      (
                          menu.get_width() / 2 - playAI.get_width() / 2,
                          menu.get_height() / 2 + 40)
                      )

            if pygame.time.get_ticks() - AInotImplementedToast < 2000:
                toast = pygame.Surface((250, 50), pygame.SRCALPHA)
                toast.fill("#ffb93b")
                pygame.draw.rect(toast, "#ff6b42", pygame.Rect(10, 10, toast.get_width() - 20 , toast.get_height() - 20))
                toastText = font.render("AI not implemented yet", True, "#1e1926")
                toast.blit(toastText, (toast.get_width() / 2 - toastText.get_width() / 2, toast.get_height() / 2 - toastText.get_height() / 2))

                toast.set_alpha(255 - int(255 * ((pygame.time.get_ticks() - AInotImplementedToast) / 2000)))
                b = pygame.Surface((toast.get_width(), toast.get_height()), pygame.SRCALPHA)
                b.fill((0, 0, 0, 80))

                toast.blit(b, (0,0))

                menu.blit(toast, (menu.get_width() / 2 - toast.get_width() / 2, 30))

            screen.blit(menu, (0, 0))

        if state.startswith("setup"):
            ...

        if state == "test":
            #print("prerandom")
            #playerA.board.randomize_ships()
            #print("playera random")
            #playerB.board.randomize_ships()
            #print("playerb random")

            print("start draw ships")
            for x in range(10):
                for y in range(10):
                    width = 380 / 10

                    if playerA.board.board[x][y].ship:
                        print("ship")
                        # upper field
                        pygame.draw.rect(screen, "#e7a1ff",
                                         pygame.Rect(10 + y * width + 4, 10 + x * width + 4, width - 4, width - 4))

                    if playerB.board.board[x][y].ship:
                        # lower field
                        pygame.draw.rect(screen, "#e7a1ff",
                                         pygame.Rect(10 + y * width + 4, 404 + x * width + 4, width - 4, width - 4))

        pygame.display.flip()
        dt = clock.tick(60)/1000
    pygame.quit()