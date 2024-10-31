import subprocess
import socket
import os
import time
import platform
import sys
from datetime import datetime

# Funções para obter a interface ativa e verificar configurações
def get_active_interface():
    interfaces = ["Ethernet", "Ethernet 2", "Conexao Local"]
    for interface in interfaces:
        result = subprocess.run(f'netsh interface show interface "{interface}"', capture_output=True, text=True, shell=True)
        if "Conectado" in result.stdout:
            return interface
    return None

def show_current_settings():
    print("\nConfigurações atuais da interface:")
    dns_info = subprocess.run(f'netsh interface ip show config name="{interface_name}"', shell=True, capture_output=True, text=True)
    mtu_info = subprocess.run("netsh interface ipv4 show subinterface", shell=True, capture_output=True, text=True)
    print(dns_info.stdout)
    print(mtu_info.stdout)

# Função para testar latência usando ping
def test_latency(host="8.8.8.8", count=4):
    try:
        print(f"\nTestando latência para {host}...")
        system = platform.system().lower()
        
        if system == "windows":
            cmd = f"ping {host} -n {count}"
        else:
            cmd = f"ping {host} -c {count}"
            
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout)
        
        # Extrair média de latência do resultado
        if "Média =" in result.stdout:  # Windows em português
            avg = result.stdout.split("Média =")[-1].split("ms")[0].strip()
        elif "Average =" in result.stdout:  # Windows em inglês
            avg = result.stdout.split("Average =")[-1].split("ms")[0].strip()
        elif "min/avg/max" in result.stdout:  # Linux/Unix
            avg = result.stdout.split("min/avg/max")[1].split("/")[1]
        else:
            avg = "N/A"
            
        print(f"\nLatência média: {avg}ms")
        return float(avg) if avg != "N/A" else None
        
    except Exception as e:
        print(f"Erro ao testar latência: {e}")
        return None

# Função para testar conexão básica
def test_connection(host="8.8.8.8", port=53, timeout=3):
    try:
        print(f"\nTestando conexão com {host}...")
        start_time = time.time()
        socket.create_connection((host, port), timeout=timeout)
        response_time = (time.time() - start_time) * 1000
        print(f"Conexão bem sucedida! Tempo de resposta: {response_time:.2f}ms")
        return True
    except socket.error as e:
        print(f"Erro na conexão: {e}")
        return False

# Função para encontrar MTU ideal usando ping
def find_optimal_mtu():
    try:
        print("\nProcurando MTU ideal...")
        mtu_sizes = [1500, 1492, 1472, 1468, 1400]
        best_mtu = 1500
        best_latency = float('inf')
        
        for mtu in mtu_sizes:
            print(f"\nTestando MTU {mtu}...")
            subprocess.run(f'netsh interface ipv4 set subinterface "{interface_name}" mtu={mtu} store=persistent', shell=True)
            time.sleep(1)
            latency = test_latency()
            if latency and latency < best_latency:
                best_latency = latency
                best_mtu = mtu
        
        return best_mtu
    except Exception as e:
        print(f"Erro ao encontrar MTU ideal: {e}")
        return 1500

def apply_optimized_settings():
    try:
        print("\n🔄 Iniciando otimização...")
        
        # Teste inicial
        print("\nRealizando teste inicial...")
        initial_latency = test_latency()
        initial_connection = test_connection()
        
        # Encontrar e aplicar MTU ideal
        optimal_mtu = find_optimal_mtu()
        
        # Aplicar configurações otimizadas
        dns_commands = [
            f'netsh interface ip set dns name="{interface_name}" source=static addr=8.8.8.8',
            f'netsh interface ip add dns name="{interface_name}" addr=8.8.4.4 index=2'
        ]
        
        for cmd in dns_commands:
            subprocess.run(cmd, shell=True)
            
        mtu_command = f'netsh interface ipv4 set subinterface "{interface_name}" mtu={optimal_mtu} store=persistent'
        subprocess.run(mtu_command, shell=True)
        
        # Teste final
        print("\nRealizando teste final...")
        final_latency = test_latency()
        final_connection = test_connection()
        
        # Mostrar comparação
        print("\n📊 Resultados da otimização:")
        print(f"MTU otimizado: {optimal_mtu}")
        if initial_latency and final_latency:
            latency_improvement = ((initial_latency - final_latency) / initial_latency) * 100
            print(f"Melhoria na latência: {latency_improvement:.1f}%")
        
        show_current_settings()
        print("✅ Configurações de rede otimizadas com sucesso.")
        
    except Exception as e:
        print("⚠️ Erro ao aplicar configurações otimizadas:", e)

def restore_original_settings():
    try:
        dns_restore_command = f'netsh interface ip set dns name="{interface_name}" source=dhcp'
        mtu_restore_command = f'netsh interface ipv4 set subinterface "{interface_name}" mtu=automatic store=persistent'
        subprocess.run(dns_restore_command, shell=True)
        subprocess.run(mtu_restore_command, shell=True)
        print("✅ Configurações de rede restauradas com sucesso.")
        show_current_settings()
    except Exception as e:
        print("⚠️ Erro ao restaurar configurações originais:", e)

# Obter a interface ativa e verificar a conexão
interface_name = get_active_interface()
if not interface_name:
    print("Nenhuma interface ativa encontrada. Verifique as conexões de rede e tente novamente.")
    sys.exit(1)
else:
    print(f"Usando a interface ativa: {interface_name}")

def show_menu():
    while True:
        print("\n================= Project LagSlayer =================")
        print("Escolha uma opção:                                   |")
        print("                                                     |")
        print("1️⃣ Otimizar Configurações de Rede                   |")
        print("2️⃣ Restaurar Configurações Originais                |")
        print("3️⃣ Testar Latência                                  |")
        print("4️⃣ Testar Conexão                                   |")
        print("5️⃣ Encontrar MTU Ideal                              |")
        print("6️⃣ Sair                                             |")
        print("=====================================================")
        
        choice = input("Digite o número da opção desejada: ")
        
        if choice == '1':
            print("\n🔄 Otimizando configurações de rede...")
            apply_optimized_settings()
        elif choice == '2':
            print("\n🔄 Restaurando configurações originais...")
            restore_original_settings()
        elif choice == '3':
            test_latency()
        elif choice == '4':
            test_connection()
        elif choice == '5':
            optimal_mtu = find_optimal_mtu()
            print(f"\nMTU ideal encontrado: {optimal_mtu}")
        elif choice == '6':
            print("\n👋 Saindo do programa. Até logo!")
            break
        else:
            print("\n❌ Opção inválida! Por favor, escolha uma opção válida (1-6).")

if __name__ == "__main__":
    show_menu()