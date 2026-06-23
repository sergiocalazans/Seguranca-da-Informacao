import myscapyLib as IDS

#-------------------------------------------------------------------------
# REGRA 1: DETECTAR ICMP FLOOD UMA FONTE (PING OF DEATH)
# -- uma fonte está enviando pacotes com uma taxa muito alta
# OBS. ESSE EXERCICIO ESTA RESOLVIDO PARA SERVIR COMO EXEMPLO

def detectaPoD(pacotes, limite):
    # A) filtre pacotes do tipo ICMP   
    pacotes = IDS.filtraTipo(pacotes, IDS.TIPO['icmp'])
    # B) crie o dicionário com o número de pacotes por origem
    origens = IDS.contaIPOrigem(pacotes)    
    # C) selecione os IPs cujo número de pacotes enviados excede o valor limite
    resultado = []
    for k,v in origens.items():
        if v > limite: resultado.append(k)        
    # D) gere uma mensagem de alerta para cada IP na seleção indicado que estão fazendo o ataque    
    for ip in resultado:
        IDS.alerta(f'O IP {ip} esta fazendo ICMP Flood')

#-------------------------------------------------------------------------    
# REGRA 2: DETECTAR ICMP FLOOD DE VARIAS FONTES (Distributed PING OF DEATH)
# -- um alvo está recebendo ICMP com uma taxa muito alta

def detectaDPoD(pacotes, limite):
    # A) filtre pacotes do tipo ICMP 
    pacotes = IDS.filtraTipo(pacotes, IDS.TIPO['icmp'])
    # B) crie o dicionário com o número de pacotes por destino
    destinos = IDS.contaIPDestino(pacotes)
    # C) selecione os IPs cujo número de pacotes recebidos excede o valor limite
    resultado = []
    for k,v in destinos.items():
        if v > limite: resultado.append(k)
    # D) gere uma mensagem de alerta para indicando quem está sendo atacado    
    for ip in resultado:
        IDS.alerta(f'O IP {ip} esta sendo ATACADO por ICMP Flood (DISTRIBUIDO)')

#-------------------------------------------------------------------------
# REGRA 3: DETECTAR SYN FLOOD PELA ORIGEM OU DESTINO
# -- uma fonte está enviando pacotes SYN com uma taxa muito alta
# -- uma destino está rebendo pacotes SYN com uma taxa muito alta
def detectaSYNFlood(pacotes, limite):
    # A) filtre pacotes pelo flag S do TCP
    pacotes = IDS.filtraTCP(pacotes,'S')
    # B) crie um dicionário com o número de pacotes por origem
    origens = IDS.contaIPOrigem(pacotes)
    # C) selecione os IPs cujo número de pacotes enviados excede o valor limite
    resultado = []
    for k,v in origens.items():
        if v > limite: resultado.append(k)
    # D) gere uma mensagem de alerta para cada IP na seleção indicado que estão fazendo o ataque            
    for ip in resultado:
        IDS.alerta(f'O IP {ip} esta fazendo SYN Flood')
    # E) crie o dicionário com o número de pacotes por destino
    destinos = IDS.contaIPDestino(pacotes)
    # F) selecione os IPs cujo número de pacotes recebidos excede o valor limite
    resultado = []
    for k,v in destinos.items():
        if v > limite: resultado.append(k)  
    # G) gere uma mensagem de alerta para indicando quem está sendo atacado 
    for ip in resultado:
        IDS.alerta(f'O IP {ip} esta sendo atacado por SYN Flood')

#-------------------------------------------------------------------------
# REGRA 4: DETECTAR PORT SCAN 
# -- uma fonte está enviando pacotes para diversas portas
def detectaPSCAN(pacotes, limite):
    # A) filtre pacotes pelo flag S do TCP
    pacotes = IDS.filtraTCP(pacotes, 'S')
    # B) crie um dicionário com a chave IP de origem e valor conjunto de portas de destino
    origens = {}

    for p in pacotes:
        ip = str(p[IDS.TIPO['ip']].src)
        porta = int(p[IDS.TIPO['tcp']].dport)
        # se for o primeiro pacote enviado por esse ip inicialize o conjunto com origens[ip] = {porta}
        if ip not in origens:
            origens[ip] = {porta}
        # senão adicione a porta ao conjunto existente com origens[ip].add(porta)
        else:
            origens[ip].add(porta)

    # C) selecione os IPs cujo número de portas endereçadas excede o valor limite
    resultado = []   
    for k,v in origens.items():
        if len(v) > limite: resultado.append(k)
    # D) gere uma mensagem de alerta para cada IP na seleção indicado que estão fazendo o ataque 
    for ip in resultado:
        IDS.alerta(f'O IP {ip} esta fazendo PORT SCAN')

#-------------------------------------------------------------------------
# REGRA 5: DETECTAR ATAQUE SYN ACK -- SMURF
# -- estão chegando pacotes SA de origens para nunca foi enviando S
def detectaSYNACK(pacotes, limite):
    # A) lista_SA = filtre pacotes pelo flag SA do TCP e crie um conjunto com os IPs de origem
    lista_SA = IDS.filtraTCP(pacotes,'SA')
    lista_SA = IDS.contaIPOrigem(lista_SA).keys()
    # B) lista_S = filtre pacotes pelos flags S do TCP e crie um conjunto com os IPs de destino
    lista_S = IDS.filtraTCP(pacotes,'S')
    lista_S = IDS.contaIPDestino(lista_S).keys()
    # C) Calcule o complemento da lista_SA e lista_S (lista_SA - lista_S)
    resultado = []
    resultado = set(lista_SA) - set(lista_S)
    # D) gere uma mensagem de alerta para cada IP na seleção indicado que estão fazendo o ataque 
    for ip in resultado:
        IDS.alerta(f'O IP {ip} esta fazendo ataques por SYN ACK')
    IDS.alerta(f'Foram detectados {len(resultado)} hosts fazendo ataques por SYN ACK')


#-------------------------------------------------------------------------
if __name__ == '__main__':

    pacotes = IDS.carregaPacotes('desafio.pcap') 
    #pacotes = IDS.filtraTipo(pacotes, IDS.TIPO['icmp'])
    #IDS.mostraPacotes(pacotes, count=10)

    detectaPoD(pacotes, limite=50)
    detectaDPoD(pacotes, limite=50)
    detectaSYNFlood(pacotes, limite=100)
    detectaPSCAN(pacotes, limite=50)
    detectaSYNACK(pacotes, limite=50)



    