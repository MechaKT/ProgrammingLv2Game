import pygame
import random
import math
# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (95, 165, 228)
WIDTH = 800
HEIGHT = 800
TITLE = "Game"

# ----- SPRITE GROUPS
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
ebullet_sprites = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("./images/ship.png")
        self.image = pygame.transform.scale(self.image, (64, 64))

        self.rect = self.image.get_rect()

        self.x_vel = 5
        self.y_vel = 5

    def move_left(self):
        self.rect.x -= self.x_vel

    def move_right(self):
        self.rect.x += self.x_vel

    def move_up(self):
        self.rect.y -= self.y_vel

    def move_down(self):
        self.rect.y += self.y_vel

    def update(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        if self.rect.left <= 0:
            self.rect.left = 0


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("./images/enemy.png")
        self.image = pygame.transform.scale(self.image, (300, 300))
        self.enemy_x_vel = 4

        self.rect = self.image.get_rect()

        self.rect.center = (self.rect.x / 2, self.rect.y /2)
    def update(self):
        self.rect.x += self.enemy_x_vel
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.enemy_x_vel *= -1

class Pbullet(pygame.sprite.Sprite):
    def __init__(self, coords):
        super().__init__()

        self.image = pygame.Surface((10, 40))
        self.image.fill(YELLOW)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords

        self.bullet_vel = -30
    def update(self):
        self.rect.y += self.bullet_vel

class Ebullet(pygame.sprite.Sprite):
    def __init__(self, coords, angle):
        super().__init__()

        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.center = coords
        self.angle = angle

        self.speedx = 5 * math.cos(math.radians(self.angle))
        self.speedy = 5 * math.sin(math.radians(self.angle))

        self.posx = self.rect.centerx
        self.posy = self.rect.centery


        self.rect.center = coords


    def update(self):
        self.posx += self.speedx
        self.posy += self.speedy
        self.rect.center = (self.posx, self.posy)
        if (self.rect.right > WIDTH or self.rect.left < 0 or self.rect.bottom > HEIGHT or self.rect.top<0):
            self.kill()

# Boss hp
hp = 1000
# Player lives
lives = 3

def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()

    # Populate sprite groups
    enemy = Enemy()
    enemy.rect.y = 50
    enemy.rect.x = 225

    all_sprites.add(enemy)
    enemy_sprites.add(enemy)


    player = Player()
    all_sprites.add(player)
    player.rect.y = 600
    player.rect.x = 350

    pbullet = Pbullet(player.rect.midtop)
    all_sprites.add(pbullet)



    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move_left()
        if keys[pygame.K_RIGHT]:
            player.move_right()
        if keys[pygame.K_UP]:
            player.move_up()
        if keys[pygame.K_DOWN]:
            player.move_down()

        # Shoot
        if keys[pygame.K_z]:
            pbullet = Pbullet(player.rect.midtop)
            all_sprites.add(pbullet)
            bullet_sprites.add(pbullet)

        if hp > 0:
            for x in range(12):
                bullet = Ebullet(enemy.rect.center, 30*x)
                ebullet_sprites.add(bullet)
                all_sprites.add(bullet)


        # ----- LOGIC
        all_sprites.update()

        #REMOVE BULLETS:
        for bullet in bullet_sprites:
            if bullet.rect.y < -20:
                bullet.kill()

        # ----- DRAW
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # ----- UPDATE
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
