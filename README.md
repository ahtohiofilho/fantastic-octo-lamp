# Sphere-Based Civilization Game

Personal project to explore the development of a round-based strategy game set on the surface of a sphere. The logic is 2D (tile-based, graph-like interactions), but the rendering is in 3D using modern OpenGL techniques.

This version focuses on:
- Rendering hexagon and pentagon tiles over a spherical mesh
- Color-coded biomes (ocean, desert, prairie, etc.)
- Orbital camera controls
- Modular architecture for future expansion

🚧 More updates coming soon: unit movement, border highlights, and gameplay mechanics.

## 🔧 Tech Stack

- Language: Python
- Graphics: Modern OpenGL (core profile)
- Windowing: GLFW
- Math: GLM (for vectors and matrices)
- Graph: NetworkX (for tile relationships and logic)

## 📁 Folder Structure

src/
├── main.py # Entry point and rendering loop
├── camera.py # Orbital camera system
├── shader_utils.py # Shader compilation tools
├── polygons.py # Procedural tile generation
└── geography.py # Biome assignment, graph logic, and JSON export
shaders/
├── vertex.glsl # Vertex shader
└── fragment.glsl # Fragment shader with color per tile
assets/ # Placeholder for textures/models
README.md # This file
requirements.txt # Project dependencies

## 🛠 Notes

The current version renders sphere-like maps (planets) using procedural geometry based on the concept of a Goldberg Polyhedron. Each tile has its own biome and color. The camera can orbit around the planet and zoom in/out.

Next steps include:
- Implementing tile selection via mouse input
- Adding UI elements (HUD, menus)
- Processing player actions simultaneously each round
- Introducing units and territorial dynamics

More updates coming soon.