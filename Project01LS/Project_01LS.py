import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import re
import time

class LagSlayerApp:
    def __init__(self, master):
        self.master = master
        master.title("LAG SLAYER")
        master.geometry("400x450")
        master.configure(bg='#f0f0f0')

        style = ttk.Style()
        style.theme_use('clam')

        title_label = ttk.Label(master, text="LAG SLAYER", font=("Arial", 24, "bold"), background='#f0f0f0')
        title_label.pack(pady=20)

        self.create_button("Otimizar (Automático)", self.optimize, 'green')
        self.create_button("Restaurar Configurações Originais", self.restore_default, 'red')
        self.create_button("Mostrar Configurações Atuais", self.show_current, 'blue')
        self.create_button("Digite o MTU manual", self.manual_mtu, 'orange')

        self.mtu_frame = ttk.Frame(master)
        self.mtu_frame.pack(pady=10)
        self.mtu_entry = ttk.Entry(self.mtu_frame, width=10)
        self.mtu_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.apply_button = ttk.Button(self.mtu_frame, text="Aplicar MTU Manual", command=self.apply_manual)
        self.apply_button.pack(side=tk.LEFT)


        self.status_label = ttk.Label(master, text="", background='#f0f0f0')
        self.status_label.pack(pady=10)

    def create_button(self, text, command, color):
        style = ttk.Style()
        style.configure(f'{color}.TButton', foreground='white', background=color)
        button = ttk.Button(self.master, text=text, command=command, style=f'{color}.TButton', width=30)
        button.pack(pady=5)

    def optimize(self):
        self.status_label.config(text="Otimizando MTU...")
        best_mtu = self.find_best_mtu()
        if best_mtu:
            self.set_mtu(best_mtu)
            self.status_label.config(text=f"MTU otimizado: {best_mtu}")
        else:
            self.status_label.config(text="Falha na otimização do MTU")

    def find_best_mtu(self):
        target = "www.google.com"  
        start_mtu = 1500
        min_mtu = 68

        while start_mtu > min_mtu:
            if self.test_mtu(start_mtu, target):
                return start_mtu
            start_mtu -= 10
        return None

    def test_mtu(self, mtu, target):
        try:

            self.set_mtu(mtu)
            time.sleep(1)
            
            packet_size = mtu - 28
            result = subprocess.run(
                f'ping -n 1 -l {packet_size} -f {target}',
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True
            )
            
            
            return "bytes=" in result.stdout and "Pacotes: Enviados = 1, Recebidos = 1, Perdidos = 0" in result.stdout
        except Exception as e:
            print(f"Erro ao testar MTU {mtu}: {e}")
            return False

    def restore_default(self):

        self.set_mtu(1500)  
        self.status_label.config(text="Configurações padrão restauradas.")

    def show_current(self):

        mtu = self.get_current_mtu()
        messagebox.showinfo("Configurações Atuais", f"MTU atual: {mtu}")

    def manual_mtu(self):

        self.mtu_frame.pack(pady=10)

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

    def get_current_mtu(self):
        try:
            result = subprocess.check_output('netsh interface ipv4 show subinterfaces', shell=True).decode()
            match = re.search(r'Ethernet\s+\d+\s+(\d+)', result)
            if match:
                return int(match.group(1))
        except Exception as e:
            print(f"Erro ao obter MTU atual: {e}")
        return None

    def set_mtu(self, mtu):
        try:
            subprocess.check_call(f'netsh interface ipv4 set subinterface "Ethernet" mtu={mtu} store=persistent', shell=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Erro", f"Falha ao definir MTU: {e}")

root = tk.Tk()
app = LagSlayerApp(root)
root.mainloop()