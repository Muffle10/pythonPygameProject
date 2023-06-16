import pygame
import random
class Block(pygame.sprite.Sprite):
    def __init__(self, path, x, y):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect( center = (x,y))

class Ball(Block):
    def __init__(self, path, x, y, speed, paddles):
        super().__init__(path, x, y)
        self.speed = pygame.Vector2()
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
            self.counter()
    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            pygame.mixer.Sound.play(pong_sound)
            self.speed.y *= -1
        if pygame.sprite.spritecollide(self, self.paddles, False):
            pygame.mixer.Sound.play(pong_sound)
            collision_paddle = pygame.sprite.spritecollide(self, self.paddles, False)[0].rect
            if abs(self.rect.right- collision_paddle.left) < 10 and self.speed.x > 0:
                self.speed.x *= -1	
            elif abs(self.rect.left - collision_paddle.right) < 10 and self.speed.x < 0:
                self.speed.x *= -1	
            elif abs(self.rect.bottom - collision_paddle.top) and self.speed.y > 0:
                self.rect.top = collision_paddle.bottom
                self.speed.y *= -1	
            elif abs(self.rect.top - collision_paddle.bottom) and self.speed.y < 0:
                self.rect.bottom = collision_paddle.top
                self.speed.y *= -1	
    def restart(self):
        self.active = False
        self.speed.x *= random.choice((-1,1))
        self.speed.y *= random.choice((-1,1))
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (screen_width/2, screen_height/2)
    def counter(self):
        current_time = pygame.time.get_ticks()
        count = 3
        if current_time - self.score_time < 700:
            three = game_font.render("3", False, light_grey)
            screen.blit(three, (screen_width/2 - 10, screen_height/2 + 20))
        if 700 < current_time - self.score_time < 1400:
            two = game_font.render("2", False, light_grey)
            screen.blit(two, (screen_width/2 - 10, screen_height/2 + 20))
        if 1400 < current_time - self.score_time < 2100:
            one = game_font.render("1", False, light_grey)
            screen.blit(one, (screen_width/2 - 10, screen_height/2 + 30))
        if current_time - self.score_time > 2100:
            self.active = True
    

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
    def update(self, ball_group):
        self.rect.y += self.movement
        self.screen_constraint()
class Opponent(Block):
    def __init__(self,path, x,y,speed):
        super().__init__(path,x,y)
        self.speed = speed
    def update(self, ball_group):
        if(self.rect.top < ball_group.sprite.rect.y):
            self.rect.y += self.speed
        if(self.rect.bottom > ball_group.sprite.rect.y):
            self.rect.y -= self.speed
        self.constrain()
    def constrain(self):
        if self.rect.top <= 0: self.rect.top = 0
        if self.rect.bottom >= screen_height: self.rect.bottom = screen_height
class GameManager:
    def __init__(self, ball_group, paddle_group):
        self.player_score = 0
        self.opponent_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group
    def run_game(self):
		# Drawing the game objects
        self.paddle_group.draw(screen)
        self.ball_group.draw(screen)

		# Updating the game objects
        self.paddle_group.update(self.ball_group)
        self.ball_group.update() 
        self.reset_ball()
        self.draw_score()
    def reset_ball(self):
        if self.ball_group.sprite.rect.right >= screen_width:
            self.opponent_score += 1
            self.ball_group.sprite.restart()
        if self.ball_group.sprite.rect.left <= 0:
            self.player_score += 1
            self.ball_group.sprite.restart()
    def draw_score(self):
        player_score = game_font.render(str(self.player_score),True,"red")
        opponent_score = game_font.render(str(self.opponent_score),True,"red")

        player_score_rect = player_score.get_rect(midleft = (screen_width / 2 + 40,screen_height/2))
        opponent_score_rect = opponent_score.get_rect(midright = (screen_width / 2 - 40,screen_height/2))
        screen.blit(player_score,player_score_rect)
        screen.blit(opponent_score,opponent_score_rect)

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
# Game Variables
player = Player("Paddle.png", 30, screen_height/2 - 70,5)
opponent = Opponent("Paddle.png", screen_width-30, screen_height/2 - 70, 5)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(opponent)
ball = Ball('Ball (1).png',screen_width/2,screen_height/2,pygame.Vector2(4,4),paddle_group)
ball2 = Ball('Ball (1).png',screen_width/2,random.choice((100,200)),pygame.Vector2(4,4),paddle_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)
game_manager = GameManager(ball_sprite,paddle_group)
middle_strip = pygame.Rect(screen_width/2 - 2,0,4,screen_height)
# Variables
background = pygame.Color('#2F373F')
light_grey = (200, 200, 200)

#Sound

pong_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")



# Run game
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player.movement+=player.speed 
            if event.key == pygame.K_UP:
                player.movement-=player.speed 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                 player.movement-=player.speed 
            if event.key == pygame.K_UP:
                 player.movement+=player.speed 

    # fill the screen with a color to wipe away anything from last frame

    screen.fill(background)
    pygame.draw.rect(screen, "orange", middle_strip)
    game_manager.run_game()
    # Screen Update
    pygame.display.flip()
    # limits FPS to 60
    clock.tick(60)

pygame.quit()
