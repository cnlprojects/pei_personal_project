import pygame
import time
import random

# Global variables are not the best way to declare 
# variables in Python but it's OK for teaching purposes

def init_game_colors():
    global white
    global yellow
    global black
    global red
    global green
    global blue

    white = (255,255,255)
    yellow = (255,255,102)
    black = (0,0,0)
    red = (213,50,80)
    green = (0,255,0)
    blue = (50,153,213)


def init_snake_properties():
    global snake_block_size
    global snake_speed
    global high_score
    global current_score
    global bite_sound
    global bomb_sound

    snake_block_size = 10
    snake_speed = 10
    high_score = 0
    current_score = 0

    bite_sound = pygame.mixer.Sound("resources\\crunch.wav")
    bomb_sound = pygame.mixer.Sound("resources\\bomb_exploding.wav")


def init_display_size(width_value, height_value):
    global display_width
    global display_height

    display_width = width_value
    display_height = height_value


def init_pygame_display(width_value, height_value, caption_value):
    global main_display

    main_display = pygame.display.set_mode((width_value, height_value))
    pygame.display.set_caption(caption_value)


def init_pygame_clock():
    # Object to help track time in the game
    global clock
    clock = pygame.time.Clock()


def init_pygame_fonts():
    global message_font_style
    global score_font_style

    message_font_style = pygame.font.SysFont("arial",25)
    score_font_style  = pygame.font.SysFont("arial",20)


def screen_message(message, color):
    next_line = 0
    for m in message:
        mesg = message_font_style.render(m, True, color)
        mesg = message_font_style.render(m, True, color)
        main_display.blit(mesg, [(display_width/2 - len(m)*5), (display_height/len(message) + next_line)])
        next_line += 30


def game_score(score):
    global current_score

    current_score = score
    value = score_font_style.render("Score: " + str(score), True, yellow)
    main_display.blit(value, [0,0])


def set_game_high_score():
    global high_score
    high_score_color = yellow

    if current_score >= high_score:
        high_score = current_score
        if high_score != 0:
            high_score_color = red

    value = score_font_style.render("High Score: " + str(high_score), True, high_score_color)
    main_display.blit(value, [0,20])


def draw_snake(snake_block, snake_list):
    count_snake_part = 0
    c1 = None
    # This will help to draw the snake in the correct order to add new colors in the body
    reversed_body = reversed(snake_list) if snake_list is not None else snake_list

    for x in reversed_body:
        if count_snake_part%2 == 0:
            c1 = black
        elif count_snake_part%3 == 0:
            c1 = red
        else:
            c1 = white
        pygame.draw.rect(main_display, c1, [x[0], x[1], snake_block, snake_block])
        count_snake_part+=1


def generate_random_food_position():
    global food_pos_x
    global food_pos_y

    food_pos_x = round(random.randrange(left_border_limit, right_border_limit - snake_block_size) / 10.0) * 10.0
    food_pos_y = round(random.randrange(upper_border_limit, bottom_border_limit - snake_block_size) / 10.0) * 10.0


def init_gaming_control_logic():
    global game_over
    global game_lost
    global snake_pos_x
    global snake_pos_y
    global snake_pos_x_delta
    global snake_pos_y_delta
    global snake_body
    global snake_length
    global current_score
    global last_direction

    game_over = False
    game_lost = False
    
    snake_pos_x = display_width / 2
    snake_pos_y = display_height / 2
    
    snake_pos_x_delta = 0
    snake_pos_y_delta = 0

    snake_body = []
    snake_length = 1

    current_score = 0

    last_direction = 'START'

    generate_random_food_position()

def game_lost_cont_quit():
    global game_over
    global game_lost

    # If you lost the game it'll wait until you decide to continue or quit
    if game_lost == True:
        pygame.mixer.Sound.play(bomb_sound)
        main_display.blit(background_image, (0, 0))
        screen_message(["You lost!", "Press Q to Quit or C to Play Again"], red)
        game_score(snake_length - 1)
        set_game_high_score()
        draw_border(display_width, display_height, 45, 4)
        pygame.display.update()

    while game_lost == True:
        # Get the Pygame events and check for the keys to continue or quit
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q:
                    game_over = True
                    game_lost = False
                if event.key==pygame.K_c:
                    game_over = False
                    game_lost = False
                    init_gaming_control_logic()
            if event.type==pygame.QUIT:
                game_over = True
                game_lost = False


