Pontificia Universidad Católica del Ecuador
Sede Esmeraldas

Escuela de Sistemas
Ingeniería en T.I.

Programación Estructurada y Funcional
2025-II

Gregory Joel Cedeño Barreiro
20/01/2026


<img width="796" height="782" alt="image" src="https://github.com/user-attachments/assets/dca84342-823e-42e9-8523-ae4a0c144c4a" />

## Paradigma utilizado

El proyecto usa principalmente Programación Orientada a Objetos (POO).  
Motivo: el juego modela entidades con estado y comportamiento propio (jugador, barriles, llamas, martillos, puentes y escaleras). Cada entidad se representa mediante una clase (por ejemplo `Player`, `Barrel`, `Flame`, `Hammer`, `Bridge`, `Ladder`) que encapsula sus propiedades y métodos (actualizar, dibujar, colisiones). Además hay un bucle principal y funciones utilitarias —por lo que hay también elementos de programación estructurada— pero la parte central y la elección del diseño se basan en OOP para facilitar la extensión y el mantenimiento.

---

## Instrucciones de instalación y ejecución

Requisitos mínimos:
- Python 3.8+ (recomendado 3.10+)
- pip

Pasos:

1. Clona el repositorio:
   ```
   git clone https://github.com/Gregory317/Donkey-Kong-in-Python.git
   cd Donkey-Kong-in-Python
   ```

2. (Opcional pero recomendado) crea y activa un entorno virtual:
   - Linux / macOS:
     ```
     python -m venv venv
     source venv/bin/activate
     ```
   - Windows (PowerShell):
     ```
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```

3. Instala pygame:
   ```
   pip install pygame
   ```

4. Ejecuta el juego:
   ```
   python GameDonkeyKong/Main.py
   ```

Notas:
- Si tienes problemas con la ventana o la inicialización de SDL, asegúrate de tener las bibliotecas del sistema necesarias para pygame instaladas (depende de tu plataforma).
- El juego asume que las imágenes están en `GameDonkeyKong/PythonDonkeyKong-Main/assets/images/...`. Mantén la estructura original de carpetas.

---

## Controles

- Flecha derecha / izquierda: moverse
- Barra espaciadora: saltar (solo si estás en el suelo)
- Flecha arriba / abajo: subir/bajar escaleras (cuando sea posible)
- En pantalla "Game Over": `R` para reiniciar, `Q` para salir

---

## Explicación rápida del código

Estructura principal:
- `GameDonkeyKong/Main.py` contiene la lógica del juego, carga de recursos y el bucle principal.

Funciones importantes:
- `splash_screen()` / `wait_for_key()` — Pantalla inicial con instrucciones y espera a que el jugador presione una tecla.
- `reset()` — Reinicia el estado del jugador, elimina sprites (barriles, llamas, martillos) y reconfigura variables para comenzar una vida nueva o reiniciar tras perder.
- `game_over_screen()` / `game_over()` — Muestran la pantalla de fin y permiten reiniciar o salir.
- `draw_screen()` — Crea y dibuja puentes y escaleras del nivel actual; devuelve listas de rects para colisiones.
- `draw_extras()` — Dibuja la HUD (score, lives, bonus), a Peach, el bidón de aceite, barriles estacionarios y Donkey Kong.
- `draw_oil()`, `draw_barrels()`, `draw_kong()` — Sub-funciones para elementos decorativos y mecánicas (p. ej. bidón de aceite que genera fuego).
- `spawn_barrel_from_kong()` — Genera un nuevo `Barrel` desde la posición de Donkey Kong.
- `check_climb()` — Determina si el jugador puede subir/bajar por una escalera y actualiza su estado.
- `barrel_collide()` — Detecta colisiones entre barriles y el jugador; aplica daño o puntaje por pasar por encima.
- `check_victory()` — Revisa si el jugador alcanzó el área objetivo para ganar el nivel y muestra la pantalla de victoria.

Clases principales:
- `Player` — Representa al jugador:
  - Atributos: posición, velocidad, rect/hitbox, estado (saltando, escalando, martillo activo), dirección.
  - Métodos: `update()` (física, animación, estado), `draw()` (selección de sprite y render), `calc_hitbox()`.

- `Barrel` — Barril rodante:
  - Atributos: rect, velocidad horizontal persistente `x_dir`, caída, bottom rect para detectar plataformas, `bounce_cooldown`.
  - Métodos: `update(fire_trig)` (gravedad, movimiento persistente, rebotes en bordes, animación), `check_fall()` (probabilidad de caer por escalera), `draw()`.

- `Flame` — Fireball (llama/bola de fuego):
  - Se mueve con patrones (cambia dirección cada cierto tiempo), puede trepar escaleras con cierta probabilidad, y aplica colisión con el jugador.

- `Hammer` — Power-up:
  - Si el jugador lo recoge, activa estado `player.hammer` por un tiempo limitado y permite destruir barriles.

- `Bridge` — Dibuja una sección de plataforma y devuelve un rect para colisiones.
- `Ladder` — Dibuja una escalera y devuelve un rect que sirve para comprobar escalado.

Sprites y grupos:
- Se usan `pygame.sprite.Group()` para `barrels`, `flames` y `hammers`. Esto facilita actualización/dibujo en bloque y eliminación de objetos.

Bucle principal:
- Actualiza contador/bonus, dibuja el mundo, actualiza sprites (barriles, llamas), comprueba colisiones (barriles/llamas con jugador), respawn de barriles desde Donkey Kong, maneja eventos de teclado y gestiona estados de victoria/derrota.

---

Si quieres, puedo:
- Preparar un archivo README.md listo para añadir al repositorio (con este contenido).
- Proponer un pequeño script para tomar automáticamente una captura al ejecutar.
- Revisar puntos concretos del código y proponer correcciones o mejoras (p. ej. manejo de sonidos, organización en módulos, tests).
