import pygame as pg, sys
from button import Button
from mr_test import Player, Enemy, Cloud
import random

pg.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
difficulty = 2
users = 1
score = 0
high_dict = {-1: "highscore_imp.txt", 0: "highscore_hard.txt", 1: "highscore_mid.txt", 2: "highscore_easy.txt"}

def get_font(size):
    return pg.font.Font("game_font.ttf", size)

def main_menu():
    while True:
        screen.blit(bg, (0, 0))

        menu_mouse_pos = pg.mouse.get_pos()

        menu_text = get_font(100).render("Börd Gäjm", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(640, 100))

        play_button = Button(image=pg.image.load("Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        options_button = Button(image=pg.image.load("Options Rect.png"), pos=(640, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(image=pg.image.load("Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(menu_text, menu_rect)

        for button in [play_button, options_button, quit_button]:
            button.change_colour(menu_mouse_pos)
            button.update(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if play_button.check_for_input(menu_mouse_pos):
                    play()
                if options_button.check_for_input(menu_mouse_pos):
                    alt_options()
                if quit_button.check_for_input(menu_mouse_pos):
                    pg.quit()
                    sys.exit()

        pg.display.update()

def play():

    clock = pg.time.Clock()

    godmode = False

    global score
    global difficulty
    global users

    run1 = True
    run2 = True

    score = 0

    add_enemy = pg.USEREVENT + 1
    pg.time.set_timer(add_enemy, 250 + 125*(int(difficulty + score/10000)))

    add_cloud = pg.USEREVENT + 2
    pg.time.set_timer(add_cloud, 600)

    timer_event = pg.USEREVENT + 3
    pg.time.set_timer(timer_event, 80)

    player1 = Player(0, pg.K_w, pg.K_s, pg.K_a, pg.K_d)

    player2 = Player(1, pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT)

    enemies = pg.sprite.Group()
    clouds = pg.sprite.Group()
    all_sprites = pg.sprite.Group()
    all_sprites.add(player1)
    all_sprites.add(player2)

    if users == 1:
        player2.kill()
        run2 = False

    while run1 or run2:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run1, run2 = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pause()
                    continue

            elif event.type == add_enemy:
                if score > 2000:
                    if score < 10000:
                        new_enemy = Enemy(0, score)
                    elif score < 25000:
                        new_enemy = Enemy(random.randint(-1, 0), score)
                    else:
                        new_enemy = Enemy(random.randint(-1, 1), score)
                    enemies.add(new_enemy)
                    all_sprites.add(new_enemy)

            elif event.type == add_cloud:
                new_cloud = Cloud(score)
                clouds.add(new_cloud)
                all_sprites.add(new_cloud)

            elif event.type == timer_event:
                score += 47

        screen.fill((135, 206, 250))

        score_text = get_font(20).render(str(score), True, "Black")
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH-50, SCREEN_HEIGHT-700))
        screen.blit(score_text, score_rect)

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        if pg.sprite.spritecollideany(player1, enemies) and not godmode:
            player1.kill()
            run1 = False

        if pg.sprite.spritecollideany(player2, enemies):
            player2.kill()
            run2 = False

        key = pg.key.get_pressed()
        player1.update(key)
        player2.update(key)
        enemies.update()
        clouds.update()

        pg.display.update()

        clock.tick(120)

    file = open(high_dict[difficulty], "r+")

    if int(file.readline()) < score:
        file.seek(0)
        file.write(str(score))
        file.truncate()
    file.close()


    game()

def game():
    global difficulty
    file = open(high_dict[difficulty], "r")
    highscore = file.read()

    global score
    while True:
        screen.blit(bg_play, (0, 0))
        game_mouse_pos = pg.mouse.get_pos()

        highscore_text = get_font(55).render("HIGHSCORE", True, "White")
        highscore_rect = highscore_text.get_rect(center=(300, 100))
        screen.blit(highscore_text, highscore_rect)

        max_score_text = get_font(30).render(highscore, True, "Red")
        max_score_rect = max_score_text.get_rect(center=(300, 200))
        screen.blit(max_score_text, max_score_rect)

        your_score_text = get_font(55).render("YOUR SCORE", True, "White")
        your_score_rect = highscore_text.get_rect(center=(SCREEN_WIDTH-350, 100))
        screen.blit(your_score_text, your_score_rect)

        score_text = get_font(30).render(str(score), True, "Red")
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH-350, 200))
        screen.blit(score_text, score_rect)

        restart = Button(image=None, pos=(640, 460),
                              text_input="RESTART", font=get_font(75), base_color="White", hovering_color="Green")
        restart.change_colour(game_mouse_pos)
        restart.update(screen)

        exit_button = Button(image=None, pos=(640, 600),
                              text_input="EXIT", font=get_font(75), base_color="White", hovering_color="Green")
        exit_button.change_colour(game_mouse_pos)
        exit_button.update(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if restart.check_for_input(game_mouse_pos):
                    play()
                elif exit_button.check_for_input(game_mouse_pos):
                    main_menu()

        pg.display.update()

def tutorial():
    pass

def alt_options():
    global difficulty
    global users
    diff_dict = {-1: "IMPOSSIBLE", 0: "HARD", 1: "MEDIUM", 2: "EASY", 3: (131, 29, 22), 4: "Red", 5: "Yellow", 6: "Green"}
    play_dict = {1: "Single Player", 2: "Two Players"}
    while True:
        options_mouse_pos = pg.mouse.get_pos()

        screen.blit(bg_options, (0, 0))

        options_text = get_font(75).render("OPTIONS", True, (48, 46, 77))
        options_rect = options_text.get_rect(center=(640, 100))
        screen.blit(options_text, options_rect)

        options_back = Button(image=None, pos=(640, 600),
                              text_input="BACK", font=get_font(75), base_color=(48, 46, 77), hovering_color="Green")
        options_back.change_colour(options_mouse_pos)
        options_back.update(screen)

        options_difficulty = Button(image=None, pos=(640, 300),
                                     text_input=diff_dict[difficulty], font=get_font(40), base_color=diff_dict[difficulty+4], hovering_color="White")
        options_difficulty.change_colour(options_mouse_pos)
        options_difficulty.update(screen)

        options_players = Button(image=None, pos=(640, 400), text_input=play_dict[users], font=get_font(40), base_color=(178, 209, 231), hovering_color="White")
        options_players.change_colour(options_mouse_pos)
        options_players.update(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if options_back.check_for_input(options_mouse_pos):
                    main_menu()
                if options_difficulty.check_for_input(options_mouse_pos):
                    if difficulty > -1:
                        difficulty -= 1
                    else:
                        difficulty = 2
                if options_players.check_for_input(options_mouse_pos):
                    if users == 2:
                        users = 1
                    else:
                        users += 1

        pg.display.update()

def pause():

    pause_screen = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    pause_screen.fill((0, 0, 0))
    pause_screen.set_alpha(160)
    pause_screen.blit(pause_screen,(0,0))
    fusk = True

    while fusk:
        pause_mouse_pos = pg.mouse.get_pos()

        exit_button = Button(image=None, pos=(640, 600),
                              text_input="EXIT GAME", font=get_font(75), base_color=(48, 46, 77), hovering_color="Green")
        exit_button.change_colour(pause_mouse_pos)
        exit_button.update(screen)

        resume = Button(image=None, pos=(640, 300),
                                    text_input="RESUME", font=get_font(70),
                                    base_color="Black", hovering_color="White")
        resume.change_colour(pause_mouse_pos)
        resume.update(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if exit_button.check_for_input(pause_mouse_pos):
                    main_menu()
                if resume.check_for_input(pause_mouse_pos):
                    fusk = False
        pg.display.update()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Menu")
bg = pg.image.load("menu_screen.jpg")
bg_play = pg.image.load("game_screen.png")
bg_options = pg.image.load("options_screen.png")

main_menu()