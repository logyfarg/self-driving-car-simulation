import pygame
import sys
from car import Car
from brain import evolve_population, NUM_CARS
import random

pygame.init()
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Self-Driving Car Simulation")
clock = pygame.time.Clock()

# Simple wall map
walls = [
    pygame.Rect(200, 100, 600, 20),
    pygame.Rect(200, 680, 600, 20),
    pygame.Rect(200, 100, 20, 600),
    pygame.Rect(780, 100, 20, 600),
    pygame.Rect(400, 300, 200, 20),
    pygame.Rect(400, 500, 200, 20)
]

generation = 0
cars = [Car(WIDTH//2, HEIGHT//2) for _ in range(NUM_CARS)]

def draw_walls():
    for wall in walls:
        pygame.draw.rect(screen, (0, 0, 0), wall)

def reset_generation():
    global cars, generation
    generation += 1
    brains = evolve_population(cars)
    cars = [Car(WIDTH//2, HEIGHT//2, brain=brains[i]) for i in range(NUM_CARS)]

running = True
while running:
    clock.tick(60)
    screen.fill((255, 255, 255))
    draw_walls()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_dead = True
    for car in cars:
        if not car.dead:
            car.update(walls)
            all_dead = False
        car.draw(screen)

    if all_dead:
        reset_generation()

    pygame.display.flip()

pygame.quit()
sys.exit()
