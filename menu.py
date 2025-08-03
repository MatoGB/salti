import pygame
from utils import toggle_music
from config import *
from puntuacion import cargar_datos

def show_menu(screen, idioma, datos, dificultad):
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    font_title = pygame.font.SysFont(None, 40)
    font_btn = pygame.font.SysFont(None, 32)
    datos = cargar_datos()

    #Salti
    salti_img = pygame.image.load("assets/img/salti_menu.png").convert_alpha()
    salti_img = pygame.transform.scale(salti_img, (100, 130))

    # Banderas
    bandera_es = pygame.image.load("assets/img/bandera_es.png").convert_alpha()
    bandera_en = pygame.image.load("assets/img/bandera_en.png").convert_alpha()
    bandera_es = pygame.transform.scale(bandera_es, (40, 30))
    bandera_en = pygame.transform.scale(bandera_en, (40, 30))
    rect_es = bandera_es.get_rect(topleft=(WIDTH - 90, 20))
    rect_en = bandera_en.get_rect(topleft=(WIDTH - 45, 20))

    # Moneda y datos
    img_moneda = pygame.image.load("assets/img/moneda.png").convert_alpha()
    img_moneda = pygame.transform.scale(img_moneda, (30, 30))
    fuente = pygame.font.SysFont(None, 28)

    # Botones
    btn_width, btn_height = 180, 50
    btn_jugar = pygame.Rect(WIDTH // 2 - btn_width // 2, HEIGHT // 2 - 60, btn_width, btn_height)
    btn_dificultad = pygame.Rect(WIDTH // 2 - btn_width // 2, HEIGHT // 2, btn_width, btn_height)
    btn_tienda = pygame.Rect(WIDTH // 2 - btn_width // 2, HEIGHT // 2 + 60, btn_width, btn_height)

    while True:
        screen.fill(BLUE)
        mouse_pos = pygame.mouse.get_pos()

        # Título
        title_text = font_title.render(tituloen if idioma == "en" else tituloes, True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3 - 60))

        # Moneda y contador
        screen.blit(img_moneda, (20, 20))
        fuente_monedas = pygame.font.SysFont(None, 30)
        txt_monedas = fuente_monedas.render(str(datos.get("monedas", 0)), True, WHITE)
        screen.blit(txt_monedas, (60, 25))

        # Banderas
        screen.blit(bandera_es, rect_es)
        screen.blit(bandera_en, rect_en)

        #Salti
        salti_x = screen.get_width() // 2 - salti_img.get_width() // 2
        salti_y = HEIGHT // 2 + 120  # Un poco debajo del último botón
        screen.blit(salti_img, (salti_x, salti_y))
        texto = fuente.render(muteen if idioma == "en" else mutees, True, WHITE)
        screen.blit(texto, (10, 550))

        # Dibujar botones con efecto hover
        for rect_btn, label_en, label_es in [
            (btn_jugar, "Play", "Jugar"),
            (btn_dificultad, "Difficulty", "Dificultad"),
            (btn_tienda, "Store", "Tienda")
        ]:
            hovered = rect_btn.collidepoint(mouse_pos)
            color = (255, 255, 255, 180) if hovered else (255, 255, 255, 80)
            surf_btn = pygame.Surface((btn_width, btn_height), pygame.SRCALPHA)
            surf_btn.fill(color)
            screen.blit(surf_btn, rect_btn.topleft)
            label = font_btn.render(label_en if idioma == "en" else label_es, True, BLACK)
            screen.blit(label, (rect_btn.centerx - label.get_width() // 2, rect_btn.centery - label.get_height() // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", idioma
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    toggle_music()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rect_es.collidepoint(event.pos):
                    idioma = "es"
                elif rect_en.collidepoint(event.pos):
                    idioma = "en"
                elif btn_jugar.collidepoint(event.pos):
                    return "start", idioma
                elif btn_dificultad.collidepoint(event.pos):
                    return "dificultad", idioma
                elif btn_tienda.collidepoint(event.pos):
                    return "tienda", idioma

        clock.tick(60)

def show_game_over(screen, idioma):
    WIDTH, HEIGHT = screen.get_size()
    font = pygame.font.SysFont(None, 48)
    subfont = pygame.font.SysFont(None, 32)
    clock = pygame.time.Clock()
    sonido_gameover = pygame.mixer.Sound("assets/snd/gameover.ogg")
    sonido_gameover.play()

    while True:
        screen.fill((0, 0, 0))
        text = font.render("¡Game Over!", True, WHITE)
        subtext = subfont.render(subtexten if idioma == "en" else subtextes, True, WHITE)

        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3))
        screen.blit(subtext, (WIDTH // 2 - subtext.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                elif event.key == pygame.K_m:
                    toggle_music()

        clock.tick(60)