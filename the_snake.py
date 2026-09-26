from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Создание базового класса для объектов игры.

    Отвечает за отрисовку, хранение позиции и цвета тела.
    """

    def __init__(self, position=None, body_color=None):
        """Инициализация объекта с позицией и цветом тела."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Определяет метод отрисовки игрового объекта."""
        pass


class Apple(GameObject):
    """Создание класса яблока.

    Отвечает за генерацию случайной позиции яблока на игровом поле.
    """

    def __init__(self, position=None, body_color=None):
        """Инициализация яблока с позицией и цветом тела."""
        super().__init__(position, body_color)

    def randomize_position(self, snake_positions):
        while True:
            x_position = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y_position = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_position = (x_position, y_position)

            if new_position not in snake_positions:
                self.position = new_position
                break

    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pygame.Rect(
            self.position,
            (GRID_SIZE, GRID_SIZE),
        )
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

class Snake(GameObject):
    """Создание класса змейки.

    Отвечает за движение, хранение длины и позиций сегментов тела.
    """

    def __init__(self, position=None, body_color=None):
        """Инициализация змейки с позицией и цветом тела."""
        super().__init__(position, body_color)
        self.length = 1
        self.positions = [position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновление направления движения змейки.

        Отвечает за смену направления движения змейки на основе следующего.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Перемещение змейки на игровом поле.

        Обновляет позицию головы змейки на основе текущего направления.
        При выходе за границы игрового поля, появляется с дрйгой стороны.
        Обновляет список сегментов тела змейки и удаляет последний сегмент,
        если длина змейки превышает текущую длину.
        """
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction

        new_x = head_x + direction_x * GRID_SIZE
        new_y = head_y + direction_y * GRID_SIZE

        new_x %= SCREEN_WIDTH
        new_y %= SCREEN_HEIGHT

        new_position = (new_x, new_y)

        self.last = self.positions[-1]
        self.positions.insert(0, new_position)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.__init__(
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            self.body_color,
        )

    def draw(self):
        """Отрисовка змейки на экране.

        Отвечает за отрисовку сегментов тела змейки и головы змейки.
        Затирает последний сегмент змейки, если он был удален в движении.
        """

        #  Отрисовка головы змейки
        head_rect = pygame.Rect(
            self.get_head_position(),
            (GRID_SIZE, GRID_SIZE),
        )
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        #  Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Обработка нажатий клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """
    Основная функция игры.

    Отвечает за инициализацию игры, создание объектов змейки и яблока,
    обработку событий, обновление состояния игры и отрисовку объектов.
    """
    pygame.init()
    snake = Snake((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), SNAKE_COLOR)
    apple = Apple(None, APPLE_COLOR)
    apple.randomize_position(snake.positions)
    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка на столкновение змейки с яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1  # Увеличиваем длину змейки с хвоста
            apple.randomize_position(snake.positions)  # Перемещаем яблоко
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()  # Сброс змейки при столкновении с самой собой
            screen.fill(BOARD_BACKGROUND_COLOR)  # Очистка экрана после сброса
        # Отрисовка объектов на экране
        snake.draw()
        apple.draw()

        # Обновление экрана
        pygame.display.update()


if __name__ == '__main__':
    main()
