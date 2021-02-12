import math
import time
import os
import sys
import numpy as np
import pygame
from pygame.locals import *
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

CHARS = '.,-~:;=!*#$@'
DONUT_WIDTH = 300
DONUT_HEIGHT = 300
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

clear = lambda: os.system('cls')

# return clear frame to print donut in 
def get_clear_frame():
    return [list( ' ' for x in range(0, DONUT_WIDTH)) for y in range(0, DONUT_HEIGHT)]

def get_clear_Z_matrix():
    return [list( 0   for x in range(0, DONUT_WIDTH)) for y in range(0, DONUT_HEIGHT)]

def main( A, B):

    screen = pygame.display.set_mode((DONUT_WIDTH,DONUT_HEIGHT))

    min_luminance = 20
    max_luminance = 0

    while True:
        
        clearScreen(screen)
        
        # precalculations
        cosA = math.cos(A)
        sinA = math.sin(A)
        cosB = math.cos(B)
        sinB = math.sin(B) 

        output = get_clear_frame()
        Z_matrix = get_clear_Z_matrix()
        tempFlatMatrix = get_clear_Z_matrix()
        
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
                y = circ_x * ( sinB * cosBeta - sinA * cosB * sinBeta) + circ_y * cosA * cosB
                z = viewer_to_donut_dist + cosA * circ_x * sinBeta + circ_y * sinA 

                ooz = 1/z # "one over Z"
                xp = int(DONUT_WIDTH/2 + viewer_screen_dist * ooz * x)
                yp = int(DONUT_HEIGHT/2 + viewer_screen_dist * ooz * y)
                
                
                # custom
                luminance = -cosA * cosAlfa * sinBeta - sinA * sinAlfa
                
                if luminance > max_luminance: max_luminance = luminance
                if luminance < min_luminance: min_luminance = luminance

                if luminance > 0:
                    if ooz > Z_matrix[xp][yp]:
                        Z_matrix[xp][yp] = ooz 

                        #luminance_indx = getLuminanceIndex(min_luminance, max_luminance, luminance)
                        luminance_indx = int(luminance * 8) 
                        output[xp][yp] = CHARS[luminance_indx]
                        
        A += math.pi / 100
        B += math.pi / 100

        printOutput(screen, output, tempFlatMatrix)
        # printOutputConsole(output)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

def getLuminanceIndex(min_l, max_l, l):
    diff = max_l - min_l
    if diff > 0:
        return int ((len(CHARS) * (l - min_l)) / ( max_l - min_l )) - 1
    else:
        return 1
    

def clearScreen(screen):
    screen.fill(BLACK)

def printOutputConsole(output):
    clear()
    for row in output:
        print(' '.join(row))

def printOutput(screen, output, Z_matrix):
    for i, row in enumerate(output):
        for j, letter in enumerate(row):
            if letter != ' ':
                # b = int(255 / Z_matrix[i][j])
                # pygame.draw.rect(screen, (b,b,b), pygame.Rect(i,j,10,10))
                img = FONT.render(letter,True,WHITE)
                screen.blit(img,(i, j))

    pygame.display.update()
        
if __name__ == "__main__":

    pygame.init()
    FONT = pygame.font.SysFont(None, 15)

    main(rot_A, rot_B) 