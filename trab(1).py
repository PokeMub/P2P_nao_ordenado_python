import random
import socket
import sys
import _thread
import os
import json
import time

PORT = 12345
node = {
    "id": None,
    "ip": sys.argv[1],
    "id_antecessor": None,
    "ip_antecessor": None,
    "id_sucessor": None,
    "ip_sucessor": None
}
def servidor(udp: socket.socket):
    while True:
        data = udp.recv(1024).decode("utf-8")
        data_converted = json.loads(data)
        opc = data_converted['codigo']
        if opc == 0:
            antt = data_converted['id']
            anttt = data_converted['ip']
            mensagem = {}
            mensagem ['codigo'] = 64
            mensagem ['identificador'] = antt
            mensagem ['id_sucessor'] = node['id']
            mensagem ['ip_sucessor'] = node['ip']
            mensagem ['id_antecessor'] = node['id_antecessor']  
            mensagem ['ip_antecessor'] = node['ip_antecessor']                
            msg_json = json.dumps(mensagem)
            udp.sendto(msg_json.encode("utf-8"), (anttt,12345))           
        elif opc == 1:
            ant = data_converted['identificador']
            antt = data_converted['id_sucessor']
            anttt = data_converted['ip_sucessor']
            antttt = data_converted['id_antecessor']
            anttttt = data_converted['ip_antecessor']
            antttttt = data_converted['ip_origen']
            if ( antt == antttt):
                node["id_antecessor"] = antttt
                node["ip_antecessor"] = anttttt        
                node["id_sucessor"] = antt
                node["ip_sucessor"] = anttt
                mensagem = {}
                mensagem ['codigo'] = 65
                mensagem ['identificador'] = ant
                msg_json = json.dumps(mensagem)
                udp.sendto(msg_json.encode("utf-8"),(antttttt,12345))
            if(antt == node['id'] ):
                node["id_antecessor"] = antttt
                node["ip_antecessor"] = anttttt
                mensagem = {}
                mensagem ['codigo'] = 65
                mensagem ['identificador'] = ant
                msg_json = json.dumps(mensagem)
                udp.sendto(msg_json.encode("utf-8"),(antttttt,12345))
            elif (antttt == node['id'] ):
                node["id_sucessor"] = antt
                node["ip_sucessor"] = anttt
                mensagem = {}
                mensagem ['codigo'] = 65
                mensagem ['identificador'] = ant
                msg_json = json.dumps(mensagem)
                udp.sendto(msg_json.encode("utf-8"),(antttttt,12345))
        elif opc == 2:
            ant = data_converted['id_busca']
            antt = data_converted['ip_origem']
            anttt = data_converted['identificador']
            if(anttt != node['id']):
                mensagem = {}
                mensagem ['codigo'] = 66
                mensagem ['id_busca'] = node['id']
                mensagem ['id_origem'] = ant
                mensagem ['ip_origem'] = antt
                mensagem ['id_sucessor'] = node['id']
                mensagem ['ip_sucessor'] = node['ip']            
                msg_json = json.dumps(mensagem)
                udp.sendto(msg_json.encode("utf-8"),(antt,12345)) 
        elif opc == 3:
            ant = data_converted['identificador']
            if(ant == node['id']):
                antt = data_converted['id_sucessor']
                anttt = data_converted['ip_sucessor']
                node['ip_sucessor'] = anttt
                node['id_sucessor'] = antt
                mensagem = {}
                mensagem ['codigo'] = 67
                mensagem ['identificador'] = node['id_antecessor']
                msg_json = json.dumps(mensagem)
                udp.sendto(msg_json.encode("utf-8"),(node['ip_sucessor'],12345))
        elif opc == 33:
            ant = data_converted['identificador']
            if(ant == node['id']):
                antt = data_converted['id_antecessor']
                anttt = data_converted['ip_antecessor']
                node['ip_antecessor'] = anttt
                node['id_antecessor'] = antt
                mensagem = {}
                mensagem ['codigo'] = 67
                mensagem ['identificador'] = node['id_sucessor']
                msg_json = json.dumps(mensagem)
                udp.sendto(msg_json.encode("utf-8"),(node['ip_antecessor'],12345))
        elif opc == 64:            
            ant = data_converted['identificador']    
            antt = data_converted['id_sucessor']
            anttt = data_converted['ip_sucessor']
            antttt = data_converted['id_antecessor']
            anttttt = data_converted['ip_antecessor']
            if(ant == node['id']):
                node['ip_sucessor'] = anttt
                node['id_sucessor'] = antt
                node['ip_antecessor'] = anttttt
                node['id_antecessor'] = antttt
                mensagem = {}
                mensagem ['codigo'] = 3
                mensagem ['identificador'] = node['id_antecessor']
                mensagem ['id_sucessor'] = node['id']
                mensagem ['ip_sucessor'] = node['ip']
                msg_json = json.dumps(mensagem)
                udp.sendto(msg_json.encode("utf-8"),(node['ip_antecessor'],12345))
                mensagem = {}
                mensagem ['codigo'] = 33
                mensagem ['identificador'] = node['id_sucessor']
                mensagem ['id_antecessor'] = node['id']
                mensagem ['ip_antecessor'] = node['ip']
                msg_json = json.dumps(mensagem)
                udp.sendto(msg_json.encode("utf-8"),(node['ip_sucessor'],12345))  
        elif opc == 65:
            ant = data_converted['identificador']
            if( node['id'] == ant ):
                node['id_antecessor'] = node['id']
                node['ip_antecessor'] = node['ip']
                node['id_sucessor'] = node['id']
                node['ip_sucessor'] = node['ip']
        elif opc == 66:
            ant = data_converted['id_busca']
            antt = data_converted['id_origem']
            anttt = data_converted['ip_origem']
            antttt = data_converted['id_sucessor']
            anttttt = data_converted['ip_sucessor']
            if( antt == node['id'] ):
                print('lookp realizado com sucesso')
                mensagem = {}
                mensagem ['codigo'] = 0
                mensagem ['id'] = node['id']
                mensagem['ip'] = node['ip']
                msg_json = json.dumps(mensagem)
                udp.sendto(msg_json.encode("utf-8"),(anttttt,12345))
        elif opc == 67:
            ant= data_converted['identificador']
            print('tudo certo! Atualizado com sucesso')
        elif opc == 90:
            print(f" Id: {node['id']}" )
            print(f" Ip:{node['ip']}")
            print(f" Id antecessor:{node['id_antecessor']}")
            print(f" Ip antecessor :{node['ip_antecessor']}")
            print(f" Id sucessor:{node['id_sucessor']} ")
            print(f" Ip sucessor:{node['ip_sucessor']}")
