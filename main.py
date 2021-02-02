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

# Calculates time between shots
tick = 0

# Music files


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
        if self.rect.right > WIDTH:
            self.enemy_x_vel *= -1
            self.rect.right = WIDTH
        elif self.rect.left < 0:
            self.enemy_x_vel *= -1
            self.rect.left = 0

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
        if self.rect.top < -20:
            self.kill()

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

class Gen_bullet(pygame.sprite.Sprite):
    def __init__(self, coords):
        super().__init__()

        self.image = pygame.Surface((20,20))
        self.image.fill((255,0,255))

        self.rect = self.image.get_rect()
        self.rect.center = coords



        self.velocity = 10

    def update(self):
        self.rect.y += self.velocity
        if (self.rect.bottom > HEIGHT):
            self.kill()


# ----- SCREEN PROPERTIES
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption(TITLE)

def write_text(text, x, y, font_size):
    font = pygame.font.Font(pygame.font.get_default_font(), font_size)
    text_surface = font.render(text, False, WHITE)
    screen.blit(text_surface, (x, y))


def main():
    pygame.init()



    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()

    # Populate sprite groups
    enemy = Enemy()
    enemy.rect.y = 50
    enemy.rect.x = 225

    # Points
    points = 0
    # Boss hp
    hp = 2000

    # Bomb
    bomb = 1

    all_sprites.add(enemy)
    enemy_sprites.add(enemy)


    player = Player()
    all_sprites.add(player)
    player.rect.y = 600
    player.rect.x = 350

    pbullet = Pbullet(player.rect.midtop)
    all_sprites.add(pbullet)

    tick = 0
    bullet_offset = 0

    music = './music/boss_theme.mp3'
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(loops=True)
    alert_sound = pygame.mixer.Sound('./music/Alert.wav')
    bullet_sound = pygame.mixer.Sound('./music/bullet.wav')
    bomb_sound = pygame.mixer.Sound('./music/thunder.wav')
    alert_sound.set_volume(1)
    bullet_sound.set_volume(1)
    bomb_sound.set_volume(1)
    warning = True

    bomb_on = False
    bomb_tick = 0

    # ----- MAIN LOOP
    while not done:
        if hp >= 1800:
            speed = 30
        if hp < 1800 and hp > 1399:
            speed = 20
        if hp < 1400 and hp > 699:
            speed = 10
        if hp <=700:
            speed = 7
            if warning:
                alert_sound.play()
                warning = False
            if enemy.enemy_x_vel < 0:
                enemy.enemy_x_vel = -8
            else:
                enemy.enemy_x_vel = 8

        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True


        # Hit detection
        for obstacle in ebullet_sprites:
            if obstacle.rect.collidepoint(player.rect.center):
                done = True
            elif obstacle.rect.colliderect(player.rect):
                points += 1
        for pobstacle in bullet_sprites:
            if pobstacle.rect.colliderect(enemy.rect):
                hp -= 1
                pobstacle.kill()



        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            player.x_vel = player.y_vel = 3
        if keys[pygame.K_LEFT]:
            player.move_left()
        if keys[pygame.K_RIGHT]:
            player.move_right()
        if keys[pygame.K_UP]:
            player.move_up()
        if keys[pygame.K_DOWN]:
            player.move_down()

        player.y_vel = player.x_vel = 5

        # Shoot
        if keys[pygame.K_z]:
            pbullet = Pbullet(player.rect.midtop)
            all_sprites.add(pbullet)
            bullet_sprites.add(pbullet)

        if keys[pygame.K_x] and bomb > 0:
            bomb -= 1
            bomb_on = True
            bomb_sound.play()


        if bomb_on:
            bomb_tick += 1
            if bomb_tick == 0.5 * 60:
                bomb_on = False
                bomb_tick = 0


        if hp > 0:
            for x in range(12):
                if tick % speed == 0:
                    bullet = Ebullet(enemy.rect.center, (30*x + bullet_offset))
                    ebullet_sprites.add(bullet)
                    all_sprites.add(bullet)
                    if hp <= 0 or bomb_on:
                        for ebullet in ebullet_sprites:
                            ebullet.kill()

            if tick % speed == 0:
                bullet_offset += 6


            if tick % speed == 0:

                gen_bullet = Gen_bullet((enemy.rect.centerx + random.randrange(-100, 100), enemy.rect.centery))
                ebullet_sprites.add(gen_bullet)
                all_sprites.add(gen_bullet)
                bullet_sound.play()
                if hp <= 0 or bomb_on:
                    for ebullet in ebullet_sprites:
                        ebullet.kill()
        if hp <= 0:
            enemy.kill()


        # Bullet speed



        # ----- LOGIC
        all_sprites.update()

        #REMOVE BULLETS:
        for bullet in bullet_sprites:
            if bullet.rect.y < -20:
                bullet.kill()

        # ----- DRAW
        screen.fill(BLACK)
        all_sprites.draw(screen)

        write_text(f"HP:{hp}", 300, 10, 50)
        write_text(f"Points:{points}", 10, 10, 30)
        if hp <= 0:
            write_text("YOU WIN!!!", 200, 300, 80)
        write_text(f"BOMB:{bomb}", 650, 10, 30)

        # ----- UPDATE
        pygame.display.flip()
        clock.tick(60)

        tick += 1

    pygame.quit()


if __name__ == "__main__":
    main()
