import pygame
import random
# Initializers

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
player = pygame.Rect(20, screen_height/2 - 70, 10, 140)
opponent = pygame.Rect(screen_width-30, screen_height/2 - 70, 10, 140)
background = pygame.Color('grey12')
light_grey = (200, 200, 200)
ball_speed = pygame.Vector2(7, 7)
player_speed = 0
opponent_speed = 7
player_score = 0
opponent_score = 0
# Timer

score_time = None

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
        ball_speed.y *= -1
    if ball.left <= 0:
        opponent_score += 1
        score_time = pygame.time.get_ticks()
    if ball.right >= screen_width:
        player_score += 1
        score_time = pygame.time.get_ticks()
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed.x *= -1
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
    if score_time:
        ball_restart()
    # Screen Update
    pygame.display.update()
    # limits FPS to 60
    clock.tick(60)

pygame.quit()
