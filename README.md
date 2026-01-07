# 🎮 Pokémon Demo Pygame

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-Community-green?logo=pygame&logoColor=white)
![Status](https://img.shields.io/badge/Status-Educational-orange)

Un motor de juego RPG estilo Pokémon desarrollado en Python utilizando la librería **Pygame**. Este proyecto es una demostración técnica que implementa las mecánicas fundamentales de exploración, interacción con NPCs y un sistema de combate por turnos completo.

---

## 📋 Características Principales

### 🌍 Exploración y Mundo
*   **Motor de Tiles:** Carga y renderizado de mapas creados en **Tiled (.tmx)** utilizando la librería `pytmx`.
*   **Cámara Dinámica:** Sistema de cámara que sigue al jugador manteniéndolo centrado en el mapa.
*   **Colisiones:** Sistema preciso de colisiones con objetos, capas de bloqueo y bordes del mapa.
*   **Animaciones:** Sprites animados multidireccionales para el jugador y NPCs.

### ⚔️ Sistema de Combate
*   **Batallas por Turnos:** Ciclo de combate clásico (Jugador vs IA).
*   **Mecánicas de Daño:** Cálculo basado en estadísticas (Atq/Def/Vel), Nivel, Potencia y **Tabla de Tipos Elemental** (Fuego, Agua, Planta, Roca, Tierra, Normal).
*   **Gestión de Equipo:**
    *   Selección de ataques con gestión de PP (Puntos de Poder).
    *   Cambio de Pokémon (Switch) durante la batalla.
    *   IA básica para el enemigo (selección aleatoria).
*   **UI de Batalla:** Barras de vida (HP) dinámicas, sprites (Front/Back) y caja de texto de eventos.

### ⚙️ Arquitectura y Datos
*   **Data Driven:** Estadísticas, sprites y movimientos se cargan desde archivos **JSON**, facilitando la expansión sin modificar el código fuente.
*   **Gestor de Diálogos:** Sistema robusto para interactuar con NPCs, soportando textos paginados y eventos.
*   **Máquina de Estados:** Gestión limpia de transiciones entre Título, Mapa, Batalla, Menú y Game Over.

---

## 🛠️ Requisitos Técnicos

El proyecto requiere **Python 3.x** y las siguientes librerías:

*   **Librerías Externas:**
    *   `pygame`: Motor gráfico, input y ventanas.
    *   `pytmx`: Procesamiento de mapas Tiled.
*   **Librerías Estándar:** `os`, `sys`, `json`, `random`.

---

## 🚀 Instalación y Ejecución

Sigue estos pasos para probar el juego en tu entorno local:

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/Wblanco0315/PokemonDemoPygame.git
    cd PokemonDemoPygame
    ```

2.  **Instalar dependencias:**
    Asegúrate de tener `pip` instalado y ejecuta:
    ```bash
    pip install pygame pytmx
    ```

3.  **Ejecutar el juego:**
    ```bash
    python main.py
    ```

---

## 🎮 Controles

| Tecla | Acción |
| :---: | --- |
| **Flechas** | Mover personaje / Navegar menús |
| **Z** | Interactuar / Aceptar / Seleccionar ataque |
| **X** | Cancelar / Volver atrás |
| **Enter** | Abrir Menú de Pausa / Iniciar juego |
| **Shift Izq** | Correr (mientras se mantiene presionado) |
| **B** | *(Debug)* Iniciar batalla instantánea de prueba |

---

## 📂 Estructura del Proyecto

El código sigue una arquitectura modular para facilitar la escalabilidad:

```text
PokemonDemoPygame/
├── main.py                 # Punto de entrada (Entry Point)
├── src/
│   ├── config.py           # Constantes (Pantalla, FPS, Colores)
│   ├── game.py             # Clase principal (Game Loop & State Machine)
│   ├── entities/           # Entidades del juego
│   │   ├── player.py       # Lógica del avatar
│   │   ├── npc.py          # Lógica de NPCs
│   │   └── pokemon.py      # Estructura de datos Pokémon
│   └── systems/            # Sistemas y Gestores
│       ├── map_manager.py  # Carga de mapas .tmx
│       ├── battle_manager.py # Lógica de combate
│       ├── dialogue.py     # Renderizado de texto
│       └── ...
└── assets/                 # Recursos multimedia
    ├── data/               # JSONs (pokedex.json, moves.json)
    ├── fonts/              # Fuentes (.ttf)
    ├── language/           # Localización (ES.json)
    ├── maps/               # Archivos Tiled (.tmx, .tsx)
    └── sprites/            # Imágenes y Spritesheets
```

---

## 📝 Créditos

*   **Desarrollo:** Wilson Blanco
*   **Recursos:**
    *   *Sprites y Tilesets:* Propiedad intelectual de Nintendo/Game Freak. Este proyecto se realiza sin ánimo de lucro y con fines **estrictamente educativos**.