def main():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind(("", PORT))
    _thread.start_new_thread(servidor,(udp,))
    opc = None  
    while opc != "6":   
        print("######################################")
        print("# 1 - Gerar node ID ")
        print("# 2 - Iniciar rede P2P (no inicial)")
        print("# 3 - Entrar em uma rede P2P ")
        print("# 4 - Sair da rede P2P")
        print("# 5 - Mostrar informacoes do No")
        print("# 6 - Sair da aplicacao")
        print("#####################################")
        opc = input('digite sua opc:')
        if opc == "1":
            os.system('clear') or None
            node['id'] = random.randrange(1, 1000)
            print('Id Sorteado: ', node['id'])
        elif opc == "2":
            node['id_antecessor'] = node['id']
            node['id_sucessor'] = node['id']
            node['ip_antecessor'] = node['ip']
            node['ip_sucessor'] = node['ip']    
            os.system('clear') or None     
        elif opc == "3":
            os.system('clear') or None
            mensagem = {}
            mensagem ['codigo'] = 2
            mensagem ['identificador'] = node['id']
            mensagem ['ip_origem'] = node['ip']
            mensagem ['id_busca'] = node['id'] 
            msg_json = json.dumps(mensagem)
            udp.sendto(msg_json.encode("utf-8"), (sys.argv[2], 12345))
            time.sleep(2)
        elif opc == '4':
            os.system('clear') or None
            if (node['id'] == node['id_sucessor'] & node['id'] == node['id_antecessor']):
                print('Vc ja e a unica pessoa da rede')
            else:
                mensagem = {}
                mensagem ['codigo'] = 1
                mensagem ['identificador'] = node['id_sucessor']
                mensagem ['ip_origen'] = node['ip']
                mensagem ['id_sucessor'] = node['id_sucessor']
                mensagem ['ip_sucessor'] = node['ip_sucessor']
                mensagem ['id_antecessor'] = node['id_antecessor']
                mensagem ['ip_antecessor'] = node['ip_antecessor']
                msg_json = json.dumps(mensagem)
                udp.sendto(msg_json.encode("utf-8"), (node['ip_sucessor'],12345))
                mensagem = {}
                mensagem ['codigo'] = 1
                mensagem ['identificador'] = node['id_antecessor']
                mensagem ['ip_origen'] = node['ip']
                mensagem ['id_sucessor'] = node['id_sucessor']
                mensagem ['ip_sucessor'] = node['ip_sucessor']
                mensagem ['id_antecessor'] = node['id_antecessor']
                mensagem ['ip_antecessor'] = node['ip_antecessor']
                msg_json = json.dumps(mensagem)
                udp.sendto(msg_json.encode("utf-8"), (node['ip_antecessor'],12345))

                mensagem = {}
                mensagem ['codigo'] = 65
                mensagem ['identificador'] = node['id']
                msg_json = json.dumps(mensagem)
                udp.sendto(msg_json.encode("utf-8"),(node['ip'],12345))
        elif opc == "5":
            os.system('clear') or None
            mensagem = {}
            mensagem ['codigo'] = 90
            msg_json = json.dumps(mensagem)
            udp.sendto(msg_json.encode("utf-8"), (node['ip'],12345))
            time.sleep(2)            
    os.system('clear') or None
if __name__ == "__main__":
    main()