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
import subprocess
import json
from datetime import datetime

# --- CONFIGURACIÓN GLOBAL ---
APP_VERSION = "v14.2" # Versión actualizada con CRUD

# --- VERIFICAR DEPENDENCIA UIAUTOMATION ---
try:
    from pywinauto import Desktop
    UIA_AVAILABLE = True
except ImportError:
    UIA_AVAILABLE = False

# --- CONSTANTES DE TECLADO ---
VK_Q = 0x51
VK_E = 0x45
VK_T = 0x54
VK_TAB = 0x09
VK_DOWN = 0x22
VK_F = 0x46
VK_R = 0x52

try:
    myappid = f'sabandijabot.{APP_VERSION}'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

# --- FUNCIONES AUXILIARES ---
def esperar_ventana(identificador_buscado, timeout=60):
    buscar_por_clase = identificador_buscado.upper().startswith("CLASS:")
    texto_buscar = identificador_buscado[6:] if buscar_por_clase else identificador_buscado
    inicio = time.time()
    while time.time() - inicio < timeout:
        ventanas_encontradas = []
        def callback(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd):
                if buscar_por_clase:
                    if texto_buscar in win32gui.GetClassName(hwnd): ventanas_encontradas.append(hwnd)
                else:
                    if texto_buscar in win32gui.GetWindowText(hwnd): ventanas_encontradas.append(hwnd)
            return True
        win32gui.EnumWindows(callback, None)
        if ventanas_encontradas: return ventanas_encontradas[0]
        time.sleep(0.5)
    return None

def enviar_clic_ventana(hwnd, x, y):
    if not hwnd: return False
    placement = win32gui.GetWindowPlacement(hwnd)
    if placement[1] == win32con.SW_SHOWMINIMIZED:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        time.sleep(1)
    lParam = win32api.MAKELONG(x, y)
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    time.sleep(0.1)
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, None, lParam)
    return True

# --- PALETA SABANDIJA ---
COLOR_BG = "#050a05"
COLOR_CARD = "#0d1a0d"
COLOR_ACCENT = "#39ff14"
COLOR_SECONDARY = "#ccff00"
COLOR_TEXT_OFF = "#4a5d4a"
COLOR_TEXT_ON = "#39ff14"
COLOR_INPUT_BG = "#162616"
COLOR_CAPTURA = "#ff0000"

COLOR_DISABLED_BG = "#1a1a1a"
COLOR_DISABLED_FG = "#555555"

# --- CLASE FRAME CON SCROLL ---
class ScrollableFrame(ttk.Frame):
    def __init__(self, parent, bg_color, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.canvas = tk.Canvas(self, bg=bg_color, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.scrollable_frame = ttk.Frame(self.canvas, style="TFrame")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind("<Enter>", self._bound_to_mousewheel)
        self.canvas.bind("<Leave>", self._unbound_to_mousewheel)

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.window_id, width=event.width)

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")


class BotInstance(threading.Thread):
    def __init__(self, hwnd, modo, delay_personalizado=5, usar_ulti=False, apodo=""):
        super().__init__()
        self.hwnd = hwnd
        self.modo = modo
        self.delay_personalizado = delay_personalizado
        self.usar_ulti = usar_ulti
        self.apodo = apodo if apodo.strip() else f"HWND {hwnd}"
        self.running = True
        self.paused = False
        self.forced_pause = False
        self.manual_pause = False
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
                    teclas = [VK_Q, VK_E]
                    random.shuffle(teclas)
                    for t in teclas:
                        if self.paused or not self.running: break
                        self.enviar_tecla(t)
                        time.sleep(random.uniform(0.3, 0.5))
                    for _ in range(3):
                        if self.paused or not self.running: break
                        self.enviar_tecla(VK_T)
                        time.sleep(0.25)
                    if not self.paused and self.running:
                        rect = win32gui.GetWindowRect(self.hwnd)
                        ancho = rect[2] - rect[0]
                        alto = rect[3] - rect[1]
                        pos = win32api.MAKELONG(ancho // 2, alto // 2)
                        for _ in range(5):
                            if self.paused or not self.running: break
                            win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, pos)
                            time.sleep(0.02)
                            win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, pos)
                            time.sleep(0.25)
                elif self.modo == 'FARMA_EXP':
                    self.enviar_tecla(VK_TAB)
                    time.sleep(0.5)
                    self.enviar_tecla(VK_DOWN)
                    time.sleep(0.4)
                    self.enviar_tecla(VK_F)
                    if self.usar_ulti:
                        time.sleep(0.4)
                        self.enviar_tecla(VK_R)
                elif self.modo == 'SUMMON_BOSS':
                    self.enviar_tecla(VK_E)

                delay = random.uniform(5, 10) if self.modo == 'MISION_Q' else self.delay_personalizado
                for _ in range(int(delay * 10)):
                    if not self.running or self.paused: break
                    time.sleep(0.1)
            except Exception:
                pass

    def pause(self): self.paused = True
    def resume(self): self.paused = False
    def stop(self): self.running = False


