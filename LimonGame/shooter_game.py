#Создай собственный Шутер!
from random import *
from pygame import *


from time import time as timer
window = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
run = True
speed = 3
font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 36)
mixer.init()
mixer.music.load('Spacy.ogg')
fire_sound = mixer.Sound('fire.ogg')
mixer.music.play()
game = True
finish = False
lost = 0
bullets_num = 0
destroy = 0
lives = 3
reloiad = False
win = font1.render('YOU WIN!', True, (0, 255, 0))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
class GameSprite(sprite.Sprite):
   #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       super().__init__()
       # каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
    def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < 700 - 80:
           self.rect.x += self.speed
   def fire(self):
       bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 500:
            lost += 1
            self.rect.x = randint(80, 700-80)
            self.rect.y = 0
class Meteor(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.x = randint(80, 700-100)
            self.rect.y = 0
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
monsters = sprite.Group()
bullets = sprite.Group()
strikes = sprite.Group()
UFO = Player('rocket.png', 340, 400, 65, 100, 5)

FPS = 60
clock = time.Clock()
for i in range(0,6):
    monster = Enemy('ufo.png', randint(0, 700-80), -40, 80, 50, randint(1,2))
    monsters.add(monster)
for i in range(0,2):
    strike = Meteor('asteroid.png', randint(0, 700-100), 0, 70, 70, randint(2,4))
    strikes.add(strike)
while run == True:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
           if e.key == K_SPACE:
               if bullets_num < 5 and reloiad == False:
                bullets_num += 1
                fire_sound.play()
                UFO.fire()
    if finish != True:
        window.blit(background, (0, 0))
        UFO.update()
        UFO.reset()
        monsters.update()
        monsters.draw(window)
        strikes.update()
        strikes.draw(window)
        text = font1.render("Счет: " + str(destroy), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        bullets.draw(window)
        bullets.update()
        text_lose = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        text_reload = font1.render("Перезарядка орудий!", 1, (98, 0, 51))
        text_lives = font1.render(str(lives) + ":Жизни", 1, (120, 183, 106))
        window.blit(text_lose, (10, 50))
        window.blit(text_lives, (550, 20))
        sprite_list = sprite.groupcollide(
            monsters, bullets, True, True
        )
        if bullets_num  >= 5 and reloiad == False : #если игрок сделал 5 выстрелов
            last_time = timer() #засекаем время, когда это произошло
            reloiad = True #ставим флаг перезарядки
        if reloiad == True:
            now_time = timer() #считываем время

            if now_time - last_time < 2: #пока не прошло 3 секунды выводим информацию о перезарядке
                window.blit(text_reload, (200,400))
            else:
                bullets_num = 0   #обнуляем счётчик пуль
                reloiad = False #сбрасываем флаг перезарядки
        for c in sprite_list:
            destroy = destroy+1
            monster = Enemy('ufo.png', randint(0, 700-80), -40, 80, 50, randint(1,5))
            monster.add(monsters)
        if destroy >= 20:
            finish = True
            window.blit(win, (280, 200))
        if sprite.spritecollide(UFO, monsters, False) or sprite.spritecollide(UFO, strikes, False):
           sprite.spritecollide(UFO, monsters, True)
           sprite.spritecollide(UFO, strikes, True)
           lives = lives - 1
        if lost >= 100 or lives <= 0:
            finish = True
            window.blit(lose, (280, 200))
        display.update()
        clock.tick(FPS)