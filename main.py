import pygame
import json
import random

class Stage: # Allows me to reference what menu is being used easier
    MenuMain = "__STAGE-MENU-MAIN__"
    MenuLearn = "__STAGE-MENU-LEARN__"
    LearnBANDS = "__STAGE-LEARN-BANDS__"
    LearnLED = "__STAGE-LEARN_LED__"
    MenuPractice = "__STAGE-MENU-PRACTICE__"
    PracticeBands = "__STAGE-PRACTICE-BANDS__"
    PracticeLED = "__STAGE-PRACTICE-LED__"
Stage = Stage() # Removing the need to create a copy of the class every time it is used

class Asset:
    def __init__(self, zIndex, instance, pos, selectable, stageChange=None, notifTimer=None): # zIndex should be between 0 and 5
        self.zIndex = zIndex
        self.instance = instance
        self.pos = pos
        self.selectable = selectable
        self.stageChange = stageChange
        self.notifTimer = notifTimer

# Setting up pygame and variables
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Arial" ,24) # rename and change later (for various different text objects)
wn = pygame.display.set_mode((500, 500)) # change later
stage = Stage.MenuMain

stageAssets = {
    Stage.MenuMain : [
        Asset(0, font.render("sample text", True, (0, 0, 0)), (0, 0), False)
    ],
    Stage.MenuLearn : [

    ]
}
assets = stageAssets[stage]

def checkSelected(asset):
    rect = asset.instance.get_rect() # Creating a temporary pygame.rect object to use the in-built collision checks
    rect.x = asset.pos[0]
    rect.y = asset.pos[1]
    return rect.collidepoint(pygame.mouse.get_pos())

def createNotif(message):
    print("change later", message)

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
    createNotif("There was an error in loading your data, any progress you make will not be saved (error code has been printed to the console)")

def run(): # Putting the loop in a function allows it to be broken out of instantly
    global stage, assets
    while True:
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
                            elif stage == Stage.PracticeBands or stage == Stage.PracticeLED: # Only selectable assets that don't change the stage will submit answers
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
        assets[0].pos = ((assets[0].pos[0] + 0.1) % 500, (assets[0].pos[1] + 0.05) % 500)
        # Rendering assets
        wn.fill((255, 255, 255))
        renderList = {0:[],1:[],2:[],3:[],4:[],5:[]}
        for i in assets:
            renderList[i.zIndex].append(i)
            if i.notifTimer:
                i.notifTimer -= 1
                if i.notifTimer <= 0:
                    assets.remove(i)
        for i in renderList.values():
            for v in i:
                wn.blit(v.instance, v.pos)
        pygame.display.flip()

run()
pygame.quit()
pygame.font.quit()
