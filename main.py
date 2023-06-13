import pygame
import math
print("Hello World")
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
rectangle = pygame.Rect(300, 300, 50, 50)
ball = pygame.Vector2(100, 200)
ball_vel = pygame.Vector2(5, 5)
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    # RENDER YOUR GAME HERE
    pygame.draw.rect(screen, (255, 20, 20), rectangle)
    pygame.draw.rect(screen, (255, 20, 20), ball_mesh)
    pygame.draw.circle(screen, "blue", ball, 20)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        rectangle.y -= 10
    if keys[pygame.K_s]:
        rectangle.y += 10
    if keys[pygame.K_a]:
        rectangle.x -= 10 
    if keys[pygame.K_d]:
        rectangle.x += 10
    ball.x += ball_vel.x
    ball.y += ball_vel.y
    if ball.x - 20 < 0:
        ball_vel.x *= -1
    if ball.x + 20 > 800:
        ball_vel.x *= -1
    if ball.y - 20 < 0:
        ball_vel.y *= -1
    if ball.y + 20 > 600:
        ball_vel.y *= -1
    # flip() the display to put your work on screen
    pygame.display.update()

    clock.tick(60)  # limits FPS to 60

pygame.quit()