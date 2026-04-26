import win32gui
import win32api
import win32con
import tkinter as tk
from tkinter import ttk
import sys

class AjustadorGridMIR4:
    def __init__(self, root):
        self.root = root
        self.root.title("Ajustador de Ventanas - SabandijaBot")
        self.root.geometry("400x220")
        self.root.attributes("-topmost", True)  # Mantener siempre al frente
        self.root.resizable(False, False)

        # Estilo visual
        style = ttk.Style()
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"))

        # Etiquetas de información
        self.status_label = ttk.Label(root, text="Buscando ventanas 'Mir4G'...", foreground="blue")
        self.status_label.pack(pady=10)

        self.label_offset = ttk.Label(root, text="Ajuste de Borde (Offset): 0")
        self.label_offset.pack()

        # Slider para ajuste fino
        self.offset_var = tk.IntVar(value=0)
        self.slider = ttk.Scale(
            root, from_=0, to=20, 
            orient='horizontal', 
            variable=self.offset_var,
            command=self.actualizar_label
        )
        self.slider.pack(fill='x', padx=30, pady=10)

        # Botón principal
        self.btn = ttk.Button(root, text="APLICAR GRID", command=self.ejecutar_ajuste)
        self.btn.pack(pady=10)

        self.note_label = ttk.Label(root, text="Nota: Ejecuta como Administrador", font=("Segoe UI", 8), foreground="gray")
        self.note_label.pack()

    def actualizar_label(self, event=None):
        self.label_offset.config(text=f"Ajuste de Borde (Offset): {self.offset_var.get()}")

    def ejecutar_ajuste(self):
        v_list = []
        
        # 1. Buscar ventanas del juego
        def enum_handler(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                text = win32gui.GetWindowText(hwnd).upper()
                # Filtramos por MIR4G pero ignoramos este script (el "DEBUG" o "AJUSTADOR")
                if "MIR4G" in text and "AJUSTADOR" not in text:
                    v_list.append(hwnd)
        
        win32gui.EnumWindows(enum_handler, None)
        v_list.sort() # Ordenar para que el grid sea consistente

        if not v_list:
            self.status_label.config(text="Error: No se detectaron ventanas 'Mir4G'", foreground="red")
            return

        self.status_label.config(text=f"Ventanas detectadas: {len(v_list)}", foreground="green")

        # 2. Obtener dimensiones del monitor (Área de trabajo)
        monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0, 0)))
        rect = monitor_info['Work']
        work_x, work_y = rect[0], rect[1]
        work_w = rect[2] - rect[0]
        work_h = rect[3] - rect[1]

        # 3. Lógica de columnas y filas
        num = len(v_list)
        cols = int(num**0.5)
        if cols * cols < num: cols += 1
        rows = (num + cols - 1) // cols

        win_w = work_w // cols
        win_h = work_h // rows
        
        offset = self.offset_var.get()

        # 4. Mover ventanas
        try:
            for i, hwnd in enumerate(v_list):
                r, c = i // cols, i % cols
                
                # Cálculo con compensación de bordes invisibles
                x = work_x + (c * win_w) - offset
                y = work_y + (r * win_h)
                w = win_w + (offset * 2)
                h = win_h + offset

                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.MoveWindow(hwnd, x, y, w, h, True)
                
        except Exception as e:
            self.status_label.config(text=f"Error de permisos: Ejecuta como ADMIN", foreground="red")
            print(f"DEBUG: {e}")

if __name__ == "__main__":
    # Verificar si el script tiene privilegios de admin (opcional para aviso)
    root = tk.Tk()
    app = AjustadorGridMIR4(root)
    root.mainloop()