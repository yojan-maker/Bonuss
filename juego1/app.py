import pygame
import threading
import random
import time

# Inicializar pygame
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Juego con Hilos")

# Cargar imágenes
fondo = pygame.image.load("galaxia.jpg")
fondo = pygame.transform.scale(fondo, (600, 400))

img_player = pygame.image.load("cohete.png")
img_player = pygame.transform.scale(img_player, (40, 40))

img_enemigo = pygame.image.load("meteorito.png")
img_enemigo = pygame.transform.scale(img_enemigo, (40, 40))

# 🎵 Música retro
pygame.mixer.init()
pygame.mixer.music.load("retro.mp3")  
pygame.mixer.music.play(-1)  # Repetir indefinidamente
pygame.mixer.music.set_volume(0.5)  # Volumen

# Jugador
player = pygame.Rect(300, 350, 40, 40)

# Enemigos
enemigos = []

# Sincronización
mutex = threading.Lock()
condicion = threading.Condition(mutex)

# Estado del juego
vidas = 3
juego_activo = True
pausado = False


def generar_enemigos():
    """Hilo para generar enemigos periódicamente"""
    global juego_activo, pausado
    while juego_activo:
        time.sleep(1)
        with condicion:
            if not pausado:
                enemigos.append(pygame.Rect(random.randint(0, 560), 0, 40, 40))
                condicion.notify()


def mover_enemigos():
    """Hilo para mover enemigos hacia abajo"""
    global juego_activo, vidas, pausado
    while juego_activo:
        with condicion:
            while not enemigos:
                condicion.wait()
            if not pausado:
                for e in enemigos:
                    e.move_ip(0, 5)
                enemigos[:] = [e for e in enemigos if e.y < 400]

                # Colisiones
                for e in enemigos[:]:
                    if e.colliderect(player):
                        vidas -= 1
                        enemigos.remove(e)
                        if vidas <= 0:
                            juego_activo = False
                            break
        time.sleep(0.05)


# Crear hilos
threading.Thread(target=generar_enemigos, daemon=True).start()
threading.Thread(target=mover_enemigos, daemon=True).start()

# Fuente y reloj
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# Loop principal
while juego_activo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            juego_activo = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            pausado = not pausado
            if pausado:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()

    # Movimiento del jugador (solo si no está en pausa)
    keys = pygame.key.get_pressed()
    if not pausado:
        if keys[pygame.K_LEFT]:
            player.move_ip(-5, 0)
        if keys[pygame.K_RIGHT]:
            player.move_ip(5, 0)

    # Dibujo
    screen.blit(fondo, (0, 0))  # Fondo de galaxia
    screen.blit(img_player, player.topleft)  # Cohete

    with mutex:
        for e in enemigos:
            screen.blit(img_enemigo, e.topleft)

    # Texto de vidas
    texto = font.render(f"Vidas: {vidas}", True, (255, 255, 255))
    screen.blit(texto, (10, 10))

    # Texto de pausa
    if pausado:
        texto_pausa = font.render("PAUSADO (P para continuar)", True, (255, 0, 0))
        screen.blit(texto_pausa, (170, 180))

    # Firma
    firma = font.render("Juego 1 - by Yojan", True, (255, 255, 255))
    screen.blit(firma, (420, 10))

    pygame.display.flip()
    clock.tick(30)

# Pantalla final
screen.blit(fondo, (0, 0))
texto_final = font.render("¡Game Over!", True, (255, 0, 0))
screen.blit(texto_final, (240, 180))
pygame.display.flip()

# Esperar unos segundos antes de cerrar
time.sleep(2)
pygame.quit()
