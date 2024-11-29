import pygame
import os
import random
from pygame.constants import K_ESCAPE, K_SPACE, MOUSEBUTTONDOWN

#Variable Declaration
#For everything
pygame.init()
mainMenuRunning = True
characterSelectRunning = False
gameRunning = False
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
HS_FILE = 'highscores.txt'
highscore = 0
characterSelected = 0
displayHitbox = True


'''
To Do:
Create sprites for tube
Playtest game speeds and balance it to create a more enjoyable game experience
Make the start of the game more accessible, Intro section where bird is flapping in the background while tutorial messages flash on screen
Change buttons and UI to images as opposed to a collection of rectangles and text

COMPLETED:
Create a score counter
Fix Screen slice glitch at the bottom third of the screen
Ensure there is only one jump per click
Fix hitbox sizes in relation to new images
Create a start menu
Create sprites for character
Create sfx for the game
Create a permanent highscore system that saves to an external location
Chuck in game background image
Emulate movement with the flap/jump. Add some rotation to give it some feel
Create a pause screen
Add different characters to the game and make them selectable in a menu
Display selected character in game
fix character select hitboxes
Allow user back to main menu from the pause screen
Fix alternate character hitboxes
'''

def loadImage(filename):
    image = pygame.image.load(os.path.join(THIS_FOLDER, filename))
    return image

def transformImage(image, width, height):
    image = pygame.transform.scale(image, (width,height))
    return image

def loadSound(filename):
    sound = pygame.mixer.Sound(os.path.join(THIS_FOLDER, filename))

    return sound

def loadHighscore():
    try:
        with open(os.path.join(THIS_FOLDER, HS_FILE), 'r+') as file:
            highscore = int(file.read())

    except:
        with open(os.path.join(THIS_FOLDER, HS_FILE), 'w') as file:
            highscore = int(file.read())
            highscore = 0
        
    return highscore

def newHighscoreCheck():
    global highscore
    try:
        if user.highScore > highscore:
            highscore = user.highScore

            try:
                with open(os.path.join(THIS_FOLDER, HS_FILE), 'w') as file:
                        file.write(str(highscore))
                        
            except:
                print('Highscore write error')
    except:
        print('userHighscore or gameHighscore not defined')

def endSession():
    newHighscoreCheck()
    pygame.quit()
    quit()

screenWidth = 750
screenHeight = 500
window = pygame.display.set_mode((screenWidth, screenHeight))
logo = loadImage("Images/Fly (1).png")
pygame.display.set_caption('My first game')
pygame.display.set_icon(logo)

font = pygame.font.SysFont('comicsans', 100)
clock = pygame.time.Clock()

plane = transformImage(loadImage("Images/Fly (1).png"), 64,64)
planeAnimationImages = [transformImage(loadImage("Images/Fly (1).png"), 64,64), transformImage(loadImage("Images/Fly (2).png"),64,64)]
planeJumpImage = transformImage(loadImage("Images/jumpImage.png"), 64,64)
planeDeathImage = transformImage(loadImage("Images/Dead (1).png"),64,64)
redSquare = transformImage(loadImage("Images/redSquare.jpg"), 64,57)
redSquareAnimationImages = [redSquare]
redSquareJumpImage = redSquare
redSquareDeathImage = redSquare
blueSquare = transformImage(loadImage("Images/blueSquare.jpg"), 64,57)
blueSquareAnimationImages = [blueSquare]
blueSquareJumpImage = blueSquare
blueSquareDeathImage = blueSquare
greenSquare = transformImage(loadImage("Images/greenSquare.jpg"), 64,57)
greenSquareAnimationImages = [greenSquare]
greenSquareJumpImage = greenSquare
greenSquareDeathImage = greenSquare


characters = [plane, redSquare, blueSquare, greenSquare]
playerAnimationImages = [planeAnimationImages, redSquareAnimationImages, blueSquareAnimationImages, greenSquareAnimationImages]
playerJumpImages = [planeJumpImage, redSquareJumpImage, blueSquareJumpImage, greenSquareJumpImage]
playerDeathImages = [planeDeathImage, redSquareDeathImage, blueSquareDeathImage, greenSquareDeathImage]

TubeImages = []

