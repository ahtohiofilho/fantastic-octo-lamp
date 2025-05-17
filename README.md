# Sphere-Based Civilization Game

Personal project to explore the development of a turn-based strategy game set on the surface of a sphere. The logic is 2D (tile-based, graph-like interactions), but the rendering is in 3D using modern OpenGL techniques.

## 🎯 Current features:

- Rendering hexagon and pentagon tiles over a spherical mesh
- Color-coded biomes (`ocean`, `desert`, `prairie`, etc.)
- Orbital camera controls with zoom and rotation
- Tile selection via **mouse picking** (color-based raycasting)
- Graph-based tile relationships using NetworkX
- Modular architecture for future expansion

## 🚧 Future plans:

- [x] Highlight selected tile visually
- [ ] Implement full unit movement system
- [ ] Allow unit pathfinding and terrain cost calculation
- [ ] Add border highlights for civilizations
- [ ] HUD/UI overlay for biome info and actions
- [ ] Save/load system for persistent games

---

## 🔧 Tech Stack

- **Language:** Python
- **Graphics:** Modern OpenGL (core profile)
- **Windowing:** GLFW
- **Math:** GLM (for vectors and matrices)
- **Graph Logic:** NetworkX (for adjacency, paths, and territorial dynamics)

---

## 📁 Folder Structure

/fantastic-octo-lamp
├── main.py # Entry point and rendering loop
├── core/
│ ├── contexto.py # Global context and game state
│ ├── render.py # Main render loop and input handling
│ ├── tile.py # Manages tile data and selection
│ ├── unidade.py # Unit representation and movement
│ └── camera.py # Orbital camera system
├── utils/
│ ├── gameplay_utils.py # Placeholder for game logic and utilities
│ ├── polygons.py # Procedural tile generation
│ ├── geography.py # Biome assignment, graph logic, JSON export
│ └── shader_utils.py # Shader compilation and picking utilities
├── shaders/
│ ├── vertex.glsl # Vertex shader (shared)
│ ├── fragment.glsl # Fragment shader with per-tile color
│ ├── picking_vertex.glsl # Vertex shader for mouse picking
│ └── picking_fragment.glsl # Special fragment shader for mouse picking
├── data/
│ └── geografia.json # Generated tile data with biomes and metadata
├── requirements.txt # Python dependencies
└── README.md # This file

---

## 🛠 Features Implemented

### 🌍 Spherical World Rendering
- Based on **Goldberg Polyhedron** tiling.
- Each tile has its own position, biome, and properties (e.g., temperature, elevation).
- Efficient rendering using a single shared VAO/VBO.

### 🖱️ Mouse Interaction: Tile Selection (Picking)
- **Color-based picking**: each tile is rendered off-screen with a unique RGB color.
- On mouse click, pixel under cursor is read via glReadPixels.
- Clicked tile is highlighted visually (red transparent overlay).
- Tile biome and coordinates are printed to console.

### 🧍 Unit Representation
- Units are represented visually by a textured sprite (.png) placed over a tile.
- Sprite always faces the camera (currently flat, with billboarding ready to be added).
- Unit starts on an arbitrary tile and follows basic camera updates.

### 🕹️ Controls

|    Key    |         Action          |
|-----------|-------------------------|
| `↑ ↓ ← →` | Adjust camera pitch/yaw |
| `=` / `-` |       Zoom in/out       |
|   `ESC`   |        Quit game        |

---

## 📦 Dependencies

The project depends on the following Python packages:

- `glfw==2.9.0` – Windowing and input handling
- `networkx==3.4.2` – Graph logic for tile relationships
- `numpy==2.2.5` – Fast numerical operations
- `pillow==11.2.1` – Image loading for unit sprites and textures
- `pyglm==2.8.2` – Vector and matrix math for OpenGL rendering
- `PyOpenGL==3.1.9` – Core OpenGL bindings
- `PyOpenGL-accelerate==3.1.9` – Optimized versions of PyOpenGL components

To install all dependencies:
```bash
pip install -r requirements.txt