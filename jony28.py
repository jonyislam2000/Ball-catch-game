from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import math
import sys
import time
WIDTH, HEIGHT = 500, 500

line_x = 0.0
line_y = -0.85
line_half = 0.25

ball = {}
gravity = -0.7
last_time = time.time()
game_over = False
score = 0
def new_ball():
    return {
        "x": random.uniform(-0.9, 0.9),
        "y": 1.2,
        "r": 0.06,  
        "vy": 0.0
    }

def draw_circle(cx, cy, r):
    glBegin(GL_TRIANGLE_FAN)
    for i in range(60):
        angle = 2 * math.pi * i / 60
        glVertex2f(cx + r * math.cos(angle),
                   cy + r * math.sin(angle))
    glEnd()

def draw_platform():
    glLineWidth(8)
    glBegin(GL_LINES)
    glVertex2f(line_x - line_half, line_y)
    glVertex2f(line_x + line_half, line_y)
    glEnd()

def draw_text(x, y, text):
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

def display():
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(1, 1, 1)
    draw_platform()

    glColor3f(0, 1, 0)
    draw_circle(ball["x"], ball["y"], ball["r"])

    glColor3f(1, 1, 0)
    draw_text(-0.95, 0.9, f"Score: {score}")

    if game_over:
        glColor3f(1, 0, 0)
        draw_text(-0.25, 0.0, "GAME OVER (Press R)")

    glutSwapBuffers()

def update(value):
    global ball, game_over, score, last_time

    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time

    if not game_over:
        ball["vy"] += gravity * dt
        ball["y"] += ball["vy"] * dt

        if (line_y <= ball["y"] - ball["r"] <= line_y + 0.03 and
            line_x - line_half <= ball["x"] <= line_x + line_half):

            score += 1
            ball = new_ball()   

        elif ball["y"] < -1:
            game_over = True
            print("Game Over! Score:", score)
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def special_keys(key, x, y):
    global line_x

    move_speed = 0.08

    if key == GLUT_KEY_LEFT:
        line_x -= move_speed
    elif key == GLUT_KEY_RIGHT:
        line_x += move_speed

    if line_x - line_half < -1:
        line_x = -1 + line_half
    if line_x + line_half > 1:
        line_x = 1 - line_half
def keyboard(key, x, y):
    global ball, game_over, score, last_time
    if key == b'r':
        ball = new_ball()
        game_over = False
        score = 0
        last_time = time.time()
        print("Restarted")
def init():
    global ball
    glClearColor(0, 0, 0, 1)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(-1, 1, -1, 1)
    ball = new_ball()
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow(b" Ball Catch Game")
    init()
    glutDisplayFunc(display)
    glutSpecialFunc(special_keys)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(0, update, 0)
    glutMainLoop()
if __name__ == "__main__":
    main()