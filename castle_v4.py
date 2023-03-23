# Veggtekstur hentet fra: https://opengameart.org/content/handpainted-stone-wall-textures
# Soldat sprite henta fra: https://opengameart.org/content/2d-soldier-guy-character
# Helikopter sprite henta fra: https://opengameart.org/content/attack-helicopter
# Tank sprites henta fra: https://opengameart.org/content/animated-tank
# Bakgrunn henta fra: https://opengameart.org/content/background-2
#Soldat hitlyd henta fra: https://opengameart.org/content/5-hit-sounds-dying
#Spillmusikk henta fra: https://opengameart.org/content/laments-of-the-war
#Helikopterlyder henta fra: https://opengameart.org/content/helicopter-sounds
#Trefflyder henta fra: 

import pygame as pg
from random import randint
import os  #Brukes for å iterere gjennom mapper


WIDTH = 1000
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)
FPS = 120

#Farger

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (220, 0, 0)

GRAVITY = -0.2
#GRAVITY = -0.4
PVP = True

#Initaliserer pygame
pg.init()

#Musikk
pg.mixer.music.load("./Lyder/Lament_of_war.mp3")
pg.mixer.music.set_volume(0.06)
pg.mixer.music.play()

#Lager en overflate
surface = pg.display.set_mode(SIZE)

#Lager en klokke
clock = pg.time.Clock()

#Bakgrunnsbilde
backgroundImg = pg.image.load('./Bilder/background/airadventurelevel1.png')
backgroundImg = pg.transform.scale(backgroundImg, SIZE)