menuBackgroundImage = transformImage(loadImage('Images/menuBackgroundImage.jpg'),screenWidth + 6, screenHeight + 6)
gameBackgroundImage = transformImage(loadImage('Images/gameBackgroundImage.png'),screenWidth + 6, screenHeight + 6)
characterSelectScreen = transformImage(loadImage('Images/characterSelectScreen.jpg'),screenWidth + 6, screenHeight + 6)

jumpSound = loadSound('Sounds/jumpSound.mp3')
deathSound = loadSound('Sounds/deathSound.mp3')
gameMusic = loadSound('Sounds/gameMusic.mp3')
selectSound = loadSound('Sounds/selectSound.mp3')

pauseIcon = loadImage('Images/pauseIcon.png')

'''
menuMusic =  
'''

class player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 55
        self.height = 48
        self.hitbox = (self.x + 5,self.y + 5,self.width,self.height)
        self.jumping = False
        self.verticalVelocity = 0
        self.fallingConstant = 0.4
        self.jumpVelocity = -6
        self.score = 0
        self.highScore = 0
        self.scoreRecieved = False
        self.canJump = True
        self.animCount = 0
        self.alive = True
        self.jumpCount = 0
 
    def move(self):
        #The user has a velocity to applied to them.
        #This velocity is updated each frame with a constant acceleration
        self.y += self.verticalVelocity
        self.verticalVelocity += self.fallingConstant
        self.hitbox = (self.x + 5,self.y + 5,self.width,self.height)

    def jump(self):
            jumpSound.play()
            #The velocity is reset to the preset constant jumpVelocity when the user incites the jump mechanic
            self.verticalVelocity = self.jumpVelocity
            self.jumpCount = 12
            
    def hit(self):
        deathSound.play()
        self.jumpCount = 0
        redrawGameWindow()
        text = font.render('You got hit!', 1, (0,0,0))
        window.blit(text, ((screenWidth/2) - (text.get_width()/2), (screenHeight/2) - (text.get_height()/2)))
        pygame.display.update()

        # This is a little timer so that the text display gets displayed for a set amount of time, however it is dependent on the speed of the computer
        # I added in the event check as otherwise you wouldn't be able to quit until after the timer 
        i = 0
        while i < 200:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    endSession()
        
        #This resets the screen view for the user so that they know that the game is ready to restart
        positionReset()
        redrawGameWindow()

        self.readyCheck()

    def readyCheck(self):
        text = font.render('Press space to begin!', 1, (0,0,0))
        window.blit(text, ((screenWidth/2) - (text.get_width()/2), (screenHeight/2) - (text.get_height()/2)))
        pygame.display.update()

        #This freezes the screen and ensures that the user is ready before the next game session begins
        userReady = False
        while not userReady:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    endSession()

            if pygame.key.get_pressed()[pygame.K_SPACE]:
                userReady = True

    def draw(self):
        #window.fill((0,0,255),(self.x,self.y,self.width,self.height))
        if self.alive:
            #This checks if the user is not still in a jumping motion 
            if self.jumpCount <= 0:
                window.blit(playerAnimationImages[characterSelected][self.animCount],(self.x,self.y))
                self.animCount += 1
                
                if self.animCount > len(playerAnimationImages[characterSelected]) - 1:
                    self.animCount = 0
            
            #If they are in a jumping motion, we display the jump image and decrease the jumpCount timer which determines how long it is displayed for
            else:
                window.blit(playerJumpImages[characterSelected], (self.x,self.y))
                self.jumpCount -= 1

        else:
            window.blit(playerDeathImages[characterSelected], (self.x,self.y))

        if displayHitbox:
            pygame.draw.rect(window, (0,0,0), self.hitbox, 2)
    
    def drawScore(self):
        font = pygame.font.SysFont('comicsans', 50)
        scoreText = font.render('Score: ' + str(user.score), 1, (0,0,0))
        highscoreText = font.render('Highscore: ' + str(highscore), 1, (0,0,0))
        window.blit(scoreText, ((screenWidth - scoreText.get_width() - 20), 10))
        window.blit(highscoreText, ((screenWidth - highscoreText.get_width() - 20), 50))

    def aliveCheck(self):
        self.alive = True

        #Checking for user collisions with enemy gameObjects or if the user had fallen out of the screen parameters
        if self.y < 0 or self.y + self.height > screenHeight:
            self.alive = False
            print('User fell outside of screen parameters')

        if self.hitbox[0] + self.hitbox[2] > topTube.hitbox[0]:
            if self.hitbox[0] < topTube.hitbox[0] + topTube.hitbox[2]:
                if self.hitbox[1] < topTube.hitbox[3]:
                    print('User collided with topTube')
                    self.alive = False
        
        if self.hitbox[0] + self.hitbox[2] > bottomTube.hitbox[0]:
            if self.hitbox[0] < bottomTube.hitbox[0] + bottomTube.hitbox[2]:
                if self.hitbox[1] + self.hitbox[3] > bottomTube.hitbox[1]:
                    print('User collided with bottomTube')
                    self.alive = False

