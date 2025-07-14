import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from drone import Drone  # Usa sua classe Drone já criada

# ambiente para o drone

class Ambiente:
    def __init__(self, obstaculos=None):
        self.terreno_base = 0.0  # altura padrão do chão
        self.obstaculos = obstaculos if obstaculos is not None else []

    def get_altura_terreno(self, x, z):
        """
        Retorna a altura do terreno na coordenada (x, z).
        Se houver um obstáculo logo abaixo, retorna a altura do obstáculo.
        """
        altura_maxima = self.terreno_base

        for obs in self.obstaculos:
            xc, yc, zc = obs["centro"]
            raio = obs["raio"]

            # verifica se o drone está acima da projeção do obstáculo no plano xz
            if (x - xc)**2 + (z - zc)**2 <= raio**2:
                # se estiver acima, considerar o topo do obstáculo como solo
                if yc + raio > altura_maxima:
                    altura_maxima = yc + raio

        return altura_maxima 

# === Janela Principal ===
root = tk.Tk()
root.title("Simulador de Drone 3D e Motores")

# === Área Gráfica 3D ===
fig = plt.figure(figsize=(5, 4))
ax = fig.add_subplot(111, projection='3d')
ax.view_init(elev=15, azim=260)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_zlim(0, 10)
ax.set_xlabel("X")
ax.set_ylabel("Z")
ax.set_zlabel("Y (Altura)")
drone_visual, = ax.plot([0], [0], [0], 'ko', markersize=4)
drone_x_axis, = ax.plot([0, 0], [0, 0], [0, 0], 'r-')  # eixo X (vermelho)
drone_y_axis, = ax.plot([0, 0], [0, 0], [0, 0], 'g-')  # eixo Y (verde)
drone_z_axis, = ax.plot([0, 0], [0, 0], [0, 0], 'b-')  # eixo Z (azul)
canvas_3d = FigureCanvasTkAgg(fig, master=root)
canvas_3d.draw()
canvas_3d.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

# Personalização visual
ax.grid(False)
fig.patch.set_facecolor('black')
ax.set_facecolor('black')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.zaxis.label.set_color('white')
ax.tick_params(colors='white')


# === Área de Visualização 2D dos Motores ===
canvas_2d = tk.Canvas(root, width=350, height=350, bg="black")
canvas_2d.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# === Ambiente ===
obstaculos = [
    {"centro": np.array([3.0, 2.0, 5.0]), "raio": 1.0},
    {"centro": np.array([7.0, 7.0, 3.0]), "raio": 1.5},
    {"centro": np.array([5.0, 4.0, 7.0]), "raio": 0.8}
]
ambiente = Ambiente(obstaculos=obstaculos)

# === Drone ===
drone = Drone(ambiente)  # Sua classe Drone implementada previamente

# === Comandos ===
comandos = {"pitch": 0.0, "roll": 0.0, "yaw": 0.0, "throttle": 0.0, "yaw_offset": 0.0}

# === Teclado ===
def tecla_pressionada(event):
    tecla = event.keysym
    if tecla == 'w': comandos["pitch"] = 1.0
    elif tecla == 's': comandos["pitch"] = -1.0
    elif tecla == 'a': comandos["roll"] = 1.0
    elif tecla == 'd': comandos["roll"] = -1.0
    elif tecla == 'z': comandos["throttle"] = 1.0
    elif tecla == 'x': comandos["throttle"] = -1.0
    elif tecla == 'q': comandos["yaw"] -= 5; comandos["yaw_offset"] = -1.0
    elif tecla == 'e': comandos["yaw"] += 5; comandos["yaw_offset"] = 1.0

def tecla_liberada(event):
    tecla = event.keysym
    if tecla in ['w', 's']: comandos["pitch"] = 0.0
    elif tecla in ['a', 'd']: comandos["roll"] = 0.0
    elif tecla in ['z', 'x']: comandos["throttle"] = 0.0
    elif tecla in ['q', 'e']: comandos["yaw_offset"] = 0.0

