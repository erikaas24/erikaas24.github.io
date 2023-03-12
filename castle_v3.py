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

#Lyder og musikk
pg.mixer.music.load("./Lyder/Lament_of_war.mp3")
pg.mixer.music.set_volume(0.06)
pg.mixer.music.play()

#Lager en overflate
surface = pg.display.set_mode(SIZE)

#Lager en klokke
clock = pg.time.Clock()

#Bakgrunnsbilde
backgroundImg = pg.image.load('./Bilder/background/airadventurelevel3.png')
backgroundImg = pg.transform.scale(backgroundImg, SIZE)

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
        #Sjekker om posisjonen er verdt å oppdateres
#         if self.x >= WIDTH + self.radius or self.x < 0:
#             return
#         if self.y <=  0 - self.radius:
#             return
        
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
            self.y = 2 * self.radius
            self.fartY = -self.fartY * 0.8
            self.alive = False
            self.x = self.startPoint[0]
            self.y = self.startPoint[1]
            
        else:
            self.fartY += self.aY
            #self.y = 2 * self.radius
            
        
    def draw(self):
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
    
    
    def __init__(self,x, y, farge, radius, startPoint, shooter, fireCooldown, imgLink, fartX = 0, fartY = 0, aY = 0):
        super().__init__(x, y, farge, radius, startPoint, fartX, fartY, aY)
        self.stigningsTall = 0
        self.shooter = shooter
        self.fireCooldown = fireCooldown
        self.lastFireTick = 0
        self.img = pg.image.load("./Bilder/tank-oga/tank-fire/shell.png")
        self.hitBox = self.img.get_rect()
        
        #Potensielle bilder
        #self.img = pg.transform.scale(self.img, (self.hitBox.width//0.5,self.hitBox.height//0.5))
        #self.img = pg.transform.flip(self.img, True, False)
        
    
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
                if self.y <= self.height + 5:
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