class tube(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (self.x,self.y,self.width,self.height)
        self.velocity = -5

    def move(self):
        #Simply moving the tubes at a constant velocity to the left, creating a side-scrolling effect
        self.x += self.velocity
        self.hitbox = (self.x,self.y,self.width,self.height)

    def draw(self):
        window.fill((255,0,0), (self.x,self.y,self.width,self.height))

        if displayHitbox:
            pygame.draw.rect(window, (0,0,0),self.hitbox, 2)

class characters_menu(object):
    def __init__(self):
        self.characterNames = ['Plane','Red Square','Blue Square','Green Square']
        self.planeHitbox = pygame.Rect(0,75,screenWidth,400/4)
        self.redSquareHitbox = pygame.Rect(0,80 + (400/4),screenWidth,400/4)
        self.blueSquareHitbox = pygame.Rect(0,85 + (400/4) * 2,screenWidth,400/4)
        self.greenSquareHitbox = pygame.Rect(0,90 + (400/4) * 3,screenWidth,400/4)

    def drawCharacters(self):
        nameCount = 0

        font = pygame.font.SysFont('comicsans', 40)

        xBufferImage = screenWidth - 185
        xBufferText = 30
        yBuffer = 80
        for character in characters:
            window.blit(character, (xBufferImage, yBuffer))

            text = font.render(self.characterNames[nameCount], 1, (255,0,0))
            window.blit(text, (xBufferText, yBuffer))

            nameCount += 1
            yBuffer += 50 + 64

    def redrawCharacterSelectWindow(self):
        window.blit(characterSelectScreen, (-3,-3))
        self.drawCharacters()
        pygame.display.update()

        if displayHitbox:
            pygame.draw.rect(window, (0,0,0), self.planeHitbox, 2)
            pygame.draw.rect(window, (0,0,0), self.redSquareHitbox, 2)
            pygame.draw.rect(window, (0,0,0), self.blueSquareHitbox, 2)
            pygame.draw.rect(window, (0,0,0), self.greenSquareHitbox, 2)

class main_menu(object):
    def __init__(self):
        self.screenBuffer = 35
        self.playButtonX = self.screenBuffer
        self.playButtonWidth = 200
        self.playButtonHeight = 100
        self.playButtonHitbox = pygame.Rect(self.screenBuffer, screenHeight - self.playButtonHeight - self.screenBuffer, self.playButtonWidth, self.playButtonHeight)
        self.charactersButtonX = self.screenBuffer + self.playButtonX + self.playButtonWidth
        self.charactersButtonWidth = 200
        self.charactersButtonHeight = 100
        self.charactersButtonHitbox = pygame.Rect(self.charactersButtonX, screenHeight - self.charactersButtonHeight - self.screenBuffer, self.charactersButtonWidth, self.charactersButtonHeight)
        self.exitButtonX = self.screenBuffer + self.charactersButtonX + self.charactersButtonWidth
        self.exitButtonWidth = 200
        self.exitButtonHeight = 100
        self.exitButtonHitbox = pygame.Rect(self.exitButtonX, screenHeight - self.exitButtonHeight - self.screenBuffer, self.exitButtonWidth, self.exitButtonHeight)

    def drawPlayButton(self):
        window.fill((255,255,255), self.playButtonHitbox)
        text = font.render('Play', 1, (255,0,0))
        window.blit(text, (self.screenBuffer + (self.playButtonWidth - text.get_width()) / 2, screenHeight - self.screenBuffer - self.playButtonHeight + (self.playButtonHeight - text.get_height()) / 2))

    def drawCharactersButton(self):
        font = pygame.font.SysFont('comicsans', 50)
        window.fill((255,255,255), self.charactersButtonHitbox)
        text = font.render('Characters', 1, (255,0,0))
        window.blit(text, (self.charactersButtonX + (self.charactersButtonWidth - text.get_width()) / 2, screenHeight - self.screenBuffer - self.charactersButtonHeight + (self.charactersButtonHeight - text.get_height()) / 2))

    def drawExitButton(self):
        window.fill((255,255,255), self.exitButtonHitbox)
        text = font.render('Exit', 1, (255,0,0))
        window.blit(text, (self.exitButtonX + (self.exitButtonWidth - text.get_width()) / 2, screenHeight - self.screenBuffer - self.exitButtonHeight + (self.exitButtonHeight - text.get_height()) / 2))

    def redrawMenuWindow(self):
        window.blit(menuBackgroundImage, (-3,-3))
        self.drawPlayButton()
        self.drawCharactersButton()
        self.drawExitButton()
        pygame.display.update()
    
    def playButtonClicked(self):
        global gameRunning
        global mainMenuRunning
        gameRunning = True
        mainMenuRunning = False

    def charactersButtonClicked(self):
        global mainMenuRunning
        global characterSelectRunning
        characterSelectRunning = True
        mainMenuRunning = False
        
        
    def exitButtonClicked(self):
        endSession()

def scoreCheck(score, scoreRecieved):
    #Checking that the user hadn't recieved score already from this tube
    if not scoreRecieved:
        temp = score
        #Checking if the user is eligible to gain score based on their position
        if user.hitbox[0] > topTube.hitbox[0] + topTube.hitbox[2]:
            score += 1
        
        if temp < score:
            scoreRecieved = True
    
    if score > user.highScore:
        user.highScore = score

    return score, scoreRecieved

def positionReset():
    global backTube 
    global bottomTube
    global topTube

    backTube= tube(0,0,60,1000)
    bottomTube = tube(screenWidth, random.randint(tubeGap, screenHeight), 50, 1000)
    topTube= tube(bottomTube.x, 0, 50, bottomTube.y - tubeGap)

    user.x = startX
    user.y = startY
    user.verticalVelocity = 0
    user.jumping = False
    user.score = 0
    user.alive = True

def redrawGameWindow():
    #window.fill((0,128,0))
    window.blit(gameBackgroundImage,(-3,-3))
    bottomTube.draw()
    topTube.draw()
    user.draw()
    backTube.draw()
    user.drawScore()
    pygame.display.update()

def pauseScreen():
    gamePaused = True
    text = font.render('Paused!', 1, (0,0,0))
    window.blit(text, ((screenWidth/2) - (text.get_width()/2), (screenHeight/2) - (text.get_height()/2) - 75))
    font1 = pygame.font.SysFont('comicsans', 75)
    text1 = font1.render('Press space to continue!', 1, (0,0,0))
    text2 = font1.render('Press "m" to return to menu', 1, (0,0,0))
    window.blit(text1, ((screenWidth/2) - (text1.get_width()/2), (screenHeight/2) - (text1.get_height()/2)))
    window.blit(text2, ((screenWidth/2) - (text1.get_width()/2) - 25, screenHeight - 25 - (text1.get_height())))

    pygame.display.update()

    #This freezes the screen and ensures that the user is ready before the next game session begins
    while gamePaused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                endSession()

            if pygame.key.get_pressed()[pygame.K_SPACE]:
                gamePaused = False

            if pygame.key.get_pressed()[pygame.K_m]:
                global mainMenuRunning
                global gameRunning
                gamePaused = False
                mainMenuRunning = True
                gameRunning = False

def backgroundAI():
    user.move()
    if user.y > 300:
        user.jump()

    window.blit(gameBackgroundImage,(-3,-3))
    user.draw()
    pygame.display.update()


while True:
    #Variable declaration
    #For MainMenu
    click = False
    mainMenu = main_menu()
    while mainMenuRunning:
        clock.tick(60)
        mainMenu.redrawMenuWindow()
        mx, my = pygame.mouse.get_pos()

        #Checking of the user has clicked the mousebutton
        if click:
            #Checking if the user's cursor is on the button
            if mainMenu.playButtonHitbox.collidepoint((mx,my)):
                print('playButton clicked')
                mainMenu.playButtonClicked()
        
            elif mainMenu.charactersButtonHitbox.collidepoint(mx, my):
                print('charactersButton clicked')
                mainMenu.charactersButtonClicked()
            
            elif mainMenu.exitButtonHitbox.collidepoint(mx, my):
                print('exitButton clicked')
                mainMenu.exitButtonClicked()
            click = False
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                endSession()

            #Checking if a mousebutton is being pressed
            if event.type == MOUSEBUTTONDOWN:
                #Checking if it is the left mouse button
                if event.button == 1:
                    print('click: ',mx,my)
                    click = True

    #Variable declaration
    #For charactersMenu
    click = False
    charactersMenu = characters_menu()
    while characterSelectRunning:
        clock.tick(60)
        charactersMenu.redrawCharacterSelectWindow()
        mx, my = pygame.mouse.get_pos()

        if click:
            if charactersMenu.planeHitbox.collidepoint((mx,my)):
                    characterSelected = 0
                    mainMenuRunning = True
                    characterSelectRunning = False
            elif charactersMenu.redSquareHitbox.collidepoint((mx,my)):
                characterSelected = 1
                mainMenuRunning = True
                characterSelectRunning = False
            elif charactersMenu.blueSquareHitbox.collidepoint((mx,my)):
                    characterSelected = 2
                    mainMenuRunning = True
                    characterSelectRunning = False
            elif charactersMenu.greenSquareHitbox.collidepoint((mx,my)):
                    characterSelected = 3
                    mainMenuRunning = True
                    characterSelectRunning = False
            selectSound.play()

            click = False
            

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                endSession()

            #Checking if a mousebutton is being pressed
            if event.type == MOUSEBUTTONDOWN:
                #Checking if it is the left mouse button
                if event.button == 1:
                    print('click: ',mx,my)
                    click = True

    #Variable declaration
    #For Game
    startX = 100
    startY = 100
    tubeWidth = 50
    tubeGap = 120
    backTube = tube(0,0,60,500)
    bottomTube = tube(screenWidth + 50, random.randint(tubeGap, screenHeight), tubeWidth, 600)
    topTube = tube(bottomTube.x, 0, tubeWidth, bottomTube.y - tubeGap)
    user = player(startX,startY)
    user.scoreRecieved = False
    firstRound = True
    while gameRunning:
        clock.tick(60)

        if firstRound:
            highscore = loadHighscore()
            gameMusic.play(-1)
            redrawGameWindow()
            user.readyCheck()
            firstRound = False

        else:
            user.aliveCheck()
            user.score, user.scoreRecieved = scoreCheck(user.score, user.scoreRecieved)

            if user.alive:
                #Resetting tube positions once they have moved offscreen
                if bottomTube.x < 0:
                    newYPos = random.randint(tubeGap,screenHeight)

                    bottomTube = tube(screenWidth, newYPos, tubeWidth, 600)
                    user.scoreRecieved = False

                if topTube.x < 0:
                    topTube = tube(bottomTube.x,0,tubeWidth,bottomTube.y - tubeGap)
                    user.scoreRecieved = False

                #Checking that the user has not called to exit the game by pressing the red x button in the top right corner of the window
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        endSession()


                keys = pygame.key.get_pressed()

                if keys[pygame.K_ESCAPE]:
                    pauseScreen()

                #Initiating the user's jump mechanic when the space key is pressed
                if keys[pygame.K_SPACE]:
                        if user.canJump:
                            user.jump()
                            user.canJump = False
                        
                if not keys[pygame.K_SPACE]:
                    user.canJump = True

                #Calling all move functions to move all game objects across the screen accordingy
                bottomTube.move()
                topTube.move()
                user.move()

                #Calling the redraw function to update the display of all new object movements 
                redrawGameWindow()
            
            #This is called when the user is no longer set to being 'alive'
            else:
                newHighscoreCheck()
                user.alive = False
                user.hit()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            endSession()

