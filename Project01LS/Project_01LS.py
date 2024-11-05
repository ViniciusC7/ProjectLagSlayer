import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import re
import time
import psutil

class LagSlayerApp:
    def __init__(self, master):
        self.master = master
        master.title("LAG SLAYER")
        master.geometry("500x600")
        master.configure(bg='#f0f0f0')

        style = ttk.Style()
        style.theme_use('clam')

        # Create title label
        title_label = ttk.Label(master, text="LAG SLAYER", font=("Arial", 24, "bold"), background='#f0f0f0')
        title_label.pack(pady=20)

        # Create buttons
        self.create_button("Otimizar para Jogos Online", self.optimize_for_games, 'green')
        self.create_button("Otimizar para Downloads/Streaming", self.optimize_for_downloads, 'blue')
        self.create_button("Restaurar Configurações Originais", self.restore_default, 'red')
        self.create_button("Mostrar Configurações Atuais", self.show_current, 'orange')
        self.create_button("Sobre o Programa", self.show_about, 'purple')

        # Create manual MTU input
        self.mtu_frame = ttk.Frame(master)
        self.mtu_frame.pack(pady=10)
        self.mtu_entry = ttk.Entry(self.mtu_frame, width=10)
        self.mtu_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.apply_button = ttk.Button(self.mtu_frame, text="Aplicar MTU Manual", command=self.apply_manual)
        self.apply_button.pack(side=tk.LEFT)

        # Create status label
        self.status_label = ttk.Label(master, text="", background='#f0f0f0')
        self.status_label.pack(pady=10)

        # Create info text area
        self.info_text = scrolledtext.ScrolledText(master, height=10, width=50)
        self.info_text.pack(pady=10)
        self.info_text.config(state=tk.DISABLED)

    def create_button(self, text, command, color):
        style = ttk.Style()
        style.configure(f'{color}.TButton', foreground='white', background=color)
        button = ttk.Button(self.master, text=text, command=command, style=f'{color}.TButton', width=30)
        button.pack(pady=5)

    def optimize_for_games(self):
        self.status_label.config(text="Otimizando para jogos online...")
        self.optimize_mtu()
        self.optimize_tcp()
        self.disable_nagle()
        self.status_label.config(text="Otimização para jogos concluída!")

    def optimize_for_downloads(self):
        self.status_label.config(text="Otimizando para downloads/streaming...")
        self.optimize_mtu()
        self.increase_tcp_window()
        self.enable_qos()
        self.status_label.config(text="Otimização para downloads/streaming concluída!")

    def optimize_mtu(self):
        best_mtu = self.find_best_mtu()
        if best_mtu:
            self.set_mtu(best_mtu)
            self.update_info(f"MTU otimizado: {best_mtu}")
        else:
            self.update_info("Falha na otimização do MTU")

    def optimize_tcp(self):
        try:
            subprocess.run("netsh int tcp set global autotuninglevel=normal", shell=True, check=True)
            subprocess.run("netsh int tcp set global chimney=enabled", shell=True, check=True)
            subprocess.run("netsh int tcp set global ecncapability=enabled", shell=True, check=True)
            self.update_info("Configurações TCP otimizadas")
        except subprocess.CalledProcessError as e:
            self.update_info(f"Erro ao otimizar TCP: {e}")

    def disable_nagle(self):
        try:
            subprocess.run("reg add HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces\\{YOUR_INTERFACE_GUID} /v TcpAckFrequency /t REG_DWORD /d 1 /f", shell=True, check=True)
            subprocess.run("reg add HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces\\{YOUR_INTERFACE_GUID} /v TCPNoDelay /t REG_DWORD /d 1 /f", shell=True, check=True)
            self.update_info("Algoritmo de Nagle desativado")
        except subprocess.CalledProcessError as e:
            self.update_info(f"Erro ao desativar Nagle: {e}")

    def increase_tcp_window(self):
        try:
            subprocess.run("netsh int tcp set global autotuninglevel=normal", shell=True, check=True)
            subprocess.run("netsh int tcp set global windowsscaling=enabled", shell=True, check=True)
            self.update_info("Janela TCP aumentada")
        except subprocess.CalledProcessError as e:
            self.update_info(f"Erro ao aumentar janela TCP: {e}")

    def enable_qos(self):
        try:
            subprocess.run("sc config Qwave start= auto", shell=True, check=True)
            subprocess.run("net start Qwave", shell=True, check=True)
            self.update_info("QoS habilitado")
        except subprocess.CalledProcessError as e:
            self.update_info(f"Erro ao habilitar QoS: {e}")

    def restore_default(self):
        self.set_mtu(1500)
        subprocess.run("netsh int tcp set global autotuninglevel=normal", shell=True)
        subprocess.run("netsh int tcp set global chimney=default", shell=True)
        subprocess.run("netsh int tcp set global ecncapability=default", shell=True)
        self.status_label.config(text="Configurações padrão restauradas.")

    def show_current(self):
        mtu = self.get_current_mtu()
        network_stats = self.get_network_stats()
        self.update_info(f"MTU atual: {mtu}\n\n{network_stats}")

    def show_about(self):
        about_text = """
        LAG SLAYER

        Este programa otimiza sua conexão de internet para melhorar o desempenho em jogos online, downloads e streaming de vídeo.

        Instruções:
        1. Use "Otimizar para Jogos Online" para reduzir lag em jogos.
        2. Use "Otimizar para Downloads/Streaming" para melhorar velocidades de download e qualidade de streaming.
        3. "Restaurar Configurações Originais" retorna tudo ao padrão.
        4. "Mostrar Configurações Atuais" exibe informações sobre sua conexão.
        5. Você pode inserir um MTU manualmente se desejar.

        Nota: Algumas otimizações podem requerer reinicialização para ter efeito completo.
        """
        messagebox.showinfo("Sobre o LAG SLAYER", about_text)

    def apply_manual(self):
        try:
            mtu = int(self.mtu_entry.get())
            if 68 <= mtu <= 1500:
                self.set_mtu(mtu)
                self.status_label.config(text=f"MTU definido para {mtu}.")
            else:
                messagebox.showerror("Erro", "O valor do MTU deve estar entre 68 e 1500.")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor numérico válido para o MTU.")

    def update_info(self, text):
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, text)
        self.info_text.config(state=tk.DISABLED)

    def get_network_stats(self):
        try:
            net_io = psutil.net_io_counters()
            
            ping_result = subprocess.run(
                ['ping', '-n', '4', 'www.google.com'],
                capture_output=True,
                text=True
            )
            
            latency = "N/A"
            if "Média = " in ping_result.stdout:
                latency = ping_result.stdout.split("Média = ")[-1].split("ms")[0].strip()

            stats = f"""Estatísticas de Rede:
            
Bytes Enviados: {net_io.bytes_sent / 1024 / 1024:.2f} MB
Bytes Recebidos: {net_io.bytes_recv / 1024 / 1024:.2f} MB
Pacotes Enviados: {net_io.packets_sent}
Pacotes Recebidos: {net_io.packets_recv}
Pacotes Perdidos: {net_io.dropin + net_io.dropout}
Latência Média: {latency}ms
"""
            return stats
        except Exception as e:
            return f"Erro ao obter estatísticas: {e}"

    def find_best_mtu(self):
        target = "www.google.com"
        start_mtu = 1500
        min_mtu = 68
        best_mtu = None
        best_latency = float('inf')

        self.update_info("Testando diferentes valores de MTU...\n")
        
        while start_mtu > min_mtu:
            current_latency = self.test_mtu_with_latency(start_mtu, target)
            if current_latency is not None and current_latency < best_latency:
                best_latency = current_latency
                best_mtu = start_mtu
            start_mtu -= 50

        return best_mtu

    def test_mtu_with_latency(self, mtu, target):
        command = f"ping -f -l {mtu} {target}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if "Esgotado o tempo limite do pedido" in result.stdout:
            return None

        if "Média = " in result.stdout:
            latency_str = result.stdout.split("Média = ")[-1].split("ms")[0].strip()
            return int(latency_str)

    def get_current_mtu(self):
        try:
            result = subprocess.run("netsh interface ipv4 show subinterfaces", shell=True, capture_output=True, text=True)
            mtu = re.search(r"(\d+)\s+\d+\s+\d+\s+\w+", result.stdout)
            return int(mtu.group(1)) if mtu else "N/A"
        except Exception as e:
            return f"Erro ao obter MTU: {e}"

    def set_mtu(self, mtu):
        try:
            subprocess.run(f"netsh interface ipv4 set subinterface \"Ethernet\" mtu={mtu} store=persistent", shell=True, check=True)
            self.update_info(f"MTU configurado para {mtu}")
        except subprocess.CalledProcessError as e:
            self.update_info(f"Erro ao definir MTU: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LagSlayerApp(root)
    root.mainloop()
