Projeto de capacitação de Python idealizado pela equipe Black Bee Drones.
Esse projeto contém no arquivo principal (simulacao.py) uma representação 3d simples do funcionamento básico de um drone. Apesar da simplificação geral de muitos aspectos comuns presentes nos testes reais (gravidade, resistencias e etc) o programa contém dados sobre a potência dos motores simplificada do drone, e sua posição no espaço 3d, além dos dados de altura gerados pelo sensor LiDAR.
A movimentação do objeto na simulação é realizado pelas teclas:
'W' - frente
'S' - tras
'A' - esquerda
'D' - direita
'Z' - cima
'X' - baixo
'Q' - virar a esquerda
'E' - virar a direita

- Drone.py

Classe principal do objeto drone. Contém as seguintes funções:

__init__(self, ambiente): inicialização do objeto drone com a passagem de parametros do ambiente 3d gerado.
aplicar_comandos(self, pitch, roll, yaw, throttle, yaw_offset): aplica os comandos enviados pelas teclas e chamaa as funções de movimento e potencia dos motores.
motor_mixing(self, pitch, roll, yaw, throttle, yaw_offset): calculo das potências dos 4 motores.
atualizar_posicao(self, delta_t, obstaculos[]): calculo da posição na simulação 3d. Parametro delta_t altera a taxa de atualização do drone (velocidade), e parametro obstaculos serve para enviar os obstaculos com colisão para o cálculo do drone.
status(self): status do drone.

- Motor.py

  Classe dos motores do drone. COntém as seguintes funções:

  __init__(self): inicialização do motor.
  ligar(self): liga o motor.
  desligar(self): desliga o motor.
  set_potencia(self, valor): recebe um float e altera a potência do motor.
  get_status(self): status do motor.

  - Sensor.py
 
    Classe do sensor LiDAR. Contém as seguintes funções:

    __init__(self, ambiente): inicialização do sensor juntamente com o ambiente.
    medir_altura(self, posicao_drone): altura do drone em relação ao objeto abaixo.
    detectar_obstaculos(self, posicao_drone): detecta see há um obstaculo abaixo do drone.
    status(self): status do sensor.

    - Simulacao.py
   
    Arquivo principal contendo a função main responsavel por simular o drone. Caso queira ver a simulação em funcionamento, buildar e compilar este arquivo.
