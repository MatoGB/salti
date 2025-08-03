import pygame
from config import BLUE, WHITE, BLACK
from utils import draw_button

def seleccionar_dificultad(screen, idioma, dificultad_actual):
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    # Botones
    botones = {
        "normal": pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 60, 200, 50),
        "dificil": pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 10, 200, 50),
    }

    while True:
        screen.fill(BLUE)

        # Título
        titulo = font.render("Dificultad" if idioma == "es" else "Difficulty", True, WHITE)
        screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, HEIGHT // 4))

        # Botones
        draw_button(screen, botones["normal"], "Normal", font, dificultad_actual == "normal")
        draw_button(screen, botones["dificil"], "Difícil" if idioma == "es" else "Hard", font, dificultad_actual == "dificil")

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", dificultad_actual
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if botones["normal"].collidepoint(event.pos):
                    return "menu", "normal"
                elif botones["dificil"].collidepoint(event.pos):
                    return "menu", "dificil"

        clock.tick(60)