def move_snake(key_pressed_event):
    global snake_pos_x_delta
    global snake_pos_y_delta
    global snake_block_size
    global last_direction

    # The direction rule is you can turn only 90 degres
    if key_pressed_event.key == pygame.K_LEFT and last_direction != 'RIGHT':
        snake_pos_x_delta = -snake_block_size
        snake_pos_y_delta = 0
        last_direction = 'LEFT'
    elif key_pressed_event.key == pygame.K_RIGHT and last_direction != 'LEFT':
        snake_pos_x_delta = snake_block_size
        snake_pos_y_delta = 0
        last_direction = 'RIGHT'
    elif key_pressed_event.key == pygame.K_UP and last_direction != 'DOWN':
        snake_pos_x_delta = 0
        snake_pos_y_delta = -snake_block_size
        last_direction = 'UP'
    elif key_pressed_event.key == pygame.K_DOWN and last_direction != 'UP':
        snake_pos_x_delta = 0
        snake_pos_y_delta = snake_block_size
        last_direction = 'DOWN'


def init_border_limits(screen_width, screen_height, header_height, line_width):
    global left_border_limit
    global upper_border_limit
    global right_border_limit
    global bottom_border_limit
    global header_height_limit
    global line_width_limit

    left_border_limit = 0 + line_width
    upper_border_limit = header_height + line_width
    right_border_limit = screen_width - line_width
    bottom_border_limit = screen_height - line_width

    header_height_limit = header_height
    line_width_limit = line_width


def draw_border(screen_width, screen_height, header_height, border_line_width):
    lines = [(0 + border_line_width/2, header_height), 
             (screen_width - border_line_width/2, header_height),
             (screen_width - border_line_width/2, header_height), 
             (screen_width - border_line_width/2, screen_height - border_line_width/2),
             (screen_width - border_line_width/2, screen_height - border_line_width/2), 
             (0 + border_line_width/2, screen_height - border_line_width/2)]
    pygame.draw.lines(main_display, white, True, lines, border_line_width)


def load_background_image():
    global background_image
    background_image = pygame.image.load("resources\\bg03.png")


# Main application Entry Point
if __name__ == '__main__':
    try:
        # Initialize Pygame 
        pygame.init()

        # Initialize Snake Properties
        init_snake_properties()

        # Initialize game colors
        init_game_colors()

        # Initialize game display size
        init_display_size(800, 600)

        # Initialize Border Limits
        init_border_limits(display_width, display_height, 45, 4)

        # Initialize Pygame Display
        init_pygame_display(display_width, display_height, 'Sea Snake Game Project')

        # Initialize Pygame clock object
        init_pygame_clock()

        # Initialize Fonts
        init_pygame_fonts()
        
        # Load background
        load_background_image()

        # Start game and init game cycle logic
        init_gaming_control_logic()

        # Play until game over
        while not game_over:
            game_lost_cont_quit()

            # Check the keys pressed by the user
            for event in pygame.event.get():
                # If the user click in the close window button
                if event.type==pygame.QUIT:
                    game_over=True
                
                # If the user pressed a key
                if event.type==pygame.KEYDOWN:
                    move_snake(event)

            # Check if the snake hit the screen limits
            if (snake_pos_x + snake_block_size) >= right_border_limit or snake_pos_x < left_border_limit or (snake_pos_y + snake_block_size) >= bottom_border_limit or snake_pos_y < upper_border_limit:
                game_lost = True
            else:
                # Set the snake head new position based on the key pressed above
                snake_pos_x += snake_pos_x_delta
                snake_pos_y += snake_pos_y_delta
                snake_head = []
                snake_head.append(snake_pos_x)
                snake_head.append(snake_pos_y)
                snake_body.append(snake_head)
                load_background_image()
                main_display.blit(background_image, (0, 0))

                # Draw snake food on screen
                pygame.draw.rect(main_display, "red4", [food_pos_x, food_pos_y, snake_block_size, snake_block_size])
                draw_border(display_width, display_height, 45, 4)

                # Adjust snake body
                if len(snake_body) > snake_length:
                    del snake_body[0]

                # Check if snake head hit the snake body
                for snake_body_part in snake_body[:-1]:
                    if snake_body_part == snake_head:
                        game_lost = True

                # Draw snake and score
                draw_snake(snake_block_size, snake_body)
                game_score(snake_length - 1)
                set_game_high_score()
                pygame.display.update()

                # Check if snake head hit the snake food
                if snake_pos_x == food_pos_x and snake_pos_y == food_pos_y:
                    pygame.mixer.Sound.play(bite_sound)
                    generate_random_food_position()
                    snake_length += 1
                    
                # Keep the game speed
                clock.tick(snake_speed)

    except Exception as e:
        print(str(e))
    finally:
        # If it's game over
        pygame.quit()
