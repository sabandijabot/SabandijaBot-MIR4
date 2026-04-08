import sys
import ctypes
import os
import tkinter as tk
from tkinter import ttk
import win32gui
import win32con
import win32api
import time
import random
import threading
import traceback

# --- FORZAR ICONO EN BARRA DE TAREAS ---
try:
    myappid = 'idynsoft.sabandijabot.reptil.v2'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except:
    pass

# --- VALIDACIÓN DE ADMINISTRADOR ---
def es_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

if not es_admin():
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    except: pass
    sys.exit()

# --- PALETA SABANDIJA REPTIL ---
COLOR_BG = "#050a05"        
COLOR_CARD = "#0d1a0d"      
COLOR_ACCENT = "#39ff14"    # Verde neón
COLOR_SECONDARY = "#ccff00" # Amarillo lima
COLOR_TEXT_OFF = "#4a5d4a"  
COLOR_TEXT_ON = "#39ff14"   
COLOR_INPUT_BG = "#162616"  

class BotInstance(threading.Thread):
    def __init__(self, hwnd, window_name, modo, delay_personalizado=5, usar_ulti=False):
        super().__init__()
        self.hwnd = hwnd
        self.modo = modo
        self.delay_personalizado = delay_personalizado
        self.usar_ulti = usar_ulti
        self.running = True
        self.daemon = True

    def enviar_tecla(self, codigo_tecla):
        if not self.running: return
        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, codigo_tecla, 0)
        time.sleep(random.uniform(0.05, 0.1))
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, codigo_tecla, 0)

    def run(self):
        while self.running:
            try:
                if self.modo == 'MISION_Q':
                    teclas = [0x51, 0x45]; random.shuffle(teclas)
                    for t in teclas: self.enviar_tecla(t); time.sleep(random.uniform(0.3, 0.5))
                    for _ in range(3): self.enviar_tecla(0x54); time.sleep(0.25)
                    rect = win32gui.GetWindowRect(self.hwnd)
                    pos = win32api.MAKELONG((rect[2]-rect[0])//2, (rect[3]-rect[1])//2)
                    for _ in range(5):
                        win32gui.PostMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, pos)
                        time.sleep(0.02); win32gui.PostMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, pos)
                        time.sleep(0.25)
                
                elif self.modo == 'FARMA_EXP':
                    self.enviar_tecla(0x09); time.sleep(0.5)
                    self.enviar_tecla(0x22); time.sleep(0.4)
                    self.enviar_tecla(0x46)
                    if self.usar_ulti:
                        time.sleep(0.4)
                        self.enviar_tecla(0x52) 

                delay = self.delay_personalizado if self.modo == 'FARMA_EXP' else random.uniform(5, 10)
                for _ in range(int(delay * 10)):
                    if not self.running: break
                    time.sleep(0.1)
            except: self.running = False

    def stop(self): self.running = False

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("SABANDIJA B0T - REPTIL EDITION")
        self.root.geometry("600x760")
        self.root.configure(bg=COLOR_BG)
        self.instances = {}
        self.ulti_var = tk.BooleanVar(value=False)
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TNotebook", background=COLOR_BG, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=COLOR_CARD, foreground=COLOR_TEXT_OFF, padding=[10, 5], font=('Segoe UI', 10, 'bold'))
        self.style.map("TNotebook.Tab", background=[("selected", COLOR_ACCENT)], foreground=[("selected", "#000")])
        self.style.configure("TFrame", background=COLOR_BG)
        self.style.configure("Card.TLabelframe", background=COLOR_BG, foreground=COLOR_ACCENT, bordercolor=COLOR_ACCENT)
        self.style.configure("Card.TLabelframe.Label", background=COLOR_BG, foreground=COLOR_ACCENT, font=('Consolas', 10, 'bold'))
        
        tk.Label(self.root, text="🐍 SABANDIJA CONTROL", bg=COLOR_BG, fg=COLOR_ACCENT, font=('Impact', 28)).pack(pady=20)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        self.tab_bot = ttk.Frame(self.notebook); self.tab_layout = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_bot, text="  SABANDIJA INSTANCES  ")
        self.notebook.add(self.tab_layout, text="  RECTIL LAYOUT  ")
        
        self.setup_tab_bot()
        self.setup_tab_layout()

    def update_radio_colors(self):
        if self.modo_var.get() == "MISION_Q":
            self.rb_mision.configure(fg=COLOR_TEXT_ON)
            self.rb_farma.configure(fg=COLOR_TEXT_OFF)
            self.check_ulti.configure(state="disabled", fg=COLOR_TEXT_OFF)
        else:
            self.rb_mision.configure(fg=COLOR_TEXT_OFF)
            self.rb_farma.configure(fg=COLOR_TEXT_ON)
            self.check_ulti.configure(state="normal", fg=COLOR_SECONDARY)

    def setup_tab_bot(self):
        frame_sel = ttk.LabelFrame(self.tab_bot, text=" RECTIL TARGET ", style="Card.TLabelframe")
        frame_sel.pack(fill="x", padx=15, pady=10)
        
        self.combo_ventanas = ttk.Combobox(frame_sel, state="readonly", width=40)
        self.combo_ventanas.pack(pady=10, padx=10)
        
        tk.Button(frame_sel, text="REFRESCAR VISIÓN", bg=COLOR_CARD, fg=COLOR_ACCENT, relief="groove", 
                  font=('Segoe UI', 9, 'bold'), command=self.listar_ventanas).pack(pady=5)

        frame_cfg = ttk.LabelFrame(self.tab_bot, text=" MODO DE CAZA ", style="Card.TLabelframe")
        frame_cfg.pack(fill="x", padx=15, pady=10)
        
        self.modo_var = tk.StringVar(value="MISION_Q")
        self.rb_mision = tk.Radiobutton(frame_cfg, text="MISIÓN Q (AUTO)", variable=self.modo_var, value="MISION_Q", 
                                       bg=COLOR_BG, fg=COLOR_TEXT_ON, selectcolor="#000", font=('Segoe UI', 10, 'bold'), command=self.update_radio_colors)
        self.rb_mision.pack(anchor="w", padx=20, pady=2)

        self.rb_farma = tk.Radiobutton(frame_cfg, text="FARMA EXP (AFK)", variable=self.modo_var, value="FARMA_EXP", 
                                      bg=COLOR_BG, fg=COLOR_TEXT_OFF, selectcolor="#000", font=('Segoe UI', 10, 'bold'), command=self.update_radio_colors)
        self.rb_farma.pack(anchor="w", padx=20, pady=2)
        
        self.check_ulti = tk.Checkbutton(frame_cfg, text="LANZAR ULTI [R] (Solo Farma)", variable=self.ulti_var,
                                        bg=COLOR_BG, fg=COLOR_TEXT_OFF, selectcolor="#000", state="disabled",
                                        activebackground=COLOR_BG, activeforeground=COLOR_SECONDARY,
                                        font=('Segoe UI', 9, 'bold'))
        self.check_ulti.pack(anchor="w", padx=40, pady=5)

        delay_frame = tk.Frame(frame_cfg, bg=COLOR_BG)
        delay_frame.pack(fill="x", padx=20, pady=10)
        tk.Label(delay_frame, text="DELAY CAZA (SEG):", bg=COLOR_BG, fg=COLOR_ACCENT, font=('Segoe UI', 9, 'bold')).pack(side="left")
        
        self.entry_delay = tk.Entry(delay_frame, width=10, bg=COLOR_INPUT_BG, fg=COLOR_ACCENT, insertbackground=COLOR_ACCENT, borderwidth=0, font=('Consolas', 10, 'bold'))
        self.entry_delay.insert(0, "5"); self.entry_delay.pack(side="left", padx=10)

        tk.Button(self.tab_bot, text="DESPLEGAR SABANDIJA", bg=COLOR_ACCENT, fg="#000", 
                 font=('Segoe UI', 12, 'bold'), relief="flat", command=self.agregar_estancia).pack(pady=15, fill="x", padx=30)

        frame_list = ttk.LabelFrame(self.tab_bot, text=" HUNTING LOG ", style="Card.TLabelframe")
        frame_list.pack(fill="both", expand=True, padx=15, pady=10)
        self.canvas = tk.Canvas(frame_list, bg=COLOR_BG, highlightthickness=0)
        self.scrollable_frame = tk.Frame(self.canvas, bg=COLOR_BG)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.listar_ventanas()

    def setup_tab_layout(self):
        frame_resize = ttk.LabelFrame(self.tab_layout, text=" RECTIL ARCHITECTURE ", style="Card.TLabelframe")
        frame_resize.pack(fill="both", expand=True, padx=15, pady=15)
        
        labels = ["ANCHO", "ALTO", "OFFSET X", "OFFSET Y"]
        self.entries = {}; defaults = ["800", "600", "40", "0"]
        
        for i, text in enumerate(labels):
            tk.Label(frame_resize, text=text, bg=COLOR_BG, fg=COLOR_TEXT_OFF, font=('Segoe UI', 9, 'bold')).grid(row=i, column=0, padx=20, pady=15, sticky="w")
            ent = tk.Entry(frame_resize, width=15, bg=COLOR_INPUT_BG, fg=COLOR_ACCENT, borderwidth=0, font=('Consolas', 11, 'bold'), insertbackground=COLOR_ACCENT)
            ent.insert(0, defaults[i]); ent.grid(row=i, column=1, padx=10); self.entries[text] = ent

        tk.Button(frame_resize, text="SINCRONIZAR CASCADA", bg=COLOR_ACCENT, fg="#000", font=('Segoe UI', 11, 'bold'), 
                  relief="flat", command=self.organizar_ventanas).grid(row=5, column=0, columnspan=2, pady=30, padx=20, sticky="nsew")

    def organizar_ventanas(self):
        try:
            target_w = int(self.entries["ANCHO"].get()); target_h = int(self.entries["ALTO"].get())
            off_x = int(self.entries["OFFSET X"].get()); off_y = int(self.entries["OFFSET Y"].get())
            cur_x, cur_y = 0, 0; v_list = []
            win32gui.EnumWindows(lambda h, _: v_list.append(h) if win32gui.IsWindowVisible(h) and "MIR4G" in win32gui.GetWindowText(h).upper() else None, None)
            v_list.sort()
            for hwnd in v_list:
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.MoveWindow(hwnd, cur_x, cur_y, target_w, target_h, True)
                cur_x += off_x; cur_y += off_y
        except: pass

    def listar_ventanas(self):
        v = []
        win32gui.EnumWindows(lambda h, _: v.append(f"{win32gui.GetWindowText(h)} (ID: {h})") if win32gui.IsWindowVisible(h) and win32gui.GetWindowText(h) else None, None)
        self.combo_ventanas['values'] = v

    def agregar_estancia(self):
        sel = self.combo_ventanas.get()
        if not sel: return
        try:
            hwnd = int(sel.split("(ID: ")[1].replace(")", ""))
            if hwnd in self.instances: return
            
            usar_ulti_real = self.ulti_var.get() if self.modo_var.get() == "FARMA_EXP" else False
            
            bot = BotInstance(hwnd, sel, self.modo_var.get(), float(self.entry_delay.get() or 5), usar_ulti=usar_ulti_real)
            self.instances[hwnd] = bot; bot.start()
            f = tk.Frame(self.scrollable_frame, bg=COLOR_CARD, pady=5); f.pack(fill="x", pady=2, padx=5)
            tk.Label(f, text=f"🐍 {self.modo_var.get()}", fg=COLOR_ACCENT, bg=COLOR_CARD, font=('Segoe UI', 8, 'bold')).pack(side="left", padx=5)
            tk.Label(f, text=f"{sel[:25]}...", fg="#fff", bg=COLOR_CARD).pack(side="left")
            tk.Button(f, text="EXPULSAR", bg="#441111", fg="white", font=('Segoe UI', 7, 'bold'), command=lambda h=hwnd, fr=f: [self.instances[h].stop(), self.instances.pop(h), fr.destroy()]).pack(side="right", padx=5)
        except: pass

if __name__ == "__main__":
    try:
        root = tk.Tk()
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "sabandijab0tico.ico")
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)

        try:
            from ctypes import windll, byref, sizeof, c_int
            hwnd_title = windll.user32.GetParent(root.winfo_id())
            windll.dwmapi.DwmSetWindowAttribute(hwnd_title, 20, byref(c_int(1)), sizeof(c_int(1)))
        except: pass
        
        App(root); root.mainloop()
    except Exception:
        traceback.print_exc(); input("\nPresiona ENTER para cerrar...")