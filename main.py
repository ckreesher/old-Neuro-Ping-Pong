import pygame
from enum import Enum


def neuro_mind(bx, by, py, ey, d1, d2, sigmoid):
    neuron1 = bx * sigmoid[0] + by * sigmoid[1] + py * sigmoid[2] + ey * sigmoid[3] + d1 * sigmoid[4] + d2 * sigmoid[5]
    neuron2 = bx * sigmoid[6] + by * sigmoid[7] + py * sigmoid[8] + ey * sigmoid[9] + d1 * sigmoid[10] + d2 * sigmoid[11]
    return neuron2, neuron1


class Player:

    def __init__(self, side, name):
        self.side = side
        self.points = 0
        self.name = name

    @property
    def score(self):
        return self.points

    @score.setter
    def score(self, val):
        self.points += val


class Directions(Enum):
    UP_LEFT = 7
    UP_RIGHT = 9
    DOWN_LEFT = 1
    DOWN_RIGHT = 3
    LEFT = 4
    RIGHT = 6


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (64, 64, 64)


class Racket(pygame.sprite.Sprite):
    def __init__(self, screen, width, height, side):
        super().__init__()

        self.width, self.height = width, height
        self.racket_height = 100
        self.movement_speed = 20
        offset = 20
        self.screen = screen
        self.image = pygame.Surface([10, self.racket_height])
        self.image.fill(WHITE)
        pygame.draw.rect(self.image, WHITE, [0, 0, 10, self.racket_height])
        self.rect = self.image.get_rect()
        print(side)
        if side is Directions.LEFT:
            self.position = (offset, self.height / 2)
        else:
            self.position = (self.width - offset - 10, self.height / 2)

    @property
    def position(self):
        return self.rect.x, self.rect.y

    @position.setter
    def position(self, pos):
        try:
            pos_x, pos_y = pos
        except ValueError:
            raise ValueError("Pass an iterable with two items")
        else:
            self.rect.x, self.rect.y = pos_x, pos_y

    def move_up(self):
        if self.position[1] > 0:
            self.position = (self.position[0], self.position[1] - self.movement_speed)

    def move_down(self):
        if self.position[1] + self.racket_height < self.height:
            self.position = (self.position[0], self.position[1] + self.movement_speed)


class Ball(pygame.sprite.Sprite):
    def __init__(self, screen, width, height, direct):
        super().__init__()
        self.width, self.height = width, height
        self.direction = direct
        self.screen = screen
        self.image = pygame.Surface([10, 10])
        self.image.fill(WHITE)
        pygame.draw.rect(self.image, WHITE, [0, 0, 10, 10])
        self.rect = self.image.get_rect()
        self.position = (width / 2 + 2, height / + 2)
        self.hits = 0
        self.speed_up = 1.0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def hit(self):
        self.hits = min(self.hits + 1, 10)
        self.speed_up = 1.0 + self.hits / 10

    @property
    def position(self):
        return self.rect.x, self.rect.y

    @position.setter
    def position(self, pos):
        try:
            pos_x, pos_y = pos
        except ValueError:
            raise ValueError("Pass an iterable with two items")
        else:
            self.rect.x, self.rect.y = pos_x, pos_y

    def up_left(self):
        self.position = (self.position[0] - 10 * self.speed_up, self.position[1] - 10 * self.speed_up)

    def up_right(self):

        self.position = (self.position[0] + 10 * self.speed_up, self.position[1] - 10 * self.speed_up)

    def down_left(self):

        self.position = (self.position[0] - 10 * self.speed_up, self.position[1] + 10 * self.speed_up)

    def down_right(self):

        self.position = (self.position[0] + 10 * self.speed_up, self.position[1] + 10 * self.speed_up)

    def update(self, dir):
        ret = dir
        if self.position[1] <= 10 and self.direction == Directions.UP_LEFT:  # upper border
            self.direction = Directions.DOWN_LEFT
            ret = -1, 1
        if self.position[1] <= 10 and self.direction == Directions.UP_RIGHT:  # upper border
            self.direction = Directions.DOWN_RIGHT
            ret = 1, 1
        if self.position[1] >= self.height - 10 and self.direction == Directions.DOWN_LEFT:  # bottom border
            self.direction = Directions.UP_LEFT
            ret = -1, -1
        if self.position[1] >= self.height - 10 and self.direction == Directions.DOWN_RIGHT:  # bottom border
            self.direction = Directions.UP_RIGHT
            ret = 1, -1

        options = {Directions.UP_LEFT: self.up_left,
                   Directions.UP_RIGHT: self.up_right,
                   Directions.DOWN_LEFT: self.down_left,
                   Directions.DOWN_RIGHT: self.down_right,
                   }
        options[self.direction]()
        return ret

    def toggle_direction(self):
        new_direction = None
        if self.direction == Directions.DOWN_LEFT:
            new_direction = Directions.DOWN_RIGHT
            ret = 1, 1

        if self.direction == Directions.DOWN_RIGHT:
            new_direction = Directions.DOWN_LEFT
            ret = -1, 1

        if self.direction == Directions.UP_RIGHT:
            new_direction = Directions.UP_LEFT
            ret = -1, -1

        if self.direction == Directions.UP_LEFT:
            new_direction = Directions.UP_RIGHT
            ret = 1, 1

        try:
            self.direction = new_direction
        except NameError:
            pass
        return ret

    def get_x_val(self):
        return self.rect.x


