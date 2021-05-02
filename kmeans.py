import pygame
import math
from random import randint
import numpy as np
from sklearn.cluster import KMeans

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))

pygame.init()

screen = pygame.display.set_mode((1200, 700))

pygame.display.set_caption('kmens visualization')

running = True

clock = pygame.time.Clock()

BACKGROUND = (214, 214, 214)
BACKGROUND_PANEL = (249, 255, 230)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (147, 153, 35)
PURPLE = (255,0,255)
SKY = (0,255,255)
ORANGE = (255,125,25)
GRAPE = (100,25,125)
GRASS = (55,155,65)

COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, SKY, ORANGE, GRAPE, GRASS]

font = pygame.font.SysFont('sans', 40)
font_small = pygame.font.SysFont('sans', 20)

text_plus = font.render('+', True, WHITE)
text_minus = font.render('-', True, WHITE)
text_run = font.render("Run", True, WHITE)
text_random = font.render("Random", True, WHITE)
text_algorithm = font.render("Algorithm", True, WHITE)
text_reset = font.render("Reset", True, WHITE)

k = 0
error = 0
points = []
clusters = []
labels = []

while running:
    clock.tick(60)
    screen.fill(BACKGROUND)
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # draw interface
    # draw panel

    pygame.draw.rect(screen, BLACK, (50, 50, 700, 500))
    pygame.draw.rect(screen, BACKGROUND_PANEL, (55, 55, 690, 490))

    # draw k button +
    pygame.draw.rect(screen, BLACK, (850, 50, 50, 50))
    screen.blit(text_plus, (860, 50))

    # K button -
    pygame.draw.rect(screen, BLACK, (950,50,50,50))
    screen.blit(text_minus, (960,50))

	# K value
    text_k = font.render("K = " + str(k), True, BLACK)
    screen.blit(text_k, (1050,50))

    # run button
    pygame.draw.rect(screen, BLACK, (850,150,150,50))
    screen.blit(text_run, (900,150))

    # random button
    pygame.draw.rect(screen, BLACK, (850,250,200,50))
    screen.blit(text_random, (850,250))

    # Reset button
    pygame.draw.rect(screen, BLACK, (850,550,150,50))
    screen.blit(text_reset, (850,550))	

    # Algorithm button
    pygame.draw.rect(screen, BLACK, (850,450,200,50))
    screen.blit(text_algorithm, (850,450))	

    # draw mouse position when mouse is in panel
    if 50 < mouse_x < 750 and 50 < mouse_y < 550:
        text_mouse = font_small.render("(" + str(mouse_x - 50) + "," + str(mouse_y - 50) + ")", True, BLACK)
        screen.blit(text_mouse, (mouse_x + 10, mouse_y))

    # end draw interface

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # create point on panel
            if 50 < mouse_x < 750 and 50 < mouse_y < 550:
                point = [mouse_x, mouse_y]
                points.append(point)

            # Change K button +
            if 850 < mouse_x < 900 and 50 < mouse_y < 100:
                if k < 8:
                    k = k + 1

            # Change K button -
            if 950 < mouse_x < 1000 and 50 < mouse_y < 100:
                if k > 0:
                    k -= 1

            # Run button
            if 850 < mouse_x < 1000 and 150 < mouse_y < 200:
                labels = []

                if clusters == []:
                    continue

                for p in points:
                    distance_to_clusters = []
                    
                    for c in clusters:
                        distance_to_clusters.append(distance(p, c))
                    
                    labels.append(distance_to_clusters.index(min(distance_to_clusters)))

                # update clusters
                for i in range(k):
                    sum_x = 0
                    sum_y = 0
                    count = 0
                    for j in range(len(points)):
                        if labels[j] == i:
                            sum_x += points[j][0]
                            sum_y += points[j][1]
                            count += 1
                    
                    if (count):        
                        clusters[i][0] = sum_x / count
                        clusters[i][1] = sum_y / count

            # Random button
            if 850 < mouse_x < 1000 and 250 < mouse_y < 300:
                labels = []
                clusters = []
                for i in range(k):
                    clusters.append([randint(50, 700), randint(50, 500)])

            # Reset button
            if 850 < mouse_x < 1000 and 550 < mouse_y < 600:
                k = 0
                error = 0
                points = []
                clusters = []
                labels = []


            # Algorithm 
            if 850 < mouse_x < 1000 and 450 < mouse_y < 500:
                kmeans = KMeans(n_clusters=k).fit(points)
                labels = np.array(kmeans.predict(points)).tolist()
                clusters = kmeans.cluster_centers_

    # draw point
    for i, point in enumerate(points):
        pygame.draw.circle(screen, BLACK, (point[0], point[1]), 6)

        if labels and (i < len(labels)):
            pygame.draw.circle(screen, COLORS[labels[i]], (point[0], point[1]), 5)
        else:
            pygame.draw.circle(screen, WHITE, (point[0], point[1]), 5)

    # draw cluster
    for i in range(len(clusters)):
        pygame.draw.circle(screen, COLORS[i], (clusters[i][0], clusters[i][1]), 10)

    error = 0

    # display error
    if labels != []:
        for i in range(len(labels)):
            error += distance(points[i], clusters[labels[i]])
        
        # Error text
        text_error = font.render("Error = " + str(int(error)), True, BLACK)
        screen.blit(text_error, (850,350))

    pygame.display.flip()

pygame.quit()