import subprocess
import tkinter as tk
from tkinter import messagebox

def get_active_interface():
    interfaces = ["Ethernet", "Ethernet 2", "Conexão Local"]
    for interface in interfaces:
        result = subprocess.run(f'netsh interface show interface "{interface}"', capture_output=True, text=True, shell=True)
        if "Conectado" in result.stdout:
            return interface
    return None

def display_status():
    interface = get_active_interface()
    if interface:
        result = subprocess.run(f'netsh interface ip show config "{interface}"', capture_output=True, text=True, shell=True)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result.stdout)
    else:
        messagebox.showerror("Erro", "Nenhuma interface ativa encontrada. Verifique as conexões de rede.")

def apply_optimized_settings():
    interface = get_active_interface()
    if interface:
        try:
            subprocess.run(f'netsh interface ip set dns name="{interface}" source=static addr=8.8.8.8', shell=True)
            subprocess.run(f'netsh interface ipv4 set subinterface "{interface}" mtu=1500 store=persistent', shell=True)
            messagebox.showinfo("Sucesso", "Configurações otimizadas aplicadas com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao aplicar configurações: {e}")
    else:
        messagebox.showerror("Erro", "Nenhuma interface ativa encontrada. Verifique as conexões de rede.")

def restore_settings():
    interface = get_active_interface()
    if interface:
        try:
            subprocess.run(f'netsh interface ip set dns name="{interface}" source=dhcp', shell=True)
            subprocess.run(f'netsh interface ipv4 set subinterface "{interface}" mtu=automatic store=persistent', shell=True)
            messagebox.showinfo("Sucesso", "Configurações originais restauradas com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao restaurar configurações: {e}")
    else:
        messagebox.showerror("Erro", "Nenhuma interface ativa encontrada. Verifique as conexões de rede.")

window = tk.Tk()
window.title("Project LagSlayer")
window.geometry("600x400")

title_label = tk.Label(window, text="Project LagSlayer", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

output_text = tk.Text(window, height=10, width=70)
output_text.pack(pady=10)

button_frame = tk.Frame(window)
button_frame.pack(pady=10)

status_button = tk.Button(button_frame, text="Exibir Status da Interface", command=display_status, width=25)
status_button.grid(row=0, column=0, padx=5, pady=5)

optimize_button = tk.Button(button_frame, text="Otimizar Configurações", command=apply_optimized_settings, width=25)
optimize_button.grid(row=0, column=1, padx=5, pady=5)

restore_button = tk.Button(button_frame, text="Restaurar Configurações Originais", command=restore_settings, width=25)
restore_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

footer_label = tk.Label(window, text="© 2024 Project LagSlayer", font=("Arial", 8))
footer_label.pack(side="bottom", pady=5)

window.mainloop()
