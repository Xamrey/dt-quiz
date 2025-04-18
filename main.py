import pygame
import json
import random

class Stage: # Allows me to reference what menu is being used easier
    MenuMain = "__STAGE-MENU-MAIN__"
    MenuLearn = "__STAGE-MENU-LEARN__"
    LearnBands = "__STAGE-LEARN-BANDS__"
    LearnLED = "__STAGE-LEARN_LED__"
    MenuPractice = "__STAGE-MENU-PRACTICE__"
    PracticeBands = "__STAGE-PRACTICE-BANDS__"
    PracticeLED = "__STAGE-PRACTICE-LED__"
    Quit = "__STAGE-QUIT__"
Stage = Stage() # Removing the need to create a copy of the class every time it is used

class Asset:
    def __init__(self, zIndex, instance, pos, selectable, stageChange=None, notifTimer=None):
        self.zIndex = zIndex # Should be between 0 and 5
        self.instance = instance
        self.pos = pos
        self.selectable = selectable
        self.stageChange = stageChange
        self.notifTimer = notifTimer * 24 if notifTimer else None # Length of time that the notification stays on screen, in seconds (multipled by framerate)

# Setting up pygame and variables
pygame.init()
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont("Arial", 24) # rename and change later (for various different text objects)
wn = pygame.display.set_mode((720, 720))
stage = Stage.MenuMain

stageAssets = {
    Stage.MenuMain : [
        Asset(0, pygame.image.load("assets/menus/background.png").convert_alpha(), (0, 0), False),
        Asset(1, pygame.image.load("assets/menus/learnbtn.png").convert_alpha(), (160, 160), True, Stage.MenuLearn),
        Asset(1, pygame.image.load("assets/menus/practicebtn.png").convert_alpha(), (160, 320), True, Stage.MenuPractice),
        Asset(1, pygame.image.load("assets/menus/quitbtn.png").convert_alpha(), (160, 480), True, Stage.Quit)
    ],
    Stage.MenuLearn : [
        Asset(0, pygame.image.load("assets/menus/background.png").convert_alpha(), (0, 0), False),
        Asset(1, pygame.image.load("assets/menus/learntxt.png").convert_alpha(), (0, 0), False),
        Asset(1, pygame.image.load("assets/menus/bandsbtn.png").convert_alpha(), (160, 250), True, Stage.LearnBands),
        Asset(1, pygame.image.load("assets/menus/ledbtn.png").convert_alpha(), (160, 390), True, Stage.LearnLED),
        Asset(1, pygame.image.load("assets/menus/menubackbtn.png").convert_alpha(), (160, 530), True, Stage.MenuMain)
    ],
    Stage.LearnBands : [
        Asset(0, pygame.image.load("assets/menus/background.png").convert_alpha(), (0, 0), False),
        Asset(1, pygame.image.load("assets/menus/lpbackbtn.png").convert_alpha(), (160, 600), True, Stage.MenuLearn)
    ],
    Stage.LearnLED : [
        Asset(0, pygame.image.load("assets/menus/background.png").convert_alpha(), (0, 0), False),
        Asset(1, pygame.image.load("assets/menus/lpbackbtn.png").convert_alpha(), (160, 600), True, Stage.MenuLearn)
    ],
    Stage.MenuPractice : [
        Asset(0, pygame.image.load("assets/menus/background.png").convert_alpha(), (0, 0), False),
        Asset(1, pygame.image.load("assets/menus/practicetxt.png").convert_alpha(), (0, 0), False),
        Asset(1, pygame.image.load("assets/menus/bandsbtn.png").convert_alpha(), (160, 250), True, Stage.PracticeBands),
        Asset(1, pygame.image.load("assets/menus/ledbtn.png").convert_alpha(), (160, 390), True, Stage.PracticeLED),
        Asset(1, pygame.image.load("assets/menus/menubackbtn.png").convert_alpha(), (160, 530), True, Stage.MenuMain)
    ],
    Stage.PracticeBands : [
        Asset(0, pygame.image.load("assets/menus/background.png").convert_alpha(), (0, 0), False),
        Asset(1, pygame.image.load("assets/menus/lpbackbtn.png").convert_alpha(), (160, 600), True, Stage.MenuPractice)
    ],
    Stage.PracticeLED : [
        Asset(0, pygame.image.load("assets/menus/background.png").convert_alpha(), (0, 0), False),
        Asset(1, pygame.image.load("assets/menus/lpbackbtn.png").convert_alpha(), (160, 600), True, Stage.MenuPractice)
    ],
    Stage.Quit : []
}
assets = stageAssets[stage]

def checkSelected(asset):
    rect = asset.instance.get_rect() # Creating a temporary pygame.rect object to use the in-built collision checks
    rect.x = asset.pos[0]
    rect.y = asset.pos[1]
    return rect.collidepoint(pygame.mouse.get_pos())

