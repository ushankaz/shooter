#Создай собственный Шутер!
from time import sleep
from time import time as timer
from pygame import *
from random import randint
win = display.set_mode((900, 900))
display.set_caption('Shooter Game')
background = transform.scale(image.load('galaxy.jpg'), (900, 900))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_s = mixer.Sound('fire.ogg')

font.init()
font1 = font.Font(None, 36)
lost = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

 
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 830:
            self.rect.x += self.speed
        
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -8)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 850:
            self.rect.y = 0
            self.rect.x = randint(80, 820)
            lost += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill()

class Asteroids(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 850:
            self.rect.y = 0
            self.rect.x = randint(80, 820)



player = Player('rocket.png', 5, 825, 65, 65, 6)
monsters = sprite.Group()
for i in range(5):
    b1 = Enemy('ufo.png', randint(30, 820), 0, 80, 60, randint(2, 4))
    monsters.add(b1)
asteroids = sprite.Group()
for i in range(2):
    b2 = Asteroids('asteroid.png', randint(30, 820), 0, 80, 60, randint(3, 6))
    asteroids.add(b2)
bullets = sprite.Group()
hp = 3
score = 0
run = True
FPS = 60
clock = time.Clock()
finish = False

rel = False
num_fire = 0 
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel == False:
                    player.fire()
                    fire_s.play()
                    num_fire += 1
                if num_fire >= 5 and rel == False:
                    start = timer()
                    rel = True
                
            
    if finish == False:

    
    
        win.blit(background, (0, 0))
        
        monsters.update()
        monsters.draw(win)
        asteroids.update()
        asteroids.draw(win)
        player.update()
        player.reset()
        bullets.update( )
        bullets.draw(win)
        
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for i in sprites_list:
            score += 1
            b1 = Enemy('ufo.png', randint(80, 820), 0, 80, 60, randint(2, 4))
            monsters.add(b1)

        bull_ast = sprite.groupcollide(asteroids, bullets, False, True)
        #for i in bull_ast:
            
            
        if rel == True:
            end = timer()
            if end - start < 2:
                text_reload = font1.render('Перезарядка...', True, (255, 0, 0))
                win.blit(text_reload, (450, 450))
            else:
                num_fire = 0
                rel = False
        
        

        text_win = font1.render('Счет: ' + str(score), True, (255, 255, 255))
        win.blit(text_win, (10, 20))
        if sprite.spritecollide(player, monsters, True):
            hp -= 1
        if sprite.spritecollide(player, asteroids, True):
            hp -= 1
        if score >= 20:
            WIN = font1.render('YOU WIN', True, (255, 255, 0))
            win.blit(WIN, (400, 400))
            finish = True
        if  lost >= 10 or hp <= 0:
            LOSE = font1.render('YOU LOSE', True, (255, 0, 0))
            win.blit(LOSE, (400, 400))
            finish = True
        
            
        text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        win.blit(text_lose, (10, 50))
        display.update()
        text_hp = font1.render('Здоровье:' + str(hp), 1, (255, 255, 255))
        win.blit(text_hp, (10, 80))
        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        hp = 3
        for i in bullets:
            i.kill()
        for i in monsters:
            i.kill()
        for i in asteroids:
            i.kill()
        sleep(3)
        for i in range(5):
            b1 = Enemy('ufo.png', randint(80, 820), 0, 80, 60, randint(2, 4))
            monsters.add(b1)
        for i in range(2):
            b2 = Asteroids('asteroid.png', randint(30, 820), 0, 80, 60, randint(3, 6))
            asteroids.add(b2)
    display.update()
    clock.tick(FPS)
    
