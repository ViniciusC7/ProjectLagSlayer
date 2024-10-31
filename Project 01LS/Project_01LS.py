
import subprocess
import socket
import os
import time
import platform

# Fun��o para salvar as configura��es originais
def backup_settings():
    # Backup do DNS atual
    original_dns = []
    dns_info = subprocess.check_output("nslookup -type=ns .", shell=True).decode()
    for line in dns_info.splitlines():
        if "Address" in line and not "Non-authoritative" in line:
            original_dns.append(line.split(":")[-1].strip())
    
    # Backup do MTU atual
    mtu_info = subprocess.check_output("netsh interface ipv4 show subinterfaces", shell=True).decode()
    mtu_lines = mtu_info.splitlines()
    original_mtu = [line.split()[2] for line in mtu_lines if "MTU" in line][0]

    print("Configura��es originais de DNS e MTU salvas.")
    return {"dns": original_dns, "mtu": original_mtu}

# Fun��o para ajustar DNS e MTU
def optimize_settings(new_dns="8.8.8.8", new_mtu="1500"):
    print(f"Ajustando DNS para {new_dns} e MTU para {new_mtu}...")
    
    # Ajustar o DNS
    subprocess.run(f"netsh interface ip set dns \"Ethernet\" static {new_dns}", shell=True)
    
    # Ajustar o MTU
    subprocess.run(f"netsh interface ipv4 set subinterface \"Ethernet\" mtu={new_mtu} store=persistent", shell=True)

    print("Configura��es otimizadas.")

# Fun��o para restaurar as configura��es originais
def restore_settings(backup):
    original_dns = backup["dns"]
    original_mtu = backup["mtu"]
    
    print("Restaurando configura��es originais...")

    # Restaurar o DNS original
    for i, dns in enumerate(original_dns):
        if i == 0:
            subprocess.run(f"netsh interface ip set dns \"Ethernet\" static {dns}", shell=True)
        else:
            subprocess.run(f"netsh interface ip add dns \"Ethernet\" {dns}", shell=True)

    # Restaurar o MTU original
    subprocess.run(f"netsh interface ipv4 set subinterface \"Ethernet\" mtu={original_mtu} store=persistent", shell=True)

    print("Configura��es restauradas.")

# Menu principal
def main():
    print("Bem-vindo ao Project LagSlayer!")
    backup = backup_settings()  # Salvar configura��es originais

    while True:
        print("\nEscolha uma op��o:")
        print("1 - Otimizar Configura��es de Rede")
        print("2 - Restaurar Configura��es Originais")
        print("3 - Sair")
        
        choice = input("Digite o n�mero da op��o desejada: ")
        
        if choice == "1":
            optimize_settings()
        elif choice == "2":
            restore_settings(backup)
        elif choice == "3":
            print("Saindo...")
            break
        else:
            print("Op��o inv�lida. Tente novamente.")

if __name__ == "__main__":
    main()
