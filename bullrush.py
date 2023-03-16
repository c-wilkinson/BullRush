import random
import pygame
from pygame.locals import *

score = 0
lives = 3
high_score = 0

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Bull Rush')

# Define game objects
bull_image = pygame.image.load('bull.png')
bull_image = pygame.transform.scale(bull_image, (50, 50))
bull_rect = bull_image.get_rect()
bull_rect.center = (screen.get_width() // 2, screen.get_height() // 2)

good_image = pygame.image.load('good.png')
good_image = pygame.transform.scale(good_image, (100, 100))
good_rect = good_image.get_rect()

bad_image = pygame.image.load('bad.png')
bad_image = pygame.transform.scale(bad_image, (100, 100))
bad_rect = bad_image.get_rect()

# Define item variables
item_rects = []
item_states = []
item_spawn_time = 0

# Define the game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
        elif event.type == FINGERDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            start_pos = event.dict['pos']
            pulling = True
        elif event.type == FINGERUP or event.type == pygame.MOUSEBUTTONUP:
            end_pos = event.dict['pos']
            pulling = False
            charge_vector = (start_pos[0] - end_pos[0], start_pos[1] - end_pos[1])
            max_charge_length = screen.get_width() * 0.4
            charge_length = min(max_charge_length, max(0, int(pygame.math.Vector2(charge_vector).length())))
            charge_direction = pygame.math.Vector2(charge_vector).normalize()
            bull_rect.move_ip(charge_direction * charge_length)

    # Spawn new items every 0.5 seconds
    time_elapsed = pygame.time.get_ticks() - item_spawn_time
    if time_elapsed > 500:
        item_type = random.choice(['good', 'bad'])
        if item_type == 'good':
            item_rect = good_rect.copy()
        elif item_type == 'bad':
            item_rect = bad_rect.copy()
        else:
            item_rect = None

        if item_rect:
            item_rect.center = (random.randint(screen.get_width() // 4, screen.get_width() * 3 // 4), 
                                random.randint(screen.get_height() // 4, screen.get_height() * 3 // 4))
            item_rects.append(item_rect)
            item_states.append('alive')
            item_spawn_time = pygame.time.get_ticks()

    # Draw the game objects
    screen.fill((255, 255, 255))
    screen.blit(bull_image, bull_rect)
    for i in range(len(item_rects)):
        if item_states[i] == 'alive':
            screen.blit(good_image if item_type == 'good' else bad_image, item_rects[i])

    # Check for collision with item
    for i in range(len(item_rects)):
        if item_states[i] == 'alive' and bull_rect.colliderect(item_rects[i]):
            item_states[i] = 'dead'
            if item_type == 'good':
                print('You knocked over a good item and earned 10 points!')
                score += 10
            elif item_type == 'bad':
                print('You collided with a bad item and lost a life!')
                lives -= 1
        # Update the score and lives
        print(f'Score: {score}    Lives: {lives}')
        if lives == 0:
            print('Game over!')
            if score > high_score:
                high_score = score
                print(f'New high score: {high_score}')
            else:
                print(f'High score: {high_score}')
            score = 0
            lives = 3

    # Update the display
    pygame.display.update()