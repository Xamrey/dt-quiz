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
notifText = pygame.font.SysFont("Arial", 40)
questionText = pygame.font.SysFont("Arial", 30)
answerText = pygame.font.SysFont("Arial", 35)
wn = pygame.display.set_mode((720, 720))
stage = Stage.MenuMain
inputted = ""
answer = None

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
        Asset(1, pygame.image.load("assets/slides/bands.png").convert_alpha(), (60, 72), False),
        Asset(1, pygame.image.load("assets/menus/lpbackbtn.png").convert_alpha(), (160, 600), True, Stage.MenuLearn)
    ],
    Stage.LearnLED : [
        Asset(0, pygame.image.load("assets/menus/background.png").convert_alpha(), (0, 0), False),
        Asset(1, pygame.image.load("assets/slides/led.png").convert_alpha(), (60, 72), False),
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
        Asset(1, pygame.image.load("assets/generate/bandbg.png").convert_alpha(), (60, 40), False),
        Asset(1, pygame.image.load("assets/menus/input.png").convert_alpha(), (110, 400), False),
        Asset(1, pygame.image.load("assets/menus/submitbtn.png").convert_alpha(), (210, 490), True),
        Asset(1, pygame.image.load("assets/menus/lpbackbtn.png").convert_alpha(), (160, 600), True, Stage.MenuPractice)
    ],
    Stage.PracticeLED : [
        Asset(0, pygame.image.load("assets/menus/background.png").convert_alpha(), (0, 0), False),
        Asset(1, pygame.image.load("assets/generate/ledbg.png").convert_alpha(), (60, 40), False),
        Asset(1, pygame.image.load("assets/menus/input.png").convert_alpha(), (110, 400), False),
        Asset(1, pygame.image.load("assets/menus/submitbtn.png").convert_alpha(), (210, 490), True),
        Asset(1, pygame.image.load("assets/menus/lpbackbtn.png").convert_alpha(), (160, 600), True, Stage.MenuPractice)
    ],
    Stage.Quit : []
}
assets = stageAssets[stage][:] # "[:]" Creates a copy of the list instead of a reference, which is what I want

def checkSelected(asset):
    rect = asset.instance.get_rect() # Creating a temporary pygame.rect object to use the in-built collision checks
    rect.x = asset.pos[0]
    rect.y = asset.pos[1]
    return rect.collidepoint(pygame.mouse.get_pos())

def createNotif(message, time):
    assets.append(Asset(4, pygame.image.load("assets/menus/notifbg.png").convert_alpha(), (0, 0), False, notifTimer=time))
    n = 0
    for i in message.split("\n"):
        assets.append(Asset(5, notifText.render(i, True, (255, 255, 255)), (0, 0), False, notifTimer=time)) # Position variable is a placeholder due to it being changed in the next line
        assets[-1].pos = (360 - assets[-1].instance.get_rect().size[0] / 2, 100 - assets[-1].instance.get_rect().size[1] * len(message.split("\n")) / 2 + assets[-1].instance.get_rect().size[1] * n)
        n += 1

def generatePractice(type): # Generates practice questions
    if type == Stage.PracticeBands: # Output format: (Question, Assets, Answer)
        B_n = random.randint(0, 1) # Randomised between 4 and 5 band resistors (0 = 4, 1 = 5)
        B_1 = random.randint(0, 9)
        B_2 = random.randint(0, 9)
        B_3 = random.randint(0, 9) if B_n == 1 else random.randint(0, 4)
        B_4 = random.randint(0, 4) if B_n == 1 else 10
        return (
            "What is the resistance of this resistor, in Ohms?",
            [
                Asset(3, pygame.image.load(f"assets/generate/band{str(B_1)}.png").convert_alpha(), (230, 180), False),
                Asset(3, pygame.image.load(f"assets/generate/band{str(B_2)}.png").convert_alpha(), (280, 180), False),
                Asset(3, pygame.image.load(f"assets/generate/band{str(B_3)}.png").convert_alpha(), (330, 180), False),
                Asset(3, pygame.image.load(f"assets/generate/band{str(B_4)}.png").convert_alpha(), (380, 180), False)
            ],
            int(str(B_1) + str(B_2)) * (pow(10, B_3)) if B_n == 0 else int(str(B_1) + str(B_2) + str(B_3)) * (pow(10, B_4)) # Colour no. to multiplayer equation is 10^n
        )
    elif type == Stage.PracticeLED: # Output format: (Question, Answer)
        V_s = [3, 5, 9, 12][random.randint(0, 3)]
        V_f = [1, 1.5, 2, 2.5][random.randint(0, 3)]
        I_f = [0.01, 0.02, 0.03][random.randint(0, 2)]
        return (
            f"What is the minimum required resistance for an LED\nwith {V_f}V of forward voltage and {I_f}A of forward\ncurrent in a circuit with {V_s}V supplied, in Ohms?",
            int((V_s - V_f) / I_f)
        )

