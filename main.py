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
    def __init__(self, zIndex, asset, pos, selectable): # zIndex should be between 0 and 5
        self.zIndex = zIndex
        self.asset = asset
        self.pos = pos
        self.selectable = selectable

# Setting up pygame and variables
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Arial" ,24) # rename and change later (for various different text objects)
wn = pygame.display.set_mode((500, 500)) # change later
stage = Stage.MenuMain

assets = [
    Asset(0, font.render("sample text", True, (0, 0, 0)), (0, 0), False)
]

def checkSelected():
    return "change later"

def createNotif(userCloses, message):
    print("change later", userCloses, message)

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
    createNotif(True, "There was an error in loading your data, any progress you make will not be saved (error code has been printed to the console)")

def run(): # Putting the loop in a function allows it to be broken out of instantly
    while True:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                if saveData:
                    data = open("data.txt", "w")
                    data.write(json.dumps(practiceData))
                    data.close()
                return
            elif i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    print("mouse1 down")
            elif i.type == pygame.KEYDOWN:
                if stage == Stage.PracticeBands or stage == Stage.PracticeLED:
                    try:
                        changevariablename = int(i.unicode)
                        print("number key down")
                    except:
                        pass

        wn.fill((255, 255, 255))
        assets[0].pos = ((assets[0].pos[0] + 0.1) % 500, (assets[0].pos[1] + 0.05) % 500)
        renderList = {0:[],1:[],2:[],3:[],4:[],5:[]}
        for i in assets:
            renderList[i.zIndex].append(i)
        for i in renderList.values():
            for v in i:
                wn.blit(v.asset, v.pos)
        pygame.display.flip()

run()
pygame.quit()
pygame.font.quit()
