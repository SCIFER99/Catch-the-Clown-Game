# By: Tim Tarver
# Catch The Clown Game

import pygame
import random

# Initialize Game

pygame.init()

# Set Display Surface Parameters

window_width = 945
window_height = 600
display_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Catch The Clown!")

# Set Frames per Second

frames_per_second = 60
clock = pygame.time.Clock()

# Set Game Values

player_starting_lives = 5
clown_starting_velocity = 5
clown_acceleration = 1

score = 0
player_lives = player_starting_lives

clown_velocity = clown_starting_velocity
clown_dx = random.choice([-1, 1])
clown_dy = random.choice([-1, 1])

# Create Colors of the Game

blue = (1, 175, 209)
yellow = (248, 231, 28)

# Create the Fonts of the Game

font = pygame.font.Font("Franxurter.ttf", 32)

# Set Text of the Game

title_text = font.render("Catch The Clown!", True, blue)
title_rectangle = title_text.get_rect()
title_rectangle.topleft = (50, 10)

score_text = font.render("Score:" + str(score), True, yellow)
score_rectangle = score_text.get_rect()
score_rectangle.topright = (window_width - 50, 10)

lives_text = font.render("Lives:" + str(player_lives), True, yellow)
lives_rectangle = lives_text.get_rect()
lives_rectangle.topright = (window_width - 50, 50)

game_over = font.render("Game Over Cuh!", True, blue, yellow)
game_over_rect = game_over.get_rect()
game_over_rect.center = (window_width // 2, window_height // 2)

continue_text = font.render("Click Anywhere to play again!", True, yellow, blue)
continue_rect = continue_text.get_rect()
continue_rect.center = (window_width // 2, window_height // 2 + 64)

# Set up Sounds and Music for the Game

click_sound = pygame.mixer.Sound("click_sound.wav")
miss_sound = pygame.mixer.Sound("miss_sound.wav")
pygame.mixer.music.load("ctc_background_music.wav")

# Set up Visuals for the Game

background_image = pygame.image.load("background.png")
background_rectangle = background_image.get_rect()
background_rectangle.topleft = (0, 0)
clown_image = pygame.image.load("clown.png")
clown_rectangle = clown_image.get_rect()
clown_rectangle.center = (window_width // 2, window_height // 2)

# The Main Game Loop

pygame.mixer.music.play(-1, 0.0)

running = True
while running:

    # Check to see if the user wants to quit
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False

        # A click is made
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]

            # The clown was clicked
            if clown_rectangle.collidepoint(mouse_x, mouse_y):
                click_sound.play()
                score += 1
                clown_velocity += clown_acceleration

                # Move the clown in a new direction
                previous_dx = clown_dx
                previous_dy = clown_dy
            
                while (previous_dx == clown_dx and previous_dy == clown_dy):
                    clown_dx = random.choice([-1, 1])
                    clown_dy = random.choice([-1, 1])

            # We missed the Clown
            else:
                miss_sound.play()
                player_lives -= 1
            

    # Move the Clown
    clown_rectangle.x += clown_dx * clown_velocity
    clown_rectangle.y += clown_dy * clown_velocity

    # Bounce the Clown off the Edges of the Display

    if clown_rectangle.left <= 0 or clown_rectangle.right >= window_width:
        clown_dx = -1 * clown_dx
    if clown_rectangle.top <= 0 or clown_rectangle.bottom >= window_height:
        clown_dy = -1 * clown_dy

    # Update HUD
    score_text = font.render("Score: " + str(score), True, yellow)
    lives_text = font.render("Lives: " + str(player_lives), True, yellow)

    # Check for Game Over
    if player_lives == 0:
        display_surface.blit(game_over, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()

        # Pause the game until the Player clicks then reset the Game
        pygame.mixer.music.stop()
        is_paused = True
        
        while is_paused:
            
            for event in pygame.event.get():

                # The player wants to play again
                if event.type == pygame.MOUSEBUTTONDOWN:
                    score = 0
                    player_lives = player_starting_lives
                    clown_rectangle.center = (window_width // 2, window_height // 2)
                    clown_velocity = clown_starting_velocity
                    clown_dx = random.choice([-1, 1])
                    clown_dy = random.choice([-1, 1])

                    pygame.mixer.music.play(-1, 0.0)
                    is_paused = False

                # The player wants to Quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
            

    # Blit the background
    display_surface.blit(background_image, background_rectangle)

    # Blit HUD
    display_surface.blit(title_text, title_rectangle)
    display_surface.blit(score_text, score_rectangle)
    display_surface.blit(lives_text, lives_rectangle)

    # Blit Assets
    display_surface.blit(clown_image, clown_rectangle)

    #Update display and tick clock
    pygame.display.update()
    clock.tick(frames_per_second)
    

# End the Game
pygame.quit()
