import pygame
import math

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
running = True
force_limit_threshold = 40
collisions = False
dt = 0
G = 1000

class Planet:
    def __init__(self, name: str, colour: str, x: float, y: float, dx: float, dy: float, mass: float, radius: float):
        self.name = name
        self.colour = colour
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.visited = []
        self.mass = mass
        self.radius = radius

    def update(self):

        for planet in planets:
            if (planet.name != self.name):
                m1 = self.mass
                m2 = planet.mass
                if (collisions):
                    r2 = (planet.y - self.y) ** 2 + (planet.x - self.x) ** 2
                else:
                    r2 = max((planet.y - self.y) ** 2 + (planet.x - self.x) ** 2, (planet.radius + self.radius + force_limit_threshold) ** 2)
                force = (G * m1 * m2) / r2
                acceleration = force / self.mass
                angle = math.atan2(planet.y - self.y, planet.x - self.x)
                self.dx += acceleration * math.cos(angle)
                self.dy += acceleration * math.sin(angle)

                if (collisions):
                    if math.sqrt(r2) < self.radius + planet.radius:
                        self.dx, planet.dx = self.calculate_collision_velocity(self.mass, self.dx, planet.mass, planet.dx)
                        self.dy, planet.dy = self.calculate_collision_velocity(self.mass, self.dy, planet.mass, planet.dy)

        self.visited.append((self.x + camera_x, self.y + camera_y))
        self.x += self.dx * dt
        self.y += self.dy * dt
        pygame.draw.circle(screen, self.colour, (self.x + camera_x, self.y + camera_y), self.radius)
        if (len(self.visited) > 1):
            pygame.draw.lines(screen, self.colour, False, self.visited)

    def calculate_collision_velocity(self, m1, v1, m2, v2):
        new_v1 = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
        new_v2 = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)
        return new_v1, new_v2

# Fictitious body that stays in the same location
class FixedPlanet(Planet):
    def __init__(self, name: str, colour: str, x: float, y: float, dx: float, dy: float, mass: float, radius: float):
        super().__init__(name, colour, x, y, dx, dy, mass, radius)
        dx = 0
        dy = 0
    def update(self):
        pygame.draw.circle(screen, self.colour, (self.x + camera_x, self.y + camera_y), self.radius)


# SMALL PLANET AROUND LARGE SUN
# planet1 = Planet("Planet", "red", 400, 1000, 0, -400, 10, 10)
# planet2 = Planet("Sun", "yellow", 640, 1000, 0, 0, 500, 50)
# planets = [planet1, planet2]

# SMALL PLANET AROUND LARGE FIXED SUN
# planet1 = Planet("Planet", "red", 400, 1000, 0, -400, 10, 10)
# planet2 = FixedPlanet("Sun", "yellow", 640, 1000, 0, 0, 500, 50)
# planets = [planet1, planet2]

# THREE BODY PROBLEM
planet1 = Planet("A", "red", 700, 400, 0, 0, 50, 10)
planet2 = Planet("B", "blue", 1000, 540, 0, 0, 50, 10)
planet3 = Planet("C", "green", 1300, 300, 0, 0, 50, 10)
planets = [planet1, planet2, planet3]

camera_x = 0
camera_y = 0

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        camera_y += 300 * dt
        for planet in planets:
            new_list = []
            for coord in planet.visited:
                new_list.append((coord[0], coord[1] + 300 * dt))
            planet.visited = new_list
    if keys[pygame.K_s]:
        camera_y -= 300 * dt
        for planet in planets:
            new_list = []
            for coord in planet.visited:
                new_list.append((coord[0], coord[1] - 300 * dt))
            planet.visited = new_list
    if keys[pygame.K_a]:
        camera_x += 300 * dt
        for planet in planets:
            new_list = []
            for coord in planet.visited:
                new_list.append((coord[0] + 300 * dt, coord[1]))
            planet.visited = new_list
    if keys[pygame.K_d]:
        camera_x -= 300 * dt
        for planet in planets:
            new_list = []
            for coord in planet.visited:
                new_list.append((coord[0] - 300 * dt, coord[1]))
            planet.visited = new_list
    if keys[pygame.K_c]:
        for planet in planets:
            planet.visited = []

    for planet in planets:
        planet.update()

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()