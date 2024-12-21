import pygame
import pygame.freetype
import random
from pygame.sprite import Sprite
from enum import Enum

def create_surface_with_text(text, font_size, text_color, background_color):
    """ Function creating a surface containing text """

    font = pygame.freetype.SysFont(None, font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_color, bgcolor=background_color)

    return surface.convert_alpha()

def title_screen(screen):
    """ Title function that controls the title screen game state """

    # initializing title screen elements
    start_button = UIElement(
        center_position=(270,265),
        font_size=25,
        background_color='black',
        text_color='white',
        text='PLAY',
        action=GameState.NEW_GAME
    )

    quit_button = UIElement(
        center_position=(270,305),
        font_size=25,
        background_color='black',
        text_color='white',
        text='QUIT',
        action=GameState.QUIT
    )

    buttons = [start_button, quit_button]
    
    while True:

        # mouse click logic
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        screen.fill('black')

        # drawing and updating button actions based on click logic
        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)

            if ui_action is not None:
                return ui_action

            button.draw(screen)

        pygame.display.flip()

def play(screen):
    """ Play function that controls the new game state """

    score = 0

    # initializing game objects
    player = GameObject(
        color='white',
        width=10,
        height=50,
        x_pos = 0,
        y_pos = 245
    )

    divider = GameObject(
        color='grey',
        width=1,
        height=540,
        x_pos=269,
        y_pos=0
    )

    computer = GameObject(
        color='white',
        width=10,
        height=50,
        x_pos = 530,
        y_pos = 245
    )

    ball = GameObject(
        color='white',
        width=10,
        height=10,
        x_pos = 265,
        y_pos = 265
    )

    game_objects = [player, divider, computer, ball]

    # setting the initial direction for the ball
    ball_direction_x = random.choice([-1, 1])
    ball_direction_y = random.choice([-1, 1])

    while True:

        # creating the scoreboard
        score_board = UIElement(
            center_position=(130,10),
            font_size=15,
            background_color='black',
            text_color='white',
            text= f"Score: {score}",
            action=None
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT

        # identifying mouse y-axis location and setting the player paddle to be at said location
        _ , mouse_y = pygame.mouse.get_pos()
        player.y_pos = mouse_y - player.height // 2

        # setting the direction for the ball
        ball.x_pos += ball_direction_x
        ball.y_pos += ball_direction_y

        # setting the location for the computer paddle, making it follow the ball
        computer.y_pos = ball.y_pos - 20

        # logic for ball/paddle physics + scoring
        if ball.y_pos <= 0 or ball.y_pos >= 540 - ball.height:
            ball_direction_y *= -1

        if ball.x_pos + ball.width >= computer.x_pos and computer.y_pos <= ball.y_pos <= computer.y_pos + computer.height:
            ball_direction_x *= -1

        if ball.x_pos <= player.x_pos + player.width and player.y_pos <= ball.y_pos <= player.y_pos + player.height:
            ball_direction_x *= -1
            score += 1

            if score > 0 and score % 10 == 0:
                ball_direction_x += 0.2
                ball_direction_y += 0.2

        if ball.x_pos <= 0:
            return GameState.TITLE_PAGE

        # visualizing all the game components
        screen.fill('black')
        score_board.draw(screen)

        for object in game_objects:
            pygame.draw.rect(screen, object.color, object.get_rect())

        pygame.display.flip()

class UIElement(Sprite):
    """ Class to create user elements that can be added to a surface """

    def __init__(self, center_position, text, font_size, background_color, text_color, action=None):
        self.mouse_over = False

        # static default surface
        default_surface = create_surface_with_text(text, font_size, text_color, background_color)

        # new surface when mouse is hovering the element
        highlighted_surface = create_surface_with_text(text, font_size*1.1, text_color, background_color)

        # creating a list of the surfaces
        self.surfaces = [default_surface, highlighted_surface]
        self.rects = [default_surface.get_rect(center=center_position), highlighted_surface.get_rect(center=center_position)]
        self.action = action

        super().__init__()

    def update(self, mouse_position, mouse_up):
        """ 
            Updating element appearance depending on mouse hovering and 
            when clicked returns the buttons action
        """
        if self.rect.collidepoint(mouse_position):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        """ Draw element onto a surface """

        surface.blit(self.surface, self.rect)

    # properties that return the proper surface and rect depending on mouse position
    @property
    def surface(self):
        return self.surfaces[1] if self.mouse_over else self.surfaces[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

class GameObject(pygame.sprite.Sprite):
    """ Class to create new game objects """

    def __init__(self, color, width, height, x_pos, y_pos):
        self.color = color
        self.width = width
        self.height = height
        self.x_pos = x_pos
        self.y_pos = y_pos

        super().__init__()

    # function to create the rects for game objects
    def get_rect(self):
        return pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)

class GameState(Enum):
    """ Handling each state of the game """

    QUIT = -1
    TITLE_PAGE = 0
    NEW_GAME = 1

def main():
    """ Main function that initiates pygame, screen and handles the game states """

    # initializing pygame
    pygame.init()
    pygame.display.set_caption("Pong")
    
    # intitializing the screen, game state and game clock
    screen = pygame.display.set_mode((540,540))
    game_state = GameState.TITLE_PAGE
    clock = pygame.time.Clock()

    while True:

        # setting fps
        clock.tick(60)

        # checking game state
        if game_state == GameState.TITLE_PAGE:
            game_state = title_screen(screen)
        
        if game_state == GameState.NEW_GAME:
            game_state = play(screen)

        if game_state == GameState.QUIT:
            pygame.quit()
            return

if __name__ == "__main__":
    main()