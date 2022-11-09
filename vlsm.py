# Network Calculator
#Daniel Felipe Alzate Mateus
#Juan David Robledo Garzon
#Manuel Felipe Sanchez Avella 
import ipaddress as ip

def menu():
    print(
    "+------------------------------------------+\n"
    "|  Bienvenido a la calculadora VLSM.       |\n"
    "|  Escribe \"help\" para ver los comandos.   |\n"
    "+------------------------------------------+\n") 
    print("Escribe aqui :) ", end="")
    entrada = input()
    entradaVec = entrada.split(" ")
    if (entradaVec[0] == "help"):
        help()
    elif (entradaVec[0] == "infoRed"):
        infoRed(entradaVec[1:])
    elif (entradaVec[0] == "vlsm"):
        vlsm(entradaVec[1:])
    elif (entradaVec[0] == "exit"):
        quit()
    elif (entradaVec[0] == ""):
        pass
    else:
        print("Comando Invalido")


def help():
    print(".:Comandos de Calculadora VLSM:.\n"
        "<help> - Ver la lista de comandos.\n"
        "<infoRed> <DireccionIP/Mascara> - Ver informacion sobre la red.\n"
        "<vlsm> <DireccionRed/Mascara> <#Hosts1> <#Hosts2> ... (Descendiente)- Dividir las redes en las subredes solicitadas\n"
        "<exit> - Finalizar calculador VLSM")
    print()


def obtenerBytesSubRed(x): #Obtiene el log
    n = 0
    while ((2**n - 2) < x):
        n = n+1
    return 32 - n


def vlsm(args):
    if (len(args) < 2):
        print("Sintaxis Invalida")
        return None
    ipsplit = args[0].split("/")
    try:
        dire = ip.ip_address(ipsplit[0])
        
    except ValueError:
        print("Direccion Invalida")
        return None
    try:
        masca = mask(dire, ipsplit[1])
    except ValueError:
        print("Mascara Invalida")
        return None 
    if(dire != ip.ip_address(int(dire) & int(masca))): #Comprobar que sea una direccion de red
        print("Direccion Invalida")
        return None
    subreds = []

    args.pop(0)
    for i in args: #Agrega los host en las subreds
        try:
            subreds.append(int(i)) 
        except:
            print("SubRed Invalida")

    if ((int(broadcast(dire, masca)) - int(dire)) < sum(subreds)): 
        print("Muchos host en la SubRed")
        return None
    j = 1
    last = dire
    for i in subreds:
        x = obtenerBytesSubRed(i)
        newmask = '' #mascara de red de cada sub red en binario
        for i in range(0, x):
            newmask += '1'
        for i in range(0, 32 - len(newmask)):
            newmask += '0'
        print("subred " + str(j) + ": ")
        print(ip.ip_address(last))
        redData(ip.ip_address(last), ip.ip_address(int(newmask, base=2)))

        last = int(broadcast(ip.ip_address(last), ip.ip_address(int(newmask, base=2)))) + 1
        j = j+1


def infoRed(args):
    if (len(args) != 1):
        print("Sintaxis Invalida")
        return None
    ipsplit = args[0].split("/")
    try:
        dire = ip.ip_address(ipsplit[0])
    except ValueError:
        print("Direccion Invalida")
        return None
    try:
        masca = mask(dire, ipsplit[1])
    except ValueError:
        print("Mascara Invalida")
        return None
    except:
        print("Ocurrio un error desconocido :(")
        return None

    dire_red = ip.ip_address(int(dire) & int(masca))
    redData(dire_red, masca)


def mask(s,m):
    masca_int = int(m)
    if (masca_int < 0 or masca_int >= 32):
        print("Mascara Invalida")
        return None
    masca_str = ""
    for i in range (0, masca_int):
        masca_str += "1"
    for i in range (masca_int, 32):
        masca_str += "0"
    masca_bin = int(masca_str, base=2) #crea la mascara de sub red y la pasa a binario
    masca = ip.ip_address(masca_bin)
    return masca


def broadcast(s,m):
    return ip.ip_address((int(s)-int(m)-1) + 2 ** 32)


def redData(s, m):
    b = broadcast(s,m)
    print("Direccion de Red:     " + str(s))
    print("Mascara de SubRed:    " + str(m))
    print("Direccion Broadcast:  " + str(b))
    print("Numero de Host:       " + str(int(b) - int(s) - 1))
    print()


while (True):
    menu()