# === Função para desenhar uma esfera ===
def desenhar_esfera(ax, centro, raio, cor='red', alpha=0.3, resolucao=30):
    u, v = np.mgrid[0:2 * np.pi:resolucao*4j, 0:np.pi:resolucao*2j]
    x = centro[0] + raio * np.cos(u) * np.sin(v)
    y = centro[1] + raio * np.sin(u) * np.sin(v)
    z = centro[2] + raio * np.cos(v)
    ax.plot_surface(x, y, z, color=cor, alpha=0.8, edgecolor='none')

# === Obstáculos ===
obstaculo = [
    {"centro": [3, 5, 2], "raio": 1.0, "cor": "red"},
    {"centro": [7, 3, 7], "raio": 1.5, "cor": "blue"},
    {"centro": [5, 7, 4], "raio": 0.8, "cor": "green"}
]

for obs in obstaculo:
    desenhar_esfera(ax, obs["centro"], obs["raio"], cor=obs["cor"])

# === Loop de Atualização ===
def atualizar():
    drone.aplicar_comandos(
        comandos["pitch"], comandos["roll"], comandos["yaw"], comandos["throttle"], comandos["yaw_offset"]
    )
    drone.atualizar_posicao(0.1, obstaculos=obstaculos)
    drone.sensor.medir_altura(drone.posicao)

    # === Atualiza Visualização 3D ===
    x, y, z = drone.posicao
    drone_visual.set_data([x], [z])
    drone_visual.set_3d_properties([y])

    # Tamanho das setas dos eixos
    eixo = 2.0  # comprimento das linhas

    # Eixo X (vermelho): girado no plano XZ com yaw
    dx = np.cos(np.radians(drone.orientacao["yaw"])) * eixo
    dz = -np.sin(np.radians(drone.orientacao["yaw"])) * eixo

    # Eixo Z (azul): 90° à frente do X (ou -90° do yaw)
    dx_z = np.sin(np.radians(drone.orientacao["yaw"])) * eixo
    dz_z =  np.cos(np.radians(drone.orientacao["yaw"])) * eixo

    # Atualiza os eixos locais do drone
    drone_x_axis.set_data([x, x + dx], [z, z + dz])
    drone_x_axis.set_3d_properties([y, y])  # linha no eixo X

    drone_y_axis.set_data([x, x], [z, z])
    drone_y_axis.set_3d_properties([y, y + eixo])  # linha no eixo Y

    drone_z_axis.set_data([x, x + dx_z], [z, z + dz_z])
    drone_z_axis.set_3d_properties([y, y])  # linha no eixo Z

    ax.set_title(f"X={x:.2f} | Y={y:.2f} | Z={z:.2f} | Yaw={drone.orientacao['yaw']:.2f}")
    canvas_3d.draw()

    # === Atualiza Canvas 2D ===
    canvas_2d.delete("all")
    r = 40
    cx, cy = 175, 175
    posicoes = [(-60, -60), (60, -60), (-60, 60), (60, 60)]
    for i, (dx, dy) in enumerate(posicoes):
        cor = "#ff00aa"
        p = drone.motores[i].potencia if hasattr(drone.motores[i], 'potencia') else drone.motores[i]
        canvas_2d.create_oval(cx+dx-r, cy+dy-r, cx+dx+r, cy+dy+r, fill=cor)
        canvas_2d.create_text(cx+dx, cy+dy, text=f"M{i+1}: {p:.2f}", fill="white")

    canvas_2d.create_text(175, 10, text=f"Yaw: {drone.orientacao['yaw']:.1f}", fill="white")
    canvas_2d.create_text(175, 30, text=f"Pos: X={x:.2f}, Y={y:.2f}, Z={z:.2f}", fill="white")
    canvas_2d.create_text(175, 50, text=drone.sensor.status(), fill="white")

    root.after(50, atualizar)

# === Eventos ===
root.bind("<KeyPress>", tecla_pressionada)
root.bind("<KeyRelease>", tecla_liberada)
root.after(100, atualizar)
root.mainloop()
