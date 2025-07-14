from motor import Motor
from sensor import Sensor
import numpy as np

class Drone:
    # inicialização dos parametros do drone
    def __init__(self, ambiente):
        self.posicao = np.array([0.0, 0.0, 0.0])  # posição inicial do drone
        self.orientacao = {
            "pitch": 0.0,  # inclinação para frente e para trás
            "yaw": 0.0,    # rotação em torno do eixo vertical
            "roll": 0.0    # inclinação lateral
        }
        self.motores = [Motor(i) for i in range(4)]  # cria 4 motores

        # inicializa com as potências dos motores
        self.potencia_base = 0.0

        # inicializa o sensor
        self.sensor = Sensor(ambiente)  # altura do solo padrão

        self.velocidade = np.array([0.0, 0.0, 0.0]) # velocidade inicial do drone

    # comandos de controle do drone
    def aplicar_comandos(self, pitch, roll, yaw, throttle, yaw_offset):
        """
        Define os comandos de controle do drone.
        :param pitch: Inclinação para frente e para trás
        :param roll: Inclinação lateral
        :param yaw: Rotação em torno do eixo vertical
        :param throttle: Potência total aplicada aos motores
        """
        # orientação do drone é atualizada com base nos comandos
        self.orientacao["yaw"] = yaw % 360  # mantém o yaw entre 0 e 360 graus
        self.orientacao["pitch"] = pitch
        self.orientacao["roll"] = roll
        self.orientacao["throttle"] = throttle
        self.orientacao["yaw_offset"] = yaw_offset
        
        self.potencia_base = self.posicao[1]
        
        # distribui a potência entre os motores
        potencias = self.motor_mixing(pitch, roll, yaw, throttle, yaw_offset)

        for i in range(4):
            self.motores[i].ligar()  # liga o motor
            self.motores[i].set_potencia(potencias[i])  # define a potência do motor

    # potencia dos motores
    def motor_mixing(self, pitch, roll, yaw, throttle, yaw_offset):
        """
        Calcula a potência para cada motor com base nos comandos de controle.
        :param pitch: Inclinação para frente e para trás
        :param roll: Inclinação lateral
        :param yaw: Rotação em torno do eixo vertical
        :param throttle: Potência total aplicada aos motores
        :return: Lista de potências para cada motor
        """

        base = self.potencia_base  # base de potência do motor

        # Mistura de motores para controlar o drone
        self.front_left = base - pitch + roll - yaw_offset 
        self.front_right = base - pitch - roll + yaw_offset
        self.back_left = base + pitch + roll + yaw_offset
        self.back_right = base + pitch - roll - yaw_offset

        """
        Movimentos do drone:
        - Pitch positivo: Inclina para frente (motores traseiros mais potentes)
        - Pitch negativo: Inclina para trás (motores dianteiros mais potentes)
        - Roll positivo: Inclina para a direita (motores esquerdos mais potentes)
        - Roll negativo: Inclina para a esquerda (motores direitos mais potentes)
        - Yaw positivo: Gira para a direita (motores dianteiros mais potentes e traseiros mais fracos)
        - Yaw negativo: Gira para a esquerda (motores traseiros mais potentes e dianteiros mais fracos)
        - Throttle: Aumenta a potência de todos os motores, elevando o drone ou abaixando.
        """
        
        # valor entre 0.0 e 1.0 devido set_potencia
        return [max(0.0, min(10.0, x)) for x in [self.front_left, self.front_right, self.back_left, self.back_right]]

    # posicao do drone
    def atualizar_posicao(self, delta_t, obstaculos=[]):
        """
        Atualiza a posição do drone com base na orientação e potencia dos motores.
        :param delta_t: Intervalo de tempo para atualização (1 segundo por padrão).
        """

        # cálculo da direção do movimento do drone
        direcao_z = self.orientacao["pitch"] * np.cos(np.radians(self.orientacao["yaw"])) + self.orientacao["roll"] * np.sin(np.radians(self.orientacao["yaw"]))
        direcao_x = self.orientacao["pitch"] * np.sin(np.radians(self.orientacao["yaw"])) - self.orientacao["roll"] * np.cos(np.radians(self.orientacao["yaw"]))
        direcao_y = self.orientacao["throttle"]  # Throttle afeta a altura (eixo Y)

        # ajuste da posição conforme a velocidade
        self.velocidade += np.array([direcao_x, direcao_y, direcao_z]) * 1.0 # # fator de escala para velocidade
        nova_posicao = self.posicao + self.velocidade * delta_t # # atualiza a posição com base na velocidade e no tempo delta
        self.velocidade = np.array([0.0, 0.0, 0.0])  # reset da velocidade após atualização

        """        Atualização da posição:
        - A velocidade é atualizada com base na orientação do drone.
        - A posição é atualizada com base na velocidade.
        - Roll = lateral (x), Pitch = frente/trás (z), Throttle = vertical (y).
        """

         # Verifica colisão com obstáculos
        for obs in obstaculos:
            distancia = np.linalg.norm(nova_posicao - obs["centro"])
            if distancia < obs["raio"] + 0.2:  # margem de segurança
                print("COLISAO DETECTADA")
                return  # colisão detectada, não move

        # Atualiza a posição se não houver colisão
        self.posicao = np.clip(nova_posicao, 0, 10)

    # print dos status do drone
    def status(self):
        """
        Retorna o status do drone, incluindo posição, orientação e status dos motores.
        :return: String com o status do drone.
        """
        motor_status = "\n".join(motor.get_status() for motor in self.motores)
        return (f"Posição: {self.posicao}\n"
                f"Orientação: {self.orientacao}\n"
                f"Motores:\n{motor_status}")
        


