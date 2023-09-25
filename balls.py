# imports
import pygame as pg
import math as m

# options
_fps = 60
_screen_size = (1000, 600)  #Default screen size
_center = (_screen_size[0] // 2, _screen_size[1] // 2)

_vector_mass = 1
_gravity = 40 * _vector_mass

_spring_stiffness = 150
_rest_length = 20
_damp_factor = 0.7

_pressure = 10000

# rendering options
_background_color = (0, 0, 0)

_text_color = (255, 255, 255)

_draw_points = True
_draw_springs = True

_point_color1 = (57, 255, 20)
_point_color2 = (57, 255, 20)
_spring_color = (57, 255, 20)  # Lime green

# circle options
_circle_radius = 100
_circle_points = 20

#compute the length of a vector
def magnitude(p):
    return m.sqrt((p[0] * p[0]) + (p[1] * p[1]))

#scale a vector to a magnitude of 1
def normalize(p):
    return (p[0] / magnitude(p), p[1] / magnitude(p))

#returns the dot product of two vectors
def dot(pa, pb):
    return pa[0] * pb[0] + pa[1] * pb[1]

#subtracts two vectors
def vector_difference(pa, pb):
    return (pa[0] - pb[0], pa[1] - pb[1])

#multiply a vector by a scalar
def vector_multiply(p, n): #where n is a floating point
    return (p[0] * n, p[1] * n)


def calculate_area(points):
    area = 0
    for i, point in enumerate(points):
        if i + 1 == len(points):
            area += (point[0][0] * points[0][0][1] - points[0][0][0] * point[0][1])
        else:
            area += (point[0][0] * points[i + 1][0][1] - points[i + 1][0][0] * point[0][1])
    return 0.5 * abs(area)

def build_circle(radius, points, screen_size):
    center = (screen_size[0] // 2, screen_size[1] // 10)
    initial_y = screen_size[1] // 4
    spacing = (m.pi * 2) / points
    positions = []
    for point in range(points):
        angle = spacing * point
        x = center[0] + (radius * m.cos(angle))
        y = center[1] + (radius * m.sin(angle)) + initial_y
        positions.append(([x, y], [0, 0], [0, 0], _vector_mass, [0, 0]))
    return positions


def move_circle(circle, offset_x, offset_y):
    for point in circle:
        point[0][0] += offset_x
        point[0][1] += offset_y

# initialize pygame
pg.init()
win = pg.display.set_mode(_screen_size) #win will be used as a reference to window
pg.display.set_caption("Softbody Engine")
clk = pg.time.Clock()

font = pg.font.Font('freesansbold.ttf', 20)

# create shape
circle = build_circle(_circle_radius, _circle_points, _screen_size)
springs = []
for i, point in enumerate(circle):
    if i + 1 == len(circle):
        springs.append((i, 0))
    else:
        springs.append((i, i + 1))

#Store variables outside game loop
user_lines = []
drawing = False
last_pos = None
mouse_position = (0,0)

# start game loop
run = True
pause = True
while run:
    # get delta time
    delta = clk.tick(_fps) / 400

    # events
    for event in pg.event.get():

        if event.type == pg.QUIT:
            run = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                pause = not pause

        elif event.type == pg.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = pg.mouse.get_pos()  # Capture the start position

        elif event.type == pg.MOUSEBUTTONUP:
            if drawing:
                end_pos = pg.mouse.get_pos()  # Capture the end position
                user_lines.append((start_pos, end_pos))  # Store the line
                drawing = False

    # create background effect based on _screen_size
    win.fill(_background_color)
    for i in range(20):
        pg.draw.circle(win, (_background_color[0] + i, _background_color[1] + i, _background_color[2] + i),_center, min(_screen_size) // 2 - (i * 50))

    #Move circle if move keys are pressed
    if pause:
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            move_circle(circle, -2, 0)
        if key[pg.K_d]:
            move_circle(circle, 2, 0)
        if key[pg.K_w]:
            move_circle(circle, 0, -2)
        if key[pg.K_s]:
            move_circle(circle, 0, 2)

   

    #update the forces on every spring
    for spring in springs:
        if pause == False:
            distance = magnitude(vector_difference(circle[spring[0]][0], circle[spring[1]][0]))
            spring_force = _spring_stiffness * (distance - _rest_length)
            direction = normalize(vector_difference(circle[spring[0]][0], circle[spring[1]][0]))
            vel_difference = vector_difference(circle[spring[0]][1], circle[spring[1]][1])
            total_force = dot(direction, vel_difference) * _damp_factor + spring_force

            normal = ((circle[spring[1]][0][1] - circle[spring[0]][0][1]),
                      -(circle[spring[1]][0][0] - circle[spring[0]][0][0]))

            circle[spring[0]][4][0] += ((_pressure * distance) / calculate_area(circle)) * normal[0]
            circle[spring[0]][4][1] += ((_pressure * distance) / calculate_area(circle)) * normal[1]
            circle[spring[1]][4][0] += ((_pressure * distance) / calculate_area(circle)) * normal[0]
            circle[spring[1]][4][1] += ((_pressure * distance) / calculate_area(circle)) * normal[1]

            circle[spring[0]][4][0] += vector_multiply(normalize(vector_difference(circle[spring[1]][0], circle[spring[0]][0])), total_force)[0]
            circle[spring[0]][4][1] += vector_multiply(normalize(vector_difference(circle[spring[1]][0], circle[spring[0]][0])), total_force)[1]
            circle[spring[1]][4][0] += vector_multiply(direction, total_force)[0]
            circle[spring[1]][4][1] += vector_multiply(direction, total_force)[1]

    # Draw the circle points
    for point in circle:
        if pause == False:
            point[2][0], point[2][1] = 0, 0  # reset force
            point[2][0] = point[4][0]  # add spring force and IGL
            point[2][1] = _gravity + point[4][1]  # add gravity and spring force and IGL

            # reset spring forces
            point[4][0], point[4][1] = 0, 0

            # add force to velocity
            point[1][0] += (point[2][0] * delta) / _vector_mass
            point[1][1] += (point[2][1] * delta) / _vector_mass

            # add velocity to position
            point[0][0] += point[1][0] * delta
            point[0][1] += point[1][1] * delta

            # Collision with the ground
            if point[0][1] > _screen_size[1]:
                point[0][1] = _screen_size[1]
                point[1][1] = 0
            # Collision with the walls
            if point[0][0] < 0:
                point[0][0] = 0
                point[1][0] = 0
            elif point[0][0] > _screen_size[0]:
                point[0][0] = _screen_size[0]
                point[1][0] = 0

        # Draw the point
        if _draw_points == True:
            pg.draw.circle(win, _point_color1, point[0], 5)
            pg.draw.circle(win, _point_color2, point[0], 3)

    # Draw the springs
    for spring in springs:
        if _draw_springs == True:
            pg.draw.line(win, _spring_color, circle[spring[0]][0], circle[spring[1]][0], 4)

    for line in user_lines:
        pg.draw.line(win, (255, 255, 255), line[0], line[1], 5)

    fps_counter = font.render(f'FPS: {round(clk.get_fps())}', True, _text_color)
    win.blit(fps_counter, (0, 0))

    if pause == True:
        paused = font.render('PAUSED', True, _text_color)
        win.blit(paused, (0, 25))

    # refresh window
    pg.display.flip()

# quit
pg.quit()
quit()
