import pygame, sys, pathlib, random

pygame.init()
pygame.font.init()

screenW, screenH = 800, 500

screen = pygame.display.set_mode((screenW, screenH))


def get_text_width(text: str, font_file: str, font_size: int) -> int:
    font = pygame.font.Font(pathlib.Path(font_file), font_size)
    t = font.render(text, 1, (0, 0, 0))
    textRect = t.get_rect()
    width = textRect.width
    return width


def get_text_rect(text: str, font_file: str, font_size: int,
                  pos=(0, 0)) -> pygame.Rect:
    font = pygame.font.Font(pathlib.Path(font_file), font_size)
    t = font.render(text, 1, (0, 0, 0))
    textRect = t.get_rect()
    textRect.center = pos
    return textRect


def draw_text(screen: pygame.Surface,
              text: str,
              font_file: str,
              font_size: int,
              color: tuple,
              pos: tuple,
              backg=None,
              bold=False,
              italic=False,
              underline=False):
    if '.ttf' in font_file:
        font = pygame.font.Font(pathlib.Path(font_file), font_size)
    else:
        font = pygame.font.SysFont(font_file, font_size)
    font.set_bold(bold)
    font.set_italic(italic)
    font.set_underline(underline)
    if backg == None:
        t = font.render(text, True, color)
    t = font.render(text, True, color, backg)
    textRect = t.get_rect()
    textRect.center = pos
    screen.blit(t, textRect)


# Input Handlers
keyModifiers = {"LShift": 1, "RShift": 2, "LCtrl": 64, "RCtrl": 128}

clipboard = ''


# RainbowTextBox Object
class RainbowTextBox:
    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 fontSize: int,
                 fontColor: tuple,
                 bold: bool,
                 italic: bool,
                 underline: bool,
                 borderRadius=0,
                 borderWidth=1,
                 backgroundColor=(0, 0, 0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.borderRadius = borderRadius
        self.borderWidth = borderWidth
        self.backgroundColor = backgroundColor
        self.text = ""
        self.selection = None
        self.select_all = False
        self.select_none = False

    def draw(self, screen):
        """Draws the RainbowTextBox to the screen."""
        pygame.draw.rect(screen,
                         self.backgroundColor,
                         (self.x, self.y, self.width, self.height),
                         width=self.borderWidth,
                         border_radius=self.borderRadius)
        if get_text_width(self.text, "fonts/OpenSans-Medium.ttf",
                          self.fontSize) > self.width:
            self.text = self.text.rstrip(self.text[-1])
        # text rect
        self.text_rect = get_text_rect(self.text,
                                       "fonts/OpenSans-Medium.ttf",
                                       self.fontSize,
                                       pos=pygame.Rect(self.x, self.y,
                                                       self.width,
                                                       self.height).center)
        if self.select_all == True:
            self.selection = self.text
        if self.select_none == True:
            self.selection = None
        # drawing selection
        if self.selection != None:
            pygame.draw.rect(
                screen, (0, 206, 209),
                get_text_rect(self.selection,
                              "fonts/OpenSans-Medium.ttf",
                              self.fontSize,
                              pos=pygame.Rect(self.x, self.y, self.width,
                                              self.height).center))
        # drawing text
        draw_text(screen, self.text, "fonts/OpenSans-Medium.ttf", self.fontSize,
                  self.fontColor,
                  pygame.Rect(self.x, self.y, self.width, self.height).center,
                  None, self.bold, self.italic, self.underline)

    def type(self, char, mods, clipboard):
        """Types characters into the RainbowTextBox"""
        if char == "backspace":
            if len(self.text) > 0:
                self.text = self.text[:-1]
        elif char == "space":
            self.text += " "
        elif len(char) == 1:
            if mods == 64: # get capital letters
                self.text += char.upper()
            else:
                self.text += char
        if len(self.text) >= 25:
            self.text = self.text[:25]


# Program Datas
rainbowTextBoxes = []
selectedRainbowTextBox = None  # current rainbow text-box
screenColor = (255, 255, 255)
changeColorMilis = 50
changeColor = pygame.time.set_timer(
    pygame.USEREVENT + 1,
    changeColorMilis)  # Set random RGB Color every few milis
editMode = False  # Determins if we are creating/deleting RainbowTextBoxes or editing them.
# Program Variables
run = True
fps = 240
clock = pygame.time.Clock()

while run:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()

        # Key Input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e and pygame.key.get_mods(
            ) & pygame.KMOD_CTRL:  # toggles edit mode
                editMode = not editMode

            if editMode == True and selectedRainbowTextBox != None:
                char = pygame.key.name(event.key)
                mods = pygame.key.get_mods()
                for rainbowTextBox in rainbowTextBoxes:
                    if rainbowTextBox == selectedRainbowTextBox:
                        rainbowTextBox.type(char, mods,
                                            clipboard)  # Typing the characters

        if event.type == pygame.USEREVENT + 1:
            for rainbowTextBox in rainbowTextBoxes:
                rainbowTextBox.fontColor = (random.randint(0, 255),
                                            random.randint(0, 255),
                                            random.randint(0, 255))

    if pygame.mouse.get_pressed()[0]:  # Add by right-clicking
        mpos = pygame.mouse.get_pos()
        if editMode == False:
            if all(
                    pygame.Rect(rainbowTextBox.x, rainbowTextBox.y,
                                rainbowTextBox.width, rainbowTextBox.height).
                    collidepoint(mpos) == False
                    for rainbowTextBox in rainbowTextBoxes
            ):  # New area, dosent intersect other rainbowTextBoxes.
                rainbowTextBox = RainbowTextBox(mpos[0], mpos[1], 200, 100, 20,
                                                (255, 255, 255), False, False,
                                                False)  # Initial Defaults
                rainbowTextBoxes.append(rainbowTextBox)
        if editMode == True:
            for rainbowTextBox in rainbowTextBoxes:
                if pygame.Rect(rainbowTextBox.x, rainbowTextBox.y,
                               rainbowTextBox.width,
                               rainbowTextBox.height).collidepoint(mpos):
                    selectedRainbowTextBox = rainbowTextBox

    if pygame.mouse.get_pressed()[2]:  # Delete by left-clicking
        mpos = pygame.mouse.get_pos()
        if editMode == False:
            for rainbowTextBox in rainbowTextBoxes:
                if pygame.Rect(rainbowTextBox.x, rainbowTextBox.y,
                               rainbowTextBox.width,
                               rainbowTextBox.height).collidepoint(mpos):
                    if selectedRainbowTextBox == rainbowTextBox:
                        selectedRainbowTextBox = None
                    rainbowTextBoxes.remove(rainbowTextBox)
        if editMode == True:
            selectedRainbowTextBox = None

    # Drawing objects
    # Sets the screen's color
    screen.fill(screenColor)
    #print(clipboard)
    # Draws all of the rainbow text-boxes
    for rainbowTextBox in rainbowTextBoxes:
        rainbowTextBox.draw(screen)
    # Highlights the selected rainbow text-box in editMode
    if selectedRainbowTextBox != None and editMode != False:
        pygame.draw.rect(
            screen, (0, 206, 209),
            (selectedRainbowTextBox.x, selectedRainbowTextBox.y,
             selectedRainbowTextBox.width, selectedRainbowTextBox.height),
            width=2,
            border_radius=selectedRainbowTextBox.borderRadius)
    pygame.display.update()
