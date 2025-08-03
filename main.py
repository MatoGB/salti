import pygame
import sys
from menu import show_menu, show_game_over
from utils import cuenta_regresiva, toggle_music
from game import play_game
from puntuacion import cargar_datos, guardar_datos
from tienda import mostrar_tienda
from dificultad import seleccionar_dificultad

def main():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("assets/snd/musica.ogg")
    pygame.mixer.music.play(-1)
    screen = pygame.display.set_mode((400, 600))
    pygame.display.set_caption("Salti")
    idioma = "en"  # idioma por defecto
    dificultad = "normal"  # por defecto
    datos = cargar_datos()

    while True:
        accion, idioma = show_menu(screen, idioma, datos, dificultad)
        if accion == "quit":
            break
        elif accion == "tienda":
            accion, datos = mostrar_tienda(screen, idioma, datos)
            if accion == "quit":
                break
            else:
                continue
        elif accion == "dificultad":
            resultado, nueva_dificultad = seleccionar_dificultad(screen, idioma, dificultad)
            if resultado == "quit":
                break
            dificultad = nueva_dificultad
            continue
        elif accion == "start":
            cuenta_regresiva(screen, idioma, dificultad)
            resultado, datos, dificultad = play_game(screen, idioma, datos, dificultad)
            guardar_datos(datos)
            if resultado == "game_over":
                if not show_game_over(screen, idioma):
                    break
                continue

        cuenta_regresiva(screen, idioma, dificultad)
        resultado, datos, dificultad = play_game(screen, idioma, datos, dificultad)

        guardar_datos(datos)

        if resultado == "game_over":
            if not show_game_over(screen, idioma):
                break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error:", e)
        input("Presioná Enter para cerrar...")