def newQuestion():
    global answer
    toRemove = []
    for i in assets:
        if i.zIndex == 2 or i.zIndex == 3:
            toRemove.append(i)
    for i in toRemove:
        assets.remove(i)
    if stage == Stage.PracticeBands:
        generate = generatePractice(stage)
        assets.append(Asset(3, questionText.render(generate[0], True, (0, 0, 0)), (0, 0), False))
        assets[-1].pos = (360 - assets[-1].instance.get_rect().size[0] / 2, 100 - assets[-1].instance.get_rect().size[1] / 2)
        for i in generate[1]:
            assets.append(i)
        answer = generate[2]
    elif stage == Stage.PracticeLED:
        generate = generatePractice(stage)
        n = 0
        for i in generate[0].split("\n"):
            assets.append(Asset(3, questionText.render(i, True, (0, 0, 0)), (0, 0), False))
            assets[-1].pos = (360 - assets[-1].instance.get_rect().size[0] / 2, 205 - assets[-1].instance.get_rect().size[1] * len(generate[0].split("\n")) / 2 + assets[-1].instance.get_rect().size[1] * n)
            n += 1
        answer = generate[1]

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
    createNotif("There was an error in loading your data,\nany progress you make will not be saved\n(error code has been printed to the console)", 5)

def run(): # Putting the loop in a function allows it to be broken out of instantly
    global stage, assets, inputted, answer # Removes errors with global vs local variables
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
                                assets = stageAssets[i.stageChange][:]
                                inputted = ""
                                if stage == Stage.PracticeBands or stage == Stage.PracticeLED:
                                    newQuestion()
                                else:
                                    answer = None
                            elif stage == Stage.PracticeBands or stage == Stage.PracticeLED: # All selectable assets that don't change the stage will submit answers
                                if inputted == str(answer):
                                    createNotif("Correct!", 2)
                                else:
                                    createNotif(f"Incorrect...\nCorrect Answer: {str(answer)}\nYour Answer: {inputted}", 2)
                                inputted = ""
                                newQuestion()
            elif i.type == pygame.KEYDOWN:
                if stage == Stage.PracticeBands or stage == Stage.PracticeLED:
                    try:
                        int(i.unicode)
                        inputted += i.unicode
                        for i in assets:
                            if i.zIndex == 2: # Input text objects will have a zIndex of 2
                                assets.remove(i)
                        assets.append(Asset(2, answerText.render(inputted, True, (0, 0, 0)), (0, 0), False))
                        assets[-1].pos = (360 - assets[-1].instance.get_rect().size[0] / 2, 440 - assets[-1].instance.get_rect().size[1] / 2)
                    except:
                        if i.key == 13:
                            if inputted == str(answer):
                                createNotif("Correct!", 2)
                            else:
                                createNotif(f"Incorrect...\nCorrect Answer: {str(answer)}\nYour Answer: {inputted}", 2)
                            inputted = ""
                            newQuestion()
                        elif i.key == 8:
                            inputted = inputted[0:-1]
                            for i in assets:
                                if i.zIndex == 2:
                                    assets.remove(i)
                            assets.append(Asset(2, answerText.render(inputted, True, (0, 0, 0)), (0, 0), False))
                            assets[-1].pos = (360 - assets[-1].instance.get_rect().size[0] / 2, 440 - assets[-1].instance.get_rect().size[1] / 2)
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
