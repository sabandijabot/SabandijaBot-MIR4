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

# --- IDENTIFICADOR ÚNICO DE APP ---
try:
    myappid = 'sabandijabot.v2'
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
COLOR_ACCENT = "#39ff14"    
COLOR_SECONDARY = "#ccff00" 
COLOR_TEXT_OFF = "#4a5d4a"  
COLOR_TEXT_ON = "#39ff14"   
COLOR_INPUT_BG = "#162616"  

class BotInstance(threading.Thread):
    def __init__(self, hwnd, window_name, modo, delay_personalizado=5, usar_ulti=False, apodo=""):
        super().__init__()
        self.hwnd = hwnd
        self.modo = modo
        self.delay_personalizado = delay_personalizado
        self.usar_ulti = usar_ulti
        self.apodo = apodo
        self.running = True
        self.paused = False
        self.daemon = True

    def toggle_pause(self):
        self.paused = not self.paused
        return self.paused

    def enviar_tecla(self, codigo_tecla):
        if not self.running or self.paused: return
        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, codigo_tecla, 0)
        time.sleep(random.uniform(0.05, 0.1))
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, codigo_tecla, 0)

    def run(self):
        while self.running:
            try:
                if not self.paused:
                    if self.modo == 'MISION_Q':
                        teclas = [0x51, 0x45]; random.shuffle(teclas)
                        for t in teclas: 
                            if not self.running or self.paused: break
                            self.enviar_tecla(t); time.sleep(random.uniform(0.3, 0.5))
                        
                        for _ in range(3): 
                            if not self.running or self.paused: break
                            self.enviar_tecla(0x54); time.sleep(0.25)
                        
                        rect = win32gui.GetWindowRect(self.hwnd)
                        pos = win32api.MAKELONG((rect[2]-rect[0])//2, (rect[3]-rect[1])//2)
                        for _ in range(5):
                            if not self.running or self.paused: break
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

                    elif self.modo == 'CORRE_RAPIDO':
                        self.enviar_tecla(0x54)

                delay = self.delay_personalizado if self.modo in ['FARMA_EXP', 'CORRE_RAPIDO'] else random.uniform(5, 10)
                delay_final = delay * random.uniform(0.9, 1.1)
                
                for _ in range(int(delay_final * 10)):
                    if not self.running: break
                    time.sleep(0.1)
            except: self.running = False

    def stop(self): self.running = False

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("SABANDIJA B0T")
        self.root.geometry("600x850")
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
        self.notebook.add(self.tab_layout, text="  ORDERNAR VENTANAS  ")
        
        self.setup_tab_bot()
        self.setup_tab_layout()

        self.version_str = self.obtener_version_estatica()
        tk.Label(self.root, text=self.version_str, bg=COLOR_BG, fg=COLOR_TEXT_OFF, 
                 font=('Consolas', 8)).pack(side="bottom", anchor="se", padx=10, pady=5)

    def obtener_version_estatica(self):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        archivo_ver = os.path.join(base_path, "version.txt")
        version = 0
        if os.path.exists(archivo_ver):
            with open(archivo_ver, "r") as f:
                try:
                    linea = f.read().strip()
                    version = int(linea) if linea else 0
                except: pass
        return f"v2.0.{version}"

    def update_radio_colors(self):
        modo = self.modo_var.get()
        self.rb_mision.configure(fg=COLOR_TEXT_OFF)
        self.rb_farma.configure(fg=COLOR_TEXT_OFF)
        self.rb_corre.configure(fg=COLOR_TEXT_OFF)
        self.check_ulti.configure(state="disabled", fg=COLOR_TEXT_OFF)

        if modo == "MISION_Q":
            self.rb_mision.configure(fg=COLOR_TEXT_ON)
        elif modo == "FARMA_EXP":
            self.rb_farma.configure(fg=COLOR_TEXT_ON)
            self.check_ulti.configure(state="normal", fg=COLOR_SECONDARY)
        elif modo == "CORRE_RAPIDO":
            self.rb_corre.configure(fg=COLOR_TEXT_ON)

    def setup_tab_bot(self):
        frame_sel = ttk.LabelFrame(self.tab_bot, text=" SELECCIONA VENTANA ", style="Card.TLabelframe")
        frame_sel.pack(fill="x", padx=15, pady=10)
        self.combo_ventanas = ttk.Combobox(frame_sel, state="readonly", width=40)
        self.combo_ventanas.pack(pady=5, padx=10)
        
        apodo_frame = tk.Frame(frame_sel, bg=COLOR_BG)
        apodo_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(apodo_frame, text="IDENTIFICADOR:", bg=COLOR_BG, fg=COLOR_TEXT_OFF, font=('Segoe UI', 8, 'bold')).pack(side="left")
        self.entry_apodo = tk.Entry(apodo_frame, bg=COLOR_INPUT_BG, fg=COLOR_ACCENT, borderwidth=0, font=('Consolas', 10), insertbackground=COLOR_ACCENT)
        self.entry_apodo.pack(side="left", padx=5, fill="x", expand=True)
        
        tk.Button(frame_sel, text="REFRESCAR VISIÓN", bg=COLOR_CARD, fg=COLOR_ACCENT, relief="groove", 
                  command=self.listar_ventanas).pack(pady=5)
        
        frame_cfg = ttk.LabelFrame(self.tab_bot, text=" MODO DE CAZA ", style="Card.TLabelframe")
        frame_cfg.pack(fill="x", padx=15, pady=10)
        self.modo_var = tk.StringVar(value="MISION_Q")
        
        self.rb_mision = tk.Radiobutton(frame_cfg, text="MISIÓN Q (AUTO)", variable=self.modo_var, value="MISION_Q", 
                                       bg=COLOR_BG, fg=COLOR_TEXT_ON, selectcolor="#000", command=self.update_radio_colors)
        self.rb_mision.pack(anchor="w", padx=20)
        
        self.rb_farma = tk.Radiobutton(frame_cfg, text="FARMA EXP (AFK)", variable=self.modo_var, value="FARMA_EXP", 
                                      bg=COLOR_BG, fg=COLOR_TEXT_OFF, selectcolor="#000", command=self.update_radio_colors)
        self.rb_farma.pack(anchor="w", padx=20)

        self.rb_corre = tk.Radiobutton(frame_cfg, text="CORRE RÁPIDO (T)", variable=self.modo_var, value="CORRE_RAPIDO", 
                                      bg=COLOR_BG, fg=COLOR_TEXT_OFF, selectcolor="#000", command=self.update_radio_colors)
        self.rb_corre.pack(anchor="w", padx=20)
        
        self.check_ulti = tk.Checkbutton(frame_cfg, text="LANZAR ULTI [R]", variable=self.ulti_var,
                                        bg=COLOR_BG, fg=COLOR_TEXT_OFF, selectcolor="#000", state="disabled")
        self.check_ulti.pack(anchor="w", padx=40)
        
        delay_frame = tk.Frame(frame_cfg, bg=COLOR_BG)
        delay_frame.pack(pady=5)
        tk.Label(delay_frame, text="DELAY (SEG):", bg=COLOR_BG, fg=COLOR_TEXT_OFF, font=('Segoe UI', 8, 'bold')).pack(side="left", padx=5)
        self.entry_delay = tk.Entry(delay_frame, width=10, bg=COLOR_INPUT_BG, fg=COLOR_ACCENT, borderwidth=0, insertbackground=COLOR_ACCENT)
        self.entry_delay.insert(0, "5")
        self.entry_delay.pack(side="left")
        
        tk.Button(self.tab_bot, text="DESPLEGAR AL SABANDIJA", bg=COLOR_ACCENT, fg="#000", 
                 font=('Segoe UI', 12, 'bold'), command=self.agregar_estancia).pack(pady=15, fill="x", padx=30)
        
        frame_list = ttk.LabelFrame(self.tab_bot, text=" HUNTING LOG ", style="Card.TLabelframe")
        frame_list.pack(fill="both", expand=True, padx=15, pady=10)
        self.canvas = tk.Canvas(frame_list, bg=COLOR_BG, highlightthickness=0)
        self.scrollable_frame = tk.Frame(self.canvas, bg=COLOR_BG)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.listar_ventanas()

    def setup_tab_layout(self):
        frame_res = ttk.LabelFrame(self.tab_layout, text=" AJUSTE DE VENTANAS ", style="Card.TLabelframe")
        frame_res.pack(fill="both", expand=True, padx=15, pady=15)
        
        tk.Label(frame_res, text="OPTIMIZACIÓN AUTOMÁTICA", bg=COLOR_BG, fg=COLOR_TEXT_OFF, font=('Segoe UI', 10, 'bold')).pack(pady=20)
        
        tk.Button(frame_res, text="AUTO AJUSTAR TODAS LAS VENTANAS", bg=COLOR_ACCENT, fg="#000", font=('Segoe UI', 12, 'bold'), 
                  command=self.auto_ajustar_grid).pack(pady=10, padx=40, fill="x")
        
        tk.Label(frame_res, text="* Organiza las ventanas de MIR4 en cuadrícula\nsegún el espacio disponible en pantalla.", 
                 bg=COLOR_BG, fg=COLOR_TEXT_OFF, font=('Segoe UI', 8), justify="center").pack(pady=10)

    def auto_ajustar_grid(self):
        try:
            offset = 8
            v_list = []
            win32gui.EnumWindows(lambda h, _: v_list.append(h) if win32gui.IsWindowVisible(h) and "MIR4" in win32gui.GetWindowText(h).upper() else None, None)
            v_list.sort()
            if not v_list: return
            rect_trabajo = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0,0)))['Work']
            area_x, area_y = rect_trabajo[0], rect_trabajo[1]
            area_w, area_h = rect_trabajo[2] - area_x, rect_trabajo[3] - area_y
            cols = int(len(v_list)**0.5)
            if cols * cols < len(v_list): cols += 1
            rows = (len(v_list) + cols - 1) // cols
            win_w, win_h = area_w // cols, area_h // rows
            for i, hwnd in enumerate(v_list):
                r, c = i // cols, i % cols
                x = area_x + (c * win_w) - offset
                y = area_y + (r * win_h)
                ancho = win_w + (offset * 2)
                alto = win_h + offset
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.MoveWindow(hwnd, x, y, ancho, alto, True)
        except: pass

    def listar_ventanas(self):
        v = []
        def callback(h, _):
            if win32gui.IsWindowVisible(h):
                title = win32gui.GetWindowText(h)
                if title.upper().startswith("MIR4"):
                    v.append(f"{title} (ID: {h})")
        win32gui.EnumWindows(callback, None)
        self.combo_ventanas['values'] = v

    def agregar_estancia(self):
        sel = self.combo_ventanas.get()
        apodo = self.entry_apodo.get().strip().upper() or "S/N"
        if not sel: return
        try:
            hwnd = int(sel.split("(ID: ")[1].replace(")", ""))
            if hwnd in self.instances: return
            
            bot = BotInstance(hwnd, sel, self.modo_var.get(), float(self.entry_delay.get() or 5), usar_ulti=self.ulti_var.get(), apodo=apodo)
            self.instances[hwnd] = bot; bot.start()
            
            f = tk.Frame(self.scrollable_frame, bg=COLOR_CARD, pady=5)
            f.pack(fill="x", pady=2, padx=5)
            
            lbl_apodo = tk.Label(f, text=f"[{apodo}]", fg=COLOR_SECONDARY, bg=COLOR_CARD, font=('Consolas', 9, 'bold'), width=12, anchor="w")
            lbl_apodo.pack(side="left", padx=5)
            
            lbl_modo = tk.Label(f, text=f"| {self.modo_var.get()}", fg=COLOR_ACCENT, bg=COLOR_CARD, font=('Segoe UI', 8, 'bold'))
            lbl_modo.pack(side="left", padx=2)

            def toggle_pause_ui(h=hwnd, label=lbl_modo):
                is_paused = self.instances[h].toggle_pause()
                if is_paused:
                    btn_pause.config(text="▶", bg="#444411", fg=COLOR_SECONDARY)
                    label.config(fg=COLOR_TEXT_OFF)
                else:
                    btn_pause.config(text="⏸", bg="#113311", fg=COLOR_ACCENT)
                    label.config(fg=COLOR_ACCENT)

            btn_pause = tk.Button(f, text="⏸", bg="#113311", fg=COLOR_ACCENT, font=('Segoe UI', 7, 'bold'), width=3,
                                 command=toggle_pause_ui)
            btn_pause.pack(side="right", padx=2)

            tk.Button(f, text="X", bg="#441111", fg="white", font=('Segoe UI', 7, 'bold'), width=3,
                      command=lambda h=hwnd, fr=f: [self.instances[h].stop(), self.instances.pop(h), fr.destroy()]).pack(side="right", padx=5)
            
            tk.Label(f, text=f"| {sel[:15]}...", fg="#666", bg=COLOR_CARD, font=('Segoe UI', 7), anchor="w").pack(side="left", fill="x", expand=True, padx=2)
            
            self.entry_apodo.delete(0, tk.END)
        except: pass

if __name__ == "__main__":
    try:
        root = tk.Tk()
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "sabandijab0tico.ico")
        if os.path.exists(icon_path): root.iconbitmap(icon_path)
        App(root); root.mainloop()
    except Exception:
        traceback.print_exc(); input()