WIN_WIDTH = 1280
WIN_HEIGHT = 720
MAX_SCORE = 1
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(DISPLAY, 0, 32)
num = 0
numbers = 0
best_num_col = 0
visible = True
vs_human = False

DONE = False
FPS = 10000
right_player_wins = 0
left_player_wins = 0

left_player = Player(Directions.LEFT, 'Left')
right_player = Player(Directions.RIGHT, 'Right')

curr_ball = Ball(screen, WIN_WIDTH, WIN_HEIGHT, Directions.UP_LEFT)

left_racket = Racket(screen, WIN_WIDTH, WIN_HEIGHT, Directions.LEFT)
right_racket = Racket(screen, WIN_WIDTH, WIN_HEIGHT, Directions.RIGHT)

rackets = pygame.sprite.Group()
rackets.add(left_racket)
rackets.add(right_racket)
stuff_to_draw = pygame.sprite.Group()
stuff_to_draw.add(left_racket)
stuff_to_draw.add(right_racket)
win = False
lplayerscore = -1
rplayerscore = 0
direction1, direction2 = 1, -1
curr_ball.direction = Directions.UP_RIGHT
old_ball_pos = curr_ball.position[1]
i, j, t, h, a, b, c, d = 0, -10, 10, 0, 0, 0, 0, 0 # 0, -10, 10, 0
d1, d2, d11, d22 = -10, 0, 0, 0
while i < 11:
                    sigmoid_left = [i / 10, j / 10, t / 10, h / 10, d11 / 10, d22 / 10, a / 10, b / 10, c / 10, d / 10, d1 / 10, d2 / 10]
                    sigmoid_right = [i / 10, j / 10, t / 10, h / 10, d11 / 10, d22 / 10, a / 10, b / 10, c / 10, d / 10, d1 / 10, d2 / 10]

                    if visible:
                        screen.fill(BLACK)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            print(sigmoid_right)
                            quit()
                    pygame.event.pump()
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_q]:
                        print(sigmoid_right, numbers)
                        DONE = True
                    if keys[pygame.K_x]:
                        visible = not visible
                    if keys[pygame.K_p]:
                        print(sigmoid_right, numbers, clock.get_fps())
                    out = neuro_mind((curr_ball.position[0] - 640) / 1000, (curr_ball.position[1] - 360) / 1000,
                                     (right_racket.position[1] - 360 + 50) / 1000,
                                     (left_racket.position[1] - 360 + 50) / 1000, direction1, direction2, sigmoid_right)
                    if out[0] > 0:
                        if out[1] > 0:
                            right_racket.move_up()
                        elif out[1] <= 0:
                            right_racket.move_down()
                    out = neuro_mind((curr_ball.position[0] - 640) / 1000, (curr_ball.position[1] - 360) / 1000,
                                     (left_racket.position[1] - 360 + 50) / 1000,
                                     (right_racket.position[1] - 360 + 50) / 1000, direction1, direction2, sigmoid_left)
                    if out[0] < 0:
                        if out[1] > 0:
                            left_racket.move_up()
                        elif out[1] <= 0:
                            left_racket.move_down()

                    if keys[pygame.K_q]:
                        print(numbers)
                        quit()

                    stuff_to_draw.update()
                    old_ball_pos = curr_ball.position[1]
                    direction1, direction2 = curr_ball.update((direction1, direction2))

                    col_left, col_right = curr_ball.rect.colliderect(left_racket.rect), curr_ball.rect.colliderect(right_racket.rect)
                    if col_right == 1:
                        direction1, direction2 = curr_ball.toggle_direction()
                        curr_ball.hit()
                    if col_left == 1:
                        direction1, direction2 = curr_ball.toggle_direction()
                        curr_ball.hit()

                    if curr_ball.get_x_val() <= 0 and old_ball_pos not in range(left_racket.position[1], left_racket.position[1]+100):  # left border
                        right_player.score = 1
                        rplayerscore += 1
                        if curr_ball.direction == Directions.DOWN_LEFT:
                            curr_ball = Ball(screen, WIN_WIDTH, WIN_HEIGHT, Directions.DOWN_LEFT)
                        elif curr_ball.direction == Directions.UP_LEFT:
                            curr_ball = Ball(screen, WIN_WIDTH, WIN_HEIGHT, Directions.UP_LEFT)
                    elif curr_ball.get_x_val() >= WIN_WIDTH and old_ball_pos not in range(right_racket.position[1], right_racket.position[1]+100):  # right border
                        left_player.score = 1
                        lplayerscore += 1
                        if curr_ball.direction == Directions.DOWN_RIGHT:
                            curr_ball = Ball(screen, WIN_WIDTH, WIN_HEIGHT, Directions.DOWN_LEFT)
                        elif curr_ball.direction == Directions.UP_RIGHT:
                            curr_ball = Ball(screen, WIN_WIDTH, WIN_HEIGHT, Directions.UP_LEFT)

                    if visible:
                        font = pygame.font.SysFont('Helvetica', 25)

                        left_player_score = font.render(
                            '{}'.format(lplayerscore), True, (255, 255, 255))
                        right_player_score = font.render(
                            '{}'.format(rplayerscore), True, (255, 255, 255))
                        goal_text = font.render(
                            '{}'.format(MAX_SCORE), True, (255, 255, 0))
                        screen.blit(left_player_score, (WIN_WIDTH / 2 - 100, 10))
                        screen.blit(right_player_score, (WIN_WIDTH / 2 + 100, 10))
                        screen.blit(goal_text, (WIN_WIDTH / 2, 0))
                        stuff_to_draw.draw(screen)
                        curr_ball.draw(screen)
                        pygame.display.set_caption('Ping Pong ' + str(clock.get_fps()))

                    if right_player.score >= MAX_SCORE or left_player.score >= MAX_SCORE:
                        right_racket.position = (20, 310)
                        left_racket.position = (1250, 310)
                        if not vs_human:
                            left_player.points, right_player.points = 0, 0
                            numbers += 1
                            # d1 += 1
                            if d1 > 10:
                                d1 = 0
                                d2 += 1
                            if d2 > 10:
                                d2 = 0
                                h += 1
                            if h > 10:
                                h = -10
                                t += 1
                            if t > 10:
                                t = -10
                                j += 1
                            if j > 10:
                                j = -10
                                i += 1

                    pygame.display.flip()
                    if visible:
                        clock.tick(30)
                    else:
                        clock.tick(FPS)

pygame.quit()