def createNotif(message, time):
    assets.append(Asset(4, pygame.image.load("assets/menus/notifbg.png").convert_alpha(), (0, 0), False, notifTimer=time))
    n = 0
    for i in message.split("\n"):
        assets.append(Asset(5, font.render(i, True, (0, 0, 0)), (0, 0), False, notifTimer=time)) # Position variable is a placeholder due to it being changed in the next line
        assets[-1].pos = (225 - assets[-1].instance.get_rect().size[0] / 2, 50 - assets[-1].instance.get_rect().size[1] * len(message.split("\n")) / 2 + assets[-1].instance.get_rect().size[1] * n) # change if screen width / notifbg width changes
        n += 1

def generatePractice(type): # Generates practice questions
    if type == Stage.PracticeBands: # Output format: (Question, Assets, Answer)
        B_n = random.randint(0, 1) # Randomised between 4 and 5 band resistors (0 = 4, 1 = 5)
        B_1 = random.randint(0, 9)
        B_2 = random.randint(0, 9)
        B_3 = random.randint(0, 9) if B_n == 1 else random.randint(0, 4)
        B_4 = random.randint(0, 4) if random.randint(0, 1) == 1 else 10
        return (
            "What is the resistance of this resistor, in Ohms? (Ignoring tolerance)",
            [
                Asset(3, pygame.image.load(f"assets/generate/band{str(B_1)}.png").convert_alpha(), (0, 0), False),
                Asset(3, pygame.image.load(f"assets/generate/band{str(B_2)}.png").convert_alpha(), (0, 0), False),
                Asset(3, pygame.image.load(f"assets/generate/band{str(B_3)}.png").convert_alpha(), (0, 0), False),
                Asset(3, pygame.image.load(f"assets/generate/band{str(B_4)}.png").convert_alpha(), (0, 0), False)
            ], # change zindex / pos later
            int(str(B_1) + str(B_2)) * (pow(10, B_3)) if B_n == 0 else int(str(B_1) + str(B_2) + str(B_3)) * (pow(10, B_4)) # Colour no. to multiplayer equation is 10^n
        )
    elif type == Stage.PracticeLED: # Output format: (Question, Answer)
        V_s = [3, 5, 9, 12][random.randint(0, 3)]
        V_f = [1, 1.5, 2, 2.5][random.randint(0, 3)]
        I_f = [0.01, 0.02, 0.03][random.randint(0, 2)]
        return (
            f"What is the minimum required resistance for an LED with {V_f}V of forward voltage and {I_f}A of forward current in a circuit with {V_s}V supplied, in Ohms?",
            (V_s - V_f) / I_f
        )
print(generatePractice(Stage.PracticeBands))
practiceData = { # Default data
    "BANDS": {
        "CORRECT": 0,
        "INCORRECT": 0
    },
    "LED": {
        "CORRECT": 0,
        "INCORRECT": 0
    }
}

saveData = True
try:
    data = open("data.txt", "r")
    formatted = json.loads(data.read())
    practiceData = formatted
    data.close()
except Exception as err:
    saveData = False
    print(f"Error Code: '{err}'")
    createNotif("There was an error in loading your data,\nany progress you make will not be saved\n(error code has been printed to the console)")

def run(): # Putting the loop in a function allows it to be broken out of instantly
    global stage, assets # Removes errors with global vs local variables
    while True:
        if stage == Stage.Quit:
            if saveData:
                data = open("data.txt", "w")
                data.write(json.dumps(practiceData))
                data.close()
            return
        for i in pygame.event.get(): # Input
            if i.type == pygame.QUIT:
                if saveData:
                    data = open("data.txt", "w")
                    data.write(json.dumps(practiceData))
                    data.close()
                return
            elif i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    for i in assets:
                        if i.selectable and checkSelected(i):
                            if i.stageChange:
                                stage = i.stageChange
                                assets = stageAssets[i.stageChange]
                            elif stage == Stage.PracticeBands or stage == Stage.PracticeLED: # All selectable assets that don't change the stage will submit answers
                                print("submit answer")
            elif i.type == pygame.KEYDOWN:
                if stage == Stage.PracticeBands or stage == Stage.PracticeLED:
                    try:
                        key = int(i.unicode)
                        print("add number to answer")
                    except:
                        if i.key == 13:
                            print("submit answer")
                        elif i.key == 8:
                            print("remove number from answer")
        # Rendering assets
        wn.fill((0, 0, 0))
        renderList = {0:[],1:[],2:[],3:[],4:[],5:[]} # zIndex functionality
        cursor = pygame.SYSTEM_CURSOR_ARROW
        for i in assets:
            if i.selectable and checkSelected(i): # Checking if a selectable button is being hovered over
                cursor = pygame.SYSTEM_CURSOR_HAND
            renderList[i.zIndex].append(i)
            if i.notifTimer:
                i.notifTimer -= 1
                if i.notifTimer <= 0:
                    assets.remove(i)
        for i in renderList.values():
            for v in i:
                if v in assets: # Stops strange bug with removing notification objects
                    wn.blit(v.instance, v.pos)
        if pygame.mouse.get_cursor() != cursor:
            pygame.mouse.set_cursor(cursor)
        pygame.display.flip()
        clock.tick(24) # Caps FPS at 24 so that timers can work correctly

run()
pygame.quit()
pygame.font.quit()
