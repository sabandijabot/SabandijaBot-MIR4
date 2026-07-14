import sys
import ctypes
import os
import tkinter as tk
from tkinter import ttk, messagebox
import win32gui
import win32con
import win32api
import win32process
import psutil
import time
import random
import threading
import subprocess
import configparser
from datetime import datetime

# --- IDENTIFICADOR ÚNICO DE APP ---
try:
    myappid = 'sabandijabot.v2'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except:
    pass

def es_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

if not es_admin():
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    except: pass
    sys.exit()

# --- PALETA SABANDIJA ---
COLOR_BG = "#050a05"        
COLOR_CARD = "#0d1a0d"      
COLOR_ACCENT = "#39ff14"    
COLOR_SECONDARY = "#ccff00" 
COLOR_TEXT_OFF = "#4a5d4a"  
COLOR_TEXT_ON = "#39ff14"   
COLOR_INPUT_BG = "#162616"  

class BotInstance(threading.Thread):
    def __init__(self, hwnd, modo, delay_personalizado=5, usar_ulti=False, apodo=""):
        super().__init__()
        self.hwnd = hwnd
        self.modo = modo
        self.delay_personalizado = delay_personalizado
        self.usar_ulti = usar_ulti
        self.apodo = apodo if apodo.strip() else f"HWND {hwnd}"
        self.running = True
        self.paused = True  
        self.forced_pause = False 
        self.daemon = True

    def enviar_tecla(self, codigo_tecla):
        if not self.running or self.paused: return
        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, codigo_tecla, 0)
        time.sleep(random.uniform(0.05, 0.1))
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, codigo_tecla, 0)

    def run(self):
        while self.running:
            if self.paused:
                time.sleep(0.5)
                continue
                
            try:
                if self.modo == 'MISION_Q':
                    teclas = [0x51, 0x45]
                    random.shuffle(teclas)
                    for t in teclas:
                        if self.paused or not self.running: break
                        self.enviar_tecla(t)
                        time.sleep(random.uniform(0.3, 0.5))
                    
                    for _ in range(3):
                        if self.paused or not self.running: break
                        self.enviar_tecla(0x54)
                        time.sleep(0.25)
                    
                    if not self.paused and self.running:
                        rect = win32gui.GetWindowRect(self.hwnd)
                        ancho = rect[2] - rect[0]
                        alto = rect[3] - rect[1]
                        pos = win32api.MAKELONG(ancho // 2, alto // 2)
                        
                        for _ in range(5):
                            if self.paused or not self.running: break
                            win32gui.PostMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, pos)
                            time.sleep(0.02)
                            win32gui.PostMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, pos)
                            time.sleep(0.25)

                elif self.modo == 'FARMA_EXP':
                    self.enviar_tecla(0x09)
                    time.sleep(0.5)
                    self.enviar_tecla(0x22)
                    time.sleep(0.4)
                    self.enviar_tecla(0x46)
                    
                    if self.usar_ulti:
                        time.sleep(0.4)
                        self.enviar_tecla(0x52)

                elif self.modo == 'SUMMON_BOSS':
                    self.enviar_tecla(0x45)

                if self.modo == 'MISION_Q':
                    delay = random.uniform(5, 10)
                else:
                    delay = self.delay_personalizado

                for _ in range(int(delay * 10)):
                    if not self.running or self.paused: break
                    time.sleep(0.1)
            except:
                self.running = False

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.running = False

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("SABANDIJA B0T - REPTIL EDITION")
        self.root.geometry("700x960")
        self.root.configure(bg=COLOR_BG)
        
        self.instancias_activas = {}
        self.ulti_var = tk.BooleanVar(value=False)
        self.config_file = "config.ini"
        self.config = configparser.ConfigParser()
        
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
        else:
            self.config['RUTAS'] = {
                'steam': r"C:\Program Files (x86)\Steam\steam.exe"
            }
            self.guardar_config()

        self.style = ttk.Style()
        self.theme_usado = self.style.theme_use('clam')
        self.style.configure("TNotebook", background=COLOR_BG, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=COLOR_CARD, foreground=COLOR_TEXT_OFF, padding=[12, 6], font=('Segoe UI', 10, 'bold'))
        self.style.map("TNotebook.Tab", background=[("selected", COLOR_ACCENT)], foreground=[("selected", "#000")])
        self.style.configure("TFrame", background=COLOR_BG)
        self.style.configure("Card.TLabelframe", background=COLOR_BG, foreground=COLOR_ACCENT, bordercolor=COLOR_ACCENT)
        self.style.configure("Card.TLabelframe.Label", background=COLOR_BG, foreground=COLOR_ACCENT, font=('Consolas', 10, 'bold'))

        self.style.configure("Treeview", background=COLOR_CARD, foreground="#fff", fieldbackground=COLOR_CARD, rowheight=24, font=('Segoe UI', 9))
        self.style.configure("Treeview.Heading", background=COLOR_INPUT_BG, foreground=COLOR_ACCENT, font=('Segoe UI', 9, 'bold'))
        self.style.map("Treeview", background=[("selected", COLOR_ACCENT)], foreground=[("selected", "#000")])

        header_frame = tk.Frame(self.root, bg=COLOR_BG)
        header_frame.pack(fill="x", pady=10)
        tk.Label(header_frame, text="🐍 SABANDIJA CONTROL", bg=COLOR_BG, fg=COLOR_ACCENT, font=('Impact', 28)).pack()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        self.tab_bot = ttk.Frame(self.notebook)
        self.tab_layout = ttk.Frame(self.notebook)
        self.tab_despliegue = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_bot, text="  SABANDIJA INSTANCES  ")
        self.notebook.add(self.tab_layout, text="  RECTIL LAYOUT  ")
        self.notebook.add(self.tab_despliegue, text="  DESPLIEGUE  ")

        self.setup_tab_bot()
        self.setup_tab_layout()
        self.setup_tab_despliegue()

        self.running_monitor = True
        self.monitor_thread = threading.Thread(target=self.monitor_foco_ventanas, daemon=True)
        self.monitor_thread.start()

    def guardar_config(self):
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def log_status(self, mensaje):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.txt_log.configure(state='normal')
        self.txt_log.insert(tk.END, f"[{timestamp}] {mensaje}\n")
        self.txt_log.see(tk.END)
        self.txt_log.configure(state='disabled')

    def monitor_foco_ventanas(self):
        while self.running_monitor:
            time.sleep(0.5)
            try:
                hwnd_activo = win32gui.GetForegroundWindow()
                if not hwnd_activo: continue

                cambio_detectado = False

                for hwnd, bot in list(self.instancias_activas.items()):
                    if hwnd == hwnd_activo:
                        if not bot.paused:
                            bot.pause()
                            bot.forced_pause = True  
                            self.log_status(f"👁️ [{bot.apodo}] Auto-Pausado: Ventana en uso por el usuario.")
                            cambio_detectado = True
                    else:
                        if bot.paused and bot.forced_pause:
                            bot.resume()
                            bot.forced_pause = False
                            self.log_status(f"🔄 [{bot.apodo}] Auto-Reanudado: Ventana liberada.")
                            cambio_detectado = True

                if cambio_detectado:
                    self.root.after(0, self.actualizar_tabla_visual)
            except:
                pass

    def setup_tab_bot(self):
        frame_sel = ttk.LabelFrame(self.tab_bot, text=" RECTIL TARGET ", style="Card.TLabelframe")
        frame_sel.pack(fill="x", padx=15, pady=5)

        self.combo_ventanas = ttk.Combobox(frame_sel, state="readonly", width=45, font=('Segoe UI', 10))
        self.combo_ventanas.pack(pady=10, padx=10, side="left", expand=True, fill="x")

        tk.Button(frame_sel, text="🔄 REFRESCAR", bg=COLOR_CARD, fg=COLOR_ACCENT, relief="groove",
                  font=('Segoe UI', 9, 'bold'), activebackground=COLOR_ACCENT, command=self.actualizar_combo).pack(pady=10, padx=10, side="right")

        frame_cfg = ttk.LabelFrame(self.tab_bot, text=" CONFIGURACIÓN OPERATIVA ", style="Card.TLabelframe")
        frame_cfg.pack(fill="x", padx=15, pady=5)

        self.modo_var = tk.StringVar(value="MISION_Q")
        
        self.rb_mision = tk.Radiobutton(frame_cfg, text="MISIÓN Q (AUTO)", variable=self.modo_var, value="MISION_Q",
                                       bg=COLOR_BG, fg=COLOR_TEXT_ON, selectcolor="#000", font=('Segoe UI', 10, 'bold'), command=self.actualizar_radio_colores)
        self.rb_mision.pack(anchor="w", padx=20, pady=2)

        self.rb_farma = tk.Radiobutton(frame_cfg, text="FARMA EXP (AFK)", variable=self.modo_var, value="FARMA_EXP",
                                      bg=COLOR_BG, fg=COLOR_TEXT_OFF, selectcolor="#000", font=('Segoe UI', 10, 'bold'), command=self.actualizar_radio_colores)
        self.rb_farma.pack(anchor="w", padx=20, pady=2)

        self.rb_summon = tk.Radiobutton(frame_cfg, text="SUMMON BOSS (TECLA E)", variable=self.modo_var, value="SUMMON_BOSS",
                                       bg=COLOR_BG, fg=COLOR_TEXT_OFF, selectcolor="#000", font=('Segoe UI', 10, 'bold'), command=self.actualizar_radio_colores)
        self.rb_summon.pack(anchor="w", padx=20, pady=2)

        self.check_ulti = tk.Checkbutton(frame_cfg, text="LANZAR ULTI [R] (Solo Farma)", variable=self.ulti_var,
                                        bg=COLOR_BG, fg=COLOR_TEXT_OFF, selectcolor="#000", state="disabled",
                                        activebackground=COLOR_BG, activeforeground=COLOR_SECONDARY, font=('Segoe UI', 9, 'bold'))
        self.check_ulti.pack(anchor="w", padx=40, pady=2)

        inputs_frame = tk.Frame(frame_cfg, bg=COLOR_BG)
        inputs_frame.pack(fill="x", padx=20, pady=4)
        
        tk.Label(inputs_frame, text="DELAY ACCIÓN (SEG):", bg=COLOR_BG, fg=COLOR_ACCENT, font=('Segoe UI', 9, 'bold')).pack(side="left")
        self.entry_delay = tk.Entry(inputs_frame, width=6, bg=COLOR_INPUT_BG, fg=COLOR_ACCENT, insertbackground=COLOR_ACCENT, borderwidth=0, font=('Consolas', 10, 'bold'))
        self.entry_delay.insert(0, "5")
        self.entry_delay.pack(side="left", padx=5)

        tk.Label(inputs_frame, text="APODO INSTANCIA:", bg=COLOR_BG, fg=COLOR_ACCENT, font=('Segoe UI', 9, 'bold')).pack(side="left", padx=(15, 0))
        self.entry_apodo = tk.Entry(inputs_frame, width=18, bg=COLOR_INPUT_BG, fg="#fff", insertbackground=COLOR_ACCENT, borderwidth=0, font=('Segoe UI', 10))
        self.entry_apodo.pack(side="left", padx=5, fill="x", expand=True)

        # --- PANEL DE INSTANCIAS ACTIVAS (TREEVIEW) ---
        frame_grid_instancias = ttk.LabelFrame(self.tab_bot, text=" INSTANCIAS EN EJECUCIÓN ", style="Card.TLabelframe")
        frame_grid_instancias.pack(fill="x", padx=15, pady=5)

        self.tabla_instancias = ttk.Treeview(frame_grid_instancias, columns=("hwnd", "apodo", "modo", "delay", "estado"), show="headings", height=5)
        self.tabla_instancias.heading("hwnd", text="HWND Target")
        self.tabla_instancias.heading("apodo", text="Apodo")
        self.tabla_instancias.heading("modo", text="Modo Operativo")
        self.tabla_instancias.heading("delay", text="Delay")
        self.tabla_instancias.heading("estado", text="Estado")
        
        self.tabla_instancias.column("hwnd", width=90, anchor="center")
        self.tabla_instancias.column("apodo", width=130, anchor="center")
        self.tabla_instancias.column("modo", width=130, anchor="center")
        self.tabla_instancias.column("delay", width=70, anchor="center")
        self.tabla_instancias.column("estado", width=110, anchor="center")
        self.tabla_instancias.pack(fill="x", padx=5, pady=5)
        
        # Vincular evento de selección de la tabla para cargar datos en caliente
        self.tabla_instancias.bind("<<TreeviewSelect>>", self.cargar_datos_instancia_seleccionada)

        # --- BOTONES DE CONTROL DE INSTANCIA ---
        btn_frame = tk.Frame(self.tab_bot, bg=COLOR_BG)
        btn_frame.pack(pady=5, fill="x", padx=15)

        tk.Button(btn_frame, text="🚀 DESPLEGAR", bg=COLOR_ACCENT, fg="#000",
                 font=('Segoe UI', 9, 'bold'), relief="flat", activebackground=COLOR_SECONDARY, command=self.activar_instancia).pack(side="left", fill="x", expand=True, padx=2)

        tk.Button(btn_frame, text="⚡ ACTUALIZAR", bg=COLOR_SECONDARY, fg="#000",
                 font=('Segoe UI', 9, 'bold'), relief="flat", command=self.actualizar_instancia_en_caliente).pack(side="left", fill="x", expand=True, padx=2)

        tk.Button(btn_frame, text="⏸️ PAUSAR", bg=COLOR_CARD, fg="#ffcc00",
                 font=('Segoe UI', 9, 'bold'), relief="groove", command=self.pausar_instancia).pack(side="left", fill="x", expand=True, padx=2)

        tk.Button(btn_frame, text="▶️ REANUDAR", bg=COLOR_CARD, fg=COLOR_ACCENT,
                 font=('Segoe UI', 9, 'bold'), relief="groove", command=self.reanudar_instancia).pack(side="left", fill="x", expand=True, padx=2)

        tk.Button(btn_frame, text="🛑 DETENER", bg="#660000", fg="#fff",
                 font=('Segoe UI', 9, 'bold'), relief="flat", command=self.detener_instancia).pack(side="left", fill="x", expand=True, padx=2)

        frame_log = ttk.LabelFrame(self.tab_bot, text=" HUNTING LOG ", style="Card.TLabelframe")
        frame_log.pack(fill="both", expand=True, padx=15, pady=5)

        self.txt_log = tk.Text(frame_log, bg="#020502", fg=COLOR_ACCENT, font=('Consolas', 9), state='disabled', borderwidth=0)
        self.txt_log.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.actualizar_combo()
        self.log_status("SabandijaBot inicializado correctamente.")

    def actualizar_radio_colores(self):
        modo = self.modo_var.get()
        if modo == "MISION_Q":
            self.rb_mision.configure(fg=COLOR_TEXT_ON)
            self.rb_farma.configure(fg=COLOR_TEXT_OFF)
            self.rb_summon.configure(fg=COLOR_TEXT_OFF)
            self.check_ulti.configure(state="disabled", fg=COLOR_TEXT_OFF)
        elif modo == "FARMA_EXP":
            self.rb_mision.configure(fg=COLOR_TEXT_OFF)
            self.rb_farma.configure(fg=COLOR_TEXT_ON)
            self.rb_summon.configure(fg=COLOR_TEXT_OFF)
            self.check_ulti.configure(state="normal", fg=COLOR_SECONDARY)
        elif modo == "SUMMON_BOSS":
            self.rb_mision.configure(fg=COLOR_TEXT_OFF)
            self.rb_farma.configure(fg=COLOR_TEXT_OFF)
            self.rb_summon.configure(fg=COLOR_TEXT_ON)
            self.check_ulti.configure(state="disabled", fg=COLOR_TEXT_OFF)

    def actualizar_combo(self):
        ventanas = []
        def enum_windows_proc(hwnd, lParam):
            if win32gui.IsWindowVisible(hwnd):
                titulo = win32gui.GetWindowText(hwnd)
                if "Mir4G" in titulo:
                    ventanas.append(f"{titulo} (HWND: {hwnd})")
            return True
        win32gui.EnumWindows(enum_windows_proc, None)
        self.combo_ventanas['values'] = ventanas
        if ventanas: self.combo_ventanas.current(0)

    def cargar_datos_instancia_seleccionada(self, event):
        seleccion = self.tabla_instancias.selection()
        if not seleccion: return
        
        valores = self.tabla_instancias.item(seleccion[0], "values")
        hwnd = int(valores[0])
        
        if hwnd in self.instancias_activas:
            bot = self.instancias_activas[hwnd]
            self.modo_var.set(bot.modo)
            self.actualizar_radio_colores()
            
            self.entry_delay.delete(0, tk.END)
            self.entry_delay.insert(0, str(bot.delay_personalizado))
            
            self.entry_apodo.delete(0, tk.END)
            self.entry_apodo.insert(0, bot.apodo)
            
            self.ulti_var.set(bot.usar_ulti)

    def actualizar_tabla_visual(self):
        seleccion_actual = self.tabla_instancias.selection()
        hwnd_seleccionado = None
        if seleccion_actual:
            hwnd_seleccionado = self.tabla_instancias.item(seleccion_actual[0], "values")[0]

        for i in self.tabla_instancias.get_children():
            self.tabla_instancias.delete(i)
        
        for hwnd, bot in self.instancias_activas.items():
            if bot.paused:
                estado_texto = "AUTO-PAUSA 👁️" if bot.forced_pause else "PAUSADO ⏸️"
            else:
                estado_texto = "EJECUTANDO ▶️"
                
            if not bot.is_alive() or not bot.running:
                estado_texto = "TERMINADO 🛑"
                
            item = self.tabla_instancias.insert("", tk.END, values=(hwnd, bot.apodo, bot.modo, f"{bot.delay_personalizado}s", estado_texto))
            if hwnd_seleccionado and str(hwnd) == str(hwnd_seleccionado):
                self.tabla_instancias.selection_set(item)

    def obtener_hwnd_seleccionado(self):
        seleccion_tabla = self.tabla_instancias.selection()
        if seleccion_tabla:
            valores = self.tabla_instancias.item(seleccion_tabla[0], "values")
            return int(valores[0])
            
        seleccion_combo = self.combo_ventanas.get()
        if seleccion_combo:
            try:
                return int(seleccion_combo.split("(HWND: ")[1].replace(")", ""))
            except:
                pass
        
        messagebox.showwarning("Atención", "No se seleccionó una instancia en ejecución ni una ventana válida.")
        return None

    def activar_instancia(self):
        seleccion = self.combo_ventanas.get()
        if not seleccion:
            messagebox.showwarning("Atención", "No se seleccionó una ventana objetivo.")
            return
        try:
            hwnd = int(seleccion.split("(HWND: ")[1].replace(")", ""))
            if hwnd in self.instancias_activas and self.instancias_activas[hwnd].is_alive():
                self.log_status(f"⚠️ La ventana HWND {hwnd} ya está bajo control.")
                return
            
            delay = float(self.entry_delay.get())
            modo = self.modo_var.get()
            usar_ulti = self.ulti_var.get() if modo == "FARMA_EXP" else False
            apodo = self.entry_apodo.get().strip()
            
            bot = BotInstance(hwnd, modo, delay, usar_ulti, apodo)
            self.instancias_activas[hwnd] = bot
            bot.start()
            
            self.log_status(f"✅ Control desplegado en [{bot.apodo}] ({modo}). Presiona REANUDAR para iniciar bucle.")
            self.entry_apodo.delete(0, tk.END)
            self.actualizar_tabla_visual()
        except Exception as e:
            self.log_status(f"❌ Error al desplegar control: {str(e)}")

    def actualizar_instancia_en_caliente(self):
        hwnd = self.obtener_hwnd_seleccionado()
        if hwnd and hwnd in self.instancias_activas:
            try:
                bot = self.instancias_activas[hwnd]
                nuevo_modo = self.modo_var.get()
                nuevo_delay = float(self.entry_delay.get())
                nuevo_apodo = self.entry_apodo.get().strip()
                nuevo_usar_ulti = self.ulti_var.get() if nuevo_modo == "FARMA_EXP" else False
                
                bot.modo = nuevo_modo
                bot.delay_personalizado = nuevo_delay
                if nuevo_apodo:
                    bot.apodo = nuevo_apodo
                bot.usar_ulti = nuevo_usar_ulti
                
                self.log_status(f"⚙️ Parámetros actualizados en caliente para [{bot.apodo}] sin detener ejecución.")
                self.actualizar_tabla_visual()
            except Exception as e:
                self.log_status(f"❌ Error al actualizar parámetros: {str(e)}")

    def pausar_instancia(self):
        hwnd = self.obtener_hwnd_seleccionado()
        if hwnd and hwnd in self.instancias_activas:
            bot = self.instancias_activas[hwnd]
            bot.forced_pause = False 
            bot.pause()
            self.log_status(f"⏸️ Instancia [{bot.apodo}] PAUSADA manualmente.")
            self.actualizar_tabla_visual()

    def reanudar_instancia(self):
        hwnd = self.obtener_hwnd_seleccionado()
        if hwnd and hwnd in self.instancias_activas:
            bot = self.instancias_activas[hwnd]
            bot.forced_pause = False
            bot.resume()
            self.log_status(f"▶️ Instancia [{bot.apodo}] REANUDADA / EN CURSO.")
            self.actualizar_tabla_visual()

    def detener_instancia(self):
        hwnd = self.obtener_hwnd_seleccionado()
        if hwnd and hwnd in self.instancias_activas:
            bot = self.instancias_activas[hwnd]
            bot.stop()
            del self.instancias_activas[hwnd]
            self.log_status(f"🛑 Instancia [{bot.apodo}] DETENIDA y eliminada.")
            self.actualizar_tabla_visual()

    def setup_tab_layout(self):
        frame_grid = ttk.LabelFrame(self.tab_layout, text=" RECTIL WINDOWS LAYOUT (GRID) ", style="Card.TLabelframe")
        frame_grid.pack(fill="both", expand=True, padx=15, pady=15)

        self.label_offset = ttk.Label(frame_grid, text="Ajuste de Borde (Offset): 0", background=COLOR_BG, foreground=COLOR_ACCENT, font=('Segoe UI', 10, 'bold'))
        self.label_offset.pack(pady=15)

        self.offset_var = tk.IntVar(value=0)
        self.slider = ttk.Scale(frame_grid, from_=0, to=20, orient='horizontal', variable=self.offset_var, command=self.actualizar_label_offset)
        self.slider.pack(fill="x", padx=30, pady=10)

        tk.Button(frame_grid, text="⚡ ORDENAR VENTANAS EN RECTIL GRID", bg=COLOR_ACCENT, fg="#000", font=('Segoe UI', 12, 'bold'), relief="flat", activebackground=COLOR_SECONDARY, command=self.ordenar_grid_ventanas).pack(pady=40, fill="x", padx=40)

    def actualizar_label_offset(self, val):
        self.label_offset.config(text=f"Ajuste de Borde (Offset): {int(float(val))}")

    def ordenar_grid_ventanas(self):
        v_list = []
        
        def callback_buscar_ventanas(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd):
                titulo = win32gui.GetWindowText(hwnd).upper()
                if "MIR4G" in titulo:
                    v_list.append(hwnd)
            return True

        win32gui.EnumWindows(callback_buscar_ventanas, None)
        v_list.sort()

        if not v_list:
            self.log_status("⚠️ No se encontraron ventanas 'Mir4G' activas.")
            return

        monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0, 0)))
        rect = monitor_info['Work']
        work_x, work_y = rect[0], rect[1]
        work_w, work_h = rect[2] - rect[0], rect[3] - rect[1]

        num = len(v_list)
        cols = int(num**0.5)
        if cols * cols < num: cols += 1
        rows = (num + cols - 1) // cols

        win_w = work_w // cols
        win_h = work_h // rows
        offset = self.offset_var.get()

        try:
            for i, hwnd in enumerate(v_list):
                r, c = i // cols, i % cols
                x = work_x + (c * win_w) - offset
                y = work_y + (r * win_h)
                w = win_w + (offset * 2)
                h = win_h + offset

                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.MoveWindow(hwnd, x, y, w, h, True)
            self.log_status(f"⚡ Grid completado para {num} ventanas (Offset: {offset}).")
        except Exception as e:
            self.log_status(f"⚠️ Error en Layout: {str(e)}")

    def setup_tab_despliegue(self):
        frame_launch = ttk.LabelFrame(self.tab_despliegue, text=" INFRAESTRUCTURA DE ENTORNO ", style="Card.TLabelframe")
        frame_launch.pack(fill="x", padx=15, pady=10)

        tk.Label(frame_launch, text="Ruta Steam Launcher:", bg=COLOR_BG, fg=COLOR_ACCENT, font=('Segoe UI', 9, 'bold')).pack(anchor="w", padx=15, pady=2)
        self.ent_steam = tk.Entry(frame_launch, bg=COLOR_INPUT_BG, fg="#fff", borderwidth=0, font=('Segoe UI', 9))
        
        if 'RUTAS' in self.config and 'steam' in self.config['RUTAS']:
            self.ent_steam.insert(0, self.config['RUTAS']['steam'])
        else:
            self.ent_steam.insert(0, r"C:\Program Files (x86)\Steam\steam.exe")
            
        self.ent_steam.pack(fill="x", padx=15, pady=4)

        tk.Button(frame_launch, text="💾 GUARDAR RUTA", bg=COLOR_CARD, fg=COLOR_SECONDARY, font=('Segoe UI', 9, 'bold'),
                  relief="groove", command=self.guardar_rutas_interfaz).pack(pady=10, anchor="e", padx=15)

        frame_actions = ttk.LabelFrame(self.tab_despliegue, text=" SECUENCIAS AUTOMÁTICAS ", style="Card.TLabelframe")
        frame_actions.pack(fill="both", expand=True, padx=15, pady=10)

        tk.Button(frame_actions, text="🎮 INICIAR MIR4 DESDE STEAM", bg="#0054a6", fg="#fff", font=('Segoe UI', 11, 'bold'),
                  relief="flat", command=self.lanzar_steam).pack(pady=25, fill="x", padx=30)

    def guardar_rutas_interfaz(self):
        if 'RUTAS' not in self.config:
            self.config['RUTAS'] = {}
        self.config['RUTAS']['steam'] = self.ent_steam.get()
        self.guardar_config()
        self.log_status("💾 Ruta de entorno para Steam actualizada.")

    def lanzar_steam(self):
        ruta = self.ent_steam.get()
        if os.path.exists(ruta):
            try:
                subprocess.Popen([ruta, "-applaunch", "1623660"])
                self.log_status("🎮 Solicitud de juego enviada a la infraestructura de Steam.")
            except Exception as e:
                self.log_status(f"❌ Error en Steam: {str(e)}")
        else:
            self.log_status("❌ Archivo ejecutable de Steam no localizado.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()