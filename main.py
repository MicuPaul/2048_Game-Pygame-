import pygame as pg
import constants as c
from grid import Grid

pg.init()
pg.display.set_caption(c.SCREEN_TITLE)
screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
clock = pg.time.Clock()
running = True
screen.fill((87, 74, 62))
g = Grid()
g.grid_setup(screen)
pg.display.update()


def draw_game_state_screen(outcome):
    screen.fill((0, 0, 0))
    font = pg.font.SysFont('arial', 40)
    title = font.render("{}".format(outcome), True, (255, 255, 255))
    restart_button = font.render('R - Restart', True, (255, 255, 255))
    quit_button = font.render('Q - Quit', True, (255, 255, 255))
    screen.blit(title, (c.SCREEN_WIDTH/2 - title.get_width()/2, 200 - title.get_height()/2))
    screen.blit(restart_button, (c.SCREEN_WIDTH/2 - restart_button.get_width()/2,
                                      220 + restart_button.get_height()))
    screen.blit(quit_button, (c.SCREEN_WIDTH/2 - quit_button.get_width()/2,
                                   200 + quit_button.get_height()/2))
    pg.display.update()


def restart_game():
    g.grid = [[0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0]]
    screen.fill((87, 74, 62))
    g.grid_setup(screen)
    pg.display.update()


while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                g.up(screen)
                screen.fill((87, 74, 62))
                g.render(screen)
            if event.key == pg.K_DOWN:
                g.down(screen)
                screen.fill((87, 74, 62))
                g.render(screen)
            if event.key == pg.K_LEFT:
                g.left(screen)
                screen.fill((87, 74, 62))
                g.render(screen)
            if event.key == pg.K_RIGHT:
                g.right(screen)
                screen.fill((87, 74, 62))
                g.render(screen)

    if g.game_check_lose():
        draw_game_state_screen("Game Over!")
        keys = pg.key.get_pressed()
        if keys[pg.K_r]:
            restart_game()
        if keys[pg.K_q]:
            pg.quit()
            quit()

    if g.is_in_grid(2048):
        draw_game_state_screen("You Won!")
        keys = pg.key.get_pressed()
        if keys[pg.K_r]:
            restart_game()
        if keys[pg.K_q]:
            pg.quit()
            quit()

    pg.display.update()

    clock.tick(120)

pg.quit()
