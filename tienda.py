import pygame
from utils import draw_button
from config import WHITE, BLACK, BLUE
import time

def mostrar_tienda(screen, idioma, datos):
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 30)
    grande = pygame.font.SysFont(None, 40)
    fuente = pygame.font.SysFont(None, 28)

    img_moneda = pygame.image.load("assets/img/moneda.png").convert_alpha()
    img_moneda = pygame.transform.scale(img_moneda, (30, 30))

    skins = ["skin1.png", "skin2.png", "skin3.png", "skin4.png"]
    precios = [0, 20, 30, 50]
    imagenes = [pygame.image.load(f"assets/img/{nombre}").convert_alpha() for nombre in skins]
    imagenes = [pygame.transform.scale(img, (60, 90)) for img in imagenes]

    botones = []
    margen = 40
    start_x = (WIDTH - (2 * 100 + margen)) // 2
    start_y = HEIGHT // 3

    for fila in range(2):
        for col in range(2):
            x = start_x + col * (100 + margen)
            y = start_y + fila * 130
            botones.append(pygame.Rect(x, y, 100, 120))

    mensaje = ""
    mensaje_timer = 0
    confirmacion_activa = False
    skin_pendiente = None
    skin_precio = 0

    while True:
        screen.fill(BLUE)

        # Título y monedas
        titulo = grande.render("Tienda" if idioma == "es" else "Shop", True, WHITE)
        screen.blit(titulo, (WIDTH//2 - titulo.get_width()//2, 10))
        screen.blit(img_moneda, (20, 20))
        screen.blit(fuente.render(str(datos.get("monedas", 0)), True, WHITE), (60, 25))
        screen.blit(fuente.render("Esc para volver" if idioma == "es" else "Esc to return", True, WHITE), (30, 550))

        # Mostrar skins
        for i, rect in enumerate(botones):
            pygame.draw.rect(screen, WHITE, rect, 3)
            screen.blit(imagenes[i], (rect.x + 20, rect.y + 10))

            if skins[i] in datos.get("skins", []):
                if datos.get("skin_equipada") == skins[i]:
                    pygame.draw.rect(screen, BLACK, rect, 5)
                elif rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(screen, (255, 255, 0), rect, 3)
            else:
                precio = precios[i]
                precio_txt = font.render(f"{precio} 🪙", True, (255, 215, 0))
                screen.blit(precio_txt, (rect.centerx - precio_txt.get_width()//2, rect.bottom - 25))

        # Mostrar mensaje si no alcanza
        if mensaje:
            msg_txt = font.render(mensaje, True, WHITE)
            screen.blit(msg_txt, (WIDTH//2 - msg_txt.get_width()//2, HEIGHT - 40))
            if time.time() - mensaje_timer > 3:
                mensaje = ""

        # Mostrar confirmación de compra
        if confirmacion_activa:
            cuadro = pygame.Rect(WIDTH//2 - 120, HEIGHT//2 - 60, 240, 120)
            pygame.draw.rect(screen, BLACK, cuadro)
            pygame.draw.rect(screen, WHITE, cuadro, 3)

            texto = fuente.render("¿Comprar?" if idioma == "es" else "Buy?", True, WHITE)
            screen.blit(texto, (cuadro.centerx - texto.get_width()//2, cuadro.y + 10))

            btn_si = pygame.Rect(cuadro.x + 30, cuadro.bottom - 50, 60, 30)
            btn_no = pygame.Rect(cuadro.right - 90, cuadro.bottom - 50, 60, 30)

            pygame.draw.rect(screen, (0, 200, 0), btn_si)
            pygame.draw.rect(screen, (200, 0, 0), btn_no)

            txt_si = fuente.render("Sí" if idioma == "es" else "Yes", True, BLACK)
            txt_no = fuente.render("No", True, BLACK)

            screen.blit(txt_si, (btn_si.centerx - txt_si.get_width()//2, btn_si.centery - txt_si.get_height()//2))
            screen.blit(txt_no, (btn_no.centerx - txt_no.get_width()//2, btn_no.centery - txt_no.get_height()//2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", datos
            elif event.type == pygame.KEYDOWN and not confirmacion_activa:
                if event.key == pygame.K_ESCAPE:
                    return "menu", datos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if confirmacion_activa:
                    if btn_si.collidepoint(event.pos):
                        datos["monedas"] -= skin_precio
                        datos["skins"].append(skin_pendiente)
                        datos["skin_equipada"] = skin_pendiente
                        confirmacion_activa = False
                    elif btn_no.collidepoint(event.pos):
                        confirmacion_activa = False
                else:
                    for i, rect in enumerate(botones):
                        if rect.collidepoint(event.pos):
                            skin = skins[i]
                            if skin in datos["skins"]:
                                datos["skin_equipada"] = skin
                            else:
                                if datos["monedas"] >= precios[i]:
                                    confirmacion_activa = True
                                    skin_pendiente = skin
                                    skin_precio = precios[i]
                                else:
                                    mensaje = "No tienes suficientes monedas" if idioma == "es" else "Not enough coins"
                                    mensaje_timer = time.time()

        clock.tick(60)
