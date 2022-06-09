#Little space game :)
from turtle import title
import pygame
import os
import time
import random
pygame.font.init()

#Spēles logs 
WIDTH, HEIGHT = 750, 750  
WIN= pygame.display.set_mode((WIDTH, HEIGHT)) #Window - pygame.display. - loga Izmērs
pygame.display.set_caption("Space Shooter game!") #Loga nosaukums!


#Konstants - CAPITAL LETTERS
#Ielādet tēlus
#Funkcijas nosaukums/no Pygame moduļa izmanto ielādes funkciju/faila lokācija - (Mapes nosaukums/faila nosaukums)
RED_SPACE_SHIP= pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP= pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP= pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))



#Spēlētāja kuģītis
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

#Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

#Background/ Pielāgo bildi pie Loga izmēriem/WIDTH, HEIGHT.
BACKGROUND = pygame.transform.scale (pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))
BACKGROUND2 = pygame.transform.scale (pygame.image.load(os.path.join("assets", "background2.png")), (WIDTH, HEIGHT))
#Grupas
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    
    def move(self, vel):
        self.y += vel #pievienojot + ies uz augšu
    
    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)



class Ship: #katram kugim ir x/y/Health
    COOLDOWN = 30


    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img= None
        self.laser_img= None
        self.lasers= []
        self.cool_down_counter = 0
        
    

    def draw(self, window):
                                                                        #uztaisīt nelielu čentrstūri        
                                                                        # #Kur atrodās    
                                                                        # #cik liels  pygame.draw.rect(window, (255,0,0), (self.x, self.y, 50,50) , 2) Būs piepildīts/0 nebus piepildīts.
                                                                        #pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 50,50))
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:               #katras lāzeris kurs atrodas uz ekrana
            laser.move(vel)                     #Iet uz leju ar - vel atrumu (px)
            if laser.off_screen(HEIGHT):        #ja iziet ara no ekrana
                self.lasers.remove(laser)       #nonems nost no ekrana
            elif laser.collision(obj):          #ja saskarās ar kadu no (obj)
                obj.health -= 10                #spelētajam atnems 10hp
                self.lasers.remove(laser)       #nonem no speles tik līdz saskarās 

    
    def cooldown(self):
        if self.cool_down_counter>= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1



    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1        


    def get_width(self):
        return self.ship_img.get_width()       
                                            #Izmanto bildes lielumu lai atrastu viņas robežu ! Speletaja kuģim!
    def get_height(self):
        return self.ship_img.get_height()


            #ieliekot iekavas tiek izmantots kopā ar class "Player"
class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img= YELLOW_SPACE_SHIP 
        self.laser_img= YELLOW_LASER
        self.mask= pygame.mask.from_surface(self.ship_img)
        self.max_health = health


    def move_lasers(self, vel, objs):  #ja speltaja lazeris trap pa pretinieku
        self.cooldown()
        for laser in self.lasers:                           #katras lāzeris kurs atrodas uz ekrana
            laser.move(vel)                                 #Iet uz leju ar - vel atrumu (px)
            if laser.off_screen(HEIGHT):                    #ja iziet ara no ekrana
                self.lasers.remove(laser)                   #nonems nost no ekrana
            else:                                           #ja trāpa pretiniiekam - nonem no speles
                for obj in objs:     
                    if laser.collision(obj):                #ja saskarās ar kadu no (obj)
                        objs.remove(obj)                       # pretinieku nonems no ekrana                     
                        if laser in self.lasers:                     
                            self.lasers.remove(laser)       #nonem no speles tik līdz saskarās
                                

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)


                            #HP bar 1. sarkans pāri viņam iet 2. zals katru reizi kad iesauj/ietriecas noiet hp
    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10 ))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))



