import pygame
import threading
import random
import time

# Inicializar pygame
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Juego con Hilos")

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Jugador
player = pygame.Rect(300, 350, 40, 40)

# Enemigos
enemigos = []

# Bloqueo (mutex)
mutex = threading.Lock()


def mover_enemigos():
    """Hilo que genera enemigos periódicamente"""
    while True:
        time.sleep(1)
        with mutex:  # proteger lista compartida
            enemigos.append(pygame.Rect(random.randint(0, 560), 0, 40, 40))


def actualizar_enemigos():
    """Mover enemigos hacia abajo"""
    with mutex:
        for e in enemigos:
            e.move_ip(0, 5)
        # Eliminar los que salen de la pantalla
        enemigos[:] = [e for e in enemigos if e.y < 400]


# Crear hilo para generar enemigos
threading.Thread(target=mover_enemigos, daemon=True).start()

# Loop principal
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_ip(-5, 0)
    if keys[pygame.K_RIGHT]:
        player.move_ip(5, 0)

    # Actualizar enemigos
    actualizar_enemigos()

    # Dibujo
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, player)
    with mutex:
        for e in enemigos:
            pygame.draw.rect(screen, RED, e)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
