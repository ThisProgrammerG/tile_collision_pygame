
import pygame


SIZE = pygame.Rect((0, 0), (900, 500))
GRAVITY = pygame.Vector2(0, 1)

class Drawable:
    def __init__(self, size, position, color, anchor='center'):
        self.position = pygame.Vector2(position)
        self.color = color
        self.anchor = anchor
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(**{self.anchor: position})
        self.image.fill(self.color)

    def update(self, events):
        pass

    def render(self, surface):
        surface.blit(self.image, self.rect)

class Entity(Drawable):
    def __init__(self, size, position, color):
        super().__init__(size, position, color)
        self.speed = 5
        self.directions = {direction: False for direction in ['up', 'down', 'left', 'right']}
        self.acceleration = pygame.Vector2()
        self.velocity = pygame.Vector2()
        self.grounded = False

    def handle_events(self, events):
        pass

    def apply_force(self, force):
        self.velocity += force

    def move(self):
        if not (self.directions['left'] and self.directions['right']):
            self.acceleration.x = 0
            self.velocity.x = 0

        if not (self.directions['up'] and self.directions['down']):
            self.acceleration.y = 0
            self.velocity.y = 0

        if self.directions['left']:
            self.acceleration.x -= self.speed
        if self.directions['right']:
            self.acceleration.x += self.speed
        if self.directions['up']:
            self.acceleration.y -= self.speed
        if self.directions['down']:
            self.acceleration.y += self.speed

    def handle_collision(self, objects):
        self.grounded = False
        rect = self.rect.copy()
        #print('Collision:', self.velocity)

        # TODO moving left and right while on top near corners. Already colliding
        # TODO have to take velocity into consideration, if velocity would collide move back.
        # TODO but movement is already calculated into the rect
        for obj in objects:
            if rect.colliderect(obj):
                if rect.right > obj.rect.left > rect.left:
                    rect.right = obj.rect.left
                elif rect.left < obj.rect.right < rect.right:
                    rect.left = obj.rect.right
            if rect.colliderect(obj):
                if rect.top < obj.rect.top:
                    rect.bottom = obj.rect.top
                    self.grounded = True
                elif rect.bottom > obj.rect.bottom:
                    rect.top = obj.rect.bottom

        self.position.update(rect.center)
        self.rect.center = self.position

    def handle_forces(self):
        if not self.grounded:
            self.apply_force(GRAVITY)

        self.velocity += self.acceleration

        if self.acceleration.magnitude() > 0:
            self.acceleration.clamp_magnitude_ip(1)
        if self.velocity.magnitude() > 0:
            self.velocity.clamp_magnitude_ip(10)

        if abs(self.velocity.x) <= 0.1:
            self.velocity.x = 0
        if abs(self.velocity.y) <= 0.1:
            self.velocity.y = 0



    def update(self, events, collision_group=None):
        self.handle_events(events)
        self.move()
        self.handle_forces()

        for group in collision_group:
            self.handle_collision(group)

        self.position += self.velocity
        self.rect.center = self.position

class Tile(Drawable):
    pass

def player_control(self, events):
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_LEFT, pygame.K_a]:
                self.directions['left'] = True
            if event.key in [pygame.K_RIGHT, pygame.K_d]:
                self.directions['right'] = True
            if event.key in [pygame.K_UP, pygame.K_w]:
                self.directions['up'] = True
            if event.key in [pygame.K_DOWN, pygame.K_s]:
                self.directions['down'] = True
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_a]:
                self.directions['left'] = False
            if event.key in [pygame.K_RIGHT, pygame.K_d]:
                self.directions['right'] = False
            if event.key in [pygame.K_UP, pygame.K_w]:
                self.directions['up'] = False
            if event.key in [pygame.K_DOWN, pygame.K_s]:
                self.directions['down'] = False

def main():
    screen = pygame.display.set_mode(SIZE.size)
    clock = pygame.time.Clock()
    running = True

    player = Entity(size=(50, 75), position=(300, 200), color='green')
    player.handle_events = lambda game_events: player_control(player, game_events)

    enemy_1 = Entity(size=(50, 75), position=(500, 200), color='purple')
    enemy_2 = Entity(size=(50, 75), position=(100, 200), color='red')

    tile_ground = Tile(size=(SIZE.width * 4, 100), position=(SIZE.width // 2, SIZE.height - 50), color='brown')
    tile_1 = Tile(size=(200, 50), position=(200, 300), color='brown')
    tile_2 = Tile(size=(200, 50), position=(700, 375), color='brown')

    players = [player]
    enemies = []  # [enemy_1, enemy_2]
    tiles = [tile_ground, tile_1, tile_2]

    while running:
        clock.tick(60)
        screen.fill('black')

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        for entity in players:
            entity.update(events, collision_group=[enemies, tiles])
            entity.render(screen)

        for entity in enemies:
            entity.update(None, collision_group=[tiles])
            entity.render(screen)

        for tile in tiles:
            tile.render(screen)

        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()

