import pygame
import math
from utils import get_sensor_data, rotate_point
from brain import NeuralNetwork

class Car:
    def __init__(self, x, y, brain=None):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 3
        self.size = 15
        self.rays = 5
        self.ray_length = 120
        self.dead = False
        self.fitness = 0
        self.color = (255, 0, 0)
        self.brain = brain or NeuralNetwork()
        self.sensor_data = []

    def update(self, walls):
        if self.dead:
            return

        inputs = get_sensor_data(self.x, self.y, self.angle, self.rays, self.ray_length, walls)
        self.sensor_data = inputs
        self.fitness += 1

        out = self.brain.forward(inputs)

        turn = out[0] * 2 - 1  # range [-1, 1]
        self.angle += turn * 5

        dx = math.cos(math.radians(self.angle)) * self.speed
        dy = math.sin(math.radians(self.angle)) * self.speed
        self.x += dx
        self.y += dy

        # Collision check
        car_rect = pygame.Rect(self.x - self.size, self.y - self.size, self.size*2, self.size*2)
        for wall in walls:
            if car_rect.colliderect(wall):
                self.dead = True
                break

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        angle_step = 180 / (self.rays - 1)
        for i, distance in enumerate(self.sensor_data):
            ray_angle = self.angle - 90 + i * angle_step
            end_x = self.x + math.cos(math.radians(ray_angle)) * distance
            end_y = self.y + math.sin(math.radians(ray_angle)) * distance
            pygame.draw.line(screen, (0, 255, 0), (self.x, self.y), (end_x, end_y), 2)
