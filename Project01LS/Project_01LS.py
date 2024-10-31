
import subprocess
import socket
import os
import time
import platform
import subprocess
import sys


def get_active_interface():
    interfaces = ["Ethernet", "Ethernet 2", "Conexao Local"]
    for interface in interfaces:
        result = subprocess.run(f'netsh interface show interface "{interface}"', capture_output=True, text=True, shell=True)
        if "Conectado" in result.stdout:
            return interface
    return None


interface_name = get_active_interface()
if not interface_name:
    print("Nenhuma interface ativa encontrada. Verifique as conexoes de rede e tente novamente.")
    sys.exit(1)
else:
    print(f"Usando a interface ativa: {interface_name}")

# Configurações otimizadas de DNS e MTU
def apply_optimized_settings():
    try:
        dns_command = f'netsh interface ip set dns name="{interface_name}" source=static addr=8.8.8.8'
        mtu_command = f'netsh interface ipv4 set subinterface "{interface_name}" mtu=1500 store=persistent'

        dns_result = subprocess.run(dns_command, shell=True, capture_output=True, text=True)
        mtu_result = subprocess.run(mtu_command, shell=True, capture_output=True, text=True)

        if dns_result.returncode != 0:
            print("Erro ao configurar o DNS:", dns_result.stderr)
        elif mtu_result.returncode != 0:
            print("Erro ao configurar o MTU:", mtu_result.stderr)
        else:
            print("✅ Configurações de rede otimizadas com sucesso.")
    except Exception as e:
        print("⚠️ Erro ao aplicar configurações otimizadas:", e)

# Restaura as configurações originais de DNS e MTU
def restore_original_settings():
    try:
        dns_restore_command = f'netsh interface ip set dns name="{interface_name}" source=dhcp'
        mtu_restore_command = f'netsh interface ipv4 set subinterface "{interface_name}" mtu=automatic store=persistent'

        dns_restore_result = subprocess.run(dns_restore_command, shell=True, capture_output=True, text=True)
        mtu_restore_result = subprocess.run(mtu_restore_command, shell=True, capture_output=True, text=True)

        if dns_restore_result.returncode != 0:
            print("Erro ao restaurar o DNS:", dns_restore_result.stderr)
        elif mtu_restore_result.returncode != 0:
            print("Erro ao restaurar o MTU:", mtu_restore_result.stderr)
        else:
            print("✅ Configurações de rede restauradas com sucesso.")
    except Exception as e:
        print("⚠️ Erro ao restaurar configurações originais:", e)


def show_menu():
    while True:
        print("\n================= Project LagSlayer =================")
        print(" Escolha uma opção:                                    |")
        print("                                                       |")
        print("1️ Otimizar Configurações de Rede                      |")
        print("2️ Restaurar Configurações Originais                   |")
        print("3️ Sair                                                |")
        print("=======================================================")

        choice = input("Digite o número da opção desejada: ")

        if choice == '1':
            print("\n🔄 Otimizando configurações de rede...")
            apply_optimized_settings()
        elif choice == '2':
            print("\n🔄 Restaurando configurações originais...")
            restore_original_settings()
        elif choice == '3':
            print("\n👋 Saindo do programa. Até logo!")
            break
        else:
            print("\n❌ Opção inválida! Por favor, escolha uma opção válida (1, 2 ou 3).")

show_menu()
