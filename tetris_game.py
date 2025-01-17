import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
BLOCK_SIZE = 30
FIELD_WIDTH = 10
FIELD_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (FIELD_WIDTH + 6)  # Дополнительное место для следующей фигуры
SCREEN_HEIGHT = BLOCK_SIZE * FIELD_HEIGHT

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
FIELD_COLOR = (40, 40, 80)  # Тёмно-синий цвет для игрового поля

COLORS = [CYAN, YELLOW, MAGENTA, RED, GREEN, BLUE, ORANGE]

# Фигуры тетрамино
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]  # Z
]


class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Тетрис")
        self.clock = pygame.time.Clock()

        self.field = [[0 for _ in range(FIELD_WIDTH)] for _ in range(FIELD_HEIGHT)]
        self.score = 0
        self.state = "start"
        self.fall_time = 0
        self.fall_speed = 0.5  # Скорость падения в секундах
        self.level_time = 0

        self.figure = None
        self.next_figure = self.new_figure()
        self.create_figure()

    def new_figure(self):
        shape = random.choice(SHAPES)
        color = random.randint(1, len(COLORS))
        return {
            'shape': shape,
            'color': color,
            'x': FIELD_WIDTH // 2 - len(shape[0]) // 2,
            'y': 0
        }

    def create_figure(self):
        self.figure = self.next_figure
        self.next_figure = self.new_figure()

    def intersects(self):
        for i, row in enumerate(self.figure['shape']):
            for j, cell in enumerate(row):
                if cell == 0:
                    continue
                if (self.figure['y'] + i >= FIELD_HEIGHT or
                        self.figure['x'] + j < 0 or
                        self.figure['x'] + j >= FIELD_WIDTH or
                        self.field[self.figure['y'] + i][self.figure['x'] + j] > 0):
                    return True
        return False

    def remove_line(self):
        lines = 0
        for i in range(FIELD_HEIGHT - 1, -1, -1):
            while all(self.field[i]):
                for i1 in range(i, 1, -1):
                    self.field[i1] = self.field[i1 - 1][:]
                self.field[0] = [0 for _ in range(FIELD_WIDTH)]
                lines += 1
        self.score += lines ** 2

    def freeze(self):
        for i, row in enumerate(self.figure['shape']):
            for j, cell in enumerate(row):
                if cell == 1:
                    self.field[self.figure['y'] + i][self.figure['x'] + j] = self.figure['color']
        self.remove_line()
        self.create_figure()
        if self.intersects():
            self.state = "gameover"

    def rotate(self):
        old_shape = self.figure['shape']
        self.figure['shape'] = list(zip(*reversed(self.figure['shape'])))
        if self.intersects():
            self.figure['shape'] = old_shape

    def move(self, dx):
        old_x = self.figure['x']
        self.figure['x'] += dx
        if self.intersects():
            self.figure['x'] = old_x

    def draw_next_figure(self):
        for i, row in enumerate(self.next_figure['shape']):
            for j, cell in enumerate(row):
                if cell == 1:
                    pygame.draw.rect(
                        self.screen,
                        COLORS[self.next_figure['color'] - 1],
                        (BLOCK_SIZE * (FIELD_WIDTH + 2 + j), BLOCK_SIZE * (2 + i), BLOCK_SIZE - 2, BLOCK_SIZE - 2)
                    )

    def draw(self):
        self.screen.fill(BLACK)

        # Отрисовка фона игрового поля
        pygame.draw.rect(
            self.screen,
            FIELD_COLOR,
            (0, 0, BLOCK_SIZE * FIELD_WIDTH, SCREEN_HEIGHT)
        )

        # Отрисовка сетки
        for i in range(FIELD_HEIGHT):
            for j in range(FIELD_WIDTH):
                pygame.draw.rect(
                    self.screen,
                    (50, 50, 90),  # Цвет линий сетки
                    (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    1  # Толщина линий
                )

        # Отрисовка поля
        for i, row in enumerate(self.field):
            for j, cell in enumerate(row):
                if cell > 0:
                    pygame.draw.rect(
                        self.screen,
                        COLORS[cell - 1],
                        (BLOCK_SIZE * j, BLOCK_SIZE * i, BLOCK_SIZE - 1, BLOCK_SIZE - 1)
                    )

        # Отрисовка текущей фигуры
        if self.figure:
            for i, row in enumerate(self.figure['shape']):
                for j, cell in enumerate(row):
                    if cell == 1:
                        pygame.draw.rect(
                            self.screen,
                            COLORS[self.figure['color'] - 1],
                            (BLOCK_SIZE * (self.figure['x'] + j),
                             BLOCK_SIZE * (self.figure['y'] + i),
                             BLOCK_SIZE - 2, BLOCK_SIZE - 2)
                        )

        # Отрисовка следующей фигуры
        self.draw_next_figure()

        # Отрисовка счета
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (BLOCK_SIZE * (FIELD_WIDTH + 1), BLOCK_SIZE * 8))

        if self.state == "gameover":
            game_over_text = font.render('Game Over', True, WHITE)
            self.screen.blit(game_over_text, (BLOCK_SIZE * (FIELD_WIDTH // 3), BLOCK_SIZE * (FIELD_HEIGHT // 2)))

        pygame.display.flip()

    def run(self):
        while True:
            # Получаем время, прошедшее с последнего кадра
            delta_time = self.clock.get_rawtime()
            self.clock.tick(60)

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move(-1)
                    elif event.key == pygame.K_RIGHT:
                        self.move(1)
                    elif event.key == pygame.K_UP:
                        self.rotate()
                    elif event.key == pygame.K_DOWN:
                        self.figure['y'] += 1
                        if self.intersects():
                            self.figure['y'] -= 1
                            self.freeze()
                        # Не сбрасываем fall_time при нажатии стрелки вниз
                    elif event.key == pygame.K_SPACE:
                        while not self.intersects():
                            self.figure['y'] += 1
                        self.figure['y'] -= 1
                        self.freeze()
                        self.fall_time = 0

            # Падение фигуры
            if self.state == "start":
                self.fall_time += delta_time
                if self.fall_time >= self.fall_speed * 1000:
                    self.fall_time = 0
                    self.figure['y'] += 1
                    if self.intersects():
                        self.figure['y'] -= 1
                        self.freeze()

            self.draw()


