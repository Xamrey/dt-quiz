import pygame
import json
import random

class Stage: # Allows me to reference what menu is being used easier
    MenuMain = "__STAGE-MENU-MAIN__"
    MenuLearn = "__STAGE-MENU-LEARN__"
    LearnBANDS = "__STAGE-LEARN-BANDS__"
    LearnLED = "__STAGE-LEARN_LED__"
    MenuPractice = "__STAGE-MENU-PRACTICE__"
    PracticeBands = "__STAGE-PRACTICE-BANDS"
    PracticeLED = "__STAGE-PRACTICE-LED__"
Stage = Stage() # Removing the need to create a copy of the class every time it is used

class Asset:
    def __init__(self, zIndex, asset, pos, selectable): # zIndex should be between 0 and 5
        self.zIndex = zIndex
        self.asset = asset
        self.pos = pos
        self.selectable = selectable

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Arial" ,24) # rename and change later (for various different text objects)
wn = pygame.display.set_mode((500, 500)) # change later

assets = [
    Asset(0, font.render("sample text", True, (0, 0, 0)), (0, 0), False)
]

def checkSelected():
    return "change later"

def createNotif(userCloses, message):
    print("change later", userCloses, message)

practiceData = {
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

run = True
while run:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False
            if saveData:
                data = open("data.txt", "w")
                data.write(json.dumps(practiceData))
                data.close()

    wn.fill((255, 255, 255))
    wn.blit(assets[0].asset, (assets[0].pos[0] + random.randint(-25, 25), assets[0].pos[1] + random.randint(-25, 25)))
    pygame.display.flip()

pygame.quit()
pygame.font.quit()
