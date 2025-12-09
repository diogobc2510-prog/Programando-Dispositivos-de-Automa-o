import socket
from umodbus import conf
from umodbus.client.tcp import read_coils as ler_bobinas
from umodbus.client.tcp import read_discrete_inputs as ler_entradas_digitais
from umodbus.client.tcp import send_message as enviar_mensagem
from umodbus.client.tcp import read_input_registers as ler_registradores_entrada
from umodbus.client.tcp import write_multiple_registers as escrever_multiplos_registradores
from umodbus.client.tcp import write_multiple_coils as escrever_multiplas_bobinas
from umodbus.client.tcp import write_single_coil as escrever_unica_bobina 

class inversorSenai:
    def __init__ (self, endereco_escravo = 2, endereco_ip = '10.26.92.149'):
        self._estado = False;
        self._velocidade = 30;
        self._sentido_de_giro = False;
        self._endereco_escravo = endereco_escravo;
        self._endereco_ip = endereco_ip;
        self._endereco_adicionar_parar = 1100;
        self._endereco_mudar_giro = 1101;
        self._endereco_estado = 100;
        self._endereco_leitura_velocidade = 30400;
        self._endereco_corrente = 30401;
        self._endereco_tensao = 30402;
        self._endereco_temperatura = 30403;
        self._endereco_controle_velocidade = 41400;        
    
    def obter_estado(self):
        conf.SIGNED_VALUES = True       
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self._endereco_ip, 502))
    
        tcp_adu = ler_entradas_digitais(
            slave_id=self._endereco_escravo, 
            starting_address=self._endereco_estado, 
            quantity=1
        )
        response = enviar_mensagem(tcp_adu,sock)
        print(response[0])
        sock.close()
        return response[0]   
        
    def acionar_motor(self):
       conf.SIGNED_VALUES = True       
       
       sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       sock.connect((self._endereco_ip, 502))
   
       tcp_adu = escrever_multiplos_registradores(
           slave_id=self._endereco_escravo, 
           starting_address=self._endereco_controle_velocidade, 
           values = [self._velocidade]
           )
       response = enviar_mensagem(tcp_adu, sock)
       
       tcp_adu = escrever_multiplas_bobinas(
           slave_id=self._endereco_escravo, 
           starting_address=self._endereco_adicionar_parar  , 
           values = [True,self._sentido_de_giro]
           )
       response = enviar_mensagem(tcp_adu,sock)
      
       sock.close()
       
       self._estado = True
       print('Motor Acionado')
       
    def parar_motor(self):
        conf.SIGNED_VALUES = True       
          
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self._endereco_ip, 502))
      
        tcp_adu = escrever_multiplos_registradores(
              slave_id=self._endereco_escravo, 
              starting_address=self._endereco_controle_velocidade, 
              values = [self._velocidade]
              )
        response = enviar_mensagem(tcp_adu, sock)
          
        tcp_adu = escrever_multiplas_bobinas(
              slave_id=self._endereco_escravo, 
              starting_address=self._endereco_adicionar_parar  , 
              values = [False,self._sentido_de_giro]
              )
        response = enviar_mensagem(tcp_adu,sock)
         
        sock.close()
          
        self._estado = True
        print('Motor Parado')
        
    def definir_velociadede(self):
        conf.SIGNED_VALUES = True       

        velocidade_num = int(input('Escolha a velocidade (1 a 60): '))

        if velocidade_num < 1 or velocidade_num > 60:
            print("Velocidade inválida")
            return

        self._velocidade = velocidade_num  

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self._endereco_ip, 502))

    
        tcp_adu = escrever_multiplos_registradores(
           slave_id=self._endereco_escravo,
           starting_address=self._endereco_controle_velocidade,
           values=[self._velocidade]
           )
        enviar_mensagem(tcp_adu, sock)

        sock.close()
        print('Velocidade definida com sucesso.')
        
    def ler_temperatura(self):
        conf.SIGNED_VALUES = True       
        
        # Criar socket TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self._endereco_ip, 502))
    
        # Montar mensagem Modbus para ler o registrador de temperatura
        tcp_adu = ler_registradores_entrada(
            slave_id=self._endereco_escravo,
            starting_address=self._endereco_temperatura,
            quantity=1
        )
        
        # Enviar mensagem e receber resposta
        response = enviar_mensagem(tcp_adu, sock)
        sock.close()
        
        # Mostrar valor diretamente na tela
        
        print("Temperatura do inversor (valor bruto):", response[0])
        
    def ler_corrente(self):
        conf.SIGNED_VALUES = False
    
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self._endereco_ip, 502))
    
        tcp_adu = ler_registradores_entrada(
            slave_id=self._endereco_escravo,
            starting_address=self._endereco_corrente,
            quantity=1
        )
    
        response = enviar_mensagem(tcp_adu, sock)
        sock.close()
    
        print("Corrente do inversor (valor bruto):", response[0])

    def ler_tensao(self):
        conf.SIGNED_VALUES = False
    
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self._endereco_ip, 502))
    
        tcp_adu = ler_registradores_entrada(
            slave_id=self._endereco_escravo,
            starting_address=self._endereco_tensao,
            quantity=1
        )
    
        response = enviar_mensagem(tcp_adu, sock)
        sock.close()
    
        print("Tensão do inversor (valor bruto):", response[0])
        
    def giro_horario(self):
        conf.SIGNED_VALUES = True
    
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self._endereco_ip, 502))
    
        tcp_adu = escrever_multiplas_bobinas(
            slave_id=self._endereco_escravo,
            starting_address=self._endereco_adicionar_parar,
            values=[True, True]  # True para ligar motor, True para sentido horário
        )
    
        response = enviar_mensagem(tcp_adu, sock)
        sock.close()
    
        self._sentido_de_giro = True
        print("Sentido de giro definido: HORÁRIO")
        
    def giro_antihorario(self):
        conf.SIGNED_VALUES = True
    
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self._endereco_ip, 502))
    
        tcp_adu = escrever_multiplas_bobinas(
            slave_id=self._endereco_escravo,
            starting_address=self._endereco_adicionar_parar,
            values=[True, False]  # True para ligar motor, False para sentido anti-horário
        )
    
        response = enviar_mensagem(tcp_adu, sock)
        sock.close()
    
        self._sentido_de_giro = False
        print("Sentido de giro definido: ANTI-HORÁRIO")



    
inversor = inversorSenai()

#inversor.definir_ip (endereco_ip = '10.26.92.149')
#inversor.definir_escravo (endereco_escravo = 2)

num = 0 

while num!=10:
    print('1. Adicionar motor')
    print('2. Para motor')
    print('3. Definir velocidade')
    print('4. Ler temperatura')
    print('5. Ler corrente')
    print('6. Ler tensão')
    print('7. Defenir sentido de giro horário')
    print('8. Definir sentido de giro antihorário')
    print('9. Ler estado')
    print('10. Fechar aplicação')
    num = int(input('Escolha uma opção:'))
    if num == 1:
        inversor.acionar_motor()
    elif num == 2:
         inversor.parar_motor() 
    elif num == 3:
         inversor.definir_velociadede()   
    elif num == 4:
         inversor.ler_temperatura()
    elif num == 5:
        inversor.ler_corrente()
    elif num == 6:
        inversor.ler_tensao()
    elif num == 7:
        inversor.giro_horario()
    elif num == 8:
        inversor.giro_antihorario()
    elif num == 9:
        inversor.obter_estado()
    elif num == 10:
        print('Fechado aplicação')
    else:
        print('Opção não existente.Tente novamente')
        
    