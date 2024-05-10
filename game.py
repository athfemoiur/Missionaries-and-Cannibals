import pygame
import sys
import time
import random

# Constants for the game
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Missionaries and Cannibals")
clock = pygame.time.Clock()

# Game state
missionaries_left = 3
cannibals_left = 3
missionaries_right = 0
cannibals_right = 0
boat_position = 'left'
boat_cargo = []

def draw_world():
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (0, HEIGHT // 2 - 30, WIDTH, 60))

    # Draw entities on the banks
    for i in range(missionaries_left):
        pygame.draw.circle(screen, YELLOW, (50 + i * 30, HEIGHT // 2 - 100), 15)
    for i in range(cannibals_left):
        pygame.draw.circle(screen, RED, (50 + i * 30, HEIGHT // 2 - 50), 15)
    for i in range(missionaries_right):
        pygame.draw.circle(screen, YELLOW, (WIDTH - 50 - i * 30, HEIGHT // 2 - 100), 15)
    for i in range(cannibals_right):
        pygame.draw.circle(screen, RED, (WIDTH - 50 - i * 30, HEIGHT // 2 - 50), 15)

    # Draw the boat
    boat_x = 100 if boat_position == 'left' else WIDTH - 150
    pygame.draw.rect(screen, GREEN, (boat_x, HEIGHT // 2 - 20, 50, 20))
    # Draw entities in the boat
    for i, entity in enumerate(boat_cargo):
        color = YELLOW if entity == 'M' else RED
        pygame.draw.circle(screen, color, (boat_x + 15 + i * 20, HEIGHT // 2 - 10), 10)

def move_boat():
    global boat_position, boat_cargo, missionaries_left, cannibals_left, missionaries_right, cannibals_right
    # Update positions after the boat reaches the other side
    if boat_position == 'left':
        for entity in boat_cargo:
            if entity == 'M':
                missionaries_left -= 1
                missionaries_right += 1
            elif entity == 'C':
                cannibals_left -= 1
                cannibals_right += 1
        boat_position = 'right'
    else:
        for entity in boat_cargo:
            if entity == 'M':
                missionaries_right -= 1
                missionaries_left += 1
            elif entity == 'C':
                cannibals_right -= 1
                cannibals_left += 1
        boat_position = 'left'
    boat_cargo = []  # Clear the boat cargo after moving

def choose_cargo(entity):
    global boat_cargo, missionaries_left, cannibals_left, missionaries_right, cannibals_right
    if len(boat_cargo) < 2:
        if boat_position == 'left':
            if entity == 'M' and missionaries_left > 0:
                boat_cargo.append('M')
                return True
            elif entity == 'C' and cannibals_left > 0:
                boat_cargo.append('C')
                return True
        else:
            if entity == 'M' and missionaries_right > 0:
                boat_cargo.append('M')
                return True
            elif entity == 'C' and cannibals_right > 0:
                boat_cargo.append('C')
                return True
    return False

def test_game_over():
    # Check for game over condition
    if (missionaries_left > 0 and cannibals_left > missionaries_left) or (missionaries_right > 0 and cannibals_right > missionaries_right):
        print("Game over! Cannibals ate the missionaries.")
        return True
    return False

def test_win():
    # Check for win condition
    if missionaries_left == 0 and cannibals_left == 0:
        print("Congratulations! You've successfully transported all missionaries and cannibals.")
        return True
    return False

def game_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if len(boat_cargo) >= 1:  # Move the boat if it's fully loaded
                        move_boat()
                        if test_game_over() or test_win():
                            running = False
                elif event.key == pygame.K_m:
                    choose_cargo('M')
                elif event.key == pygame.K_c:
                    choose_cargo('C')

        draw_world()
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
