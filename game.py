import pygame
import random
from utils import toggle_music
from config import *

# Futuro: dificultad, skins, puntuación, monedas

def play_game(screen, idioma, datos, dificultad="normal"):
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    FPS = 60

    # Tamaño del jugador y plataformas
    player_size = (50, 70)
    platform_width, platform_height = 80, 20

    #Imagen fondo
    fondo_claro = pygame.image.load("assets/img/fondo_claro.png").convert()
    fondo_rojo = pygame.image.load("assets/img/fondo_rojo.png").convert()
    fondo = fondo_rojo if dificultad == "dificil" else fondo_claro

    # Imágenes del jugador
    # Obtener nombre de skin equipada
    skin = datos.get("skin_equipada", "skin1.png")  # fallback a skin1.png si no existe

    # Armar nombre de la imagen "de caída"
    skin_abajo = skin.replace(".png", "abajo.png")

    # Cargar imágenes del jugador
    player_img_up_right = pygame.image.load(f"assets/img/{skin}").convert_alpha()
    player_img_down_right = pygame.image.load(f"assets/img/{skin_abajo}").convert_alpha()

    player_img_up_right = pygame.transform.scale(player_img_up_right, player_size)
    player_img_down_right = pygame.transform.scale(player_img_down_right, player_size)
    player_img_up_left = pygame.transform.flip(player_img_up_right, True, False)
    player_img_down_left = pygame.transform.flip(player_img_down_right, True, False)

    # Imagen de plataforma
    # Carga ambas imágenes antes del bucle principal
    cloud_img = pygame.image.load("assets/img/nubeok.png").convert_alpha()
    cloud_img = pygame.transform.scale(cloud_img, (80, 40))

    cloud_img_boost = pygame.image.load("assets/img/nube_dorada.png").convert_alpha()
    cloud_img_boost = pygame.transform.scale(cloud_img_boost, (80, 40))

    # Sonido
    sonido_salto = pygame.mixer.Sound("assets/snd/salto.ogg")

    # Jugador
    player = pygame.Rect(WIDTH//2 - player_size[0]//2, HEIGHT - player_size[1] - 10, *player_size)
    facing_right = True
    player_vel_y = 0
    gravity = 0.5
    jump_strength = -18
    paused = False

    # Plataforma inicial y lista
    start_platform = pygame.Rect(player.centerx - platform_width // 2, player.bottom + 5, platform_width, platform_height)
    platforms = []
    scroll_y = 0
    gap_base = 120 if dificultad == "normal" else 180
    y = HEIGHT - 100
    while y > -HEIGHT:
        gap = random.randint(gap_base - 10, gap_base + 10)
        x = random.randint(0, WIDTH - platform_width)
        is_boosted = random.random() < 0.05  # 5% de probabilidad
        platforms.append((pygame.Rect(x, y, platform_width, platform_height), is_boosted))
        y -= gap

    # Puntuación y monedas
    puntaje = 0
    monedas = datos.get("monedas", 0)
    fuente = pygame.font.SysFont(None, 28)
    ultima_entrega = 0

    running = True
    while running:
        clock.tick(FPS)
        screen.fill(BLUE)
        screen.blit(fondo, (0, 0))
        scroll_factor = 1


        # === Eventos ===
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", datos
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                elif paused and event.key == pygame.K_q:
                    return "menu", datos, dificultad
                elif event.key == pygame.K_m:
                    toggle_music()

        if paused:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            font = pygame.font.SysFont(None, 36)
            t1 = font.render(text1en if idioma == "en" else text1es, True, WHITE)
            t2 = font.render(text2en if idioma == "en" else text2es, True, WHITE)
            screen.blit(t1, (WIDTH//2 - t1.get_width()//2, HEIGHT//2 - 30))
            screen.blit(t2, (WIDTH//2 - t2.get_width()//2, HEIGHT//2 + 10))
            pygame.display.flip()
            continue

        # === Movimiento ===
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= 5
            facing_right = False
        if keys[pygame.K_RIGHT]:
            player.x += 5
            facing_right = True
        
        # Limitar a los bordes de la pantalla
        if player.left < 0:
            player.left = 0
        elif player.right > WIDTH:
            player.right = WIDTH

        player_vel_y += gravity
        player.y += player_vel_y

        # === Colisiones ===
        if player_vel_y > 0:
            for plat, is_boosted in platforms:
                if player.colliderect(plat) and player.bottom - player_vel_y <= plat.top + 10:
                    player.bottom = plat.top
                    player_vel_y = jump_strength * (2 if is_boosted else 1)
                    scroll_factor = 2 if is_boosted else 1
                    sonido_salto.play()
                    
                    if is_boosted:
                        puntaje += 5
                        monedas += 1
                    else:
                        puntaje += 1
                        if puntaje % 20 == 0 and puntaje != ultima_entrega:
                            monedas += 1
                            ultima_entrega = puntaje
            if player.colliderect(start_platform):
                player.bottom = start_platform.top
                player_vel_y = jump_strength

        # === Scroll ===
        if player.y < HEIGHT // 2:
            diff = (HEIGHT // 2 - player.y) * scroll_factor  # scroll_factor = 1 por defecto
            player.y = HEIGHT // 2
            scroll_y += diff
            for i in range(len(platforms)):
                plat, is_boosted = platforms[i]
                plat.y += diff
                platforms[i] = (plat, is_boosted)
            start_platform.y += diff
            if dificultad == "normal":
                min_gap, max_gap = 90, 120
            else:  # dificil
                min_gap, max_gap = 130, 160  # más separación en difícil

            while platforms[-1][0].top > -100:
                x = random.randint(0, WIDTH - platform_width)
                y = platforms[-1][0].top - random.randint(min_gap, max_gap)
                is_boosted = random.random() < 0.05  # 5% de probabilidad
                platforms.append((pygame.Rect(x, y, platform_width, platform_height), is_boosted))

        platforms = [(p, b) for (p, b) in platforms if p.top < HEIGHT + 100]

        # === Dibujar ===
        for plat, is_boosted in platforms:
            if is_boosted:
                screen.blit(cloud_img_boost, plat)
            else:
                screen.blit(cloud_img, plat)
        pygame.draw.ellipse(screen, (200, 200, 200), start_platform)

        if player_vel_y < 0:
            img = player_img_up_right if facing_right else player_img_up_left
        else:
            img = player_img_down_right if facing_right else player_img_down_left

        screen.blit(img, player)

        # Puntuación
        texto = fuente.render(f"Puntos: {puntaje} - Monedas: {monedas}", True, WHITE)
        screen.blit(texto, (10, 10))

        pygame.display.flip()

        # Game over
        if player.top > HEIGHT:
            if puntaje > datos.get("highscore", 0):
                datos["highscore"] = puntaje
            datos["monedas"] = monedas
            return "game_over", datos, dificultad
