import game_classes
import pygame
from pygame.locals import *

# global screen vairable to be used globaly (as all parts of the game
# refrence the same screen)
global screen

# colors definitions for pygame
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
darkBlue = (0, 0, 128)
white = (255, 255, 255)
black = (0, 0, 0)
pink = (255, 200, 200)
nice_one = (95, 158, 160)
last_played = []
pygame.font.init()
check = 0

# defining screen 16:9 native
size_o = screen_width, screen_height = 1600, 900
scale_size = size_o
scale_card_size = 0

# scaling factors that are initially set the scale value of 1 (native to
# 1600x900 pixel resolution)
scale_x = 1
scale_y = 1

# defining the global pygame screen value to be used within PY-UNO
screen = pygame.display.set_mode(size_o, HWSURFACE | DOUBLEBUF | RESIZABLE)
screen.fill(nice_one)

# default card rectangle size and card size and default card pygame rectangle
card_width = 130
card_height = 182
def_rect = pygame.Rect(0, 0, card_width, card_height)

# defining the default facedown card value
face_down_card = game_classes.Card(
    "face_down", "small_cards/card_back_alt.png", None)


def pygame_text_input_field():

    # Create a font object
    pygame.font.init()
    font = pygame.font.SysFont("arial", 32)
    # Create a text input box
    text_input = pygame.Rect(50, 50, 140, 32)

    # Create a color for the text input box
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive

    # Create a variable to store the text
    text = ''

    # Create a flag to check if the text input box is active
    active = False

    while True:
        # Get events from the event queue
        for event in pygame.event.get():
            # Check if the user has quit
            if event.type == pygame.QUIT:
                pygame.quit()
                return text

            # Check if the user has clicked on the text input box
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user has clicked on the text input box
                if text_input.collidepoint(event.pos):
                    # Set the active flag to True
                    active = not active
                else:
                    # Set the active flag to False
                    active = False
                # Change the color of the text input box
                color = color_active if active else color_inactive

            # Check if the user has pressed a key
            if event.type == pygame.KEYDOWN:
                # If the user has pressed the backspace key
                if event.key == pygame.K_BACKSPACE:
                    # Remove the last character from the text
                    text = text[:-1]
                elif event.key == pygame.K_RETURN:
                    print(text)
                    text = ''
                else:
                    # Add the character to the text
                    text += event.unicode

        txt_surface = font.render(text, True, color)
        screen.blit(txt_surface, (text_input.x + 5, text_input.y + 5))


def adding(color, type):
    # global check
    # check = 1
    print(type)
    print(color)
    colors = 'bryg'
    colors1 = ['blue', 'red', 'yellow', 'green']
    types = '0123456789prs'
    types1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'picker', 'reverse', 'skip']
    if color in colors:
        file = "small_cards/" + colors1[colors.find(color)] + "_" + types1[types.find(type)]
    else:
        file = 'small_cards/wild_color_changer'
    if len(last_played) != 0:
        if len(last_played) >= 5 and file != last_played[0][0]:
            for i in range(3, -1, -1):
                last_played[i + 1] = last_played[i]
            last_played[0] = (file, colors1[colors.find(color)])
        elif file != last_played[0][0]:
            last_played.insert(0, (file, colors1[colors.find(color)]))
    else:
        last_played.append((file, colors1[colors.find(color)]))


def interesting():
    pygame.draw.rect(screen, white, pygame.Rect(0, 270, 720, 300), 3)
    pygame.draw.rect(screen, white, pygame.Rect(717, 270, 160, 300), 3)
    pygame.draw.rect(screen, white, pygame.Rect(0, 325, 877, 2), 3)
    font = pygame.font.Font('freesansbold.ttf', 32)
    played = 'Последние сыгранные (старые <- новые)'
    text = font.render(played, True, white, nice_one)
    textRect = text.get_rect()
    textRect.center = (360, 300)
    screen.blit(text, textRect)
    played = 'Текущая'
    text = font.render(played, True, white, nice_one)
    textRect = text.get_rect()
    textRect.center = (797, 300)
    screen.blit(text, textRect)


def handle_resize(event):
    """
    Small function that is called when the PY-GAME window is resized.

    Functinon updates the scale_x and scale_y globals for easy resizing display
    functionality.

    O(1) runtime
    """
    # grabbing the newely resized windows size
    scale_size = event.dict['size']

    # save these scaling factors globally as they affect the global screen
    # rendering
    global scale_x
    global scale_y

    # grabbing new scaling factor values
    (x_o, y_o) = size_o
    (x_1, y_1) = scale_size
    # calculating new scaling factor values
    scale_x = (x_1 / x_o)
    scale_y = (y_1 / y_o)


