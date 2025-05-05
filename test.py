import subprocess
import time
import tkinter as tk
from tkinter import ttk, messagebox

SCRCPY_PATH = r"scrcpy.exe"

def conectar_dispositivo(ip):
    try:
        subprocess.run(["adb", "connect", f"{ip}:5555"], check=True)
        time.sleep(2)
    except subprocess.CalledProcessError:
        return False
    return True

def verificar_online(ip):
    output = subprocess.check_output(["adb", "devices"]).decode()
    for line in output.splitlines():
        if f"{ip}:5555" in line and "device" in line:
            return True
    return False

def iniciar_scrcpy(ip):
    try:
        subprocess.run([SCRCPY_PATH, "--serial", f"{ip}:5555"], check=True)
    except subprocess.CalledProcessError:
        messagebox.showerror("Erro", "Erro ao iniciar o scrcpy.")

def ativar_adb_wifi():
    try:
        subprocess.run(["adb", "tcpip", "5555"], check=True)
        messagebox.showinfo("Sucesso", "✅ ADB via Wi-Fi ativado.\nAgora digite o IP abaixo.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Erro", "Erro ao ativar o ADB via Wi-Fi.\nConecte o dispositivo via USB primeiro.")

def desativar_adb_wifi():
    try:
        subprocess.run(["adb", "usb"], check=True)
        messagebox.showinfo("Sucesso", "📴 ADB via Wi-Fi desativado. Voltando para USB.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Erro", "Erro ao desativar o ADB via Wi-Fi.")

def executar():
    ip = ip_entry.get().strip()
    if not ip:
        messagebox.showwarning("Aviso", "Digite um IP válido.")
        return

    status_label.config(text="🔄 Conectando ao dispositivo...")
    janela.update_idletasks()

    if not conectar_dispositivo(ip):
        messagebox.showerror("Erro", "❌ Falha ao conectar ao dispositivo.")
        status_label.config(text="")
        return

    if not verificar_online(ip):
        messagebox.showerror("Erro", "⚠️ Dispositivo está offline.")
        status_label.config(text="")
        return

    status_label.config(text="✅ Dispositivo conectado. Iniciando scrcpy...")
    iniciar_scrcpy(ip)
    status_label.config(text="")

def encerrar():
    janela.destroy()

# Janela principal
janela = tk.Tk()
janela.title("📱 Scrcpy via Wi-Fi")
janela.geometry("500x450")
janela.configure(bg="#624bff")
janela.resizable(False, False)

# Estilo visual
style = ttk.Style()
style.theme_use("clam")

style.configure("TFrame", background="#624bff")
style.configure("TLabel", background="#624bff", foreground="white", font=("Segoe UI", 11))
style.configure("TEntry", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)

# Frame central
frame = ttk.Frame(janela)
frame.pack(expand=True)

# Cabeçalho
ttk.Label(frame, text="📶 Conectar ao Dispositivo", font=("Segoe UI", 16, "bold")).pack(pady=(20, 15))

# Campo de IP
ip_container = ttk.Frame(frame)
ip_container.pack(pady=(0, 15), padx=20, fill='x')

ttk.Label(ip_container, text="Digite o IP do dispositivo:").pack(anchor="w", pady=(0, 5))
ip_entry = ttk.Entry(ip_container, width=40)
ip_entry.pack(fill='x')

# Botões de ação
button_container = ttk.Frame(frame)
button_container.pack(pady=10)

btn_wifi = ttk.Button(button_container, text="📡 Ativar ADB via USB", command=ativar_adb_wifi, width=24)
btn_wifi.grid(row=0, column=0, padx=5, pady=5)

btn_conectar = ttk.Button(button_container, text="🚀 Iniciar scrcpy", command=executar, width=24)
btn_conectar.grid(row=0, column=1, padx=5, pady=5)

btn_desativar_wifi = ttk.Button(frame, text="📴 Desativar ADB Wi-Fi", command=desativar_adb_wifi, width=50)
btn_desativar_wifi.pack(pady=(5, 5))

btn_encerrar = ttk.Button(frame, text="❌ Encerrar", command=encerrar, width=50)
btn_encerrar.pack(pady=(15, 10))

# Status
status_label = ttk.Label(frame, text="", font=("Segoe UI", 10, "italic"))
status_label.pack(pady=(10, 0))

janela.mainloop()