#Slyngebilde
slingshotImg = pg.image.load("./Bilder/slingshot.png")
hitboxSlingshot = slingshotImg.get_rect()
slingshotImg = pg.transform.scale( slingshotImg, (hitboxSlingshot.width//30, hitboxSlingshot.height//30))


#Øverste klassen
class Objekt:
    
    def __init__(self, x, y, farge, fartX = 0, fartY = 0, aY = 0):
        
        self.x = x
        self.y = y
        self.fartX = fartX
        self.fartY = fartY
        self.aY = aY
        
        self.farge = farge
        
    def updatePosition(self):
        
        self.x += self.fartX
        self.y += self.fartY

#Tekst
class Tekst(Objekt):
    tekstList = []
    def __init__(self, tekst, x, y, farge, fontSize):
        
        super().__init__(x,y,farge)
        self.tekst = tekst
        self.fontSize = fontSize
        self.font = pg.font.SysFont("Arial", fontSize)
        self.img = self.font.render(tekst, True, farge)
        self.rect = self.img.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        
        Tekst.tekstList.append(self)
        
    def draw(self):
        surface.blit(self.img, (self.x - self.rect.width//2, self.y - self.rect.height//2))
    
    def hoverTekst(self,mousePos):
            
            if mousePos[0] >= self.x - self.width//2 and mousePos[0] <= self.x + self.width//2 and mousePos[1] >= self.y - self.height//2 and mousePos[1] <= self.y + self.height//2:
                self.img = self.font.render(self.tekst, True, RED)
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
                return True
            else:
                self.img = self.font.render(self.tekst, True, BLACK)
                return False
 
        
class Prosjektil(Objekt):
    
    prosjektilListe = []
    
    def __init__(self, x, y, farge, radius, startPoint, fartX = 0, fartY = 0, aY = GRAVITY,):
        super().__init__(x, y, farge, fartX, fartY, aY)
        self.radius = radius
        self.alive = False
        self.startPoint = startPoint
        
        Prosjektil.prosjektilListe.append(self)
        
        
    def updatePosition(self):
        
        super().updatePosition()
        
    #Sjekker om posisjonen er verdt å oppdateres. Sjekker kollisjon med de vertikale sidene
        if self.x >= WIDTH - self.radius or self.x < 0 + self.radius:
            self.alive = False
            self.x = self.startPoint[0]
            self.y = self.startPoint[1]
            return
        
        #Sjekker kollisjon med x aksen
        if self.y  <= self.radius:
            self.alive = False
            self.x = self.startPoint[0]
            self.y = self.startPoint[1]
            
        else:
            self.fartY += self.aY
            #self.y = 2 * self.radius
            
        
    def draw(self):
        if self.alive: 
            pg.draw.circle(surface, self.farge,(self.x, HEIGHT - self.y), self.radius)
        

    def collision(self, objekt):
        
        #Sjekker først kollisjon med topp-flaten. 
        if self.x >= objekt.x and self.x <= objekt.x + objekt.width and self.y - self.radius <= objekt.y and self.y >= objekt.y - objekt.height:
            self.fartY = -0.7 * self.fartY
            self.y = objekt.y + self.radius
            return True #Dette løser problemer knyttet til hjørnekollisjon, siden return gir kula en prioriteringsrekkefølge
        
        #Sjekker kollisjon med venstre vegg
        elif self.x + self.radius >= objekt.x and self.x <= objekt.x + objekt.width and self.y <= objekt.y and self.y >= objekt.y - objekt.height :
            self.fartX = -0.8 * self.fartX
            self.x = objekt.x - self.radius
            self.aY = GRAVITY
            return True
        
        #Sjekker kollisjon med bunnen: slik kollisjon skjer kun hvis man skyter undersiden av et fly, ofte ved å sprette ballen på en tanks
        elif self.x >= objekt.x and self.x <= objekt.x + objekt.width and self.y - self.radius <= objekt.y and self.y + self.radius >= objekt.y - objekt.height:
            self.fartY = -0.9 * fartY
            self.y = objekt.y - objekt.height - self.radius
            return True
        
        #Sjekker kollisjon med høyre vegg, skjer når ballen spretter tilbake på veggen vår
        elif self.x >= objekt.x and self.x - self.radius <= objekt.x + objekt.width and self.y <= objekt.y and self.y >= objekt.y - objekt.height:
            self.fartX = -0.8 * fartX
            self.x = objekt.x + objekt.width + self.radius
            self.aY = GRAVITY
        


class SkuddObj(Prosjektil):
    
    def __init__(self, x, y, farge, radius, startPoint, shooter, fireCooldown, fartX = 0, fartY = 0, aY = 0):
        super().__init__(x, y, farge, radius, startPoint, fartX, fartY, aY)
        self.stigningsTall = 0
        self.shooter = shooter
        self.fireCooldown = fireCooldown
        self.lastFireTick = 0
        
        
    
    #Sjekker kollisjon med veggen
    def collision(self, objekt):
        
        #Trengs kun å sjekke x akse
        if self.x - self.radius <= objekt.x + objekt.width:
            self.alive = False
            objekt.health -= 1
            return True
        
    def updatePosition(self):
        self.x += self.fartX
        self.y -= -self.fartX * self.stigningsTall
        
    
    def fire(self, target, ticks):
        #Sjekker om nok tid har gått før den kan skyte
        if ticks - self.fireCooldown >= self.lastFireTick:
            self.lastFireTick = ticks
            self.alive = True
            self.x, self.y = self.shooter.x, self.shooter.y
            self.x, self.y = self.startPoint[0], self.startPoint[1]
                #target = (Wall.x + Wall.width, Wall.y + Wall.height//2)
            self.stigningsTall = (target[1] - self.startPoint[1]) / (target[0] - self.startPoint[0])
            
            
            if isinstance(self.shooter, Tank):
                return True

class TankShell(SkuddObj):
    
    def __init__(self, x, y, farge, radius, startPoint, shooter, fireCooldown, imgLink, fartX = -3, fartY = 0, aY = 0):
        super().__init__(x, y, farge, radius, startPoint, shooter, fireCooldown, fartX, fartY, aY)
        
        self.img = pg.image.load("./Bilder/shell.png")
        self.hitBox = self.img.get_rect()
        self.img = pg.transform.scale(self.img, (self.hitBox.width//1.2,self.hitBox.height//1.2))
        self.img = pg.transform.flip(self.img, True, False)
        
        
    def draw(self):
        surface.blit(self.img, (self.x, HEIGHT - self.y))
        
    def fire(self, target, ticks):
        
        if super().fire(target, ticks):
            self.shooter.fireAnimation = True
            self.shooter.fireIndex = 0
            
            
        self.stigningsTall = 0
        
        
        
        
    #def updatePosi
        
        

#Separat klasse for lyd
class Lyd:
    def __init__(self,lydFil, volum, lastTick):
        
        self.lydObjekt = pg.mixer.Sound(lydFil)
        self.lydTid = self.lydObjekt.get_length() * 1000
        self.volum = self.lydObjekt.set_volume(volum)
        self.lastTick = 0



class Rektangel (Objekt):
    
    rektangelList = []
    def __init__(self, x, y, farge, width, height, fartX = 0, fartY = 0, aY = 0):

        super().__init__(x, y, farge, fartX, fartY, aY)
        
        self.width = width
        self.height = height
        
        #Legger bare til rektangler i listen, og ikke fra subklassene
        if not isinstance(self, Enemy):
            Rektangel.rektangelList.append(self)
            
    def draw(self):
        pg.draw.rect(surface, self.farge,(self.x, HEIGHT - self.y, self.width, self.height))
        


class Enemy(Rektangel):
    
    def __init__(self, x, y, farge, width, height, health, animationRate, imgLink, fartX = 0, fartY = 0, aY = GRAVITY):
        super().__init__(x, y, farge, 0, 0, fartX, fartY, aY)
        
        self.health = health
        #Nøvendig for senere animasjoner
        self.img = pg.image.load(imgLink)
        self.hitBox = self.img.get_rect()
        self.width = self.hitBox.width
        self.height = self.hitBox.height
        self.images = {}
        self.spriteIndex = 0
        self.animationRate = animationRate
        self.lastTick = 0
#         self.fireIndex = 0

    #y offset og x offset er nyttig når man skal justere hitbox i forhold til bilde f.eks
    def draw(self, img, yOffset, xOffset):
        surface.blit(img, (self.x + xOffset, HEIGHT - self.y - yOffset))
        
    #Metode for å granske bilder i forhold til hitbokser
    def drawHitBox(self):
        super().draw()
        
    def animationTrue(self, animationType):
        
        if ticks - self.lastTick > self.animationRate:
            self.lastTick = ticks
            self.spriteIndex += 1
            
            if self.spriteIndex >= len(self.images[animationType]):
                self.spriteIndex = 0
            return True
            
 
    

#Klassen til player 2
class Player(Enemy):
    
    def __init__(self, x, y, farge, width, height, health, animationRate, imgLink, fartX = 0, fartY = 0, aY = GRAVITY):
        
        super().__init__(x, y, farge, width, height, health, animationRate, imgLink, fartX, fartY, aY)
        
        self.keys = (pg.K_UP, pg.K_DOWN, pg.K_RIGHT, pg.K_LEFT, pg.K_UP)
        self.shoot = False
        #For animasjon
        self.hitbox = self.img.get_rect()
        self.hurtAnimation = False
        self.lastHit = self.animationRate * 10
        
        #Skalerer bredde og høyde
        self.width = self.hitbox.width//7
        self.height = self.hitbox.height//7
        self.y = self.height
        
        
    #Tillater tast-bevegelse
    def move(self, ticks):
        #Henter knappene fra tastaturet
        keys = pg.key.get_pressed()
        
        self.fartX = 0
        self.shoot = True

        if self.hurtAnimation == False:
            
            if self.y > self.height:
                self.shoot = False
                self.draw(self.images["jump"][0], 0, 0)

            elif keys[self.keys[2]] or keys[self.keys[3]]:
                
                self.animationTrue("run")
                if self.y <= self.height:
                    self.draw(self.images["run"][self.spriteIndex], 0, 0)
     
        if self.hurtAnimation == False:
            
            #Sjekker tasten "->"
            if keys[self.keys[2]]:
                self.shoot = False
                if self.x + self.width >= WIDTH:
                    return
                self.fartX = 1.5
                
            #Sjekker tasten "<-"
            elif keys[self.keys[3]]:
                self.shoot = False
                if self.x <= Wall.x + Wall.width:
                    return
                self.fartX = -1.5
            else:
                self.animationTrue("idle")
                self.draw(self.images["idle"][self.spriteIndex], 0, 0)
                
    
    def updatePosition(self):
        super().updatePosition()

        if self.y - self.height <= 0:
            self.y = self.height

        else:
            self.aY = GRAVITY
            self.fartY += self.aY

#Klassen for roboter. Jeg ser at det kunne vært hensiktsmessig å hatt de to fiendene som to ulike klassene  
            
class Bot(Enemy):
    
    botList = []
    tankList = []
    chopperList = []
    
    def __init__(self, x, y, farge, width, height, health, fireRate, enemyType, animationRate, imgLink, fartX = 0, fartY = 0, aY = 0):
        
        super().__init__(x, y, width, height, farge, health, animationRate, imgLink, fartX, fartY, aY)
        
        self.enemyType = enemyType
        
        self.healthBars = [Rektangel(self.x + self.width//3 - 1 , self.y + self.height//3 + 1, BLACK, self.width//3 + 2, self.height//5 + 2), Rektangel(self.x + self.width//3, self.y + self.height//3, RED, self.width//3, self.height//5) ]
        
        
        
        #Skytingsattributter
        self.fireRate = fireRate
        self.lastFireTick = 0
        self.shots = [SkuddObj(self.x, self.y, BLACK, 5, (self.x, self.y), self, 1_000, fartX = -2, fartY = 0, aY = 0)]
        
        #Bildeattributter
        self.hitBox = self.img.get_rect()
        self.width =  self.hitBox.width
        self.height = self.hitBox.height
        
        #Bevegelsesattributter
        self.move = False
        self.movementCooldown = 4000
        self.lastMovementTick = 0
        self.destinationIndex = 0
        self.fortegnBevegelse = 1
        

        #Legger til i listen
        Bot.botList.append(self)

        
    #Genrerer et random tall
    def randomMovement(self, ticks):
        
        if ticks - self.lastMovementTick > self.movementCooldown:
            self.lastMovementTick = ticks
            self.destinationIndex = randint(0,5)
            
    
class Helicopter(Bot):
    
    chopperList = []
    
    def __init__(self, x, y, farge, width, height, health, fireRate, enemyType, animationRate, imgLink, fartX = 0, fartY = 0, aY = 0):
        
        super().__init__(x, y, width, height, farge, health, fireRate, enemyType, animationRate, imgLink, fartX, fartY, aY)
        
        self.healthBars = [Rektangel(self.x + self.width//3 - 1 , self.y + self.height//3 + 1, BLACK, self.width//3 + 2, self.height//5 + 2), Rektangel(self.x + self.width//3, self.y + self.height//3, RED, self.width//3, self.height//5) ]
        self.destinations = {
            0: (self.x, HEIGHT - 100),
            1: (self.x, HEIGHT - 100 - 100),
            2: (self.x, HEIGHT - 100- 200),
            3: (self.x, HEIGHT - 100 - 250),
            4: (self.x, HEIGHT - 100 - 350),
            5: (self.x, HEIGHT - 100 - 300)
            }
        
        Helicopter.chopperList.append(self)
        
        
    def updatePosition(self):
        
        for destination in self.destinations.values():
            
            if self.y > self.destinations[self.destinationIndex][1] + 5:
                self.fortegnBevegelse = -1
            elif self.y < self.destinations[self.destinationIndex][1] - 5:
                self.fortegnBevegelse = 1
            else:
                self.fortegnBevegelse = 0
                
        #Setter en fart
            if destination == self.destinations[self.destinationIndex] and self.y != self.destinations[self.destinationIndex][1]:
                self.fartY = 0.15 * self.fortegnBevegelse
                
            if self.fartY != 0:
                self.y += self.fartY
                
class Tank(Bot):
    
    tankList = []
    
    def __init__(self, x, y, farge, width, height, health, fireRate, enemyType, animationRate, imgLink, fartX = 0, fartY = 0, aY = 0):
        
        super().__init__(x, y, width, height, farge, health, fireRate, enemyType, animationRate, imgLink, fartX, fartY, aY)
        
        #self.shots = [SkuddObj(self.x, self.y, BLACK, 5, (self.x, self.y), self, 1_000,"", fartX = -2, fartY = 0, aY = 0)]
        self.width -= self.width//2
        self.healthBars = [Rektangel(self.x + self.width//3 - 1 , self.y + self.height//8 + 1, BLACK, self.width//3 + 2, self.height//10 + 2), Rektangel(self.x + self.width//3, self.y + self.height//3, RED, self.width//3, self.height//10) ]
        self.fireAnimation = False
        self.fireIndex = 0
        
        self.destinations = {
            0: (self.x - 150, self.y),
            1: (self.x - 200, self.y),
            2: (self.x - 300, self.y),
            3: (self.x - 400, self.y),
            4: (self.x - 500, self.y),
            5: (self.x - 600, self.y)
            }
        
        Tank.tankList.append(self)
    
    def updatePosition(self):
        
        for destination in self.destinations.values():
            
            if self.x > self.destinations[self.destinationIndex][0] + 5:
                self.fortegnBevegelse = -1
            elif self.x < self.destinations[self.destinationIndex][0] - 5:
                self.fortegnBevegelse = 1
            else:
                self.fortegnBevegelse = 0
                
            if destination == self.destinations[self.destinationIndex] and self.x != self.destinations[self.destinationIndex][1]:
                self.fartX = 0.15 * self.fortegnBevegelse
                
            if self.fartX != 0:
                
                self.animationTrue("move")
                self.draw(self.images["move"][self.spriteIndex],0,-self.width//3)
                self.x += self.fartX
            elif self.fartX == 0:
                #self.draw(self.images["move"][self.spriteIndex],0,-self.width//3)
                self.draw(self.images["move"][0],0,-self.width//3)
                
        #Kode for animasjon av skudd
        
        
        if self.fireAnimation:
            #
            self.animationTrue("move")
            self.draw(self.images["smoke"][self.fireIndex], -5, -self.width//1.65)
            self.draw(self.images["fire"][self.fireIndex], -self.height//3.7, -self.width//1.8)
            
            if self.fireIndex == 7: #en(self.images["smoke"]):
                self.fireAnimation = False
                self.fireIndex == 0
                
    def animationTrue(self, animationType):
        if super().animationTrue(animationType):
            self.fireIndex += 1
        if self.fireIndex >= len(self.images["smoke"]):
            self.fireIndex = 0
 
                

#Funksjoner og variabler knyttet til bildehenting. 
mappeStiPlayer = "./Bilder/Soldier-Guy-PNG/_Mode-Gun/"
mappeStiTanks = "./Bilder/tank-oga/wholetank/key-frames"
mappeStiTanks2 = "./Bilder/tank-oga/tank-fire/fire-keyframes"

bilderPlayer = []
bilderTanks = []

#Funksjon som henter ut en liste med masse "paths". Henter i tilfeldig rekkefølge, derfor brukes bubblesort nedenfor
def hentStier(liste, sti):
    for root, mapper, filer in os.walk(sti):
        tempListe = []
        for fil in filer:
            tempListe.append(os.path.join(root, fil))
        liste.append(tempListe)
    liste.pop(0)
    return liste

hentStier(bilderPlayer,mappeStiPlayer)
hentStier(bilderTanks, mappeStiTanks)



#Bruker bubblesort for å sortere bildestiene jeg henta i forrige funksjon.
def sortStier(liste, index1, index2):
    tempVar = 0
    for i in range(0,len(liste)-1):
        for j in range(0, len(liste)-1):
            if liste[j][index1:index2] > liste[j+1][index1:index2]:
                tempVar = liste[j+1]
                liste[j+1] = liste[j]
                liste[j] = tempVar   
    return liste

#Sorterer listene
for i in range(1,len(bilderPlayer)):
    bilderPlayer[i] = sortStier(bilderPlayer[i],-7,-4)

for i in range(1, len(bilderTanks)):
    bilderTanks[i] = sortStier(bilderTanks[i], -5, -4)
    




#Funksjon som genererer bildene fra listene med paths, og som legger til bildene som attributter i et objekt
#Henter over  60 bilder med funksjonen.
def addImages(objekt, imgList, keyList, skalering):
    
    for liste in imgList:
        j = 0
        for bildeSti in liste:
            
            bilde = pg.image.load(bildeSti)
            hitbox = bilde.get_rect()
            bilde = pg.transform.scale(bilde, (hitbox.width//skalering,hitbox.height//skalering))
            bilde = pg.transform.flip(bilde, True, False)
            
            liste[j] = bilde
#             liste[j] = bildeSti
            j+=1
            
    dic = {}
    i = 0
    for key in keyList:
        dic[key] = imgList[i]
        i+=1
    objekt.images = dic
    
    
#Legger til bildene
    
# bilderTanks[1] = bilderTanks[1][0]
Player2 = Player(WIDTH-100, 60, BLACK, 40, 60, 5, 50, "./Bilder/Soldier-Guy-PNG/_Mode-Gun/01-Idle/E_E_Gun__Idle_000.png")
Tank1 = Tank(WIDTH + 20, 140, BLACK, 100, 70, -1, 3_000, "tank", 50, "./Bilder/tank-oga/wholetank/key-frames/right/right-1.png")
addImages(Player2, bilderPlayer, ["run", "jump", "hurt", "idle", "attack", "die"], 7)
addImages(Tank1, bilderTanks, ["move", "smoke", "fire"], 1.5)

#Lyder
chopperLyd = Lyd("./Lyder/helicopter.mp3", 0.05, 0)
eksplosjonLyd = Lyd("./Lyder/explotion.mp3", 0.15, 0)
treffLyd = Lyd("./Lyder/treffLyd.wav", 0.1, 0)
treffLydSoldat = Lyd("./Lyder/mp3/hit1.mp3", 0.1, 0)
dødLydSoldat = Lyd("./Lyder/mp3/die1.mp3", 0.1, 0)

kuleListe = []
skuddListePlayer = []
skuddListeBot = []



Sprettert = Prosjektil(120, 150, RED, 5, (120,150))

#Player2
#Player2 = Player(WIDTH-100, 60, BLACK, 40, 60, 5, 50, "./Bilder/Soldier-Guy-PNG/_Mode-Gun/01-Idle/E_E_Gun__Idle_000.png")
healthBarOutline = Rektangel(WIDTH - 250 -50 - 2, HEIGHT -50 + 2, BLACK, 250 + 4, 50 + 4)
healthBarPlayer = Rektangel(WIDTH - 250 - 50, HEIGHT-50, RED, 250, 50)

#Forhåndsgenererer prosjektiler. Sørger for at player2 ikke kun kan spamme fordi man maksimalt kan ha 6 kuler i lufta samtidig
for i in range(0,6):
    Skudd = SkuddObj(Player2.x,  Player2.height//2, BLACK, 5, (Player2.x, Player2.height//2), Player, 0,  -5,0,0)#, shooter, fartX = -6, fartY = 0, aY = 0)
    skuddListePlayer.append(Skudd)
        
#Bots  
Chopper = Helicopter(WIDTH-107, HEIGHT - 100, BLACK, 80, 50, -1, 1_000, "chopper", 50, "./Bilder/heli.png")
Helicopter.chopperList.pop()
#Chopper2 = Helicopter(WIDTH-107, HEIGHT - 100, BLACK, 80, 50, 3, 1_000, "chopper", 50, "./Bilder/heli.png")
#Tank1 = Tank(WIDTH + 20, 140, BLACK, 100, 70, 5, 3_000, "tank", 50, "./Bilder/tank-oga/wholetank/key-frames/right/right-1.png")
#114 i y
#x, y, farge, radius, startPoint, shooter, fireCooldown, imgLink,
SkuddBot = SkuddObj(Chopper.x, Chopper.y, BLACK, 5, (Chopper.x, Chopper.y), Chopper, 1_000, fartX = -2, fartY = 0, aY = 0)
skuddListeBot.append(SkuddBot)
SkuddTank = TankShell(Tank1.x, Tank1.y, BLACK, 10, (Tank1.x, Tank1.y), Tank1, 2_500,"./Bilder/shell.png", fartX = -3, fartY = 0, aY = 0)

#Genererer alle prosjektilene til spretterten
for i in range(0,8):
    Kule = Prosjektil(Sprettert.x, Sprettert.y, BLACK, 10,(Sprettert.x, Sprettert.y) )
    kuleListe.append(Kule)

#Muren
Wall = Enemy(Sprettert.x + 150, 240, BLACK, 30, 240, 80, 0, "./Bilder/wall.png")
Wall.img = pg.transform.scale(Wall.img, (Wall.hitBox.width//10,Wall.hitBox.height//10))
Wall.width = Wall.hitBox.width//10
Wall.height = Wall.hitBox.height//4.2
WallOutline = Rektangel(Sprettert.x + 150 - 2, 240 + 2, BLACK, Wall.width+ 4, Wall.height + 4)

#Healthbars
healthBarWallOutline = Rektangel(50 - 2, HEIGHT-50 + 2, BLACK, 240 + 4, 50 + 4)
healthBarWall = Rektangel(50, HEIGHT-50, RED, 240, 50)

#Variabler for kula
fireRate = 400 #Millisekunder
fartX = 0
kuleIndeks = 0
cooldownTick = 0

skuddIndeks = 0
enemiesKilled = 0
tanksKilled = 0
choppersKilled = 0

run = True

#Variabler for generering av bots
WAVES = ["Wave 1","Wave 2","Wave 3","Wave 4","Wave 5","Wave 6","Wave 7", 0]#"Wave 8","Wave 9","Wave 10"]
waveIndex = 0
#Tekst
tittelTekst = Tekst("CASTLE DEFENCE",WIDTH//2, HEIGHT//3, BLACK, 60)
tekstPVE = Tekst("PVP", WIDTH//3, HEIGHT//1.5, BLACK, 30)
tekstPVP = Tekst("PVE", 2*WIDTH//3, HEIGHT//1.5, BLACK, 30)
tekstInstruksjoner = Tekst("Player 1: F = fire, mousepad for aiming. Player 2: Arrow-keys for movement, Right-alt = shoot", WIDTH//2, HEIGHT//1.25, BLACK, 15)

tekstWaves = Tekst(WAVES[waveIndex], WIDTH//2, 50, BLACK, 30)
sluttTekst = [Tekst("Castle Defended!", WIDTH//2, HEIGHT//3, BLACK, 60), Tekst("Retry", WIDTH//3, HEIGHT//1.5, BLACK, 30), Tekst("Gamemodes", 2*WIDTH//3, HEIGHT//1.5, BLACK, 30), Tekst("Castle destroyed!", WIDTH//2, HEIGHT//3, BLACK, 60)]


#Variabler for generering av bots
lastChopperGeneratedTick = 0
lastTankGeneratedTick = 0
chopperCooldowns = {
    "Wave 1": 6_000,
    "Wave 2": 5_000,
    "Wave 3": 5_000,
    "Wave 4": 5_000,
    "Wave 5": 4_000,
    "Wave 6": 4_000,
    "Wave 7": 3_000
    }
tankCooldowns = {
    "Wave 1": 15_050,
    "Wave 2": 7_890,
    "Wave 3": 10_000,
    "Wave 4": 3_500,
    "Wave 5": 6_000,
    "Wave 6": 5_500,
    "Wave 7": 2_000
    }

enemiesPerWave = {
    #chopper, tanks
    "Wave 1": [5,0],
    "Wave 2": [7,0],
    "Wave 3": [6,3],
    "Wave 4": [0,7],
    "Wave 5": [5,5],
    "Wave 6": [4,4],
    "Wave 7": [5,5]
    }

#Funksjonen som genererer bots avhengig av wave
def generateBot(ticks, wave):
    
    global lastChopperGeneratedTick
    global lastTankGeneratedTick
    global botCoolDowns
    global skuddListeBot
    
    #Genererer helikoptre
    
    if enemiesPerWave[wave][0] > len(Helicopter.chopperList):
        
        if ticks - chopperCooldowns[wave] >= lastChopperGeneratedTick:
            lastChopperGeneratedTick = ticks
            randomYVerdi = randint(200, HEIGHT - Chopper.height - 10)
            newBot = Helicopter(WIDTH-107, randomYVerdi, BLACK, 80, 50, 3, 1_000, "chopper", 50, "./Bilder/heli.png")

            return True
    
    #Genererer tanks
    if enemiesPerWave[wave][1] > len(Tank.tankList):
        if ticks - tankCooldowns[wave] >= lastTankGeneratedTick:
            lastTankGeneratedTick = ticks
            
            randomVerdi = randint(130,145)
            
            newBot = Tank(WIDTH + 50, randomYVerdi, BLACK, 100, 70, 5, 3_000, "tank", 50, "./Bilder/tank-oga/wholetank/key-frames/right/right-1.png")
            newBot.images = Tank1.images
            #Tank = Bot(WIDTH, 114, BLACK, 100, 70, 5, 3_000, "tank", 50, "./Bilder/tank-oga/wholetank/key-frames//left/left-1.png")
            return True
        

#Lager den estimerte bevegelsen til kula man slenger
def tegnKurve(posNow, x, y):
    
    yConst = y
    #pg.draw.circle(surface, BLACK,(Sprettert.x, HEIGHT - Sprettert.y), 10)
    fartX = (x - posNow[0])/9
    fartY = (posNow[1] - (HEIGHT - y))/9
    i = 0
    
    while i < 42:
        if i % 3 == 0:
            pg.draw.circle(surface, Sprettert.farge, (x, HEIGHT - y), Sprettert.radius)
        fartY += GRAVITY
        y += fartY
        x += fartX
        i += 1

gameCompleted = False
gameStarted = False
hovering = False
cooldownAfterGame = 500
lastTickAfterGame = 0

#Spill-løkke
while run:
    
    surface.blit(backgroundImg, (0, 0))
    clock.tick(FPS)
    mousePos = pg.mouse.get_pos()
    events = pg.event.get()
    ticks = pg.time.get_ticks()
    #Gjør at man kan lukke vinduet
    for event in events:
            if event.type == pg.QUIT:
                run = False
    
    #If tester for når spillet er ferdig. Sjekker henholdvis: om veggen er ødelagt, om spiller2 er død og om man holder ut alle WAVES'ene
    if Wall.health <= 0 or Player2.health <= 0 or waveIndex == len(WAVES) - 1:
        #gameStarted = None
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        
        
        
        if ticks - lastTickAfterGame >= cooldownAfterGame:
            print("go")
            
            
            gameStarted = None
            for tekst in sluttTekst[1:3]:
                tekst.draw()
                if tekst.hoverTekst(mousePos):
                    for event in events:
                        if event.type == pg.MOUSEBUTTONUP:
                            Wall.health, Player2.health = 80, 5
                            healthBarPlayer.x = WIDTH - 300
                            waveIndex = 0
                            gameCompleted = False
                            if tekst == sluttTekst[1]:
                                pg.mouse.set_pos([Sprettert.x - 75, HEIGHT-Sprettert.y + 65])
                                pg.mixer.music.rewind()
                                Helicopter.chopperList, Tank.tankList = [], []
                                gameStarted = True
      
                            elif tekst == sluttTekst[2]:
                                gameStarted = False
                                
            #Mer spesifikke tester for resets av spillet
            if Wall.health <= 0:
                sluttTekst[3].draw()
            elif Wall.health >= 0 and Player2.health <= 0 or Wall.health >= 0 and waveIndex == len(WAVES)-1:
                sluttTekst[0].draw()
                                
        for prosjektil in Prosjektil.prosjektilListe:
            prosjektil.alive = False
            prosjektil.x, prosjektil.y = prosjektil.startPoint[0], prosjektil.startPoint[1]
                
        for bot in Bot.botList:
            bot.health = -1
            

        
                     
    if gameStarted == False and gameCompleted == False:
        
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        for tekst in Tekst.tekstList[0:4]:
            tekst.draw()
            if tekst.hoverTekst(mousePos) and tekst != Tekst.tekstList[3]:
                for event in events:
                    if event.type == pg.MOUSEBUTTONUP:
                        gameStarted = True
                        pg.mixer.music.rewind()
                        pg.mouse.set_pos([Sprettert.x - 75, HEIGHT-Sprettert.y + 65])
                        if tekst == tekstPVP:
                            PVP = False
                        elif tekst == tekstPVE:
                            PVP = True

            else:
                tekst.img = tekst.font.render(tekst.tekst, True, BLACK)
                
    #Bakgrunnsbilde
    
    elif gameStarted == True:

        
        #ticks = pg.time.get_ticks()
        
        if ticks < 10:
            pg.mixer.music.rewind()
        
        
        #Sjekker om man er ferdig
        if waveIndex != len(WAVES) - 1:
            tekstWaves.img = tekstWaves.font.render(WAVES[waveIndex], True, BLACK)
            tekstWaves.draw()

        
        #Går gjennom hendelser (events)
        for event in events:
            
            #Sjekker om man prøver å lukke vinduet
            if event.type == pg.QUIT:
                run = False
            
            if event.type == pg.KEYDOWN:
                #ticks = pg.time.get_ticks()
                
                if event.key == pg.K_f:
                    #Cooldown
                    if ticks - cooldownTick > fireRate:
                        cooldownTick = ticks
                        Kule = kuleListe[kuleIndeks]
                        kuleIndeks += 1
                        Kule.alive = True
                        
                        if kuleIndeks > 7:
                            kuleIndeks = 0

                        fartX = (Sprettert.x - mousePos[0])/9
                        fartY = (mousePos[1] - (HEIGHT - Sprettert.y))/9
                        
                        Kule.fartX = fartX
                        Kule.fartY = fartY
                        
                        antallSprett = 0

                if event.key == pg.K_RALT and Player2.shoot and Player2.health > 0:
                    
                    Skudd = skuddListePlayer[skuddIndeks]
                    Skudd.alive = True
                    skuddIndeks += 1
                    if skuddIndeks > len(skuddListePlayer) - 1:
                        skuddIndeks = 0
            
                if event.key == pg.K_UP and Player2.health > 0:
                    
                    
                    if Player2.y - Player2.height <= 0:
                        Player2.fartY = 7
        
        #Genererer bots
        if PVP == False:
            generateBot(ticks, WAVES[waveIndex])
                    
        
        #Skyter kuler: Objektet må leve, og jeg har cooldown
        
        if PVP == False:
            
            #Tegner uanimerte bots og skuddene deres
            for bot in Bot.botList:

                if bot.health > 0:
                    if bot.enemyType == "chopper":
                        bot.draw(bot.img, 0, 0)
                        #if chopperLyd
                        if ticks - chopperLyd.lydTid >= chopperLyd.lastTick:
                            chopperLyd.lydObjekt.play()
                            chopperLyd.lastTick = ticks
                        bot.healthBars[1].width = (bot.width//3)/3 * bot.health
                    elif bot.enemyType == "tank":
                        bot.healthBars[1].width = (bot.width//3)/5 * bot.health
                        
                    bot.healthBars[0].x, bot.healthBars[0].y  = bot.x + bot.width//3 - 1, bot.y + 30 + 1
                    bot.healthBars[1].x, bot.healthBars[1].y = bot.x + bot.width//3, bot.y + 30
                    bot.healthBars[0].draw(), bot.healthBars[1].draw()

                    bot.randomMovement(ticks)
                    bot.updatePosition()
                
                
                if bot.enemyType == "chopper":
                    
                    if ticks - SkuddBot.fireCooldown >= bot.shots[-1].lastFireTick and bot.health > 0:
                        
                        skuddBot = SkuddObj(bot.x, bot.y, BLACK, 5, (bot.x + bot.width//8, bot.y - bot.height//0.95), bot, 1_000, fartX = -5, fartY = 0, aY = 0)
                        bot.shots.append(skuddBot)
                        skuddBot.fire((Wall.x + Wall.width, Wall.height//2), ticks)
                        skuddListeBot.append(skuddBot)
                
                elif bot.enemyType == "tank":
                    
                    if ticks - SkuddTank.fireCooldown >= bot.shots[-1].lastFireTick and bot.health > 0:
                        
                        skuddBot = TankShell(bot.x, bot.y, BLACK, 10, (bot.x - bot.width//2.3, bot.y - bot.height//3), bot, 2_500, "./Bilder/shell.png", fartX = -3, fartY = 0, aY = 0)
                        bot.shots.append(skuddBot)
                        skuddBot.fire((Wall.x + Wall.width, Wall.height - Wall.height/8), ticks)
                        skuddListeBot.append(skuddBot)

            for skudd in skuddListeBot:

                if skudd.alive:
                    skudd.collision(Wall)
                    skudd.updatePosition()
                    skudd.draw()
        
        if Player2.health > 0 and PVP:
            Player2.move(ticks)
            Player2.updatePosition()
        

            for skudd in skuddListePlayer:
                
                if skudd.alive:
                    skudd.collision(Wall)        
                    skudd.updatePosition()
                    skudd.draw()
                    skudd.startPoint = (Player2.x + Player2.width//2, Player2.y//2 - skudd.radius)
                else:
                    skudd.x, skudd.y = Player2.x, Player2.y//3
                    
        #Tegner sprettert
        if mousePos[0] <= Wall.x and HEIGHT - mousePos[1] <= Wall.y:
            pg.draw.line(surface, BLACK, (Sprettert.x - 26, HEIGHT - Sprettert.y), (mousePos[0], mousePos[1]), 10)
            pg.draw.line(surface, BLACK, (Sprettert.x + 26, HEIGHT - Sprettert.y), (mousePos[0], mousePos[1]), 10)
        surface.blit(slingshotImg, (Sprettert.x - WIDTH//20, HEIGHT//1.43))
        
        tegnKurve(mousePos, Sprettert.x, Sprettert.y)
                    

        
        for kule in kuleListe:
            if kule.alive:
                #Sjekker for kollisjon
                kule.collision(Wall)
                kule.updatePosition()
                kule.draw()
                
                #Sjekker om man trefer noen
                for enemy in Bot.botList:
                    if enemy.health > 0:
                        if kule.collision(enemy):
                            enemy.health -= 1
                            treffLyd.lydObjekt.play()
    
                #Dersom man treffer Player 2 
                if PVP:
                    if kule.collision(Player2):
                        Player2.health -=1
                        Player2.hurtAnimation = True
                        Player2.lastHit = ticks
                        Player2.spriteIndex = 0
                        treffLydSoldat.lydObjekt.play()
                        
                        
                                
                    
        #Treff animasjoner              
        if ticks - Player2.lastHit <= len(Player2.images["hurt"]) * Player2.animationRate and PVP:
            
            if Player2.health > 0:
                Player2.animationTrue("hurt")
                Player2.draw(Player2.images["hurt"][Player2.spriteIndex], 3, 0)
                Player2.hurtAnimation = True
                
            else:
                if Player2.y == Player2.height :
                    
                    Player2.animationTrue("die")
                    Player2.draw(Player2.images["die"][Player2.spriteIndex], 10, 20)
                    lastTickAfterGame = ticks
                    
                    
                    if Player2.spriteIndex == 0:
                        dødLydSoldat.lydObjekt.play()
                    
                elif Player2.y > Player2.height:
                    Player2.animationTrue("jump")
                    Player2.draw(Player2.images["jump"][Player2.spriteIndex], 0, 0)
                    Player2.updatePosition()
                    Player2.lastHit = ticks
                    lastTickAfterGame = ticks
    
        else:
            Player2.hurtAnimation = False
    
        

        #Tegner motstandere, og sjekker kollisjon
        for bot in Bot.botList:
            if bot.health == 0:
                eksplosjonLyd.lydObjekt.play()
                
                if isinstance(bot, Helicopter):
                    choppersKilled +=1
                elif isinstance(bot, Tank):
                    tanksKilled += 1
                    
                enemiesKilled += 1
                bot.health -= 1
        #Dersom man ødelegger hele wavet
        if enemiesKilled == enemiesPerWave[WAVES[waveIndex]][0] + enemiesPerWave[WAVES[waveIndex]][1]:
            Helicopter.chopperList, Tank.tankList = [], []
            waveIndex += 1
            Wall.health += 30
            enemiesKilled = 0
            
            for bot in Bot.botList:
                bot.health = -1
                
        #for healthBar in Rektangel.rektangelList[7:9]:
        healthBarWallOutline.draw() 
        healthBarWall.draw()
        
#         healthBarPlayerOutline.draw()
#         healthBarPlayer.draw()

            
#         for healthBar in Rektangel.rektangelList[5:]:
#             for bot in Bot.botList:
#                 if bot.health > 0:
#                     healthBar.draw()
#             
            
        
            
        if PVP:
            healthBarOutline.draw()
            healthBarPlayer.draw()

                

        healthBarWall.width = Wall.health * 3
         
        if PVP:
            healthBarPlayer.width =  Player2.health * 50
        
        if healthBarWall.width > 240:
            healthBarWall.width = 240

        #Tegner veggen
        if Wall.health > 0:
            WallOutline.draw()
            Wall.draw(Wall.img, 0, 0)
            Wall.draw(Wall.img, - Wall.height//2.45, 0)
            Wall.draw(Wall.img, - Wall.height//1.225, 0)
            #Wall.draw(Wall.img, - Wall.height//2, 0)
            
        if Player2.health <= 0:
            gameCompleted = True
            
    
            
    pg.display.flip()
        

#Avslutte pygame 
pg.quit()
    
    
    




































f
