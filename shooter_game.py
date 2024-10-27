#Создай собственный Шутер!

from pygame import *
from random import *
from time import time as timer

window = display.set_mode((700, 500))
display.set_caption('шутер')
background = transform.scale(image.load('galaxy.jpg'), (700,500))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')
number = 0
lost = 0
font.init()
font1 = font.SysFont(None, 36)

class GameSprite(sprite.Sprite):
    def __init__(self,player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= speed
        if keys_pressed[K_d] and self.rect.x < 595:
            self.rect.x += speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,15,20, 5)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed 
        global lost
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(0,700)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

life = 10
bullets = sprite.Group()
score = 0
rel_time = False
num_fire = 0

asteroids = sprite.Group()
for i in range(1,4):
    asteroid = Enemy('asteroid.png', randint(0,700), -40,80,50, randint(1,7))
    asteroids.add(asteroid)


monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png', randint(0,700), -40,80, 50, randint(1,3) )
    monsters.add(monster)


kick = mixer.Sound('fire.ogg')
clock = time.Clock()
FPS = 60
rocket = Player('rocket.png',300,400,80,100,10)
game = True
speed = 13
finish = False
while game:
    for e in event.get():
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    rocket.fire()
                    kick.play()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
        if e.type == QUIT:
            game = False
            
    if not finish:
        text_lose = font1.render('Пропущено:' + str(lost), 1, (255,255,255))
        text_got = font1.render('Счёт:' + str(score), 1, (255,255,255))
        window.blit(background, (0,0))
        window.blit(text_lose, (0,0))
        window.blit(text_got, (0,50))
        rocket.reset()
        rocket.update()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        if lost >= 3 or sprite.spritecollide(rocket, monsters, False):  
            text_win = font1.render('YOU LOST', 1, (255, 0, 0))
            window.blit(text_win, (250,250))
            finish = True
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font1.render('wait,reload...', 1, (150,0,0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(0,700), -40,80, 50, randint(1,3) )
            monsters.add(monster)
        if score >= 10:
            finish = True
            you_win = font1.render('YOU WON!', True, (0, 255, 0))
            window.blit(you_win,(250,250))




    clock.tick(FPS)
    display.update()