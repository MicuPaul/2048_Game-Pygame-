import random
import constants as c
import pygame as pg
import copy as cop


def new_cell():
    cell_row = random.randint(0, 3)
    cell_col = random.randint(0, 3)
    if random.randint(0, 100) < 90:
        number = 2
    else:
        number = 4
    return cell_row, cell_col, number


class Grid:

    def __init__(self):
        self.grid = [[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]]

    def grid_setup(self, screen):
        for k in range(2):
            self.add_random_cell()

        self.render(screen)

    def is_in_grid(self, value):
        return any(
            value in nested_list
            for nested_list in self.grid
        )

    def game_check_lose(self):
        ok = 0
        for i in range(4):
            for j in range(4):
                if not self.is_in_grid(0):
                    if j != 3 and i != 3:
                        if self.grid[i][j] == self.grid[i][j + 1] or self.grid[i][j] == self.grid[i + 1][j]:
                            ok = 1
                    elif j == 3 and i != 3 and self.grid[i][j] == self.grid[i + 1][j]:
                        ok = 1
                    elif i == 3 and j != 3 and self.grid[i][j] == self.grid[i][j + 1]:
                        ok = 1
        if ok == 1:
            return False
        elif not self.is_in_grid(0) and ok == 0:
            return True

    def add_random_cell(self):
        (cell_r, cell_c, num) = new_cell()
        while self.grid[cell_r][cell_c] != 0:
            if not self.is_in_grid(0):
                return
            (cell_r, cell_c, num) = new_cell()
        self.grid[cell_r][cell_c] = num

    def render(self, screen):
        for i in range(4):
            for j in range(4):
                img = pg.image.load("Sprites/Nr_{}.jpg".format(self.grid[i][j])).convert()
                screen.blit(img, (c.CELL_SPACE * (j + 1) + c.CELL_SIZE * j,
                                  c.CELL_SPACE * (i + 1) + c.CELL_SIZE * i))

    def move_up(self, screen):
        for i, v in enumerate(self.grid):
            for j, n in enumerate(v):
                if n and i != 0:
                    self.grid[i][j] = 0
                    x = c.CELL_SPACE * (j + 1) + c.CELL_SIZE * j
                    if i == 1 and self.grid[0][j] == 0:
                        self.grid[0][j] = n
                        y = c.CELL_SPACE * 2 + c.CELL_SIZE * 1
                        limit = c.CELL_SPACE
                        self.animate(screen, x, y, n, limit, up=True)
                    else:
                        ok = 0
                        index = 0
                        for k in range(i - 1, -1, -1):
                            if self.grid[k][j] != 0:
                                index = k + 1
                                ok = 1
                                break
                        if ok == 0:
                            self.grid[0][j] = n
                            y = c.CELL_SPACE * (i + 1) + c.CELL_SIZE * i
                            limit = c.CELL_SPACE
                            self.animate(screen, x, y, n, limit, up=True)
                        else:
                            self.grid[index][j] = n
                            y = c.CELL_SPACE * (i + 1) + c.CELL_SIZE * i
                            limit = c.CELL_SPACE * (index + 1) + c.CELL_SIZE * index
                            self.animate(screen, x, y, n, limit, up=True)

    def up(self, screen):
        copy = cop.deepcopy(self.grid)
        self.move_up(screen)
        for i in range(3):
            for j in range(4):
                if self.grid[i][j] == self.grid[i + 1][j] and self.grid[i][j] != 0:
                    self.grid[i][j] = self.grid[i][j] * 2
                    self.grid[i + 1][j] = 0
                    y = c.CELL_SPACE * (i + 2) + c.CELL_SIZE * (i+1)
                    x = c.CELL_SPACE * (j + 1) + c.CELL_SIZE * j
                    limit = c.CELL_SPACE * (i + 1) + c.CELL_SIZE * i
                    self.animate(screen, x, y, int(self.grid[i][j]/2), limit, merge=True, up=True)
        self.move_up(screen)
        moved = self.grid == copy
        if not moved:
            self.add_random_cell()

    def move_down(self, screen):
        for i, v in reversed(list(enumerate(self.grid))):
            for j, n in reversed(list(enumerate(v))):
                if n and i != 3:
                    self.grid[i][j] = 0
                    x = c.CELL_SPACE * (j + 1) + c.CELL_SIZE * j
                    if i == 2 and self.grid[3][j] == 0:
                        self.grid[3][j] = n
                        y = c.CELL_SPACE * 3 + c.CELL_SIZE * 2
                        limit = c.CELL_SPACE * 4 + c.CELL_SIZE * 3
                        self.animate(screen, x, y, n, limit, down=True)
                    else:
                        ok = 0
                        index = 0
                        for k in range(i + 1, 4):
                            if self.grid[k][j] != 0:
                                index = k - 1
                                ok = 1
                                break
                        if ok == 0:
                            self.grid[3][j] = n
                            y = c.CELL_SPACE * (i+1) + c.CELL_SIZE * i
                            limit = c.CELL_SPACE * 4 + c.CELL_SIZE * 3
                            self.animate(screen, x, y, n, limit, down=True)
                        else:
                            self.grid[index][j] = n
                            y = c.CELL_SPACE * (i + 1) + c.CELL_SIZE * i
                            limit = c.CELL_SPACE * (index + 1) + c.CELL_SIZE * index
                            self.animate(screen, x, y, n, limit, down=True)

    def down(self, screen):
        copy = cop.deepcopy(self.grid)
        self.move_down(screen)
        for i in range(3, 0, -1):
            for j in range(3, -1, -1):
                if self.grid[i][j] == self.grid[i - 1][j] and self.grid[i][j] != 0:
                    self.grid[i][j] = self.grid[i][j] * 2
                    self.grid[i - 1][j] = 0
                    y = c.CELL_SPACE * i + c.CELL_SIZE * (i - 1)
                    x = c.CELL_SPACE * (j + 1) + c.CELL_SIZE * j
                    limit = c.CELL_SPACE * (i + 1) + c.CELL_SIZE * i
                    self.animate(screen, x, y, int(self.grid[i][j] / 2), limit, merge=True, down=True)
        self.move_down(screen)
        moved = self.grid == copy
        if not moved:
            self.add_random_cell()

    def move_left(self, screen):
        for i, v in enumerate(self.grid):
            for j, n in enumerate(v):
                if n and j != 0:
                    self.grid[i][j] = 0
                    y = c.CELL_SPACE * (i+1) + c.CELL_SIZE * i
                    if j == 1 and self.grid[i][0] == 0:
                        self.grid[i][0] = n
                        x = c.CELL_SPACE * 2 + c.CELL_SIZE * 1
                        limit = c.CELL_SPACE
                        self.animate(screen, x, y, n, limit, left=True)
                    else:
                        ok = 0
                        index = 0
                        for k in range(j - 1, -1, -1):
                            if self.grid[i][k] != 0:
                                index = k + 1
                                ok = 1
                                break
                        if ok == 0:
                            self.grid[i][0] = n
                            x = c.CELL_SPACE * (j + 1) + c.CELL_SIZE * j
                            limit = c.CELL_SPACE
                            self.animate(screen, x, y, n, limit, left=True)
                        else:
                            self.grid[i][index] = n
                            x = c.CELL_SPACE * (j + 1) + c.CELL_SIZE * j
                            limit = c.CELL_SPACE * (index + 1) + c.CELL_SIZE * index
                            self.animate(screen, x, y, n, limit, left=True)

    def left(self, screen):
        copy = cop.deepcopy(self.grid)
        self.move_left(screen)
        for i in range(4):
            for j in range(3):
                if self.grid[i][j] == self.grid[i][j + 1] and self.grid[i][j] != 0:
                    self.grid[i][j] = self.grid[i][j] * 2
                    self.grid[i][j + 1] = 0
                    y = c.CELL_SPACE * (i + 1) + c.CELL_SIZE * i
                    x = c.CELL_SPACE * (j + 2) + c.CELL_SIZE * (j + 1)
                    limit = c.CELL_SPACE * (j + 1) + c.CELL_SIZE * j
                    self.animate(screen, x, y, int(self.grid[i][j] / 2), limit, merge=True, left=True)
        self.move_left(screen)
        moved = self.grid == copy
        if not moved:
            self.add_random_cell()

    def move_right(self, screen):
        for i, v in reversed(list(enumerate(self.grid))):
            for j, n in reversed(list(enumerate(v))):
                if n and j != 3:
                    self.grid[i][j] = 0
                    y = c.CELL_SPACE * (i + 1) + c.CELL_SIZE * i
                    if j == 2 and self.grid[i][3] == 0:
                        self.grid[i][3] = n
                        x = c.CELL_SPACE * 3 + c.CELL_SIZE * 2
                        limit = c.CELL_SPACE * 4 + c.CELL_SIZE * 3
                        self.animate(screen, x, y, n, limit, right=True)
                    else:
                        ok = 0
                        index = 0
                        for k in range(j + 1, 4):
                            if self.grid[i][k] != 0:
                                index = k - 1
                                ok = 1
                                break
                        if ok == 0:
                            self.grid[i][3] = n
                            x = c.CELL_SPACE * (j+1) + c.CELL_SIZE * j
                            limit = c.CELL_SPACE * 4 + c.CELL_SIZE * 3
                            self.animate(screen, x, y, n, limit, right=True)
                        else:
                            self.grid[i][index] = n
                            x = c.CELL_SPACE * (j + 1) + c.CELL_SIZE * j
                            limit = c.CELL_SPACE * (index + 1) + c.CELL_SIZE * index
                            self.animate(screen, x, y, n, limit, right=True)

    def right(self, screen):
        copy = cop.deepcopy(self.grid)
        self.move_right(screen)
        for i in range(3, -1, -1):
            for j in range(3, 0, -1):
                if self.grid[i][j] == self.grid[i][j - 1] and self.grid[i][j] != 0:
                    self.grid[i][j] = self.grid[i][j] * 2
                    self.grid[i][j - 1] = 0
                    y = c.CELL_SPACE * (i + 1) + c.CELL_SIZE * i
                    x = c.CELL_SPACE * j + c.CELL_SIZE * (j - 1)
                    limit = c.CELL_SPACE * (j + 1) + c.CELL_SIZE * j
                    self.animate(screen, x, y, int(self.grid[i][j] / 2), limit, merge=True, right=True)
        self.move_right(screen)
        moved = self.grid == copy
        if not moved:
            self.add_random_cell()

    def animate(self, screen, x, y, n, limit, merge=False, up=False, down=False, left=False, right=False):
        img1 = pg.image.load("Sprites/Nr_{}.jpg".format(n)).convert()
        empty = pg.image.load("Sprites/Nr_0.jpg").convert()
        if up or down:
            while abs(y - limit) >= 10.25:
                if up:
                    y -= 24.25
                elif down:
                    y += 24.25
                screen.fill((87, 74, 62))
                self.render(screen)
                if not merge:
                    screen.blit(empty, (x, limit))
                screen.blit(img1, (x, y))
                pg.display.flip()
        elif left or right:
            while abs(x - limit) >= 10.25:
                if left:
                    x -= 24.25
                elif right:
                    x += 24.25
                screen.fill((87, 74, 62))
                self.render(screen)
                if not merge:
                    screen.blit(empty, (limit, y))
                screen.blit(img1, (x, y))
                pg.display.flip()
