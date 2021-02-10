import math
import time
import sys
import numpy as np
import pygame
from pygame.locals import *
from matplotlib import pyplot as plt

CHARS = '.,-~:;=!*#$@'
DONUT_WIDTH = 500
DONUT_HEIGHT = 500
CENTER = (DONUT_WIDTH / 2, DONUT_HEIGHT / 2)

RADIUS = 1   #donut thicknes
RADIUS_2 = 2 #donut diameter

ALFA_SPACING = 0.1
BETA_SPACING = 0.1

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)

rot_A = math.pi
rot_B = math.pi

viewer_to_donut_dist = 5
viewer_screen_dist = DONUT_WIDTH * viewer_to_donut_dist * 3/( 10 * (RADIUS + RADIUS_2))

# return clear frame to print donut in 
def get_clear_frame():
    return [list( ' ' for x in range(0, DONUT_WIDTH)) for y in range(0, DONUT_HEIGHT)]

def get_clear_Z_matrix():
    return [list( 0   for x in range(0, DONUT_WIDTH)) for y in range(0, DONUT_HEIGHT)]

def main( A, B):

    screen = pygame.display.set_mode((DONUT_WIDTH,DONUT_HEIGHT))

    while True:
        clearScreen(screen)

        # precalculations
        cosA = math.cos(A)
        sinA = math.sin(A)
        cosB = math.cos(B)
        sinB = math.sin(B) 

        output = get_clear_frame()
        Z_matrix = get_clear_Z_matrix()
        
        # Draw circles arount Y axis
        for alfa in np.arange(0, math.pi * 2 , ALFA_SPACING):
            
            cosAlfa = math.cos(alfa)
            sinAlfa = math.sin(alfa)

            # then spin them 
            for beta in np.arange(0, math.pi * 2, BETA_SPACING):
    
                cosBeta = math.cos(beta)
                sinBeta = math.sin(beta)

                circ_x = RADIUS_2 + RADIUS * cosAlfa
                circ_y = RADIUS * sinAlfa

                x = circ_x * ( cosB * cosBeta + sinA * sinB * sinBeta) - circ_y * cosA * sinB
                y = circ_x * ( sinB * cosBeta - sinA * cosB * sinBeta) - circ_y * cosA * cosB
                z = viewer_to_donut_dist + cosA * circ_x * sinBeta + circ_y * sinA 

                ooz = 1/z # "one over Z"
                xp = int(DONUT_WIDTH/2 + viewer_screen_dist * ooz * x)
                yp = int(DONUT_HEIGHT/2 + viewer_screen_dist * ooz * y)
                
                luminance = cosBeta * cosAlfa * sinB - cosA * cosAlfa * sinBeta - sinA * sinAlfa + cosB * (cosA * sinAlfa - cosAlfa * sinA * sinBeta)
                
                # print(luminance)
                # if luminance > 0:
                    # if ooz < Z_matrix[xp][yp] or Z_matrix[xp][yp] == 0:
                if ooz > Z_matrix[xp][yp]:
                    Z_matrix[xp][yp] = ooz 
                    luminance_indx = int(luminance * 8) 
                    # output[xp][yp] = CHARS[luminance_indx]
                    output[xp][yp] = '.'
            
        A += math.pi / 100
        B += math.pi / 100
        printOutput(screen, output)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

def clearScreen(screen):
    screen.fill(BLACK)

def printOutput(screen, output):

    for i, row in enumerate(output):
        for j, letter in enumerate(row):
            if letter != ' ':
                img = FONT.render(letter,True,WHITE)
                screen.blit(img,(i, j))

    pygame.display.update()
        
if __name__ == "__main__":

    pygame.init()
    FONT = pygame.font.SysFont(None, 15)

    main(rot_A, rot_B) 