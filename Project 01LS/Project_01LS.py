
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

# Troca de DNS e teste de latência
def check_dns_latency(dns):
    try:
        start = time.time()
        socket.gethostbyname_ex("google.com")
        latency = (time.time() - start) * 1000
        print(f"Latência com {dns}: {latency} ms")
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
    print("Não foi possível ajustar o MTU")
    return None

# Automatizar as melhorias
def optimize_connection(target_ip="8.8.8.8"):
    # Backup das configurações iniciais
    original_dns = "8.8.8.8"  # DNS padrão para restaurar (ajuste conforme necessário)
    
    try:
        # 1. Testar rota
        print("Testando rota inicial...")
        initial_route = traceroute(target_ip)
        print(initial_route)

        # 2. Trocar DNS para o mais rápido
        dns_options = ["8.8.8.8", "1.1.1.1"]
        best_dns = min(dns_options, key=check_dns_latency)
        set_dns(best_dns)

        # 3. Ajustar MTU
        best_mtu = adjust_mtu(target_ip)
        if best_mtu:
            os.system(f"netsh interface ipv4 set subinterface Wi-Fi mtu={best_mtu} store=persistent")
        
        # 4. Verificar otimização
        print("Otimização concluída. Monitorando latência...")
        while True:
            if not ping(target_ip):
                print("Perda de conexão detectada. Restaurando configurações iniciais.")
                break
            time.sleep(10)  # Intervalo para monitoramento
        
    finally:
        # Restaurar configurações originais
        print("Restaurando configurações originais...")
        set_dns(original_dns)
        os.system("netsh interface ipv4 set subinterface Wi-Fi mtu=1500 store=persistent")
        print("Configurações restauradas.")

# Executar o programa de otimização
optimize_connection("8.8.8.8")
