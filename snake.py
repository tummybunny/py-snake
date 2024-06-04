"""
Simple Snake game by Alexander Yanuar Koentjara - created when learning python
"""
import pygame
import random

FPS = 7
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4


class Snake(object):
    def __init__(self, block_size, width, height, blocks):
        self.block_size = block_size  # size of a block
        self.width = width            # number of horizontal blocks
        self.height = height          # number of vertical blocks
        self.blocks = blocks          # array of (x,y) tuples: [(1,1), (2,1), (3,1)], element 0 is the head
        self.dir = RIGHT              # current direction
        self.score = 100              # current score

    def draw(self, surface):
        """Draw snake on surface"""
        col = 255
        for (x, y) in self.blocks:
            xx = self.block_size * x
            yy = self.block_size * y
            surface.fill((col, 0, 0), (xx, yy, self.block_size, self.block_size))
            col = col - 20
            if col < 100:
                col = 100

    def steer(self, new_direction):
        """Change new direction"""
        self.dir = new_direction

    def move(self, food):
        """Move snake according to its direction, check whether the head collide with the food
        coordinate (which will cause the snake to grow 1 size) or whether it collide with itself
        or become out of bound (game over)"""
        x, y = self.blocks[0]
        if self.dir == UP:
            y -= 1
        elif self.dir == RIGHT:
            x += 1
        elif self.dir == DOWN:
            y += 1
        elif self.dir == LEFT:
            x -= 1

        if (x, y) in self.blocks or x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        else:
            self.blocks[:0] = ((x, y),)
            if (x, y) == (food.x, food.y):  # eaten the food
                food.spawn(self)
                self.score += 100
            else:
                self.score -= 1
                del self.blocks[len(self.blocks) - 1]
        return False


class Food(object):
    def __init__(self, block_size, width, height):
        self.block_size = block_size  # size of a block
        self.width = width            # number of horizontal blocks
        self.height = height          # number of vertical blocks
        self.x, self.y = (0, 0)       # initialization of food coordinate
        self.rd = random.Random()

    def spawn(self, snake):
        """To spawn new food at random coordinate (x, y)"""
        while True:
            x = self.rd.randint(0, self.width - 1)
            y = self.rd.randint(0, self.height - 1)
            if (x, y) not in snake.blocks:
                self.x = x
                self.y = y
                break

    def draw(self, surface):
        """Draw the food on surface"""
        xx = self.block_size * self.x
        yy = self.block_size * self.y
        surface.fill((0, 0, 255), (xx, yy, self.block_size, self.block_size))


class SnakeGame(object):
    def __init__(self, initial_blocks, block_size, width, height):
        self.block_size = block_size  # size of a block
        self.width = width          # number of horizontal blocks
        self.height = height        # number of vertical blocks
        self.screen = pygame.display.set_mode((width * block_size + 1, height * block_size + 1))
        self.background = pygame.Surface((width * block_size, height * block_size)).convert()
        self.snake = Snake(block_size, width, height, [(i, 0) for i in range(initial_blocks - 1, -1, -1)])
        self.food = Food(block_size, width, height)
        self.food.spawn(self.snake)

    def run(self):
        """Main game loop, return True only if player wishes to restart"""
        sc = self.screen
        bg = self.background
        clock = pygame.time.Clock()
        font = pygame.font.SysFont('mono', 13, bold=True)
        restart = False
        mainloop = True
        game_over = False

        while mainloop:
            if game_over:
                text = font.render("Game over! Press 'R' to restart.", True, (255, 255, 255))
                bg.blit(text, (5, 25))
                sc.blit(bg, (0, 0))
                clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        mainloop = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            mainloop = False
                        elif event.key == pygame.K_r:
                            restart = True
                            mainloop = False
            else:
                bg.lock()
                bg.fill((0, 0, 0))
                game_over = self.snake.move(self.food)
                for i in range(0, self.width):
                    pygame.draw.line(bg, (70, 70, 70), (i * self.block_size, 0),
                                     (i * self.block_size, self.height * self.block_size))
                for i in range(0, self.height):
                    pass
                    pygame.draw.line(bg, (70, 70, 70), (0, i * self.block_size),
                                     (self.width * self.block_size, i * self.block_size))
                self.snake.draw(bg)
                self.food.draw(bg)
                text = font.render(f"Score: {self.snake.score}", True, (255, 255, 255))
                bg.unlock()
                bg.blit(text, (5, 5))
                sc.blit(bg, (0, 0))
                clock.tick(FPS)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        mainloop = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            mainloop = False

                        # Snake cannot reverse, e.g. while moving to right, it cannot change direction to left
                        # otherwise it is an instant game over
                        elif event.key == pygame.K_DOWN and self.snake.dir != UP:
                            self.snake.steer(DOWN)
                        elif event.key == pygame.K_UP and self.snake.dir != DOWN:
                            self.snake.steer(UP)
                        elif event.key == pygame.K_RIGHT and self.snake.dir != LEFT:
                            self.snake.steer(RIGHT)
                        elif event.key == pygame.K_LEFT and self.snake.dir != RIGHT:
                            self.snake.steer(LEFT)
                        elif event.key == pygame.K_r:
                            restart = True
                            mainloop = False

            pygame.display.flip()  # needed to repaint display
        return restart


def main():
    pygame.init()
    pygame.display.set_caption("Simple Snake Game by Husci")
    while True:
        game = SnakeGame(3, 20, 20, 20)
        if not game.run():
            break

    pygame.quit()


if __name__ == "__main__":
    main()
