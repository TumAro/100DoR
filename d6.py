import pygame, pymunk, math
import pymunk.pygame_util
from d6_objects import *
from d6_sat import SATheorem

# init pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, 0)      # no gravity for top-down view
drawOptions = pymunk.pygame_util.DrawOptions(screen)

space.add(*bodies, *shapes)
vel = 300
running = True

red = (255, 0, 0)
green = (0, 255, 0)

def movement(body, speed=vel):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
        # Manual control
        if keys[pygame.K_LEFT]:
            botBody.velocity = (-vel, 0)
        if keys[pygame.K_RIGHT]:
            botBody.velocity = (vel, 0)
        if keys[pygame.K_UP]:
            botBody.velocity = (0, -vel)
        if keys[pygame.K_DOWN]:
            botBody.velocity = (0, vel)
    elif botBody.velocity == (0, 0):
        # If stopped and not manually controlling, restart autonomous movement
        botBody.velocity = (vel, 0)

# ====================
def avoidObstacle(botBody, shapes, botShape, sensorRange=10):
    pos = botBody.position
    vel = botBody.velocity

    # normalise the direction vec
    speed = math.sqrt(vel[0]**2 + vel[1]**2)
    if speed < 1:
        botBody.velocity = (vel, 0)
        return
    
    dirX, dirY = vel[0]/speed, vel[1]/speed
    
    # creating a sensor point
    sensors = [
        (pos[0] + dirX*sensorRange*0.25, pos[1] + dirY*sensorRange*0.25),  # Forward
        (pos[0] + dirX*sensorRange*0.2 - dirY*sensorRange*0.25, 
         pos[1] + dirY*sensorRange*0.2 + dirX*sensorRange*0.25),  # Forward-Left
        (pos[0] + dirX*sensorRange*0.2 + dirY*sensorRange*0.25, 
         pos[1] + dirY*sensorRange*0.2 - dirX*sensorRange*0.25)   # Forward-Right
    ]
    # Draw sensors for debugging (small circles)
    for sensor in sensors:
        pygame.draw.circle(screen, (255, 0, 255), sensor, 4)
    
    # check for collision with any sensor
    for sensor in sensors:
        for shape in shapes:
            if shape != botShape:
                # Create a small square sensor
                tempSensor = pymunk.Poly(pymunk.Body(), [
                    (sensor[0]-5, sensor[1]-5), 
                    (sensor[0]+5, sensor[1]-5),
                    (sensor[0]+5, sensor[1]+5),
                    (sensor[0]-5, sensor[1]+5)
                ])
                
                # Convert shape vertices to world coordinates
                shapeVert = [shape.body.local_to_world(v) for v in shape.get_vertices()]    
                tempShape = pymunk.Poly(pymunk.Body(), shapeVert)

                if SATheorem(tempSensor, tempShape):
                    # Obstacle detected - turn 90 degrees
                    botBody.velocity = (-dirY * speed, dirX * speed)
                    return True
    
    return False

# ====================

color = green
while running:
    # checks for closing = event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Change to manual control if space pressed
                botBody.velocity = (0, 0)

    
    movement(botBody, vel)
    # Draw physics objects
    space.step(1/60)
    screen.fill("silver")
    space.debug_draw(drawOptions)

    collision = avoidObstacle(botBody=botBody, shapes=shapes, botShape=botShape, sensorRange=150)
    color = red if collision else green

    # Keep robot on screen
    pos = botBody.position
    if pos.x < 0 or pos.x > 1280 or pos.y < 0 or pos.y > 720:
        # Bounce off screen edges
        vel_x, vel_y = botBody.velocity
        if pos.x < 0 or pos.x > 1280:
            botBody.velocity = (-vel_x, vel_y)
        if pos.y < 0 or pos.y > 720:
            botBody.velocity = (vel_x, -vel_y)

    # draw the bot
    vertices = [botBody.local_to_world(v) for v in botVert]
    pygame.draw.polygon(screen, color, vertices)

    # update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