class Enemy(Ship):
    COLOR_MAP= {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
                }



    def __init__(self, x, y, color, health= 100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel #Kustība notiks uz leju! Pretiniekiem!

            #Salabo no kurienes šaus pretinieki
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-15, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1 

def collide(obj1, obj2):
        offset_x = obj2.x - obj1.x
        offset_y = obj2.y - obj1.y
        return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None #if these to masks overlap   it will return - True/ if they will not over lap its -None
        


#main Loop - Galvenās funkcijas(def)
def main():
    run = True #True - nosaka vai strādās while run funkcija-
    FPS = 60
    level = 0
    lives = 5
    score = 0
    main_font = pygame.font.SysFont("comicsans", 40) #text fonts / dzivibam/level
    score_font = pygame.font.SysFont("comicsans", 25)    
    lost_font = pygame.font.SysFont("comicsans", 40) #text fonts prieks lost texta

    enemies = []#Kur būs pretinieki.
    wave_length = 5  #katru levelu mainisies pozicijas ar katru level maiņu.
    enemy_vel = 1 #Cik ātri kustēsies.


    player_vel = 7 #katru reizi uzspiedos pogu paies 5px
    laser_vel = 5 #laseru atrums
        #speletaju location/hitbox
    player = Player(300,630)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0 #ja zaude

    def redraw_window(): #iekš funkcijā
        WIN.blit(BACKGROUND, (0,0))#Uzliek uz ekrāna #Paņem BACKGROUND- un ielādē 0/0
        #Draw text                                          #red,green,blue(no 0-255)
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
        score_label = score_font.render(f"Score: {score}", 1, (255,255,255))

        #Ielādet lives_label un viņu pozīcija x=10px y=10px
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        WIN.blit(score_label, (300, 10))

        for enemy in enemies:
            enemy.draw(WIN)


        player.draw(WIN)
        
        if lost: #Ja 
            lost_laber = lost_font.render("You LOST!", 1, (255, 255, 255)) #texts
            WIN.blit(lost_laber, (WIDTH/2 - lost_laber.get_width()/2, 350 )) #atnemot pusi no WIDTH - no Txt fonta atnem pusi no lost_laber = texts bus pa vidu ekranam

        pygame.display.update() #Refresh display


    while run:

        clock.tick(FPS) #Izmantos FPS - 60 ticks per second
         #Loopā izmanto šo funkciju. (Redraw_window/funkcijas nosaukums)
        redraw_window() 

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3: #Paradis zinu 3 sec per 60 fps
                run = False     #ja ir vairak pa > FPS * 3: spele apstasies
            else:
                continue # ja nav tad spele turpinas

        if len(enemies) == 0: #katru reizi beidzas pretinieki
            level += 1 #pievieno klāt līmeni
            wave_length += 5 #katru lvl pievieno 5 pretiniekus klat

            for i in range(wave_length): #kur un ka vini rādīsies
                                            #X- pozicija                      #Y pozicija #-100 lai neiet ara no ekrana pa sāniem
                enemy= Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500,-100), random.choice(["red", "green", "blue"]))
                                                                                                #randoma izvēlās no 3 variantiem
                enemies.append(enemy) #Pievieno pie enemy grupas/ pievienojās kustība
       

        for event in pygame.event.get(): #Ik pēc 60tickiem vins pārbauda, ja kāda no lietam notiks tā laikā aktivizēsies apaksējās funkcijas 
            if event.type == pygame.QUIT: #Ja nospiedīs augsā uz krustiņu - spēle apstāsies/aizvērsies/ #if event.type == pygame.KEYDOWN/ visas Eveny.type meklēt pygame majaslapā
                quit()
     

        keys = pygame.key.get_pressed() #Nospiežot parbaudis kuras pogas tiek izmantotas.
        if keys[pygame.K_a] and player.x - player_vel > 0 : #Uz kreiso
            player.x -= player_vel #pa kreisi kas ir norādits player-vel (cik pixelus)
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: #Uz labo
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0: #Uz augšu
            player.y -= player_vel
            # player_vel + player.y pozīcija ir mazaka par (Height)- Lauj kusēties ja neesmu < neļauj (Pievienot +50 nozīmē pievienot klucitim savu lielumu klāt.)
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 20 < HEIGHT: #Uz leju
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()   #laser shoot


        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player) #vai lāzeris pieskaras spēlētājam.
            #enemy shot
            if random.randrange(0, 160) == 1:
                enemy.shoot()
#Kad Pretinieks saskaras ar speletaju - nonem 10 hp nost no speletaja un nonem pretinieku
            if collide(enemy, player):
                player.health -= 10
                score += 1
                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)


        player.move_lasers(-laser_vel, enemies) 

                
                
                #main menu!!!!!

def main_menu():
    title_font = pygame.font.SysFont("comicsans", 30)   #teksta fonts/grupa/izmers
    welcome_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        WIN.blit(BACKGROUND2, (0,0)) # Pāri backgroundam

        welcome_label = welcome_font.render("Space Attack!", 0, (255,255,255))
        WIN.blit(welcome_label, (WIDTH/2 - welcome_label.get_width()/2, 50))

        title_label = title_font.render("Click to play", 0, (255,255,255))# uzlikt tekstu "" /krasa
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 700)) #kur atrodas
        pygame.display.update() #Refresh screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main() 
    pygame.quit()




main_menu()
            
        