class App:
    def __init__(self, root):
        self.root = root
        self.root.title(f"SABANDIJA B0T - EDITION {APP_VERSION}")
        self.root.geometry("780x720") 
        self.root.minsize(600, 500)   
        self.root.configure(bg=COLOR_BG)
             # Cargar el ícono para la ventana de la app
        try:
            if getattr(sys, 'frozen', False):
                # Si es un .exe, busca el ícono en la carpeta temporal de descompresión
                icon_path = os.path.join(sys._MEIPASS, "sabandijab0tico.ico")
            else:
                # Si es un .py, busca en la misma carpeta
                icon_path = "sabandijab0tico.ico"
            self.root.iconbitmap(icon_path)
        except Exception:
            pass

        self.instancias_activas = {}
        self.ulti_var = tk.BooleanVar(value=False)
        self.capturando_activo = False
        self.item_a_hwnd = {} # Mapeo invisible entre fila de tabla y HWND
        
        # --- CORRECCIÓN PARA .EXE ---
        if getattr(sys, 'frozen', False):
            dir_aplicacion = os.path.dirname(sys.executable)
        else:
            dir_aplicacion = os.path.dirname(os.path.abspath(__file__))
        self.config_file = os.path.join(dir_aplicacion, "config.json")
        
        self.config = {}

        # --- CARGA / CREACIÓN DE JSON ---
        if not os.path.exists(self.config_file):
            self.config = {
                'RUTAS': {'steam': r"C:\Program Files (x86)\Steam\steam.exe"},
                'LAUNCHER': {
                    'ruta': r"C:\Wemade\Mir4Global\Mir4Launcher\Mir4Launcher.exe",
                    'g1_x': 815, 'g1_y': 539, 'g2_x': 968, 'g2_y': 541,
                    'titulo': "CLASS:HwndWrapper[Mir4Launcher.exe",
                    'delay_pre_click': 15, 'delay': 15
                },
                'LAYOUT': {'offset': 0}
            }
            self.guardar_config()
        else:
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except Exception as e:
                print(f"Error cargando JSON: {e}")
                self.config = {}

        if 'RUTAS' not in self.config:
            self.config['RUTAS'] = {'steam': r"C:\Program Files (x86)\Steam\steam.exe"}
            self.guardar_config()
        if 'LAUNCHER' not in self.config:
            self.config['LAUNCHER'] = {
                'ruta': r"C:\Wemade\Mir4Global\Mir4Launcher\Mir4Launcher.exe",
                'g1_x': 815, 'g1_y': 539, 'g2_x': 968, 'g2_y': 541,
                'titulo': "CLASS:HwndWrapper[Mir4Launcher.exe",
                'delay_pre_click': 15, 'delay': 15
            }
            self.guardar_config()
        if 'LAYOUT' not in self.config:
            self.config['LAYOUT'] = {'offset': 0}
            self.guardar_config()

        self.style = ttk.Style()
        self.style.theme_use('clam')
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
        header_frame.pack(fill="x", pady=5)
        tk.Label(header_frame, text="🐍 SABANDIJA CONTROL", bg=COLOR_BG, fg=COLOR_ACCENT, font=('Impact', 24)).pack()

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

        self.log_status("🛡️ Sistema CRUD activado. Crea, edita y ejecuta tus perfiles fácilmente.")

        self.running_monitor = True
        self.monitor_thread = threading.Thread(target=self.monitor_foco_ventanas, daemon=True)
        self.monitor_thread.start()

    # --- SISTEMA DE POPUPS ---
    def mostrar_alerta(self, titulo, mensaje, es_error=False):
        popup = tk.Toplevel(self.root)
        popup.title(titulo)
        popup.geometry("400x180")
        popup.configure(bg=COLOR_BG)
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.grab_set()

        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 90
        popup.geometry(f"+{x}+{y}")

        color_titulo = COLOR_CAPTURA if es_error else "#ffcc00"
        icono = "❌" if es_error else "⚠️"

        tk.Label(popup, text=f"{icono} {titulo}", bg=COLOR_BG, fg=color_titulo, font=('Segoe UI', 12, 'bold')).pack(pady=(20, 10))
        tk.Label(popup, text=mensaje, bg=COLOR_BG, fg="#ffffff", font=('Segoe UI', 10), justify="center").pack(pady=5)

        tk.Button(popup, text="ENTENDIDO", bg=COLOR_CARD, fg=COLOR_ACCENT, activebackground=COLOR_ACCENT, activeforeground="#000", font=('Segoe UI', 9, 'bold'), relief="groove", width=15, command=popup.destroy).pack(pady=(15, 10))

    def pedir_confirmacion(self, titulo, mensaje):
        self.resultado_confirmacion = False
        popup = tk.Toplevel(self.root)
        popup.title(titulo)
        popup.geometry("400x180")
        popup.configure(bg=COLOR_BG)
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.grab_set()

        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 90
        popup.geometry(f"+{x}+{y}")

        tk.Label(popup, text=f"❓ {titulo}", bg=COLOR_BG, fg=COLOR_SECONDARY, font=('Segoe UI', 12, 'bold')).pack(pady=(20, 10))
        tk.Label(popup, text=mensaje, bg=COLOR_BG, fg="#ffffff", font=('Segoe UI', 10), justify="center").pack(pady=5)

        def on_yes():
            self.resultado_confirmacion = True
            popup.destroy()

        def on_no():
            self.resultado_confirmacion = False
            popup.destroy()

        btn_frame = tk.Frame(popup, bg=COLOR_BG)
        btn_frame.pack(pady=(15, 10))

        tk.Button(btn_frame, text="SÍ, ELIMINAR", bg="#330000", fg="#ff0000", activebackground="#ff0000", activeforeground="#fff", font=('Segoe UI', 9, 'bold'), relief="groove", width=15, command=on_yes).pack(side="left", padx=10)
        tk.Button(btn_frame, text="CANCELAR", bg=COLOR_CARD, fg=COLOR_ACCENT, activebackground=COLOR_ACCENT, activeforeground="#000", font=('Segoe UI', 9, 'bold'), relief="groove", width=15, command=on_no).pack(side="left", padx=10)

        self.root.wait_window(popup)
        return self.resultado_confirmacion

    # --- LOG Y MONITOR ---
    def log_status(self, mensaje):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.root.after(0, self._insertar_log, f"[{timestamp}] {mensaje}\n")

    def _insertar_log(self, texto):
        self.txt_log.configure(state='normal')
        self.txt_log.insert(tk.END, texto)
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
                    if not bot.is_alive(): continue
                    if hwnd == hwnd_activo:
                        if not bot.paused:
                            bot.pause(); bot.forced_pause = True
                            self.log_status(f"👁️ [{bot.apodo}] Auto-Pausado.")
                            cambio_detectado = True
                    else:
                        if bot.paused and bot.forced_pause and not bot.manual_pause:
                            bot.resume(); bot.forced_pause = False
                            self.log_status(f"🔄 [{bot.apodo}] Auto-Reanudado.")
                            cambio_detectado = True
                if cambio_detectado: self.root.after(0, self.actualizar_tabla_visual)
            except Exception: pass

    # --- TAB BOT (SISTEMA CRUD) ---
    def setup_tab_bot(self):
        scroll_wrapper = ScrollableFrame(self.tab_bot, COLOR_BG)
        scroll_wrapper.pack(fill="both", expand=True)
        container = scroll_wrapper.scrollable_frame

        # 1. LISTA DE PERFILES E INSTANCIAS (READ)
        frame_lista = ttk.LabelFrame(container, text=" 📋 INSTANCIAS Y PERFILES GUARDADOS ", style="Card.TLabelframe")
        frame_lista.pack(fill="x", padx=15, pady=5)
        
        self.tabla_instancias = ttk.Treeview(frame_lista, columns=("apodo", "modo", "ventana", "delay", "estado"), show="headings", height=6)
        for col, txt, w in [("apodo","Apodo",120), ("modo","Modo",110), ("ventana","Ventana Asignada",180), ("delay","Delay",60), ("estado","Estado",110)]:
            self.tabla_instancias.heading(col, text=txt); self.tabla_instancias.column(col, width=w, anchor="center")
        self.tabla_instancias.pack(fill="x", padx=5, pady=5)
        self.tabla_instancias.bind("<<TreeviewSelect>>", self.cargar_datos_seleccionados)

        # 2. FORMULARIO DE EDICIÓN (CREATE / UPDATE)
        frame_form = ttk.LabelFrame(container, text=" 🛠️ CONFIGURACIÓN DEL PERFIL ", style="Card.TLabelframe")
        frame_form.pack(fill="x", padx=15, pady=5)
        
        self.modo_var = tk.StringVar(value="MISION_Q")

        # Fila 1: Apodo y Ventana
        f1 = tk.Frame(frame_form, bg=COLOR_BG); f1.pack(fill="x", padx=15, pady=5)
        tk.Label(f1, text="APODO:", bg=COLOR_BG, fg=COLOR_ACCENT, font=('Segoe UI', 9, 'bold'), width=10).pack(side="left")
        self.entry_apodo = tk.Entry(f1, width=15, bg=COLOR_INPUT_BG, fg="#fff", insertbackground=COLOR_ACCENT, borderwidth=0, font=('Segoe UI', 10))
        self.entry_apodo.pack(side="left", padx=5)
        
        tk.Label(f1, text="VENTANA:", bg=COLOR_BG, fg=COLOR_ACCENT, font=('Segoe UI', 9, 'bold'), width=10).pack(side="left", padx=(10,0))
        self.combo_ventanas = ttk.Combobox(f1, state="readonly", width=30, font=('Segoe UI', 9))
        self.combo_ventanas.pack(side="left", padx=5, fill="x", expand=True)
        tk.Button(f1, text="🔄", bg=COLOR_CARD, fg=COLOR_ACCENT, relief="groove", command=self.actualizar_combo).pack(side="left", padx=2)

        # Fila 2: Modos
        f2 = tk.Frame(frame_form, bg=COLOR_BG); f2.pack(fill="x", padx=15, pady=2)
        def on_mode_change():
            self.actualizar_radio_colores()
        self.rb_mision = tk.Radiobutton(f2, text="MISIÓN Q", variable=self.modo_var, value="MISION_Q", bg=COLOR_BG, fg=COLOR_TEXT_ON, selectcolor="#000", font=('Segoe UI', 9, 'bold'), command=on_mode_change)
        self.rb_mision.pack(side="left", padx=5)
        self.rb_farma = tk.Radiobutton(f2, text="FARMA EXP", variable=self.modo_var, value="FARMA_EXP", bg=COLOR_BG, fg=COLOR_TEXT_OFF, selectcolor="#000", font=('Segoe UI', 9, 'bold'), command=on_mode_change)
        self.rb_farma.pack(side="left", padx=5)
        self.rb_summon = tk.Radiobutton(f2, text="SUMMON BOSS", variable=self.modo_var, value="SUMMON_BOSS", bg=COLOR_BG, fg=COLOR_TEXT_OFF, selectcolor="#000", font=('Segoe UI', 9, 'bold'), command=on_mode_change)
        self.rb_summon.pack(side="left", padx=5)

        # Fila 3: Delay y Ulti
        f3 = tk.Frame(frame_form, bg=COLOR_BG); f3.pack(fill="x", padx=15, pady=5)
        tk.Label(f3, text="DELAY (SEG):", bg=COLOR_BG, fg=COLOR_ACCENT, font=('Segoe UI', 9, 'bold')).pack(side="left")
        self.entry_delay = tk.Entry(f3, width=5, bg=COLOR_INPUT_BG, fg=COLOR_ACCENT, insertbackground=COLOR_ACCENT, borderwidth=0, font=('Consolas', 10, 'bold'))
        self.entry_delay.insert(0, "5"); self.entry_delay.pack(side="left", padx=5)
        self.check_ulti = tk.Checkbutton(f3, text="LANZAR ULTI [R]", variable=self.ulti_var, bg=COLOR_BG, fg=COLOR_TEXT_OFF, selectcolor="#000", state="disabled", activebackground=COLOR_BG, activeforeground=COLOR_SECONDARY, font=('Segoe UI', 9, 'bold'), command=on_mode_change)
        self.check_ulti.pack(side="left", padx=15)

        # Botones CRUD
        btn_crud_frame = tk.Frame(frame_form, bg=COLOR_BG); btn_crud_frame.pack(fill="x", padx=15, pady=5)
        tk.Button(btn_crud_frame, text="🆕 NUEVO", bg=COLOR_CARD, fg="#fff", font=('Segoe UI', 9, 'bold'), relief="groove", command=self.limpiar_formulario).pack(side="left", fill="x", expand=True, padx=2)
        tk.Button(btn_crud_frame, text="💾 GUARDAR / ACTUALIZAR", bg=COLOR_ACCENT, fg="#000", font=('Segoe UI', 9, 'bold'), relief="flat", command=self.guardar_o_actualizar_perfil).pack(side="left", fill="x", expand=True, padx=2)
        tk.Button(btn_crud_frame, text="🗑️ ELIMINAR", bg="#330000", fg="#ff0000", font=('Segoe UI', 9, 'bold'), relief="groove", command=self.eliminar_perfil_seleccionado).pack(side="left", fill="x", expand=True, padx=2)

        # 3. CONTROL DE EJECUCIÓN
        frame_exec = ttk.LabelFrame(container, text=" 🎮 CONTROL DE EJECUCIÓN ", style="Card.TLabelframe")
        frame_exec.pack(fill="x", padx=15, pady=5)
        
        btn_exec_frame = tk.Frame(frame_exec, bg=COLOR_BG); btn_exec_frame.pack(pady=5, fill="x", padx=10)

        self.btn_iniciar = tk.Button(btn_exec_frame, text="🚀 INICIAR BOT", font=('Segoe UI', 9, 'bold'), relief="flat", command=self.iniciar_instancia)
        self.btn_iniciar.pack(side="left", fill="x", expand=True, padx=2)

        self.btn_pausar = tk.Button(btn_exec_frame, text="⏸️ PAUSAR", font=('Segoe UI', 9, 'bold'), relief="flat", command=self.pausar_instancia)
        self.btn_pausar.pack(side="left", fill="x", expand=True, padx=2)

        self.btn_reanudar = tk.Button(btn_exec_frame, text="▶️ REANUDAR", font=('Segoe UI', 9, 'bold'), relief="flat", command=self.reanudar_instancia)
        self.btn_reanudar.pack(side="left", fill="x", expand=True, padx=2)

        self.btn_detener = tk.Button(btn_exec_frame, text="🛑 DETENER", font=('Segoe UI', 9, 'bold'), relief="flat", command=self.detener_instancia)
        self.btn_detener.pack(side="left", fill="x", expand=True, padx=2)

        # 4. PANICO Y LOG
        btn_panico = tk.Button(container, text="☠️ BOTÓN DE PÁNICO (CERRAR TODO MIR4) ☠️",
                               bg="#cc0000", fg="#ffffff", font=('Segoe UI', 9, 'bold'), 
                               relief="flat", activebackground="#ff3333", 
                               pady=4, command=self.boton_de_panico)
        btn_panico.pack(fill="x", padx=15, pady=(5, 5))

        frame_log = ttk.LabelFrame(container, text=" HUNTING LOG ", style="Card.TLabelframe")
        frame_log.pack(fill="both", expand=True, padx=15, pady=5)
        self.txt_log = tk.Text(frame_log, bg="#020502", fg=COLOR_ACCENT, font=('Consolas', 9), state='disabled', borderwidth=0, height=8)
        self.txt_log.pack(fill="both", expand=True, padx=5, pady=5)

        self.actualizar_combo()
        self.actualizar_tabla_visual()

        estado_uia = "✅ UIAutomation Seguro Cargado" if UIA_AVAILABLE else "❌ FALTA: Ejecuta 'pip install pywinauto'"
        self.log_status(f"SabandijaBot {APP_VERSION} inicializado. [{estado_uia}]")

        ruta_abs_json = os.path.abspath(self.config_file)
        if os.path.exists(self.config_file):
            self.log_status(f"📁 Archivo de configuración JSON ubicado en:\n   {ruta_abs_json}")
        else:
            self.log_status(f"⚠️ No se encontró el archivo JSON. Se creará en:\n   {ruta_abs_json}")

    # --- LÓGICA CRUD ---
    def limpiar_formulario(self):
        self.tabla_instancias.selection_remove(self.tabla_instancias.selection())
        self.entry_apodo.delete(0, tk.END)
        self.entry_delay.delete(0, tk.END)
        self.entry_delay.insert(0, "5")
        self.modo_var.set("MISION_Q")
        self.ulti_var.set(False)
        self.actualizar_radio_colores()
        if self.combo_ventanas['values']:
            self.combo_ventanas.current(0)
        self.evaluar_estado_botones_seleccion()
        self.log_status("📝 Formulario limpio. Listo para crear un nuevo perfil.")

    def cargar_datos_seleccionados(self, event=None):
        sel = self.tabla_instancias.selection()
        if not sel: return
        item = sel[0]
        hwnd_val = self.item_a_hwnd.get(item)
        valores = self.tabla_instancias.item(item, "values")
        apodo_val = str(valores[0])

        if isinstance(hwnd_val, int) and hwnd_val in self.instancias_activas:
            bot = self.instancias_activas[hwnd_val]
            self.modo_var.set(bot.modo); self.actualizar_radio_colores()
            self.entry_delay.delete(0, tk.END); self.entry_delay.insert(0, str(bot.delay_personalizado))
            self.entry_apodo.delete(0, tk.END); self.entry_apodo.insert(0, bot.apodo)
            self.ulti_var.set(bot.usar_ulti)
            
            # Seleccionar ventana en combo
            for i, val in enumerate(self.combo_ventanas['values']):
                if f"(HWND: {hwnd_val})" in val:
                    self.combo_ventanas.current(i)
                    break
        elif apodo_val in self.config:
            perfil = self.config[apodo_val]
            self.modo_var.set(perfil.get("modo", "MISION_Q"))
            self.actualizar_radio_colores()
            self.entry_delay.delete(0, tk.END)
            self.entry_delay.insert(0, str(perfil.get("delay", 5.0)))
            self.ulti_var.set(perfil.get("ulti", False))
            self.entry_apodo.delete(0, tk.END)
            self.entry_apodo.insert(0, apodo_val)
            
            ventana_guardada = perfil.get("ventana_titulo", "")
            if ventana_guardada:
                for i, val in enumerate(self.combo_ventanas['values']):
                    if ventana_guardada in val:
                        self.combo_ventanas.current(i)
                        break

        self.evaluar_estado_botones_seleccion()

    def guardar_o_actualizar_perfil(self):
        apodo = self.entry_apodo.get().strip()
        if not apodo:
            self.mostrar_alerta("Atención", "Debes ingresar un APODO\npara guardar el perfil.")
            return

        # Si el bot está corriendo, actualizamos en caliente
        sel = self.tabla_instancias.selection()
        item = sel[0] if sel else None
        hwnd_val = self.item_a_hwnd.get(item) if item else None

        if isinstance(hwnd_val, int) and hwnd_val in self.instancias_activas:
            try:
                bot = self.instancias_activas[hwnd_val]
                bot.modo = self.modo_var.get()
                bot.delay_personalizado = float(self.entry_delay.get())
                if apodo: bot.apodo = apodo
                bot.usar_ulti = self.ulti_var.get() if bot.modo == "FARMA_EXP" else False
                self.log_status(f"⚙️ [{bot.apodo}] actualizado en caliente.")
            except Exception as e:
                self.log_status(f"❌ Error en caliente: {str(e)}")

        # Guardar en JSON
        if apodo not in self.config:
            self.config[apodo] = {}

        self.config[apodo]["modo"] = self.modo_var.get()
        try:
            self.config[apodo]["delay"] = float(self.entry_delay.get())
        except ValueError:
            self.config[apodo]["delay"] = 5.0

        self.config[apodo]["ulti"] = self.ulti_var.get()

        sel_combo = self.combo_ventanas.get()
        titulo_limpio = sel_combo.split(" (HWND:")[0].strip() if sel_combo else ""
        self.config[apodo]["ventana_titulo"] = titulo_limpio

        self.guardar_config()
        self.log_status(f"💾 Perfil [{apodo}] guardado exitosamente.")
        self.actualizar_tabla_visual()

    def eliminar_perfil_seleccionado(self):
        if not self.tabla_instancias.selection():
            self.mostrar_alerta("Atención", "Selecciona un perfil de la tabla\npara eliminar.")
            return

        item = self.tabla_instancias.selection()[0]
        valores = self.tabla_instancias.item(item, "values")
        apodo = str(valores[0])

        hwnd_val = self.item_a_hwnd.get(item)
        if isinstance(hwnd_val, int) and hwnd_val in self.instancias_activas:
            self.mostrar_alerta("Atención", "No puedes eliminar un perfil en ejecución.\nDetenlo primero.")
            return

        if apodo in self.config:
            if self.pedir_confirmacion("Confirmar Eliminación", f"¿Seguro que quieres eliminar\nel perfil [{apodo}]?"):
                del self.config[apodo]
                self.guardar_config()
                self.log_status(f"🗑️ Perfil [{apodo}] eliminado.")
                self.actualizar_tabla_visual()
                self.limpiar_formulario()
        else:
            self.mostrar_alerta("Atención", "Ese no es un perfil guardado válido.")

    def evaluar_estado_botones_seleccion(self, event=None):
        sel = self.tabla_instancias.selection()
        if not sel:
            self.btn_iniciar.config(state="normal", bg=COLOR_ACCENT, fg="#000")
            self.btn_pausar.config(state="disabled", bg=COLOR_DISABLED_BG, fg=COLOR_DISABLED_FG)
            self.btn_reanudar.config(state="disabled", bg=COLOR_DISABLED_BG, fg=COLOR_DISABLED_FG)
            self.btn_detener.config(state="disabled", bg=COLOR_DISABLED_BG, fg=COLOR_DISABLED_FG)
            return

        item = sel[0]
        hwnd_val = self.item_a_hwnd.get(item)

        if isinstance(hwnd_val, int) and hwnd_val in self.instancias_activas:
            self.btn_iniciar.config(state="disabled", bg=COLOR_DISABLED_BG, fg=COLOR_DISABLED_FG)
            self.btn_pausar.config(state="normal", bg=COLOR_CARD, fg="#ffcc00")
            self.btn_reanudar.config(state="normal", bg=COLOR_CARD, fg=COLOR_ACCENT)
            self.btn_detener.config(state="normal", bg="#660000", fg="#fff")
        else:
            self.btn_iniciar.config(state="normal", bg=COLOR_ACCENT, fg="#000")
            self.btn_pausar.config(state="disabled", bg=COLOR_DISABLED_BG, fg=COLOR_DISABLED_FG)
            self.btn_reanudar.config(state="disabled", bg=COLOR_DISABLED_BG, fg=COLOR_DISABLED_FG)
            self.btn_detener.config(state="disabled", bg=COLOR_DISABLED_BG, fg=COLOR_DISABLED_FG)

    def actualizar_radio_colores(self):
        modo = self.modo_var.get()
        self.rb_mision.configure(fg=COLOR_TEXT_ON if modo=="MISION_Q" else COLOR_TEXT_OFF)
        self.rb_farma.configure(fg=COLOR_TEXT_ON if modo=="FARMA_EXP" else COLOR_TEXT_OFF)
        self.rb_summon.configure(fg=COLOR_TEXT_ON if modo=="SUMMON_BOSS" else COLOR_TEXT_OFF)
        self.check_ulti.configure(state="normal" if modo=="FARMA_EXP" else "disabled", fg=COLOR_SECONDARY if modo=="FARMA_EXP" else COLOR_TEXT_OFF)

    def actualizar_combo(self):
        ventanas = []
        def enum_windows_proc(hwnd, lParam):
            if win32gui.IsWindowVisible(hwnd) and "Mir4G" in win32gui.GetWindowText(hwnd): ventanas.append(f"{win32gui.GetWindowText(hwnd)} (HWND: {hwnd})")
            return True
        win32gui.EnumWindows(enum_windows_proc, None)
        self.combo_ventanas['values'] = ventanas
        if ventanas and not self.combo_ventanas.get(): self.combo_ventanas.current(0)

    def actualizar_tabla_visual(self):
        seleccion_actual = self.tabla_instancias.selection()
        item_seleccionado_valores = self.tabla_instancias.item(seleccion_actual[0], "values") if seleccion_actual else None
        apodo_seleccionado = item_seleccionado_valores[0] if item_seleccionado_valores else None

        self.item_a_hwnd = {} 
        for i in self.tabla_instancias.get_children(): self.tabla_instancias.delete(i)

        apodos_activos = []
        for hwnd, bot in self.instancias_activas.items():
            estado = "AUTO-PAUSA 👁️" if (bot.paused and bot.forced_pause) else ("PAUSADO ⏸️" if bot.paused else "EJECUTANDO ▶️")
            if not bot.is_alive() or not bot.running: estado = "TERMINADO 🛑"
            
            try:
                titulo_ventana = win32gui.GetWindowText(hwnd) or f"HWND {hwnd}"
            except:
                titulo_ventana = f"HWND {hwnd}"
                
            item = self.tabla_instancias.insert("", tk.END, values=(bot.apodo, bot.modo, titulo_ventana, f"{bot.delay_personalizado}s", estado))
            self.item_a_hwnd[item] = hwnd
            if bot.apodo == apodo_seleccionado: self.tabla_instancias.selection_set(item)
            apodos_activos.append(bot.apodo)

        for section in self.config.keys():
            if section in ['RUTAS', 'LAUNCHER', 'LAYOUT']: continue
            if section not in apodos_activos:
                modo = self.config[section].get("modo", "MISION_Q")
                delay = self.config[section].get("delay", 5.0)
                ventana_t = self.config[section].get("ventana_titulo", "Pendiente")
                item = self.tabla_instancias.insert("", tk.END, values=(section, modo, ventana_t, f"{delay}s", "GUARDADO 💾"))
                self.item_a_hwnd[item] = None
                if section == apodo_seleccionado: self.tabla_instancias.selection_set(item)

        self.evaluar_estado_botones_seleccion()

    def obtener_hwnd_seleccionado(self):
        # Priorizar el combobox si el usuario acaba de seleccionarlo
        sel_combo = self.combo_ventanas.get()
        if sel_combo:
            try: return int(sel_combo.split("(HWND: ")[1].replace(")", ""))
            except: pass
            
        # Si no, usar la tabla
        if self.tabla_instancias.selection():
            item = self.tabla_instancias.selection()[0]
            hwnd_val = self.item_a_hwnd.get(item)
            if isinstance(hwnd_val, int):
                return hwnd_val
                
        self.mostrar_alerta("Atención", "Selecciona una ventana válida\nen el formulario o despliega el perfil primero."); 
        return None

    # --- CONTROL DE EJECUCIÓN ---
    def iniciar_instancia(self):
        apodo = self.entry_apodo.get().strip()
        if not apodo:
            self.mostrar_alerta("Atención", "Debes ingresar o seleccionar un APODO.")
            return

        # Asegurarnos de guardar el perfil antes de iniciar
        self.guardar_o_actualizar_perfil()

        sel = self.combo_ventanas.get()
        if not sel: 
            self.mostrar_alerta("Atención", "No hay ninguna ventana de MIR4 seleccionada en el formulario.")
            return
            
        try:
            hwnd = int(sel.split("(HWND: ")[1].replace(")", ""))
            if hwnd in self.instancias_activas and self.instancias_activas[hwnd].is_alive():
                self.log_status(f"⚠️ HWND {hwnd} ya está en ejecución."); return

            modo = self.modo_var.get()
            delay = float(self.entry_delay.get())
            usar_ulti = self.ulti_var.get() if modo == "FARMA_EXP" else False

            bot = BotInstance(hwnd, modo, delay, usar_ulti, apodo)
            self.instancias_activas[hwnd] = bot
            bot.start()
            self.log_status(f"✅ [{bot.apodo}] INICIADO y ejecutándose.")
            self.actualizar_tabla_visual()
        except Exception as e: self.log_status(f"❌ Error: {str(e)}")

    def pausar_instancia(self):
        hwnd = self.obtener_hwnd_seleccionado()
        if hwnd and hwnd in self.instancias_activas:
            bot = self.instancias_activas[hwnd]; bot.manual_pause = True; bot.forced_pause = False; bot.pause()
            self.log_status(f"⏸️ [{bot.apodo}] PAUSADO."); self.actualizar_tabla_visual()

    def reanudar_instancia(self):
        hwnd = self.obtener_hwnd_seleccionado()
        if hwnd and hwnd in self.instancias_activas:
            bot = self.instancias_activas[hwnd]; bot.manual_pause = False; bot.forced_pause = False; bot.resume()
            self.log_status(f"▶️ [{bot.apodo}] REANUDADO."); self.actualizar_tabla_visual()

    def detener_instancia(self):
        hwnd = self.obtener_hwnd_seleccionado()
        if hwnd and hwnd in self.instancias_activas:
            bot = self.instancias_activas[hwnd]; bot.stop(); del self.instancias_activas[hwnd]
            self.log_status(f"🛑 [{bot.apodo}] DETENIDO."); self.actualizar_tabla_visual()

    # --- TAB LAYOUT ---
    def setup_tab_layout(self):
        frame_grid = ttk.LabelFrame(self.tab_layout, text=" RECTIL WINDOWS LAYOUT (GRID) ", style="Card.TLabelframe")
        frame_grid.pack(fill="both", expand=True, padx=15, pady=15)
        
        saved_offset = self.config.get('LAYOUT', {}).get('offset', 0)
        
        self.label_offset = ttk.Label(frame_grid, text=f"Ajuste de Borde (Offset): {saved_offset}", background=COLOR_BG, foreground=COLOR_ACCENT, font=('Segoe UI', 10, 'bold'))
        self.label_offset.pack(pady=15)
        
        self.offset_var = tk.IntVar(value=saved_offset)
        
        def on_offset_change(v):
            val = int(float(v))
            self.label_offset.config(text=f"Ajuste de Borde (Offset): {val}")
            if 'LAYOUT' not in self.config: self.config['LAYOUT'] = {}
            self.config['LAYOUT']['offset'] = val
            self.guardar_config()
            
        self.slider = ttk.Scale(frame_grid, from_=0, to=20, orient='horizontal', variable=self.offset_var, command=on_offset_change)
        self.slider.pack(fill="x", padx=30, pady=10)
        
        tk.Button(frame_grid, text="⚡ ORDENAR Y ENFOCAR VENTANAS", bg=COLOR_ACCENT, fg="#000", font=('Segoe UI', 12, 'bold'), relief="flat", activebackground=COLOR_SECONDARY, command=self.ordenar_grid_ventanas).pack(pady=(40, 10), fill="x", padx=40)
        tk.Button(frame_grid, text="⬇️ MINIMIZAR TODAS LAS VENTANAS", bg=COLOR_CARD, fg="#fff", font=('Segoe UI', 12, 'bold'), relief="flat", activebackground=COLOR_DISABLED_FG, command=self.minimizar_grid_ventanas).pack(pady=(0, 40), fill="x", padx=40)

    def ordenar_grid_ventanas(self):
        v_list = []
        def cb(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd) and "MIR4G" in win32gui.GetWindowText(hwnd).upper(): v_list.append(hwnd)
            return True
        win32gui.EnumWindows(cb, None); v_list.sort()
        if not v_list: 
            self.log_status("⚠️ No hay ventanas Mir4G."); return
        
        rect = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0, 0)))['Work']
        w_x, w_y, w_w, w_h = rect[0], rect[1], rect[2]-rect[0], rect[3]-rect[1]
        num = len(v_list); cols = int(num**0.5)
        if cols * cols < num: cols += 1
        rows = (num + cols - 1) // cols; win_w = w_w // cols; win_h = w_h // rows; offset = self.offset_var.get()
        
        if 'LAYOUT' not in self.config: self.config['LAYOUT'] = {}
        self.config['LAYOUT']['offset'] = offset
        self.guardar_config()
        
        try:
            for i, hwnd in enumerate(v_list):
                r, c = i // cols, i % cols
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.MoveWindow(hwnd, w_x + (c * win_w) - offset, w_y + (r * win_h), win_w + (offset * 2), win_h + offset, True)
                win32gui.SetForegroundWindow(hwnd)
                time.sleep(0.05)
                
            self.root.after(100, lambda: self.root.focus_force())
            self.log_status(f"⚡ Grid aplicado a {num} ventanas (Enfocadas).")
        except Exception as e: self.log_status(f"❌ Error Layout: {str(e)}")

    def minimizar_grid_ventanas(self):
        v_list = []
        def cb(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd) and "MIR4G" in win32gui.GetWindowText(hwnd).upper(): v_list.append(hwnd)
            return True
        win32gui.EnumWindows(cb, None); v_list.sort()
        if not v_list: 
            self.log_status("⚠️ No hay ventanas Mir4G para minimizar."); return
        try:
            for hwnd in v_list:
                win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            self.log_status(f"⬇️ {len(v_list)} ventanas minimizadas.")
        except Exception as e: self.log_status(f"❌ Error al minimizar: {str(e)}")

    # --- TAB DESPLIEGUE ---
    def setup_tab_despliegue(self):
        scroll_wrapper = ScrollableFrame(self.tab_despliegue, COLOR_BG)
        scroll_wrapper.pack(fill="both", expand=True)
        container = scroll_wrapper.scrollable_frame

        frame_steam = ttk.LabelFrame(container, text=" INFRAESTRUCTURA STEAM ", style="Card.TLabelframe")
        frame_steam.pack(fill="x", padx=15, pady=(10, 5))
        tk.Label(frame_steam, text="Ruta Steam Launcher:", bg=COLOR_BG, fg=COLOR_ACCENT, font=('Segoe UI', 9, 'bold')).pack(anchor="w", padx=15, pady=(5,0))
        self.ent_steam = tk.Entry(frame_steam, bg=COLOR_INPUT_BG, fg="#fff", borderwidth=0, font=('Segoe UI', 9))
        steam_path = self.config.get('RUTAS', {}).get('steam', r"C:\Program Files (x86)\Steam\steam.exe")
        self.ent_steam.insert(0, steam_path)
        self.ent_steam.pack(fill="x", padx=15, pady=2)
        btn_steam_frame = tk.Frame(frame_steam, bg=COLOR_BG)
        btn_steam_frame.pack(fill="x", padx=15, pady=(5, 10))
        tk.Button(btn_steam_frame, text="💾 GUARDAR RUTA STEAM", bg=COLOR_CARD, fg=COLOR_SECONDARY, font=('Segoe UI', 9, 'bold'), relief="groove", command=self.guardar_rutas_interfaz).pack(side="left", fill="x", expand=True, padx=5)
        tk.Button(btn_steam_frame, text="🎮 INICIAR MIR4 DESDE STEAM", bg="#0054a6", fg="#fff", font=('Segoe UI', 10, 'bold'), relief="flat", command=self.lanzar_steam).pack(side="left", fill="x", expand=True, padx=5)

        frame_ruta = ttk.LabelFrame(container, text=" RUTA DEL LAUNCHER MIR4 (GAME 1 & 2) ", style="Card.TLabelframe")
        frame_ruta.pack(fill="x", padx=15, pady=5)
        self.ent_launcher = tk.Entry(frame_ruta, bg=COLOR_INPUT_BG, fg="#fff", borderwidth=0, font=('Segoe UI', 9))
        self.ent_launcher.pack(fill="x", padx=15, pady=(10,5))

        frame_coord = ttk.LabelFrame(container, text=" COORDENADAS DE BOTONES (X, Y) ", style="Card.TLabelframe")
        frame_coord.pack(fill="x", padx=15, pady=5)

        f1 = tk.Frame(frame_coord, bg=COLOR_BG); f1.pack(fill="x", padx=15, pady=5)
        tk.Label(f1, text="GAME 1 -> X:", bg=COLOR_BG, fg=COLOR_ACCENT, font=('Consolas', 10, 'bold'), width=12, anchor="w").pack(side="left")
        self.ent_g1_x = tk.Entry(f1, width=8, bg=COLOR_INPUT_BG, fg=COLOR_ACCENT, insertbackground=COLOR_ACCENT, borderwidth=0, font=('Consolas', 11, 'bold')); self.ent_g1_x.pack(side="left", padx=5)
        tk.Label(f1, text="Y:", bg=COLOR_BG, fg=COLOR_ACCENT, font=('Consolas', 10, 'bold')).pack(side="left", padx=(10,0))
        self.ent_g1_y = tk.Entry(f1, width=8, bg=COLOR_INPUT_BG, fg=COLOR_ACCENT, insertbackground=COLOR_ACCENT, borderwidth=0, font=('Consolas', 11, 'bold')); self.ent_g1_y.pack(side="left", padx=5)
        tk.Button(f1, text="🎯 Capturar", bg=COLOR_CARD, fg="#fff", font=('Segoe UI', 8, 'bold'), relief="flat", command=lambda: self.iniciar_captura(self.ent_g1_x, self.ent_g1_y)).pack(side="right", padx=5)

        f2 = tk.Frame(frame_coord, bg=COLOR_BG); f2.pack(fill="x", padx=15, pady=5)
        tk.Label(f2, text="GAME 2 -> X:", bg=COLOR_BG, fg=COLOR_SECONDARY, font=('Consolas', 10, 'bold'), width=12, anchor="w").pack(side="left")
        self.ent_g2_x = tk.Entry(f2, width=8, bg=COLOR_INPUT_BG, fg=COLOR_SECONDARY, insertbackground=COLOR_ACCENT, borderwidth=0, font=('Consolas', 11, 'bold')); self.ent_g2_x.pack(side="left", padx=5)
        tk.Label(f2, text="Y:", bg=COLOR_BG, fg=COLOR_SECONDARY, font=('Consolas', 10, 'bold')).pack(side="left", padx=(10,0))
        self.ent_g2_y = tk.Entry(f2, width=8, bg=COLOR_INPUT_BG, fg=COLOR_SECONDARY, insertbackground=COLOR_ACCENT, borderwidth=0, font=('Consolas', 11, 'bold')); self.ent_g2_y.pack(side="left", padx=5)
        tk.Button(f2, text="🎯 Capturar", bg=COLOR_CARD, fg="#fff", font=('Segoe UI', 8, 'bold'), relief="flat", command=lambda: self.iniciar_captura(self.ent_g2_x, self.ent_g2_y)).pack(side="right", padx=5)

        frame_extra = ttk.LabelFrame(container, text=" AJUSTES FINOS ", style="Card.TLabelframe")
        frame_extra.pack(fill="x", padx=15, pady=5)

        f3 = tk.Frame(frame_extra, bg=COLOR_BG); f3.pack(fill="x", padx=15, pady=5)
        tk.Label(f3, text="TITULO O CLASE:", bg=COLOR_BG, fg=COLOR_ACCENT, font=('Segoe UI', 9, 'bold'), width=16, anchor="w").pack(side="left")
        self.ent_titulo_launcher = tk.Entry(f3, bg=COLOR_INPUT_BG, fg="#fff", insertbackground=COLOR_ACCENT, borderwidth=0, font=('Segoe UI', 9))
        self.ent_titulo_launcher.pack(side="left", fill="x", expand=True, padx=5)
        tk.Label(frame_extra, text="💡 Si no lo encuentra, usa solo: MIR4", bg=COLOR_BG, fg=COLOR_TEXT_OFF, font=('Segoe UI', 8, 'italic')).pack(anchor="w", padx=20)

        f5 = tk.Frame(frame_extra, bg=COLOR_BG); f5.pack(fill="x", padx=15, pady=5)
        tk.Label(f5, text="ESPERA TRAS ENCONTRAR LAUNCHER (Seg):", bg=COLOR_BG, fg=COLOR_ACCENT, font=('Segoe UI', 9, 'bold'), width=30, anchor="w").pack(side="left")
        self.ent_delay_pre_click = tk.Entry(f5, width=6, bg=COLOR_INPUT_BG, fg=COLOR_ACCENT, insertbackground=COLOR_ACCENT, borderwidth=0, font=('Consolas', 11, 'bold'))
        self.ent_delay_pre_click.pack(side="left", padx=5)

        f4 = tk.Frame(frame_extra, bg=COLOR_BG); f4.pack(fill="x", padx=15, pady=(0,10))
        tk.Label(f4, text="ESPERA ENTRE G1 Y G2 (Seg):", bg=COLOR_BG, fg=COLOR_ACCENT, font=('Segoe UI', 9, 'bold'), width=30, anchor="w").pack(side="left")
        self.ent_delay_launch = tk.Entry(f4, width=6, bg=COLOR_INPUT_BG, fg=COLOR_ACCENT, insertbackground=COLOR_ACCENT, borderwidth=0, font=('Consolas', 11, 'bold'))
        self.ent_delay_launch.pack(side="left", padx=5)

        frame_btn = tk.Frame(container, bg=COLOR_BG); frame_btn.pack(fill="x", padx=15, pady=15)
        tk.Button(frame_btn, text="💾 GUARDAR CONFIG LAUNCHER", bg=COLOR_CARD, fg=COLOR_SECONDARY, font=('Segoe UI', 10, 'bold'), relief="groove", command=self.guardar_config_launcher).pack(side="left", fill="x", expand=True, padx=5)
        tk.Button(frame_btn, text="🛡️ INICIAR (UIAutomation Seguro)", bg=COLOR_ACCENT, fg="#000", font=('Segoe UI', 11, 'bold'), relief="flat", activebackground=COLOR_SECONDARY, command=self.lanzar_game1_game2).pack(side="left", fill="x", expand=True, padx=5)

        self.cargar_config_launcher()

    def boton_de_panico(self):
        try:
            self.log_status("☠️ BOTÓN DE PÁNICO ACTIVADO. Eliminando procesos...")
            ejecutables = ["Mir4G.exe", "Mir4Launcher.exe", "Mir4GClient.exe", "Mir4Client.exe", "Mir4.exe", "Mir4S.exe", "Mir4-Win64-Shipping.exe", "Mir4G-Win64-Shipping.exe"]
            for exe in ejecutables:
                subprocess.run(f"taskkill /F /IM {exe} /T", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            for hwnd, bot in list(self.instancias_activas.items()):
                bot.stop()
            self.instancias_activas.clear()
            self.actualizar_tabla_visual()
            self.log_status("✅ Todos los procesos Mir4 (incluido Steam) han sido aniquilados.")

            popup = tk.Toplevel(self.root)
            popup.title("SISTEMA DE EMERGENCIA")
            popup.geometry("380x180")
            popup.configure(bg=COLOR_BG)
            popup.resizable(False, False)
            popup.transient(self.root)
            popup.grab_set()

            x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 190
            y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 90
            popup.geometry(f"+{x}+{y}")

            tk.Label(popup, text="☠️ SECUENCIA DE PÁNICO ☠️", bg=COLOR_BG, fg=COLOR_CAPTURA, font=('Segoe UI', 14, 'bold')).pack(pady=(15, 5))
            tk.Label(popup, text="¡Aniquilación completada con éxito!\nTodos los procesos de MIR4 y sus Launchers\nhan sido cerrados de manera forzada.", bg=COLOR_BG, fg="#ffffff", font=('Segoe UI', 10)).pack(pady=10)
            btn_ok = tk.Button(popup, text="ENTENDIDO", bg=COLOR_CARD, fg=COLOR_ACCENT, activebackground=COLOR_ACCENT, activeforeground="#000", font=('Segoe UI', 9, 'bold'), relief="groove", width=15, command=popup.destroy)
            btn_ok.pack(pady=(5, 10))

        except Exception as e:
            self.log_status(f"❌ Error al intentar cerrar los procesos: {str(e)}")

    def iniciar_captura(self, entry_x, entry_y):
        if self.capturando_activo: return
        self.capturando_activo = True
        self.log_status("🎯 MODO CAPTURA ACTIVADO. Haz clic en el botón del Launcher...")
        original_bg_x = entry_x.cget('bg'); original_bg_y = entry_y.cget('bg')
        entry_x.configure(bg=COLOR_CAPTURA); entry_y.configure(bg=COLOR_CAPTURA)
        threading.Thread(target=self._hilo_captura, args=(entry_x, entry_y, original_bg_x, original_bg_y), daemon=True).start()

    def _hilo_captura(self, entry_x, entry_y, original_bg_x, original_bg_y):
        try:
            hwnd_launcher = esperar_ventana(self.ent_titulo_launcher.get(), timeout=2)
            last_state = win32api.GetKeyState(0x01)
            while True:
                screen_x, screen_y = win32api.GetCursorPos()
                if hwnd_launcher:
                    rel_x, rel_y = win32gui.ScreenToClient(hwnd_launcher, (screen_x, screen_y))
                    self.root.after(0, self._actualizar_texto_captura, entry_x, entry_y, rel_x, rel_y)
                else:
                    self.root.after(0, self._actualizar_texto_captura, entry_x, entry_y, screen_x, screen_y)

                current_state = win32api.GetKeyState(0x01)
                if last_state >= 0 and current_state < 0:
                    break
                last_state = current_state
                time.sleep(0.02)

            if hwnd_launcher:
                rel_x, rel_y = win32gui.ScreenToClient(hwnd_launcher, (screen_x, screen_y))
                if rel_x >= 0 and rel_y >= 0:
                    self.root.after(0, self._terminar_captura, entry_x, entry_y, str(rel_x), str(rel_y), original_bg_x, original_bg_y, True)
                    return
                else:
                    self.root.after(0, self._terminar_captura, entry_x, entry_y, "0", "0", original_bg_x, original_bg_y, False, "Clic fuera de la ventana.")
                    return
            else:
                self.root.after(0, self._terminar_captura, entry_x, entry_y, str(screen_x), str(screen_y), original_bg_x, original_bg_y, False, "Launcher no encontrado.")
        except Exception as e:
            self.root.after(0, self._terminar_captura, entry_x, entry_y, "0", "0", original_bg_x, original_bg_y, False, f"Error: {str(e)}")

    def _actualizar_texto_captura(self, entry_x, entry_y, x, y):
        entry_x.delete(0, tk.END); entry_x.insert(0, str(x))
        entry_y.delete(0, tk.END); entry_y.insert(0, str(y))

    def _terminar_captura(self, entry_x, entry_y, x, y, bg_x, bg_y, exito, msg_extra=""):
        self.capturando_activo = False
        entry_x.configure(bg=bg_x); entry_y.configure(bg=bg_y)
        if exito:
            entry_x.delete(0, tk.END); entry_x.insert(0, x)
            entry_y.delete(0, tk.END); entry_y.insert(0, y)
            self.log_status(f"✅ Coordenadas capturadas: X={x}, Y={y}")
        else:
            self.log_status(f"❌ Captura fallida. {msg_extra}")

    def guardar_rutas_interfaz(self):
        if 'RUTAS' not in self.config: self.config['RUTAS'] = {}
        self.config['RUTAS']['steam'] = self.ent_steam.get()
        self.guardar_config(); self.log_status("💾 Ruta de Steam actualizada.")

    def lanzar_steam(self):
        ruta = self.ent_steam.get()
        if os.path.exists(ruta):
            try: subprocess.Popen([ruta, "-applaunch", "1623660"]); self.log_status("🎮 Solicitud enviada a Steam.")
            except Exception as e: self.log_status(f"❌ Error en Steam: {str(e)}")
        else: self.log_status("❌ Steam no localizado.")

    def guardar_config_launcher(self):
        if 'LAUNCHER' not in self.config: self.config['LAUNCHER'] = {}
        try:
            self.config['LAUNCHER']['ruta'] = self.ent_launcher.get()
            self.config['LAUNCHER']['g1_x'] = int(self.ent_g1_x.get())
            self.config['LAUNCHER']['g1_y'] = int(self.ent_g1_y.get())
            self.config['LAUNCHER']['g2_x'] = int(self.ent_g2_x.get())
            self.config['LAUNCHER']['g2_y'] = int(self.ent_g2_y.get())
            self.config['LAUNCHER']['titulo'] = self.ent_titulo_launcher.get()
            self.config['LAUNCHER']['delay_pre_click'] = float(self.ent_delay_pre_click.get())
            self.config['LAUNCHER']['delay'] = float(self.ent_delay_launch.get())
        except ValueError:
            self.log_status("❌ Error: Verifica que las coordenadas y tiempos sean números.")
            return

        self.guardar_config()
        self.log_status("💾 Configuración de Launcher guardada.")

    def cargar_config_launcher(self):
        defaults = {
            'ruta': r"C:\Wemade\Mir4Global\Mir4Launcher\Mir4Launcher.exe",
            'g1_x': 815, 'g1_y': 539,
            'g2_x': 968, 'g2_y': 541,
            'titulo': "CLASS:HwndWrapper[Mir4Launcher.exe",
            'delay_pre_click': 15, 'delay': 15
        }
        cfg = self.config.get('LAUNCHER', defaults)

        self.ent_launcher.insert(0, str(cfg.get('ruta', defaults['ruta'])))
        self.ent_g1_x.insert(0, str(cfg.get('g1_x', defaults['g1_x'])))
        self.ent_g1_y.insert(0, str(cfg.get('g1_y', defaults['g1_y'])))
        self.ent_g2_x.insert(0, str(cfg.get('g2_x', defaults['g2_x'])))
        self.ent_g2_y.insert(0, str(cfg.get('g2_y', defaults['g2_y'])))
        self.ent_titulo_launcher.insert(0, str(cfg.get('titulo', defaults['titulo'])))
        self.ent_delay_pre_click.insert(0, str(cfg.get('delay_pre_click', defaults['delay_pre_click'])))
        self.ent_delay_launch.insert(0, str(cfg.get('delay', defaults['delay'])))

    def lanzar_game1_game2(self):
        if not UIA_AVAILABLE:
            self.log_status("❌ FALTA LIBRERIA ANTI-BAN. CMD > pip install pywinauto")
            self.mostrar_alerta("Error Crítico", "Falta la librería 'pywinauto'.\nAbre CMD y ejecuta: pip install pywinauto\n\nLuego reinicia el bot.", es_error=True)
            return
        try:
            ruta = self.ent_launcher.get()
            g1_x = int(self.ent_g1_x.get()); g1_y = int(self.ent_g1_y.get())
            g2_x = int(self.ent_g2_x.get()); g2_y = int(self.ent_g2_y.get())
            titulo_launcher = self.ent_titulo_launcher.get()
            delay_pre_click = int(float(self.ent_delay_pre_click.get()))
            delay = int(float(self.ent_delay_launch.get()))
            if not os.path.exists(ruta): self.log_status("❌ Ruta incorrecta."); return
            self.log_status("🛡️ Iniciando Secuencia Segura (UIAutomation)...")
            threading.Thread(target=self._hilo_lanzamiento_uia, args=(ruta, g1_x, g1_y, g2_x, g2_y, titulo_launcher, delay_pre_click, delay), daemon=True).start()
        except ValueError: self.log_status("❌ Error: Los tiempos y coordenadas deben ser números.")
        except Exception as e: self.log_status(f"❌ Error al leer configuración: {str(e)}")

    def uia_click(self, hwnd, target_x, target_y):
        try:
            abs_x, abs_y = win32gui.ClientToScreen(hwnd, (target_x, target_y))
            desktop = Desktop(backend="uia"); launcher = desktop.window(handle=hwnd)
            self.log_status(f"🔍 Escaneando elementos UIA en ({abs_x}, {abs_y})...")

            buttons = launcher.descendants(control_type="Button")
            for btn in buttons:
                rect = btn.rectangle()
                if rect.left <= abs_x <= rect.right and rect.top <= abs_y <= rect.bottom:
                    if btn.is_enabled():
                        self.log_status("✅ Botón oficial detectado. Invocando...")
                        btn.invoke()
                        return True

            self.log_status("⚠️ Buscando controles genéricos...")
            controls = launcher.descendants()
            for ctrl in controls:
                try:
                    rect = ctrl.rectangle()
                    if rect.left <= abs_x <= rect.right and rect.top <= abs_y <= rect.bottom:
                        if ctrl.is_enabled():
                            try:
                                self.log_status(f"✅ Control encontrado ({ctrl.element_info.class_name}). Invocando...")
                                ctrl.invoke()
                                return True
                            except Exception:
                                pass
                except Exception:
                    continue

            self.log_status("❌ No se pudo encontrar elemento clickeable en esas coordenadas.")
            return False
        except Exception as e:
            self.log_status(f"❌ Error interno UIA: {str(e)}")
            return False

    def _hilo_lanzamiento_uia(self, ruta, g1_x, g1_y, g2_x, g2_y, titulo_launcher, delay_pre_click, delay):
        try:
            self.log_status("🚀 Abriendo ejecutable del Launcher...")
            subprocess.Popen(ruta)

            self.log_status(f"⏳ Buscando ventana ('{titulo_launcher}')...")
            hwnd_launcher = esperar_ventana(titulo_launcher, timeout=30)
            if not hwnd_launcher:
                self.log_status("❌ No se encontró la ventana del Launcher.")
                return

            self.log_status(f"✅ ¡Ventana encontrada (HWND: {hwnd_launcher})!")
            self.log_status(f"⏳ Esperando {delay_pre_click} seg para renderizar UI...")
            time.sleep(delay_pre_click)

            self.log_status(f"🛡️ Presionando Game 1 vía UIAutomation...")
            if not self.uia_click(hwnd_launcher, g1_x, g1_y): return

            self.log_status("⏳ Esperando que cargue Game 1...")
            if not esperar_ventana("Mir4G", timeout=90):
                self.log_status("⚠️ Game 1 tardó demasiado, pero continuando con Game 2...")

            self.log_status(f"💤 Esperando {delay} segundos...")
            time.sleep(delay)

            hwnd_launcher = esperar_ventana(titulo_launcher, timeout=15)
            if not hwnd_launcher:
                self.log_status("❌ No se pudo encontrar el Launcher para abrir el Game 2.")
                return

            self.log_status(f"🛡️ Presionando Game 2 vía UIAutomation...")
            if not self.uia_click(hwnd_launcher, g2_x, g2_y): return

            self.log_status("⏳ Esperando que cargue Game 2...")
            if esperar_ventana("Mir4G", timeout=90):
                self.log_status("🎉 ¡Despliegue completado 100% Seguro!")
            else:
                self.log_status("⚠️ Proceso finalizado, pero Game 2 pudo no haber cargado a tiempo.")

        except Exception as e:
            self.log_status(f"❌ Error crítico en el Launcher: {str(e)}")

    # --- FUNCIÓN DE GUARDADO JSON ---
    def guardar_config(self):
        with open(self.config_file, 'w', encoding='utf-8') as configfile:
            json.dump(self.config, configfile, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()