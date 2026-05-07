"""
Main Entry Point

Run the Custom UNO Online client UI.
"""

import sys


def main():
    try:
        import pygame
    except ImportError:
        print("Missing dependency: pygame")
        print("Install it with:")
        print("pip install pygame")
        sys.exit(1)

    try:
        from UI.ui_manager import UIManager
    except ImportError as error:
        print("Import error:", error)
        print("Please check your folder structure and __init__.py files.")
        sys.exit(1)

    pygame.init()

    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 720
    FPS = 60

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Custom UNO Online")

    clock = pygame.time.Clock()

    ui_manager = UIManager()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            ui_manager.handle_event(event)

        ui_manager.update()

        screen.fill((30, 30, 30))

        ui_manager.render(screen)

        pygame.display.flip()
        clock.tick(FPS)

    try:
        ui_manager.disconnect()
    except Exception:
        pass

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
