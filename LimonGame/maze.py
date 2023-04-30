#создай игру "Лабиринт"!
from pygame import *

window = display.set_mode((700, 500))
display.set_caption('Догонялки')
background = transform.scale(image.load('background.jpg'), (700, 500))
player = transform.scale(image.load('hero.png'), (65, 65))
enemy = transform.scale(image.load('cyborg.png'), (65, 65))
chest = transform.scale(image.load('treasure.png'), (80, 80))
font.init()
x2 = 10
y2 = 420
y1 = 280
x1 = 620
speed = 5
mixer.init()
mixer.music.load('Epic-Chase.ogg')
mixer.music.play()
game = True
clock = time.Clock()
class GameSprite(sprite.Sprite):
   #конструктор класса
   def __init__(self, player_image, player_x, player_y, player_speed):
       super().__init__()
       # каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (65, 65))
       self.speed = player_speed
       # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y


   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
class Enemy(GameSprite):
    def update(self):
        if self.rect.x <= 470:
            self.direction = 'right'
        if self.rect.x >= 700 - 85:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Player(GameSprite):
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < 700 - 80:
           self.rect.x += self.speed
       if keys[K_UP] and self.rect.y > 5:
           self.rect.y -= self.speed
       if keys[K_DOWN] and self.rect.y < 500 - 80:
           self.rect.y += self.speed
class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_widgh, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.widgh = wall_widgh
        self.height = wall_height
        self.color_2 = color_2
        self.color_3 = color_3
        self.image = Surface((self.widgh, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
wall1 = Wall(101, 117, 90, 50, 10, 600, 10)
wall2 = Wall(101, 117, 90, 350, 140, 10, 400)
wall3 = Wall(101, 117, 90, 45, 10, 10, 400)
player = Player('hero.png', x2, y2, 5)
enemy = Enemy('cyborg.png', x1, y1, 5)
chest = GameSprite('treasure.png', 700 - 120, 500 - 80, 0)
FPS = 60
font = font.Font(None, 70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))
finish = False
money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

while game:
    for e in event.get():
        if e.type == QUIT:
           game = False
 
    if finish != True:
       window.blit(background,(0, 0))
       player.update()
       enemy.update()
     
       player.reset()
       enemy.reset()
       chest.reset()


       wall1.draw_wall()
       wall2.draw_wall()
       wall3.draw_wall()


        #Ситуация "Проигрыш"
    if sprite.collide_rect(player, enemy) or sprite.collide_rect(player, wall1) or sprite.collide_rect(player, wall2)or sprite.collide_rect(player, wall3):
        finish = True
        window.blit(lose, (200, 200))
        kick.play()
            #Ситуация "Выигрыш"
    if sprite.collide_rect(player, chest):
        finish = True
        window.blit(win, (200, 200))
        money.play()

    display.update()
    clock.tick(FPS)