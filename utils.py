import pygame
from config import BLUE, WHITE, BLACK

music_paused = False

def toggle_music():
    global music_paused
    if music_paused:
        pygame.mixer.music.unpause()
        music_paused = False
    else:
        pygame.mixer.music.pause()
        music_paused = True

def cuenta_regresiva(screen, idioma, dificultad):
    WIDTH, HEIGHT = screen.get_size()
    font = pygame.font.Font(None, 100)
    texto_ya = "Go!" if idioma == "en" else "¡Ya!"
    numeros = ["3", "2", "1", texto_ya]

    for n in numeros:
        screen.fill((0, 0, 0))
        texto = font.render(n, True, (255, 255, 255))
        rect = texto.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(texto, rect)
        pygame.display.flip()
        pygame.time.delay(700)

    screen.fill((0, 0, 0))
    pygame.display.flip()

def draw_button(screen, rect, text, font, seleccionado=False):
    color = (255, 255, 255, 150) if seleccionado else (255, 255, 255, 50)
    boton = pygame.Surface(rect.size, pygame.SRCALPHA)
    boton.fill(color)
    screen.blit(boton, rect.topleft)

    texto = font.render(text, True, BLACK)
    screen.blit(texto, (
        rect.centerx - texto.get_width() // 2,
        rect.centery - texto.get_height() // 2
    ))
