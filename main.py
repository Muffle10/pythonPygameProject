import pygame
import random
class Block(pygame.sprite.Sprite):
    def __init__(self, path, x, y):
        super().__init__()
        self.image = pygame.image.load(path)
        self.image.fill(color)
        self.rect = self.image.get_rect( center = (x,y))

class Ball(Block):
    def __init__(self, path, x, y, speed, paddles):
        super().__init__(path, x, y)
        self.speed.x = speed.x * random.choice((-1,1))
        self.speed.y = speed.y * random.choice((-1,1))
        self.paddles = paddles
        self.active=False
        self.score_time = 0
    def update(self):
        if self.active:
            self.rect.x += self.speed.x
            self.rect.y += self.speed.y
            self.collisions()
        else:
            self.restart()
    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= screen.height:
            pygame.mixer.Sound.play(pong_sound)
            self.speed.y *= -1
        if pygame.sprite.spritecollide(self, self.paddles, False):
            pygame.mixer.Sound.play(pong_sound)
            collision_paddle = pygame.sprite.spritecollide(self, self.paddles, False)[0].rect
            if abs(self.rect.left - collision_paddle.right) < 10 and self.speed.y > 0:
                self.speed.x *= -1	
            elif abs(self.rect.right - collision_paddle.left) < 10 and self.speed.y < 0:
                self.speed.x *= -1	
            elif abs(self.rect.bottom - collision_paddle.top) and self.speed.y > 0:
                self.speed.y *= -1	
            elif abs(self.rect.top - collision_paddle.bottom) and self.speed.y < 0:
                self.speed.y *= -1	
    def restart(self):
        self.active = False
        self.speed.x *= random.choice((-1,1))
        self.speed.y *= random.choice((-1,1))
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (screen_width/2, screen_height/2)
            

class Player(Block):
    def __init__(self, path,x,y, speed):
        super().__init__(path,x,y)
        self.speed = speed
        self.movement = 0
    def screen_constraint(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
    def update(self):
        self.rect.y += self.movement
        self.screen_constraint()
class Opponent(Block):
    pass
class GameManager:
    pass

# Initializers
pygame.mixer.pre_init(44100, -16, 2,512)
pygame.init()
screen_width = 960
screen_height = 720
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")
game_font = pygame.font.Font("freesansbold.ttf", 32)
running = True

print(screen_height)
# Variables
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = Player("Paddle.png", 30, screen_height/2 - 70,5)
opponent = pygame.Rect(screen_width-30, screen_height/2 - 70, 10, 140)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)

background = pygame.Color('#2F373F')
light_grey = (200, 200, 200)
ball_speed = pygame.Vector2(7, 7)
player_speed = 0
opponent_speed = 7
player_score = 0
opponent_score = 0
# Timer and Sound

score_time = None
pong_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")

# Functions

def ball_restart():
    global score_time
    ball.center = (screen_width/2, screen_height/2)
    current_time = pygame.time.get_ticks()

    if current_time - score_time < 700:
        three = game_font.render("3", False, light_grey)
        screen.blit(three, (screen_width/2 - 10, screen_height/2 + 20))
    if 700 < current_time - score_time < 1400:
        two = game_font.render("2", False, light_grey)
        screen.blit(two, (screen_width/2 - 10, screen_height/2 + 20))
    if 1400 < current_time - score_time < 2100:
        one = game_font.render("1", False, light_grey)
        screen.blit(one, (screen_width/2 - 10, screen_height/2 + 30))
    
    if current_time - score_time == 700:
        pygame.mixer.Sound.play(score_sound)
    if 1380 < current_time - score_time < 1400:
        pygame.mixer.Sound.play(score_sound)
    if 2080 < current_time - score_time < 2100:
        pygame.mixer.Sound.play(score_sound)
    if current_time - score_time < 2100:
        ball_speed.x, ball_speed.y = 0, 0
    else:
        ball_speed.x = 7 * random.choice((-1, 1))
        ball_speed.y = 7 * random.choice((-1, 1))
        score_time = None
    ball_speed.y *= random.choice((1, -1))
    ball_speed.x *= random.choice((1, -1))


def ball_move():
    global opponent_score, player_score, score_time
    if ball.top <= 0 or ball.bottom >= screen_height:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed.y *= -1
    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        opponent_score += 1
        score_time = pygame.time.get_ticks()
    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        score_time = pygame.time.get_ticks()


    if ball.colliderect(player) and ball_speed.x <0 :
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - player.right) < 10:
            ball_speed.x *= -1	
        elif abs(ball.bottom - player.top) and ball_speed.y > 0:
            ball_speed.y *= -1	
        elif abs(ball.top - player.bottom) and ball_speed.y < 0:
            ball_speed.y *= -1	

    if ball.colliderect(opponent) and ball_speed.x > 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - opponent.left) < 10:
            ball_speed.x *= -1
        elif abs(ball.bottom - opponent.top) and ball_speed.y > 0:
            ball_speed.y *= -1	
        elif abs(ball.top - opponent.bottom) and ball_speed.y < 0:
            ball_speed.y *= -1	
    ball.x += ball_speed.x
    ball.y += ball_speed.y


def player_move():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def opponent_move():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height
    if opponent.top <= 0:
        opponent.top = 0


# Run game
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7

    # Actions and Logic
    player_text = game_font.render(f"{player_score}", False, light_grey)
    opponent_text = game_font.render(f"{opponent_score}", False, light_grey)
    ball_move()
    player_move()
    opponent_move()

    # fill the screen with a color to wipe away anything from last frame

    screen.fill(background)

    # RENDER YOUR GAME HERE
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width/2,
                       0), (screen_width/2, screen_height))
    player_text = game_font.render(f"{player_score}", False, light_grey)
    screen.blit(player_text, (495, 470))
    screen.blit(opponent_text, (450, 470))
    screen.blit(block.image, (100,100))
    if score_time:
        ball_restart()
    # Screen Update
    pygame.display.update()
    # limits FPS to 60
    clock.tick(60)

pygame.quit()