def scale_card_blit(image, position, transform_ov=False):
    """
    Scaling blit function that uses the scale_x and scale_y globals for
    correctly transforming the image onto a resized screen.

    This function both scales the position of the image and the size of the
    image itself aswell.

    O(1) runtime (neglecting blit)
    """
    # scale the inputted card image to the global scale factors
    card_width = int(130 * scale_x)
    card_height = int(182 * scale_y)
    if transform_ov:  # transform override for half image transform
        image = pygame.transform.scale(
            image, (card_width // 2, card_height // 2))
    else:
        image = pygame.transform.scale(image, (card_width, card_height))
    # scale the images position with the global scale factors
    l = int(position.left * scale_x)
    t = int(position.top * scale_y)
    w = int(position.width * scale_x)
    h = int(position.height * scale_y)

    scale_pos = pygame.Rect(l, t, w, h)
    screen.blit(image, scale_pos)


def draw_top_stack_card(board):
    """
    Renders the top card of the card_stack on the board.

    O(1) runtime
    """
    if board.card_stack != []:
        top_card = board.card_stack[-1]
        top_card.rect = def_rect
        top_card.rect = top_card.rect.move(
            (screen_width - card_width) // 2 - 3,
            (screen_height - card_height) // 2)
        # blit top card of board onto center screen
        adding(top_card.color, top_card.type)
        scale_card_blit(top_card.card_data, top_card.rect)

    interesting()

    for i in range(len(last_played)):
        cards_last = game_classes.Card(last_played[i][1], last_played[i][0] + ".png", None)
        cards_last.rect = def_rect
        cards_last.rect = cards_last.rect.move((screen_width - card_width)\
            // 2 - 20 - card_width - (card_width + 15) * i, screen_height - (900 / 2) - card_height // 2)
        scale_card_blit(cards_last.card_data, cards_last.rect)


def redraw_hand_visble(player, selected=None):
    """
    Redraws a players hand to be face up.

    O(n) runtime where n is the size of the players hand
    """
    # player playing indicator placeholder graphic
    player_num = str(player.name[7])
    card_disp = game_classes.Card(
        "red", "small_cards/grey_" + player_num + ".png", None)
    card_disp.rect = card_disp.rect.move(10, screen_height - card_height - 10)

    # dynamic card spacing
    player_handsize = len(player.hand)
    if player_handsize <= 9:
        iterating_fact = 100
    else:
        iterating_fact = (3 * (screen_width // 4)) // player_handsize

    # get a "middle" start postion for bliting cards
    start_pos = (screen_width - 100 * len(player.hand)) // 2
    if start_pos < 150:
        start_pos = 150

    card_index = 0
    for card in player.hand:  # O(n)
        card.rect = def_rect
        if card_index == selected:
            card.rect = card.rect.move(start_pos, 600)
        else:
            card.rect = card.rect.move(start_pos, 700)

        card.rect = card.rect.move(iterating_fact * card_index, 0)
        scale_card_blit(card.card_data, card.rect)

        card_index += 1

    # displaying the placeholder playing player number
    scale_card_blit(card_disp.card_data, card_disp.rect)


def redraw_hand_nonvisble(player, start_horz, start_vert=0):
    """
    Draws a players hand to be non-visible (face down cards).

    O(n) runtime where n is the size of the players hand
    """
    # placeholder player num graphics
    player_num = str(player.name[7])
    card_disp = game_classes.Card(
        "red", "small_cards/grey_" + player_num + ".png", None)
    card_disp.rect = card_disp.rect.move(start_horz + 10, start_vert + 10)

    # dynamic card spacing
    player_handsize = len(player.hand)
    if player_handsize <= 7:
        iterating_fact = 130
    else:
        iterating_fact = 550 // player_handsize

    card_index = 0
    for card in player.hand:  # O(n)
        card.rect = def_rect
        card.rect = card.rect.move(start_horz, start_vert)
        card.rect = card.rect.move(iterating_fact * card_index, 0)
        scale_card_blit(face_down_card.card_data, card.rect)

        card_index += 1

    # displaying the placeholder player num graphics
    scale_card_blit(card_disp.card_data, card_disp.rect, True)


def redraw_hand_nonvisble_loop(players_temp):
    """
    Loop function that orders rendering players_temps hands facedown onto the
    screen. redraw_hand_nonvisble is used within this loop to actually do the
    rendering. This loop simply orders each hands location on the screen.

    O(m*n) runtime where m is the amount of players to be drawn and
    n is the size of the players hand. Since both of these sizes should be
    relatively small optimizing was considered negligible.
    """
    start_horz = 0
    start_vert = 0
    loop_iteration = 0
    # draw all active other hands in nice other places in the screen
    for player in players_temp:  # O(m*n)

        if len(player.hand) == 0:
            hand_size = card_width
        elif len(player.hand) > 7:
            hand_size = (80 * 7) + (card_width - 80)
        else:
            hand_size = (80 * len(player.hand)) + (card_width - 80)

        if loop_iteration == 1:
            start_horz = screen_width - hand_size

        elif loop_iteration > 1:
            start_vert = start_vert + card_height + 20
            start_horz = 0
            loop_iteration = 0

        redraw_hand_nonvisble(player, start_horz, start_vert)  # O(n)

        loop_iteration += 1


def redraw_screen(player_you, board, players_other):
    """
    Redraws the screen to its "normal" state.

    Renders the current players hand face up, the current card selected is
    raised, the most recentl played card on the board face up, and other
    players' hands face down.

    O(m*n) runtime where m is the amount of players to be drawn and
    n is the size of the players hand. Since both of these sizes should be
    relatively small optimizing was considered negligible.
    """
    # clear screen completely
    screen.fill(nice_one)

    # draw personal players hand should only be O(n) as player_you should
    # only be one person. n is the number of cards in player_you's hand
    for player in player_you:
        (player_dat, selected) = player
        redraw_hand_visble(player_dat, selected)  # O(n)

    # grab a list of all players excluding the currenly playing one
    players_temp = players_other[:]  # O(n)
    players_temp.remove(player_dat)  # O(n)

    # draw all players (excluding the currently playing player) hands facedown
    # an orderly fashion on the screen
    redraw_hand_nonvisble_loop(players_temp)  # O(m*n)

    # draw the top card on the board
    draw_top_stack_card(board)  # O(1)

    # refreshing the screen
    pygame.display.flip()  # O(1)?


def redraw_screen_menu_color(selected=None):
    """
    Draws a simple color menu with placeholder graphics.

    Function clears the top half of the screen and clears display of nonvisible
    hands while it runs.

    O(1) runtime as the number of colors is 4 thus the for loop only runs
    4 times thus being negligible
    """
    # zero input catch
    if selected is None:
        selected = 0

    # clear screen
    pygame.draw.rect(
        screen, nice_one, (0, 0, screen_width, int(600 * scale_y)), 0)

    # get a "middle" start postion for bliting cards
    start_pos = ((screen_width) // 2) - ((300 * 2 + card_width) // 2)

    # placeholders for color slection graphics
    card_g = game_classes.Card("green", "small_cards/green_0.png", None)
    card_b = game_classes.Card("blue", "small_cards/blue_0.png", None)
    card_y = game_classes.Card("yellow", "small_cards/yellow_0.png", None)
    card_r = game_classes.Card("red", "small_cards/red_0.png", None)

    color_array = [card_g, card_b, card_y, card_r]
    color_index = 0
    for card_c in color_array:  # O(4)
        card_c.rect = def_rect
        if color_index == selected:
            card_c.rect = card_c.rect.move(start_pos, 200)
        else:
            card_c.rect = card_c.rect.move(start_pos, 300)

        card_c.rect = card_c.rect.move(200 * color_index, 0)
        scale_card_blit(card_c.card_data, card_c.rect)

        color_index += 1


    # refresh the screen
    pygame.display.flip()


def redraw_screen_menu_target(players, selected=None):
    """
    Draws a simple menu with placeholder graphics (red number cards) that
    refrences a target player to use a card effect on. Thus function clears
    the top half of the screen and clears  display of nonvisible hands while it
    runs.

    O(n) runtime where n is the number of players that can be a proper target
    """

    # zero input catch
    if selected is None:
        selected = 0

    # clear screen (top half)
    pygame.draw.rect(
        screen, nice_one, (0, 0, screen_width, int(600 * scale_y)), 0)

    # get a "middle" start postion for bliting cards
    start_pos = ((screen_width) // 2) - \
        (200 * (len(players) - 1) + card_width) // 2

    target_index = 0
    for player in players:  # O(n)
        player_num = str(player.name[7])
        card_disp = game_classes.Card(
            "red", "small_cards/red_" + player_num + ".png", None)
        card_disp.rect = def_rect

        if target_index == selected:
            card_disp.rect = card_disp.rect.move(start_pos, 200)
        else:
            card_disp.rect = card_disp.rect.move(start_pos, 300)

        card_disp.rect = card_disp.rect.move(200 * target_index, 0)
        scale_card_blit(card_disp.card_data, card_disp.rect)

        target_index += 1

    # refresh the screen
    pygame.display.flip()


def draw_winners(winners):
    """
    Function that draws the winners in win placement from left to right.
    Left being the first winner and right being last place.

    O(n) runtime where n is the size of the list winners
    """
    # clear screen (top half)
    screen.fill(nice_one)
    global last_played
    last_played = []

    # get a "middle" start postion for bliting cards
    start_pos = ((screen_width) // 2) - \
        (200 * (len(winners) - 1) + card_width) // 2
    target_index = 0
    ok = 0
    for player in winners:  # O(n)
        player_num = str(player.name[7])
        if ok == 0:
            tp = 'Winner is player ' + str(player.name[7])
            ok += 1
            print(player)
        card_disp = game_classes.Card(
            "red", "small_cards/green_" + player_num + ".png", None)
        card_disp.rect = def_rect
        card_disp.rect = card_disp.rect.move(start_pos, 300)
        card_disp.rect = card_disp.rect.move(200 * target_index, 0)
        scale_card_blit(card_disp.card_data, card_disp.rect)
        font = pygame.font.Font('freesansbold.ttf', 38)
        text = font.render(tp, True, white)
        textRect = text.get_rect()
        textRect.center = (300, 400)
        screen.blit(text, textRect)
        target_index += 1



    # refresh the screen
    pygame.display.flip()
