class Motor:
    # inicialização dos parametros do motor
    def __init__(self, motor_id : int):
        self.id = motor_id
        self.potencia = 0.0
        self.estado = "desligado"

    # arma o drone
    def ligar(self):
        self.estado = "ligado"
    
    # desligar o motor
    def desligar(self):
        self.estado = "desligado"
        self.potencia = 0.0

    # muda a potencia do motor
    def set_potencia(self, valor: float):
        # valor deve estar entre 0.0 e 10.0
        if 0.0 <= valor <= 10.0:
            self.potencia = valor
        else:
            raise ValueError("Potência deve estar entre 0.0 e 1.0")
        
    # print status do motor
    def get_status(self):
        return f"Motor {self.id}: {self.estado} com potência {self.potencia:.2f}"
