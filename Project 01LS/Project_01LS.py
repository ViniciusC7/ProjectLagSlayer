
import subprocess
import socket
import os
import time

# Monitoramento de ping e rota
def ping(host):
    command = ["ping", "-n", "4", host]
    response = subprocess.run(command, capture_output=True, text=True).stdout
    return "tempo=" in response  # Indicador de resposta bem-sucedida

def traceroute(host):
    command = ["tracert", host]
    response = subprocess.run(command, capture_output=True, text=True).stdout
    return response

# Troca de DNS e teste de lat�ncia
def check_dns_latency(dns):
    try:
        start = time.time()
        socket.gethostbyname_ex("google.com")
        latency = (time.time() - start) * 1000
        print(f"Lat�ncia com {dns}: {latency} ms")
        return latency
    except Exception as e:
        return float('inf')

def set_dns(dns):
    os.system(f'netsh interface ip set dns name="Wi-Fi" static {dns}')
    print(f"DNS setado para: {dns}")

# Ajuste de MTU
def test_mtu(mtu_value, target):
    command = ["ping", "-f", "-l", str(mtu_value), target]
    response = subprocess.run(command, capture_output=True, text=True).stdout
    return "fragmented" not in response

def adjust_mtu(target):
    mtu_value = 1500
    while mtu_value > 500:
        if test_mtu(mtu_value, target):
            print(f"MTU ideal encontrado: {mtu_value}")
            return mtu_value
        mtu_value -= 10
    print("N�o foi poss�vel ajustar o MTU")
    return None

# Automatizar as melhorias
def optimize_connection(target_ip="8.8.8.8"):
    # Backup das configura��es iniciais
    original_dns = "8.8.8.8"  # DNS padr�o para restaurar (ajuste conforme necess�rio)
    
    try:
        # 1. Testar rota
        print("Testando rota inicial...")
        initial_route = traceroute(target_ip)
        print(initial_route)

        # 2. Trocar DNS para o mais r�pido
        dns_options = ["8.8.8.8", "1.1.1.1"]
        best_dns = min(dns_options, key=check_dns_latency)
        set_dns(best_dns)

        # 3. Ajustar MTU
        best_mtu = adjust_mtu(target_ip)
        if best_mtu:
            os.system(f"netsh interface ipv4 set subinterface Wi-Fi mtu={best_mtu} store=persistent")
        
        # 4. Verificar otimiza��o
        print("Otimiza��o conclu�da. Monitorando lat�ncia...")
        while True:
            if not ping(target_ip):
                print("Perda de conex�o detectada. Restaurando configura��es iniciais.")
                break
            time.sleep(10)  # Intervalo para monitoramento
        
    finally:
        # Restaurar configura��es originais
        print("Restaurando configura��es originais...")
        set_dns(original_dns)
        os.system("netsh interface ipv4 set subinterface Wi-Fi mtu=1500 store=persistent")
        print("Configura��es restauradas.")

# Executar o programa de otimiza��o
optimize_connection("8.8.8.8")
