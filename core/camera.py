# core/camera.py

import glm

class CameraOrbital:
    def __init__(self, center=(0.0, 0.0, 0.0), radius=10.0, pitch=20.0, yaw=0.0):
        self.center = glm.vec3(center)
        self.radius = radius  # distância do centro
        self.pitch = pitch    # ângulo vertical
        self.yaw = yaw        # ângulo horizontal
        self.speed = 0.5      # velocidade de rotação e zoom
        self.position = glm.vec3(0.0, 0.0, 0.0)

        # Atualiza posição inicial
        self.update()

    def update(self):
        """Atualiza a posição da câmera com base no pitch/yaw/radius"""
        self.position.x = self.center.x + self.radius * glm.cos(glm.radians(self.pitch)) * glm.cos(glm.radians(self.yaw))
        self.position.y = self.center.y + self.radius * glm.sin(glm.radians(self.pitch))
        self.position.z = self.center.z + self.radius * glm.cos(glm.radians(self.pitch)) * glm.sin(glm.radians(self.yaw))

    def get_view_matrix(self):
        """Retorna a matriz de view (glm.lookAt)"""
        return glm.lookAt(self.position, self.center, glm.vec3(0.0, 1.0, 0.0))

    def get_projection_matrix(self, width, height):
        """Retorna a matriz de projeção perspectiva"""
        aspect = width / height if height != 0 else 1
        return glm.perspective(glm.radians(60.0), aspect, 0.1, 1000.0)