#Klassen for roboter. Jeg ser at det kunne vært hensiktsmessig å hatt de to fiendene som to ulike klasser
class Bot(Enemy):
    
    botList = []
    tankList = []
    chopperList = []
    
    def __init__(self, x, y, farge, width, height, health, fireRate, enemyType, animationRate, imgLink, fartX = 0, fartY = 0, aY = 0):
        
        super().__init__(x, y, width, height, farge, health, animationRate, imgLink, fartX, fartY, aY)
        
        self.enemyType = enemyType
        
        #Skytingsattributter
        self.fireRate = fireRate
        self.lastFireTick = 0
        self.shots = [SkuddObj(self.x, self.y, BLACK, 5, (self.x, self.y), self, 1_000,"", fartX = -2, fartY = 0, aY = 0)]
        
        #Bildeattributter
        self.hitBox = self.img.get_rect()
        self.width =  self.hitBox.width
        self.height = self.hitBox.height
        
        if self.enemyType == "tank":
            self.width -= self.width//2
            
        
        #Bevegelsesattributter
        self.move = False
        self.movementCooldown = 4000
        self.lastMovementTick = 0
        self.destinationIndex = 0
        self.fortegnBevegelse = 1
        
        #Jeg har valgt å ha manuelle destinasjoner istedenfor tilfeldig genererte fordi det gjør at vanskelighetsgraden holder seg relativt lik fra spill til spill 
        self.destinationsY = {
            0: (self.x, self.y),
            1: (self.x, self.y - 100),
            2: (self.x, self.y - 200),
            3: (self.x, self.y - 250),
            4: (self.x, self.y - 350),
            5: (self.x, self.y - 300)
            }
        
        self.destinationsX = {
            0: (self.x, self.y),
            1: (self.x - 200, self.y),
            2: (self.x - 300, self.y),
            3: (self.x - 400, self.y),
            4: (self.x - 500, self.y),
            5: (self.x - 600, self.y)
            }
        
        #Legger til i de respektive listene.
        Bot.botList.append(self)
        if self.enemyType == "tank":
            Bot.tankList.append(self)
        elif self.enemyType == "chopper":
            Bot.chopperList.append(self)
        
    #Genrerer et random tall
    def randomMovement(self, ticks):
        
        if ticks - self.lastMovementTick > self.movementCooldown:
            self.lastMovementTick = ticks
            self.destinationIndex = randint(0,5)
            

    def updatePosition(self):
        
        #Hvis objektet er et helikopter
        if self.enemyType == "chopper":
            for destination in self.destinationsY.values():
                
                if self.y > self.destinationsY[self.destinationIndex][1] + 5:
                    self.fortegnBevegelse = -1
                elif self.y < self.destinationsY[self.destinationIndex][1] - 5:
                    self.fortegnBevegelse = 1
                else:
                    self.fortegnBevegelse = 0
                    
            #Setter en fart
                if destination == self.destinationsY[self.destinationIndex] and self.y != self.destinationsY[self.destinationIndex][1]:
                    self.fartY = 0.8 * self.fortegnBevegelse
        #Hvis objektet er en tanks
        elif self.enemyType == "tank":
            
            for destination in self.destinationsX.values():
                
                if self.x > self.destinationsX[self.destinationIndex][0] + 5:
                    self.fortegnBevegelse = -1
                elif self.x < self.destinationsX[self.destinationIndex][0] - 5:
                    self.fortegnBevegelse = 1
                else:
                    self.fortegnBevegelse = 0
                    
                if destination == self.destinationsX[self.destinationIndex] and self.x != self.destinationsX[self.destinationIndex][1]:
                    self.fartX = 0.8 * self.fortegnBevegelse
    
    
        if self.fartY != 0 and self.enemyType == "chopper":
            self.y += self.fartY
        
        if self.fartX != 0 and self.enemyType == "tank":
            
            self.animationTrue("move")
            self.draw(self.images["move"][self.spriteIndex],0,-self.width//3)
            
            self.x += self.fartX
        elif self.fartX == 0 and self.enemyType == "tank":
            self.draw(self.images["move"][self.spriteIndex],0,-self.width//3)
            
    
#Lyder
chopperLyd = Lyd("./Lyder/helicopter.mp3", 0.05, 0)
eksplosjonLyd = Lyd("./Lyder/explotion.mp3", 0.15, 0)
treffLyd = Lyd("./Lyder/treffLyd.wav", 0.1, 0)

kuleListe = []
skuddListePlayer = []
skuddListeBot = []



Sprettert = Prosjektil(120, 150, RED, 5, (120,150))

#Player2
Player2 = Player(WIDTH-100, 60, BLACK, 40, 60, 5, 50, "./Bilder/Soldier-Guy-PNG/_Mode-Gun/01-Idle/E_E_Gun__Idle_000.png")
healthBarOutline = Rektangel(WIDTH - 250 -50 - 2, HEIGHT -50 + 2, BLACK, 250 + 4, 50 + 4)
healthBarPlayer = Rektangel(WIDTH - 250 - 50, HEIGHT-50, RED, 250, 50)

#Forhåndsgenererer prosjektiler. Sørger for at player2 ikke kun kan spamme fordi man maksimalt kan ha 6 kuler i lufta samtidig
for i in range(0,6):
    Skudd = SkuddObj(Player2.x,  Player2.height//2, BLACK, 5, (Player2.x, Player2.height//2), Player2, "", 0,  -5,0,0)#, shooter, fartX = -6, fartY = 0, aY = 0)
    skuddListePlayer.append(Skudd)
        
#Bots
Chopper = Bot(WIDTH-107, HEIGHT - 100, BLACK, 80, 50, 5, 1_000, "chopper", 50, "./Bilder/heli.png")
Tank = Bot(WIDTH + 50, 114, BLACK, 100, 70, 5, 3_000, "tank", 50, "./Bilder/tank-oga/wholetank/key-frames//left/left-1.png")
SkuddBot = SkuddObj(Chopper.x, Chopper.y, BLACK, 5, (Chopper.x, Chopper.y), Chopper,1_000 , "", fartX = -2, fartY = 0, aY = 0)
skuddListeBot.append(SkuddBot)
SkuddTank = SkuddObj(Tank.x, Tank.y, BLACK, 10, (Tank.x, Tank.y), Tank, 2_500,"", fartX = -2, fartY = 0, aY = 0)

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
enemiesKilled = 1

run = True

#Variabler for generering av bots
WAVES = ["Wave 1","Wave 2","Wave 3","Wave 4","Wave 5","Wave 6","Wave 7", 0]#"Wave 8","Wave 9","Wave 10"]
waveIndex = 0
#Tekst
tittelTekst = Tekst("CASTLE DEFENCE",WIDTH//2, HEIGHT//3, BLACK, 60)
tekstPVE = Tekst("PVP", WIDTH//3, HEIGHT//1.5, BLACK, 30)
tekstPVP = Tekst("PVE", 2*WIDTH//3, HEIGHT//1.5, BLACK, 30)
tekstWaves = Tekst(WAVES[waveIndex], WIDTH//2, 50, BLACK, 30)
sluttTekst = [Tekst("Castle Defended!", WIDTH//2, HEIGHT//3, BLACK, 60), Tekst("Retry", WIDTH//3, HEIGHT//1.5, BLACK, 30), Tekst("Gamemodes", 2*WIDTH//3, HEIGHT//1.5, BLACK, 30), Tekst("Castle destroyed!", WIDTH//2, HEIGHT//3, BLACK, 60)]


#Variabler for generering av bots
lastChopperGeneratedTick = 0
lastTankGeneratedTick = 0
chopperCooldowns = {
    "Wave 1": 10_000,
    "Wave 2": 8_000,
    "Wave 3": 6_000,
    "Wave 4": 5_000,
    "Wave 5": 4_000,
    "Wave 6": 4_000,
    "Wave 7": 4_000
    }
tankCooldowns = {
    "Wave 1": 15_050,
    "Wave 2": 12_890,
    "Wave 3": 10_000,
    "Wave 4": 8_500,
    "Wave 5": 8_000,
    "Wave 6": 7_500,
    "Wave 7": 7_000
    }

enemiesPerWave = {
    #chopper, tanks
    "Wave 1": [5,0],
    "Wave 2": [7,0],
    "Wave 3": [7,2],
    "Wave 4": [0,7],
    "Wave 5": [6,6],
    "Wave 6": [7,7],
    "Wave 7": [15,0]
    }

#Funksjonen som genererer bots avhengig av wave
def generateBot(ticks, wave):
    
    global lastChopperGeneratedTick
    global lastTankGeneratedTick
    global botCoolDowns
    global skuddListeBot
    
    #Genererer helikoptre
    if enemiesPerWave[wave][0] >= len(Bot.chopperList):
        
        if ticks - chopperCooldowns[wave] >= lastChopperGeneratedTick:
            lastChopperGeneratedTick = ticks
            newBot = Bot(WIDTH-107, HEIGHT - 100, BLACK, 80, 50, 5, 1_000, "chopper", 50, "./Bilder/heli.png")
            return True
    
    #Genererer tanks
    if enemiesPerWave[wave][1] >= len(Bot.tankList):
        if ticks - tankCooldowns[wave] >= lastTankGeneratedTick:
            lastTankGeneratedTick = ticks
            newBot = Bot(WIDTH + 50, 117, BLACK, 100, 70, 5, 3_000, "tank", 50, "./Bilder/tank-oga/wholetank/key-frames//left/left-1.png")
            newBot.images = Tank.images
            #Tank = Bot(WIDTH, 114, BLACK, 100, 70, 5, 3_000, "tank", 50, "./Bilder/tank-oga/wholetank/key-frames//left/left-1.png")
            return True
        

#Lager den estimerte bevegelsen til kula man slenger
def tegnKurve(posNow, x, y):
    
    yConst = y
    pg.draw.circle(surface, BLACK,(Sprettert.x, HEIGHT - Sprettert.y), 10)
    fartX = (x - posNow[0])/9
    fartY = (posNow[1] - (HEIGHT - y))/9
    i = 0
    while i < 42:
        if i % 3 == 0:
            pg.draw.circle(surface, Sprettert.farge,(x, HEIGHT - y), Sprettert.radius)
        fartY += GRAVITY
        y += fartY
        x += fartX
        i += 1
        
        
#Funksjoner og variabler knyttet til bildehenting. 
mappeStiPlayer = "./Bilder/Soldier-Guy-PNG/_Mode-Gun/"
mappeStiTanks = "./Bilder/tank-oga/wholetank/key-frames"
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
bilderTanks = bilderTanks[0]

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
bilderTanks = sortStier(bilderTanks, -5, -4)


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
addImages(Player2, bilderPlayer, ["run", "jump", "hurt", "idle", "attack", "die"], 7)
addImages(Tank, [bilderTanks], ["move"], 1.5)

gameCompleted = False
gameStarted = False

#Spill-løkke
while run:
    
    surface.blit(backgroundImg, (0, 0))
    clock.tick(FPS)
    mousePos = pg.mouse.get_pos()
    events = pg.event.get()
    
    #Gjør at man kan lukke vinduet
    for event in events:
            if event.type == pg.QUIT:
                run = False
    
    #If tester for når spillet er ferdig. Sjekker henholdvis: om veggen er ødelagt, om spiller2 er død og om man holder ut alle WAVES'ene
    if Wall.health <= 0 or Player2.health <= 0 or waveIndex == len(WAVES) - 1:
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
                            gameStarted = True
  
                        elif tekst == sluttTekst[2]:
                            gameStarted = False
                            
        for prosjektil in Prosjektil.prosjektilListe:
            prosjektil.alive = False
            prosjektil.x, prosjektil.y = prosjektil.startPoint[0], prosjektil.startPoint[1]
                
        for bot in Bot.botList:
            bot.health = -1
            
    #Mer spesifikke tester for resets av spillet
    if Wall.health <= 0:
        sluttTekst[3].draw()
    elif Wall.health >= 0 and Player2.health <= 0 or Wall.health >= 0 and waveIndex == len(WAVES)-1:
        sluttTekst[0].draw()
                     
    if gameStarted == False and gameCompleted == False:
        
        for tekst in Tekst.tekstList[0:3]:
            tekst.draw()
                
            if tekst.hoverTekst(mousePos):
                
                for event in events:
                    if event.type == pg.MOUSEBUTTONUP:
                        gameStarted = True
                        if tekst == tekstPVP:
                            PVP = False
                        elif tekst == tekstPVE:
                            PVP = True
                 
            else:
                tekst.img = tekst.font.render(tekst.tekst, True, BLACK)
                
    #Bakgrunnsbilde
    
    elif gameStarted == True:
        

        ticks = pg.time.get_ticks()
        
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

                if event.key == pg.K_SPACE and Player2.shoot and Player2.health > 0:
                    
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

                    #bot.drawHitBox()
                    bot.randomMovement(ticks)
                    bot.updatePosition()
                
                
                if bot.enemyType == "chopper":
                    
                    if ticks - SkuddBot.fireCooldown >= bot.shots[-1].lastFireTick and bot.health > 0:
                        
                        skuddBot = SkuddObj(bot.x, bot.y, BLACK, 5, (bot.x + bot.width//8, bot.y - bot.height//0.95), bot, 1_000, "", fartX = -5, fartY = 0, aY = 0)
                        bot.shots.append(skuddBot)
                        skuddBot.fire((Wall.x + Wall.width, Wall.height//2), ticks)
                        skuddListeBot.append(skuddBot)
                
                elif bot.enemyType == "tank":
                    
                    if ticks - SkuddTank.fireCooldown >= bot.shots[-1].lastFireTick and bot.health > 0:
                        
                        skuddBot = SkuddObj(bot.x, bot.y, BLACK, 10, (bot.x, bot.y - bot.height//2.5), bot, 2_500, "", fartX = -3, fartY = 0, aY = 0)
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
                        
                        #healthBarPlayer.x += 50
                                
                    
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
                    
                elif Player2.y > Player2.height:
                    Player2.animationTrue("jump")
                    Player2.draw(Player2.images["jump"][Player2.spriteIndex], 0, 0)
                    Player2.updatePosition()
                    Player2.lastHit = ticks
      
                
        else:
            Player2.hurtAnimation = False
    
        tegnKurve(mousePos, Sprettert.x, Sprettert.y)

        #Tegner motstandere, og sjekker kollisjon
        for enemy in Bot.botList:
            
            if enemy.health == 0:
                eksplosjonLyd.lydObjekt.play()
                enemiesKilled += 1
                enemy.health -= 1
                
        if enemiesKilled == enemiesPerWave[WAVES[waveIndex]][0] + enemiesPerWave[WAVES[waveIndex]][1]:
            Bot.chopperList, Bot.tankList = [], []
            waveIndex += 1
            Wall.health += 30
            enemiesKilled = 0
            
            for bot in Bot.botList:
                bot.health = -1
                
        for healthBar in Rektangel.rektangelList[2:]:
            healthBar.draw()
            
        if PVP:
            for healthBar in Rektangel.rektangelList[:2]:
                healthBar.draw()

        healthBarWall.width = Wall.health * 3
         
        if PVP:
            healthBarPlayer.width =  Player2.health * 50
        
        #print(Player2.health)
        if healthBarWall.width > 240:
            healthBarWall.width = 240
            
        #Tegner veggen
        if Wall.health > 0:
            WallOutline.draw()
            Wall.draw(Wall.img, 0, 0)
            Wall.draw(Wall.img, - Wall.height//2.45, 0)
            Wall.draw(Wall.img, - Wall.height//1.225, 0)
            
        if Player2.health <= 0:
            gameCompleted = True
            
    pg.display.flip()
        

#Avslutte pygame 
pg.quit()
    
    
    




































