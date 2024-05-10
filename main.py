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


# Function to generate all possible valid solutions using backtracking
def generate_solutions():
    solutions = []

    # Define the backtracking function
    def backtrack(m_left, c_left, m_right, c_right, path):
        # Base case: all missionaries and cannibals are on the right side
        if m_left == 0 and c_left == 0:
            solutions.append(path[:])
            return

        # Generate all possible moves
        moves = []
        if m_left > 0:
            moves.append(('M',))
        if c_left > 0:
            moves.append(('C',))
        if m_left > 1:
            moves.append(('M', 'M'))
        if c_left > 1:
            moves.append(('C', 'C'))
        if m_left > 0 and c_left > 0:
            moves.append(('M', 'C'))

        # Apply each move and recursively call the function
        for move in moves:
            m, c = m_left, c_left
            for entity in move:
                if entity == 'M':
                    m -= 1
                    m_right += 1
                elif entity == 'C':
                    c -= 1
                    c_right += 1
            if (m_right >= c_right or m_right == 0) and (
                    3 - m_right >= 3 - c_right or 3 - m_right == 0):
                backtrack(m, c, m_right, c_right, path + [move])
            for entity in move:
                if entity == 'M':
                    m += 1
                    m_right -= 1
                elif entity == 'C':
                    c += 1
                    c_right -= 1

    # Start backtracking from the initial state
    backtrack(3, 3, 0, 0, [])
    return solutions


# Generate all possible solutions
solutions = generate_solutions()

# Select a random solution to use in the game
chosen_solution = [('C', 'C'),
                   ('C',),
                   ('C', 'C'),
                   ('C',),
                   ('M', 'M'),
                   ('M', 'C'),
                   ('M', 'M'),
                   ('C',),
                   ('C', 'C'),
                   ('M',),
                   ('M', 'C'), []]
print("Chosen Solution:", chosen_solution)


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


def game_loop():
    global boat_cargo
    running = True
    for move in chosen_solution:
        if not running:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        draw_world()
        pygame.display.flip()
        time.sleep(2)  # Visibility delay

        if not boat_cargo:  # Load the boat if it's empty
            boat_cargo = list(move)
            move_boat()
        else:  # Move the boat if it's loaded
            move_boat()

    # Game over message
    if missionaries_left == 0 and cannibals_left == 0:
        print("Congratulations! You've successfully transported all missionaries and cannibals.")
    elif (missionaries_left > 0 and cannibals_left > missionaries_left) or (
            missionaries_right > 0 and cannibals_right > missionaries_right):
        print("Game over! Cannibals ate the missionaries.")

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    game_loop()
