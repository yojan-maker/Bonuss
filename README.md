# 🕹️ Juego Multihilo con PyGame — "Cohete y Meteoritos"

Este proyecto implementa un pequeño **juego 2D con hilos (threads)** en Python utilizando la librería **PyGame**.  
El jugador controla un cohete que debe esquivar meteoritos que caen del cielo, mientras suena música retro de fondo y un fondo espacial ambienta la partida 🚀🌌.

---

## 📦 Requisitos

Asegúrate de tener instalado Python 3 y PyGame:

```bash
pip install pygame
```

## 🎮 Descripción del juego
  • El jugador controla un cohete con las flechas del teclado.
	•	Los meteoritos aparecen de forma aleatoria desde la parte superior y caen hacia abajo.
	•	El movimiento de los meteoritos es controlado por hilos independientes, lo que simula ejecución concurrente.
	•	Al presionar “P” el juego entra en pausa (los hilos se detienen y la música se pausa).
	•	Se puede reanudar presionando “P” nuevamente.
	•	Incluye un fondo galáctico y música de tipo retro.

## 🧠 Explicación técnica

El programa utiliza hilos, mutex (Lock) y variables de condición (Condition) para sincronizar el acceso a los datos compartidos y coordinar los eventos concurrentes.

---

## 🔹 Recurso compartido

```bash
enemigos = []
```

Esta lista contiene los rectángulos (o sprites) de los meteoritos activos en pantalla.

🔹 Sección crítica

Cada vez que los hilos acceden o modifican esta lista, se entra a una sección crítica, protegida por un mutex para evitar condiciones de carrera.
ejemplo:
```bash
with condicion:
    if not pausado:
        enemigos.append(pygame.Rect(random.randint(0, 560), 0, 40, 40))
        condicion.notify()
```

Aquí, el bloque with condicion: asegura que solo un hilo pueda modificar la lista enemigos a la vez.
El método notify() despierta a otro hilo que estuviera esperando para mover los enemigos.

## 🔹 Mutex (Lock)

Un mutex (mutual exclusion lock) garantiza que solo un hilo acceda a la lista enemigos al mismo tiempo.
```bash
mutex = threading.Lock()
condicion = threading.Condition(mutex)
```
Dentro del juego, esto evita que los hilos de generación y movimiento de enemigos colisionen al manipular la misma lista.

## 🔹 Condition Variable

Una variable de condición (Condition) permite que un hilo espere un evento antes de continuar.
En este caso, el hilo que mueve los enemigos espera hasta que haya enemigos disponibles:
```bash
with condicion:
    while not enemigos:
        condicion.wait()  # El hilo se duerme hasta que haya nuevos enemigos
    for e in enemigos:
        e.move_ip(0, 5)
```
Cuando otro hilo genera un nuevo meteorito, lo notifica:
```bash
with condicion:
    enemigos.append(...)
    condicion.notify()  # Despierta al hilo que estaba esperando
```
## 🎵 Multimedia
El juego incorpora
- Imagen de fondo
- Sprite del jugador
- Sprite del enemigo
- Música retro
La música se reproduce en bucle continuo y se pausa automáticamente cuando el juego se detiene.

## 🎮 Controles
⬅️ Mover nave hacia la izquierda 
➡️ Mover nave hacia la derecha
P Pausar el juego

## ⚙️ Conceptos destacados
- Programación concurrente con hilos
- Protección de secciones críticas con Lock.
- Comunicación entre hilos con Condition.
- Integración de multimedia: imágenes, sonido y gráficos 2D
- Control de pausa sincronizada entre lógica y música
 ---
 
## 🧩 Resumen de Concurrencia

| Concepto | Implementación en el código | Función principal |
|-----------|-----------------------------|-------------------|
| **Recurso compartido** | `enemigos = []` | Lista global donde se almacenan los meteoritos que se generan y se mueven. |
| **Sección crítica** | Bloques `with mutex:` y `with condicion:` | Zona protegida donde los hilos acceden o modifican la lista de enemigos de forma segura. |
| **Mutex (Lock)** | `mutex = threading.Lock()` | Permite que solo un hilo a la vez entre en la sección crítica, evitando condiciones de carrera. |
| **Variable de condición (Condition)** | `condicion = threading.Condition(mutex)` | Sincroniza los hilos: uno espera (`wait()`) y otro notifica (`notify()`) cuando hay cambios en los enemigos. |
| **Espera y notificación entre hilos** | `condicion.wait()` / `condicion.notify()` | El hilo de movimiento espera hasta que el hilo generador cree nuevos enemigos. |
| **Control de pausa (estado compartido)** | Variable `pausado` | Suspende temporalmente las acciones de los hilos y la música, manteniendo coherencia en la ejecución. |
| **Thread de generación** | `threading.Thread(target=generar_enemigos, daemon=True)` | Crea nuevos meteoritos en intervalos regulares. |
| **Thread de movimiento** | `threading.Thread(target=mover_enemigos, daemon=True)` | Mueve los meteoritos hacia abajo de forma continua y concurrente. |
| **Sincronización general** | Uso combinado de `Lock` y `Condition` | Garantiza que no haya acceso simultáneo conflictivo y que los hilos se coordinen correctamente. |

--- 
##  📷 Registro fotográfico

![Image](https://github.com/user-attachments/assets/79b86b02-7acd-4687-8285-d7c58a2ab98a)
![Image](https://github.com/user-attachments/assets/5846d5ae-9b42-4409-a47d-26e4852b78fc)
![Image](https://github.com/user-attachments/assets/c686e0b3-9485-4601-b557-2dcdec4b963c)
