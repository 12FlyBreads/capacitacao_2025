import numpy as np

class Sensor:
    # inicialização do sensor LiDAR
    def __init__(self, ambiente):
        """
        ambiente: instância da classe Ambiente (que define o terreno/obstáculos)
        """
        self.ambiente = ambiente
        self.leitura_atual = None

    # método para medir a altura do drone em relação ao solo
    def medir_altura(self, posicao_drone):
        """
        Simula a medição da altura em relação ao solo, usando a posição atual do drone.
        """
        x, y, z = posicao_drone  # y é a altura (eixo vertical)
        altura_terreno = self.ambiente.get_altura_terreno(x, z)
        altura = y - altura_terreno  # diferença entre drone e solo
        self.leitura_atual = max(0.0, altura)
        return self.leitura_atual

    # método para detectar obstáculos abaixo do drone
    def detectar_obstaculo(self, posicao_drone):
        """
        (Opcional) Verifica se há obstáculo logo abaixo do drone.
        """
        x, y, z = posicao_drone
        return self.ambiente.tem_obstaculo_abaixo(x, y, z)

    # método para retornar o status do sensor
    def status(self):
        """Retorna a última leitura de altura registrada."""
        return f"LiDAR: {self.leitura_atual:.2f}"

