import pygame
import esper
from typing import Tuple
from dataclasses import dataclass as component

WINDOW_DIMENSIONSE: Tuple[int, int] = (640, 480)

@component
class Position:
    x: float = 0.0
    y: float = 0.0

@component
class Velocity:
    x: float = 0.0
    y: float = 0.0

@component
class Speed:
    value: float = 0.0

@component
class Player:
    def __init__(self, image_path: str):
        temp = pygame.image.load(image_path)
        self.image = pygame.transform.scale(temp, (32, 64))

    image: pygame.Surface

    def hitbox(self, position: Position) -> pygame.Rect:
        return pygame.Rect(position.x, position.y, self.image.get_width(), self.image.get_height())

class PlayerController(esper.Processor):
    def process(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            _, (_, speed, vel) = esper.get_components(Player, Speed, Velocity)[0]
            if event.key == pygame.K_a:
                vel.x -= speed.value
            elif event.key == pygame.K_d:
                vel.x += speed.value
            elif event.key == pygame.K_w:
                vel.y -= speed.value
            elif event.key == pygame.K_s:
                vel.y += speed.value
            vel.x = max(min(vel.x, 1), -1)  # clamp to [-3, 3] min
            vel.y = max(min(vel.y, 1), -1)  # clamp to [-3, 3] min
        elif event.type == pygame.KEYUP:
            _, (_, vel) = esper.get_components(Player, Velocity)[0]
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                vel.x = 0
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                vel.y = 0

class UpdatePlayerSystem(esper.Processor):
    def process(self, delta_time: float):
        _, (player, position, velocity) = esper.get_components(Player, Position, Velocity)[0]

        # TEMPORARY just for testing
        hitbox = player.hitbox(position)
        if hitbox.x + hitbox.width >= WINDOW_DIMENSIONSE[0]:
            position.x = WINDOW_DIMENSIONSE[0] - hitbox.width
        elif hitbox.x <= 0:
            position.x = 0
        if hitbox.y + hitbox.height >= WINDOW_DIMENSIONSE[1]:
            position.y = WINDOW_DIMENSIONSE[1] - hitbox.height
        elif hitbox.y <= 0:
            position.y = 0
        # -- End TEMPORARY just for testing --

        position.x += velocity.x * delta_time
        position.y += velocity.y * delta_time

class DrawPlayerSystem(esper.Processor):
    def __init__(self, *, screen: pygame.Surface):
        super().__init__()
        self.screen = screen
    def process(self):
        for _, (position, player) in esper.get_components(Position, Player):
            # pygame.draw.rect(self.screen, (255, 0, 0), player.hitbox(position))
            self.screen.blit(player.image, player.hitbox(position))


pygame.init()

def main() -> None:
    """Main function to run the Pygame loop."""
    #  ----  Set up display ----
    screen_size: Tuple[int, int] = WINDOW_DIMENSIONSE
    screen: pygame.Surface = pygame.display.set_mode(screen_size)
    #  ----  End set up display ----

    player = esper.create_entity()
    esper.add_component(player, Player('./assets/player.jpg'))
    esper.add_component(player, Position(x=100, y=100))
    esper.add_component(player, Velocity(x=0, y=0))
    esper.add_component(player, Speed(value=0.001))

    player_controller = PlayerController()
    esper.add_processor(player_controller)
    update_player_processor = UpdatePlayerSystem()
    esper.add_processor(update_player_processor )
    draw_player_processor = DrawPlayerSystem(screen=screen)
    esper.add_processor(draw_player_processor)


    # ---- Main loop ----
    running: bool = True
    while running:
        # UPDATE
        delta_time = pygame.time.get_ticks() / 1000
        update_player_processor.process(delta_time)

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            player_controller.process(event)


        # DRAWING
        screen.fill((0, 0, 0))

        draw_player_processor.process()

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
