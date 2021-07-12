import pygame
from random import choice
import sys
from random import randint
from random import randrange

RES = WIDTH, HEIGHT = 1202, 742
TILE = 100
shift = 40
cols, rows = WIDTH // TILE, (HEIGHT - shift) // TILE


pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36, bold = True)

level_count = 1
score_count = 0
player_color = '#48ffff'
exit_color = '#56c456'

WHITE = (255,255,255)
GRAY = (200,200,200)
BLACK = (0, 0, 0)

menu_trigger = True

def menu(menu_trigger):
    button_font = pygame.font.SysFont('Arial', 72)
    label_font = pygame.font.SysFont('Arial', 200)
    button_start = pygame.Rect(0,0, 400, 150)
    button_start.center = WIDTH // 2, HEIGHT // 2
    button_exit = pygame.Rect(0, 0, 400, 150)
    button_exit.center = WIDTH // 2, HEIGHT // 2 + 200

    while menu_trigger:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        start = button_font.render('START', 1, GRAY)
        exit = button_font.render('EXIT', 1, GRAY)

        sc.fill(pygame.Color('darkslategray'))

        pygame.draw.rect(sc, BLACK, button_start)
        pygame.draw.rect(sc, BLACK, button_exit)

        color = randrange(40)
        label = label_font.render('MazePy', 1, (color, color, color))
        label_rect = label.get_rect()
        label_rect.centerx = WIDTH//2
        label_rect.top = 20
        sc.blit(label, label_rect)

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if button_start.collidepoint(mouse_pos):
            start = button_font.render('START', 1, WHITE)
            if mouse_click[0]:
                menu_trigger = False
        elif button_exit.collidepoint(mouse_pos):
            exit = button_font.render('EXIT', 1, WHITE)
            if mouse_click[0]:
                pygame.quit()
                sys.exit()

        start_rect = start.get_rect()
        start_rect.center = button_start.center
        exit_rect = exit.get_rect()
        exit_rect.center = button_exit.center
        sc.blit(start, start_rect)
        sc.blit(exit, exit_rect)
        pygame.display.update()
        clock.tick(30)



class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {# [1,2,3,4]
            'top': True,
            'right': True,
            'left': True,
            'bottom': True
            }
        self.visited = False

    def draw_current_cell(self, color):
        x, y = self.x*TILE, self.y * TILE + shift
        pygame.draw.rect(sc, pygame.Color(color),
                         (x+2, y+2, TILE - 4, TILE - 4))

    def draw(self):
        x, y = self.x * TILE, self.y * TILE + shift
        if self.visited:
            pygame.draw.rect(sc, pygame.Color('black'), (x, y, TILE, TILE))

        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('red'),
                             (x,y),(x+TILE,y), 1)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('red'),
                             (x,y+TILE),(x+TILE,y+TILE), 1)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('red'),
                             (x+TILE,y),(x+TILE,y+TILE), 1)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('red'),
                             (x,y),(x,y+TILE), 1)

    def check_cell(self, x, y):
        find_index = lambda x,y: x + y*cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x,y)]

    def check_neighbors(self):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        right = self.check_cell(self.x + 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        if right and not right.visited:
            neighbors.append(right)

        return choice(neighbors) if neighbors else False



def remove_walls(current, next):
    dx = current.x - next.x
    dy = current.y - next.y
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False


while True:
    menu(menu_trigger)
    grid_cells = [Cell(col,row) for row in range(rows) for col in range(cols)]
    #[клетка с координатами 00, клетка с координатами 01,....]
    current_cell = grid_cells[0]
    stack = []
    colors, color = [], 40

    while True:
        sc.fill(pygame.Color('darkslategray'))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        [cell.draw() for cell in grid_cells]
        current_cell.visited = True
        current_cell.draw_current_cell(player_color)

        next_cell = current_cell.check_neighbors()
        if next_cell:
            next_cell.visited = True
            stack.append(current_cell)
            colors.append((min(color, 255), 19, 100))
            color += 1
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        else:
            if stack:
                current_cell = stack.pop()
            else:
                break

        #for i, cell in enumerate(stack):
         #   pygame.draw.rect(sc, colors[i], (cell.x * TILE + 5, cell.y * TILE + 5,
          #                                   TILE - 10, TILE - 10))

        #pygame.display.update()
        #clock.tick(30)

    ex, ey = randint(0,cols-1), randint(0,rows - 1)
    exit_cell = grid_cells[0]
    exit_cell = exit_cell.check_cell(ex, ey)
    
    right, left, up, down = False, False, False, False
    
    render_level = font.render(f'Уровень: {level_count}', 1, (255,255,255))
    render_level_rect = render_level.get_rect()
    render_level_rect.centery = 20
    render_level_rect.centerx = WIDTH // 2
    
    render_score = font.render(f'Счет: {score_count}', 1, (255,255,255))
    render_score_rect = render_score.get_rect()
    render_score_rect.centery = 20
    render_score_rect.right = WIDTH - 20
    game_over = False
    while True:
        sc.fill(pygame.Color('darkslategray'))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    right = True
                if event.key == pygame.K_LEFT:
                    left = True
                if event.key == pygame.K_UP:
                    up = True
                if event.key == pygame.K_DOWN:
                    down = True
                if event.key == pygame.K_ESCAPE:
                    game_over = True
                    menu_trigger = True
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    right = False
                if event.key == pygame.K_LEFT:
                    left = False
                if event.key == pygame.K_UP:
                    up = False
                if event.key == pygame.K_DOWN:
                    down = False
        if game_over:
            break

        if right and not current_cell.walls['right']:
            x = current_cell.x
            y = current_cell.y
            x += 1
            current_cell = current_cell.check_cell(x,y)
            right = False
        if left and not current_cell.walls['left']:
            x = current_cell.x
            y = current_cell.y
            x -= 1
            current_cell = current_cell.check_cell(x,y)
            left = False
        if up and not current_cell.walls['top']:
            x = current_cell.x
            y = current_cell.y
            y -= 1
            current_cell = current_cell.check_cell(x,y)
            up = False
        if down and not current_cell.walls['bottom']:
            x = current_cell.x
            y = current_cell.y
            y += 1
            current_cell = current_cell.check_cell(x,y)
            down = False

        [cell.draw() for cell in grid_cells]
        current_cell.draw_current_cell(player_color)
        exit_cell.draw_current_cell(exit_color)

        if current_cell.x == exit_cell.x and current_cell.y == exit_cell.y:
            break
        sc.blit(render_level, render_level_rect)
        sc.blit(render_score, render_score_rect)
        pygame.display.update()
        clock.tick(30)
    
    cols = cols + 1
    TILE = WIDTH // cols
    if TILE < 10:
        TILE = 10
    rows = (HEIGHT - shift)// TILE
    score_count += 1000//TILE
    level_count += 1
    
