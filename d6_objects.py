import pymunk, math
import pymunk.pygame_util

# our robot
botBody = pymunk.Body(1,100)
botBody.position = (640, 360)
botVert = [(0,0), (20, 0), (10, 20)]
botShape = pymunk.Poly(botBody, botVert)
botShape.color = (0, 255, 0, 255)

# ==========================================================
# rectangle
body1 = pymunk.Body(body_type=pymunk.Body.STATIC)
body1.position = (100,600)
rect1 = pymunk.Poly.create_box(body1, (200, 75))

# triangle
body2 = pymunk.Body(body_type=pymunk.Body.STATIC)
body2.position = (300, 500)
body2.angle = math.radians(-30)
triVert = [(-50,-50), (50,-50), (0,50)]
tri = pymunk.Poly(body2, triVert)

# rot rectangle
body3 = pymunk.Body(body_type=pymunk.Body.STATIC)
body3.position = (1000, 100)
body3.angle = math.radians(45)
rect2 = pymunk.Poly.create_box(body3, (500, 300))

# polygon
body4 = pymunk.Body(body_type=pymunk.Body.STATIC)
body4.position = (300,200)
polyVert = [
    (0, -60),     # Top point
    (20, -20),    # Right shoulder
    (60, -10),    # Right spike
    (25, 20),     # Inward curve
    (40, 50),     # Bottom-right spike
    (0, 30),      # Bottom dip
    (-40, 50),    # Bottom-left spike
    (-25, 20),    # Inward curve
    (-60, -10),   # Left spike
    (-20, -20)    # Left shoulder
]
poly1 = pymunk.Poly(body4, polyVert)



bodies = [botBody, body1, body2, body3, body4]
shapes = [botShape, rect1, tri, rect2, poly1]


# disable built in collision
for shape in [botShape, rect1, tri, rect2, poly1]:
    shape.sensor = True
