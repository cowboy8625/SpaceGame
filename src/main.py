import pygame
from typing import Tuple

# Initialize Pygame
pygame.init()

# Define types for screen dimensions
ScreenDimensions = Tuple[int, int]

def create_window(size: ScreenDimensions) -> pygame.Surface:
    """Create and return the main window surface."""
    return pygame.display.set_mode(size)

def main() -> None:
    """Main function to run the Pygame loop."""
    # Set up display
    screen_size: ScreenDimensions = (640, 480)
    screen: pygame.Surface = create_window(screen_size)
    pygame.display.set_caption('Hello, World!')

    # Set up font
    font: pygame.font.Font = pygame.font.Font(None, 74)
    text: pygame.Surface = font.render('Hello, World!', True, (255, 255, 255))
    text_rect: pygame.Rect = text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))

    # Main loop
    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the screen with a color (black)
        screen.fill((0, 0, 0))

        # Draw the text onto the screen
        screen.blit(text, text_rect)

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()

if __name__ == '__main__':
    main()
