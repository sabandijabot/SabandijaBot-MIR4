import sys
import ctypes
import os
import tkinter as tk
from tkinter import ttk
import win32gui
import win32con
import win32api
import win32process
import time
import random
import threading
import subprocess
import json
import shutil
import tempfile
from datetime import datetime

# --- CONFIGURACIÓN GLOBAL ---
APP_VERSION = "v14.5" # Versión con interfaz en español e inglés
RESERVED_CONFIG_SECTIONS = {"RUTAS", "LAUNCHER", "LAYOUT", "IDIOMA"}

TRANSLATIONS = {
    "es": {
        "app.title": "SABANDIJA B0T - EDICIÓN {version}",
        "app.header": "🐍 CONTROL DE SABANDIJA",
        "tab.instances": "  INSTANCIAS SABANDIJA  ",
        "tab.layout": "  DISEÑO RECTIL  ",
        "tab.deploy": "  DESPLIEGUE  ",
        "tab.log": "  REGISTRO DE CAZA  ",
        "language.selector": "Idioma / Language:",
        "language.spanish": "Español",
        "language.english": "English",
        "language.restart.title": "Idioma guardado",
        "language.restart.message": "Reiniciando el bot para aplicar el idioma seleccionado...",
        "frame.instances": " 📋 INSTANCIAS Y PERFILES GUARDADOS ",
        "frame.profile": " 🛠️ CONFIGURACIÓN DEL PERFIL ",
        "frame.execution": " 🎮 CONTROL DE EJECUCIÓN ",
        "frame.log": " REGISTRO DE CAZA ",
        "frame.layout": " DISEÑO DE VENTANAS RECTIL (CUADRÍCULA) ",
        "frame.fixed_size": " TAMAÑO FIJO ",
        "frame.custom_distribution": " DISTRIBUCIÓN PERSONALIZADA ",
        "frame.steam": " INFRAESTRUCTURA STEAM ",
        "frame.launcher_path": " RUTA DEL LAUNCHER MIR4 (GAME 1 Y 2) ",
        "frame.coordinates": " COORDENADAS DE BOTONES (X, Y) ",
        "frame.fine_tuning": " AJUSTES FINOS ",
        "column.nickname": "Apodo",
        "column.mode": "Modo",
        "column.window": "Ventana asignada",
        "column.delay": "Espera",
        "column.status": "Estado",
        "label.nickname": "APODO:",
        "label.window": "VENTANA:",
        "label.delay": "ESPERA (SEG):",
        "label.launcher_path": "Ruta del launcher:",
        "label.title_class": "TÍTULO O CLASE:",
        "label.launcher_wait": "ESPERA TRAS ENCONTRAR EL LAUNCHER (seg):",
        "label.game_wait": "ESPERA ENTRE GAME 1 Y GAME 2 (seg):",
        "label.offset": "Ajuste de borde (offset): {value}",
        "label.width": "ANCHO:",
        "label.height": "ALTO:",
        "label.columns": "COLUMNAS:",
        "label.rows": "FILAS:",
        "label.launcher_hint": "💡 Si no lo encuentra, usa solo: MIR4",
        "mode.mission": "MISIÓN Q",
        "mode.farm": "FARMA EXP",
        "mode.boss": "SUMMON BOSS",
        "tooltip.mode.mission": "Misión Q: ejecuta una secuencia automática de Q, E y T, seguida de clics en el centro de la ventana.",
        "tooltip.mode.farm": "Farma EXP: activa la secuencia de farmeo con TAB, flecha abajo y F. Puede usar la ulti con R.",
        "tooltip.mode.boss": "Summon Boss: pulsa E periódicamente para ejecutar la acción de invocación del boss.",
        "check.ultimate": "LANZAR ULTI [R]",
        "button.new": "🆕 NUEVO",
        "button.save_profile": "💾 GUARDAR / ACTUALIZAR",
        "button.delete": "🗑️ ELIMINAR",
        "button.start": "🚀 INICIAR BOT",
        "button.pause": "⏸️ PAUSAR",
        "button.resume": "▶️ REANUDAR",
        "button.stop": "🛑 DETENER",
        "button.panic": "☠️ BOTÓN DE PÁNICO (CERRAR TODO MIR4) ☠️",
        "button.apply_fixed": "APLICAR TAMAÑO FIJO",
        "button.apply_grid": "APLICAR FILAS Y COLUMNAS",
        "button.arrange": "⚡ ORDENAR Y ENFOCAR VENTANAS",
        "button.minimize": "⬇️ MINIMIZAR TODAS LAS VENTANAS",
        "button.save_steam": "💾 GUARDAR RUTA STEAM",
        "button.start_steam": "🎮 INICIAR MIR4 DESDE STEAM",
        "button.capture": "🎯 CAPTURAR",
        "button.save_launcher": "💾 GUARDAR CONFIGURACIÓN DEL LAUNCHER",
        "button.start_uia": "🛡️ INICIAR (UIAutomation SEGURO)",
        "button.ok": "ENTENDIDO",
        "button.yes_delete": "SÍ, ELIMINAR",
        "button.cancel": "CANCELAR",
        "status.auto_paused": "AUTO-PAUSADO 👁️",
        "status.paused": "PAUSADO ⏸️",
        "status.running": "EJECUTANDO ▶️",
        "status.finished": "TERMINADO 🛑",
        "status.saved": "GUARDADO 💾",
        "status.uia_ready": "✅ UIAutomation seguro cargado",
        "status.uia_missing": "❌ FALTA: Ejecuta 'pip install pywinauto'",
        "log.crud_ready": "🛡️ Sistema CRUD activado. Crea, edita y ejecuta tus perfiles fácilmente.",
        "log.initialized": "SabandijaBot {version} inicializado. [{uia}]",
        "log.config_found": "📁 Archivo de configuración JSON ubicado en:\n   {path}",
        "log.config_missing": "⚠️ No se encontró el archivo JSON. Se creará en:\n   {path}",
        "log.auto_paused": "👁️ [{nickname}] Auto-pausado.",
        "log.auto_resumed": "🔄 [{nickname}] Auto-reanudado.",
        "log.form_cleared": "📝 Formulario limpio. Listo para crear un nuevo perfil.",
        "log.updated_live": "⚙️ [{nickname}] actualizado en caliente.",
        "log.saved_profile": "💾 Perfil [{nickname}] guardado correctamente.",
        "log.deleted_profile": "🗑️ Perfil [{nickname}] eliminado.",
        "log.started": "✅ [{nickname}] iniciado y ejecutándose.",
        "log.paused": "⏸️ [{nickname}] pausado.",
        "log.resumed": "▶️ [{nickname}] reanudado.",
        "log.stopped": "🛑 [{nickname}] detenido.",
        "log.hwnd_running": "⚠️ HWND {hwnd} ya está en ejecución.",
        "log.error": "❌ Error: {error}",
        "log.layout_error": "❌ Error de diseño: {error}",
        "log.no_windows": "⚠️ No hay ventanas MIR4/MIR4G del proceso del juego.",
        "log.no_windows_minimize": "⚠️ No hay ventanas MIR4/MIR4G del proceso del juego para minimizar.",
        "log.layout_applied": "⚡ {message} a {count} ventanas MIR4 (enfocadas).",
        "log.layout_auto": "Cuadrícula automática aplicada",
        "log.layout_fixed": "Tamaño fijo {width}x{height} aplicado",
        "log.layout_custom": "Distribución {columns}x{rows} aplicada",
        "log.minimized": "⬇️ {count} ventanas MIR4 minimizadas.",
        "log.steam_closed": "🪟 Ventanas de Steam cerradas: {count}.",
        "log.mir4_timeout": "⚠️ MIR4 no apareció a tiempo; no se cerraron ventanas de Steam.",
        "log.capture_started": "🎯 MODO CAPTURA ACTIVADO. Haz clic en el botón del launcher...",
        "log.coordinates_captured": "✅ Coordenadas capturadas: X={x}, Y={y}",
        "log.capture_failed": "❌ Captura fallida. {message}",
        "log.invalid_path": "❌ Ruta incorrecta.",
        "capture.outside_window": "Clic fuera de la ventana.",
        "log.steam_updated": "💾 Ruta de Steam actualizada.",
        "log.steam_request": "🎮 Solicitud enviada a Steam.",
        "log.steam_error": "❌ Error en Steam: {error}",
        "log.steam_missing": "❌ Steam no localizado.",
        "log.launcher_saved": "💾 Configuración del launcher guardada.",
        "log.coordinates_error": "❌ Error: Verifica que las coordenadas y tiempos sean números.",
        "log.anti_ban_missing": "❌ FALTA LIBRERÍA ANTI-BAN. CMD > pip install pywinauto",
        "log.safe_sequence": "🛡️ Iniciando secuencia segura (UIAutomation)...",
        "log.uia_scan": "🔍 Escaneando elementos UIA en ({x}, {y})...",
        "log.uia_button": "✅ Botón oficial detectado. Invocando...",
        "log.uia_generic": "⚠️ Buscando controles genéricos...",
        "log.uia_control": "✅ Control encontrado ({class_name}). Invocando...",
        "log.uia_not_found": "❌ No se pudo encontrar un elemento clickeable en esas coordenadas.",
        "log.uia_error": "❌ Error interno UIA: {error}",
        "log.launcher_open": "🚀 Abriendo ejecutable del launcher...",
        "log.launcher_search": "⏳ Buscando ventana ('{title}')...",
        "log.launcher_not_found": "❌ No se encontró la ventana del launcher.",
        "log.window_found": "✅ ¡Ventana encontrada (HWND: {hwnd})!",
        "log.wait_render": "⏳ Esperando {seconds} seg para renderizar la UI...",
        "log.press_game": "🛡️ Presionando {game} vía UIAutomation...",
        "log.wait_game": "⏳ Esperando que cargue {game}...",
        "log.game_slow": "⚠️ {game} tardó demasiado, pero continuando con {next_game}...",
        "log.wait_seconds": "💤 Esperando {seconds} segundos...",
        "log.game_launcher_missing": "❌ No se pudo encontrar el launcher para abrir {game}.",
        "log.deploy_complete": "🎉 ¡Despliegue completado 100% seguro!",
        "log.deploy_timeout": "⚠️ Proceso finalizado, pero {game} pudo no haber cargado a tiempo.",
        "log.launcher_error": "❌ Error crítico en el launcher: {error}",
        "log.restart_error": "❌ No se pudo reiniciar el bot: {error}",
        "log.panic_started": "☠️ BOTÓN DE PÁNICO ACTIVADO. Eliminando procesos...",
        "log.panic_finished": "✅ Todos los procesos MIR4 (incluido Steam) han sido aniquilados.",
        "log.panic_error": "❌ Error al intentar cerrar los procesos: {error}",
        "popup.panic_title": "SISTEMA DE EMERGENCIA",
        "popup.panic_header": "☠️ SECUENCIA DE PÁNICO ☠️",
        "popup.panic_message": "¡Aniquilación completada con éxito!\nTodos los procesos de MIR4 y sus launchers\nhan sido cerrados de manera forzada.",
        "popup.attention": "Atención",
        "popup.invalid_value": "Valor inválido",
        "popup.confirm_delete": "Confirmar eliminación",
        "popup.confirm_delete_message": "¿Seguro que quieres eliminar\nel perfil [{nickname}]?",
        "popup.critical_error": "Error crítico",
        "popup.critical_error_message": "Falta la librería 'pywinauto'.\nAbre CMD y ejecuta: pip install pywinauto\n\nLuego reinicia el bot.",
        "popup.nickname_required": "Debes ingresar un APODO\npara guardar el perfil.",
        "popup.reserved_name": "[{nickname}] es un nombre reservado\nde configuración y no puede usarse como perfil.",
        "popup.select_profile_delete": "Selecciona un perfil de la tabla\npara eliminar.",
        "popup.running_profile": "No puedes eliminar un perfil en ejecución.\nDetenlo primero.",
        "popup.invalid_profile": "Ese no es un perfil guardado válido.",
        "popup.select_window": "Selecciona una ventana válida\nen el formulario o despliega el perfil primero.",
        "popup.nickname_start": "Debes ingresar o seleccionar un APODO.",
        "popup.no_mir4_window": "No hay ninguna ventana de MIR4 seleccionada en el formulario.",
        "popup.invalid_layout": "{name} debe ser un número entero positivo.",
        "popup.positive_layout": "{name} debe ser mayor que cero.",
        "popup.size_unavailable": "Con {width}x{height} solo caben {count} ventanas en el área útil del monitor.",
        "popup.distribution_insufficient": "La cuadrícula de {columns}x{rows} solo tiene {spaces} espacios para {count} ventanas.",
        "popup.distribution_invalid": "La cantidad de filas o columnas supera el tamaño del área útil del monitor.",
        "popup.config_error": "La configuración debe ser un objeto JSON",
        "config.load_error": "Error cargando JSON: {error}",
        "config.backup_created": "Copia de seguridad de configuración corrupta: {path}",
        "config.backup_error": "No se pudo respaldar la configuración corrupta: {error}",
    },
    "en": {
        "app.title": "SABANDIJA B0T - EDITION {version}",
        "app.header": "🐍 SABANDIJA CONTROL",
        "tab.instances": "  SABANDIJA INSTANCES  ",
        "tab.layout": "  RECTIL LAYOUT  ",
        "tab.deploy": "  DEPLOYMENT  ",
        "tab.log": "  HUNTING LOG  ",
        "language.selector": "Idioma / Language:",
        "language.spanish": "Español",
        "language.english": "English",
        "language.restart.title": "Language saved",
        "language.restart.message": "Restarting the bot to apply the selected language...",
        "frame.instances": " 📋 SAVED INSTANCES AND PROFILES ",
        "frame.profile": " 🛠️ PROFILE CONFIGURATION ",
        "frame.execution": " 🎮 EXECUTION CONTROL ",
        "frame.log": " HUNTING LOG ",
        "frame.layout": " RECTIL WINDOWS LAYOUT (GRID) ",
        "frame.fixed_size": " FIXED SIZE ",
        "frame.custom_distribution": " CUSTOM DISTRIBUTION ",
        "frame.steam": " STEAM INFRASTRUCTURE ",
        "frame.launcher_path": " MIR4 LAUNCHER PATH (GAME 1 & 2) ",
        "frame.coordinates": " BUTTON COORDINATES (X, Y) ",
        "frame.fine_tuning": " FINE-TUNING ",
        "column.nickname": "Nickname",
        "column.mode": "Mode",
        "column.window": "Assigned window",
        "column.delay": "Delay",
        "column.status": "Status",
        "label.nickname": "NICKNAME:",
        "label.window": "WINDOW:",
        "label.delay": "DELAY (SEC):",
        "label.launcher_path": "Steam launcher path:",
        "label.title_class": "TITLE OR CLASS:",
        "label.launcher_wait": "WAIT AFTER FINDING LAUNCHER (sec):",
        "label.game_wait": "WAIT BETWEEN GAME 1 AND GAME 2 (sec):",
        "label.offset": "Border offset: {value}",
        "label.width": "WIDTH:",
        "label.height": "HEIGHT:",
        "label.columns": "COLUMNS:",
        "label.rows": "ROWS:",
        "label.launcher_hint": "💡 If it cannot be found, use only: MIR4",
        "mode.mission": "MISSION Q",
        "mode.farm": "FARM EXP",
        "mode.boss": "SUMMON BOSS",
        "tooltip.mode.mission": "Mission Q: runs an automatic Q, E and T sequence, followed by clicks in the center of the window.",
        "tooltip.mode.farm": "EXP Farm: runs the farming sequence with TAB, Down Arrow and F. It can use the ultimate with R.",
        "tooltip.mode.boss": "Summon Boss: presses E periodically to execute the boss summoning action.",
        "check.ultimate": "USE ULTIMATE [R]",
        "button.new": "🆕 NEW",
        "button.save_profile": "💾 SAVE / UPDATE",
        "button.delete": "🗑️ DELETE",
        "button.start": "🚀 START BOT",
        "button.pause": "⏸️ PAUSE",
        "button.resume": "▶️ RESUME",
        "button.stop": "🛑 STOP",
        "button.panic": "☠️ PANIC BUTTON (CLOSE ALL MIR4) ☠️",
        "button.apply_fixed": "APPLY FIXED SIZE",
        "button.apply_grid": "APPLY ROWS AND COLUMNS",
        "button.arrange": "⚡ ARRANGE AND FOCUS WINDOWS",
        "button.minimize": "⬇️ MINIMIZE ALL WINDOWS",
        "button.save_steam": "💾 SAVE STEAM PATH",
        "button.start_steam": "🎮 START MIR4 FROM STEAM",
        "button.capture": "🎯 CAPTURE",
        "button.save_launcher": "💾 SAVE LAUNCHER CONFIGURATION",
        "button.start_uia": "🛡️ START (SAFE UIAutomation)",
        "button.ok": "OK",
        "button.yes_delete": "YES, DELETE",
        "button.cancel": "CANCEL",
        "status.auto_paused": "AUTO-PAUSED 👁️",
        "status.paused": "PAUSED ⏸️",
        "status.running": "RUNNING ▶️",
        "status.finished": "FINISHED 🛑",
        "status.saved": "SAVED 💾",
        "status.uia_ready": "✅ Safe UIAutomation loaded",
        "status.uia_missing": "❌ MISSING: Run 'pip install pywinauto'",
        "log.crud_ready": "🛡️ CRUD system enabled. Create, edit and run your profiles easily.",
        "log.initialized": "SabandijaBot {version} initialized. [{uia}]",
        "log.config_found": "📁 JSON configuration file located at:\n   {path}",
        "log.config_missing": "⚠️ JSON file not found. It will be created at:\n   {path}",
        "log.auto_paused": "👁️ [{nickname}] Auto-paused.",
        "log.auto_resumed": "🔄 [{nickname}] Auto-resumed.",
        "log.form_cleared": "📝 Form cleared. Ready to create a new profile.",
        "log.updated_live": "⚙️ [{nickname}] updated live.",
        "log.saved_profile": "💾 Profile [{nickname}] saved successfully.",
        "log.deleted_profile": "🗑️ Profile [{nickname}] deleted.",
        "log.started": "✅ [{nickname}] started and running.",
        "log.paused": "⏸️ [{nickname}] paused.",
        "log.resumed": "▶️ [{nickname}] resumed.",
        "log.stopped": "🛑 [{nickname}] stopped.",
        "log.hwnd_running": "⚠️ HWND {hwnd} is already running.",
        "log.error": "❌ Error: {error}",
        "log.layout_error": "❌ Layout error: {error}",
        "log.no_windows": "⚠️ No MIR4/MIR4G windows from the game process.",
        "log.no_windows_minimize": "⚠️ No MIR4/MIR4G windows from the game process to minimize.",
        "log.layout_applied": "⚡ {message} to {count} MIR4 windows (focused).",
        "log.layout_auto": "Automatic grid applied",
        "log.layout_fixed": "Fixed size {width}x{height} applied",
        "log.layout_custom": "{columns}x{rows} distribution applied",
        "log.minimized": "⬇️ {count} MIR4 windows minimized.",
        "log.steam_closed": "🪟 Steam windows closed: {count}.",
        "log.mir4_timeout": "⚠️ MIR4 did not appear in time; Steam windows were not closed.",
        "log.capture_started": "🎯 CAPTURE MODE ENABLED. Click the launcher button...",
        "log.coordinates_captured": "✅ Coordinates captured: X={x}, Y={y}",
        "log.capture_failed": "❌ Capture failed. {message}",
        "log.invalid_path": "❌ Incorrect path.",
        "capture.outside_window": "Click outside the window.",
        "log.steam_updated": "💾 Steam path updated.",
        "log.steam_request": "🎮 Request sent to Steam.",
        "log.steam_error": "❌ Steam error: {error}",
        "log.steam_missing": "❌ Steam not found.",
        "log.launcher_saved": "💾 Launcher configuration saved.",
        "log.coordinates_error": "❌ Error: Check that coordinates and times are numbers.",
        "log.anti_ban_missing": "❌ ANTI-BAN LIBRARY MISSING. CMD > pip install pywinauto",
        "log.safe_sequence": "🛡️ Starting safe sequence (UIAutomation)...",
        "log.uia_scan": "🔍 Scanning UIA elements at ({x}, {y})...",
        "log.uia_button": "✅ Official button detected. Invoking...",
        "log.uia_generic": "⚠️ Looking for generic controls...",
        "log.uia_control": "✅ Control found ({class_name}). Invoking...",
        "log.uia_not_found": "❌ Could not find a clickable element at those coordinates.",
        "log.uia_error": "❌ Internal UIA error: {error}",
        "log.launcher_open": "🚀 Opening launcher executable...",
        "log.launcher_search": "⏳ Looking for window ('{title}')...",
        "log.launcher_not_found": "❌ Launcher window not found.",
        "log.window_found": "✅ Window found (HWND: {hwnd})!",
        "log.wait_render": "⏳ Waiting {seconds} sec for UI to render...",
        "log.press_game": "🛡️ Pressing {game} via UIAutomation...",
        "log.wait_game": "⏳ Waiting for {game} to load...",
        "log.game_slow": "⚠️ {game} took too long, continuing with {next_game}...",
        "log.wait_seconds": "💤 Waiting {seconds} seconds...",
        "log.game_launcher_missing": "❌ Could not find the launcher to open {game}.",
        "log.deploy_complete": "🎉 Deployment completed 100% safely!",
        "log.deploy_timeout": "⚠️ Process finished, but {game} may not have loaded in time.",
        "log.launcher_error": "❌ Critical launcher error: {error}",
        "log.restart_error": "❌ Could not restart the bot: {error}",
        "log.panic_started": "☠️ PANIC BUTTON ACTIVATED. Terminating processes...",
        "log.panic_finished": "✅ All MIR4 processes (including Steam) have been terminated.",
        "log.panic_error": "❌ Error while closing processes: {error}",
        "popup.panic_title": "EMERGENCY SYSTEM",
        "popup.panic_header": "☠️ PANIC SEQUENCE ☠️",
        "popup.panic_message": "Annihilation completed successfully!\nAll MIR4 processes and launchers\nwere forcibly closed.",
        "popup.attention": "Attention",
        "popup.invalid_value": "Invalid value",
        "popup.confirm_delete": "Confirm deletion",
        "popup.confirm_delete_message": "Are you sure you want to delete\nprofile [{nickname}]?",
        "popup.critical_error": "Critical error",
        "popup.critical_error_message": "The 'pywinauto' library is missing.\nOpen CMD and run: pip install pywinauto\n\nThen restart the bot.",
        "popup.nickname_required": "Enter a NICKNAME\nto save the profile.",
        "popup.reserved_name": "[{nickname}] is a reserved configuration name\nand cannot be used as a profile.",
        "popup.select_profile_delete": "Select a profile from the table\nto delete it.",
        "popup.running_profile": "You cannot delete a running profile.\nStop it first.",
        "popup.invalid_profile": "That is not a valid saved profile.",
        "popup.select_window": "Select a valid window\nin the form or deploy the profile first.",
        "popup.nickname_start": "Enter or select a NICKNAME.",
        "popup.no_mir4_window": "No MIR4 window is selected in the form.",
        "popup.invalid_layout": "{name} must be a positive integer.",
        "popup.positive_layout": "{name} must be greater than zero.",
        "popup.size_unavailable": "Only {count} windows fit in the monitor work area at {width}x{height}.",
        "popup.distribution_insufficient": "The {columns}x{rows} grid has only {spaces} spaces for {count} windows.",
        "popup.distribution_invalid": "The number of rows or columns exceeds the monitor work area size.",
        "popup.config_error": "Configuration must be a JSON object",
        "config.load_error": "Error loading JSON: {error}",
        "config.backup_created": "Corrupt configuration backup: {path}",
        "config.backup_error": "Could not back up corrupt configuration: {error}",
    },
}

MODE_TRANSLATION_KEYS = {
    "MISION_Q": "mode.mission",
    "FARMA_EXP": "mode.farm",
    "SUMMON_BOSS": "mode.boss",
}

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


def obtener_ventanas_mir4():
    ventanas = []

    def callback(hwnd, _):
        if es_ventana_mir4(hwnd):
            ventanas.append(hwnd)
        return True

    win32gui.EnumWindows(callback, None)
    return ventanas


def es_ventana_mir4(hwnd):
    """Valida que la ventana sea del juego y no solo tenga MIR4 en el título."""
    if not win32gui.IsWindowVisible(hwnd):
        return False
    if "MIR4" not in win32gui.GetWindowText(hwnd).upper():
        return False

    proceso = None
    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        proceso = win32api.OpenProcess(
            win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ,
            False,
            pid,
        )
        ruta_proceso = win32process.GetModuleFileNameEx(proceso, 0)
        return os.path.basename(ruta_proceso).lower() in MIR4_GAME_PROCESS_NAMES
    except Exception:
        return False
    finally:
        if proceso:
            win32api.CloseHandle(proceso)


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

MIR4_GAME_PROCESS_NAMES = {
    "mir4.exe",
    "mir4g.exe",
    "mir4gclient.exe",
    "mir4s.exe",
    "mir4-win64-shipping.exe",
    "mir4g-win64-shipping.exe",
}

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


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.after_id = None
        widget.bind("<Enter>", self._schedule, add="+")
        widget.bind("<Leave>", self._hide, add="+")
        widget.bind("<ButtonPress>", self._hide, add="+")

    def _schedule(self, _event=None):
        self._hide()
        self.after_id = self.widget.after(350, self._show)

    def _show(self):
        if self.tipwindow or not self.widget.winfo_viewable():
            return
        x = self.widget.winfo_rootx() + 12
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 6
        self.tipwindow = tk.Toplevel(self.widget)
        self.tipwindow.wm_overrideredirect(True)
        self.tipwindow.wm_geometry(f"+{x}+{y}")
        tk.Label(
            self.tipwindow,
            text=self.text,
            justify="left",
            wraplength=320,
            bg="#172417",
            fg="#ffffff",
            relief="solid",
            borderwidth=1,
            padx=8,
            pady=6,
            font=("Segoe UI", 9),
        ).pack()

    def _hide(self, _event=None):
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None


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
    def t(self, key, **kwargs):
        text = TRANSLATIONS.get(self.idioma, TRANSLATIONS["es"]).get(key, key)
        return text.format(**kwargs)

    def modo_visible(self, modo):
        return self.t(MODE_TRANSLATION_KEYS.get(modo, "mode.mission"))

    def __init__(self, root):
        self.root = root
        self.idioma = "es"
        self.root.geometry("640x590")
        self.root.minsize(520, 440)
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
        self.reiniciando = False
        self.item_a_hwnd = {} # Mapeo invisible entre fila de tabla y HWND
        
        # --- CORRECCIÓN PARA .EXE ---
        if getattr(sys, 'frozen', False):
            dir_aplicacion = os.path.dirname(sys.executable)
        else:
            dir_aplicacion = os.path.dirname(os.path.abspath(__file__))
        self.config_file = os.path.join(dir_aplicacion, "config.json")
        
        self.config = {}

        # --- CARGA / CREACIÓN DE JSON ---
        defaults = {
            'RUTAS': {'steam': r"C:\Program Files (x86)\Steam\steam.exe"},
            'LAUNCHER': {
                'ruta': r"C:\Wemade\Mir4Global\Mir4Launcher\Mir4Launcher.exe",
                'g1_x': 815, 'g1_y': 539, 'g2_x': 968, 'g2_y': 541,
                'titulo': "CLASS:HwndWrapper[Mir4Launcher.exe",
                'delay_pre_click': 15, 'delay': 15
            },
            'LAYOUT': {
                'offset': 0,
                'fixed_width': 800,
                'fixed_height': 450,
                'columns': 2,
                'rows': 2,
            },
        }
        config_necesita_guardado = False

        if not os.path.exists(self.config_file):
            self.config = {}
            config_necesita_guardado = True
        else:
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                if not isinstance(self.config, dict):
                    raise ValueError(self.t("popup.config_error"))
            except Exception as e:
                print(self.t("config.load_error", error=e))
                try:
                    shutil.copy2(self.config_file, self.config_file + ".corrupt")
                    print(self.t("config.backup_created", path=f"{self.config_file}.corrupt"))
                except OSError as backup_error:
                    print(self.t("config.backup_error", error=backup_error))
                self.config = {}
                config_necesita_guardado = True

        for section, default_value in defaults.items():
            if section not in self.config or not isinstance(self.config[section], dict):
                self.config[section] = default_value.copy()
                config_necesita_guardado = True

        idioma_guardado = self.config.get("IDIOMA", "es")
        self.idioma = idioma_guardado if isinstance(idioma_guardado, str) and idioma_guardado in TRANSLATIONS else "es"
        if self.config.get("IDIOMA") != self.idioma:
            self.config["IDIOMA"] = self.idioma
            config_necesita_guardado = True

        if config_necesita_guardado:
            self.guardar_config()

        self.root.title(self.t("app.title", version=APP_VERSION))

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TNotebook", background=COLOR_BG, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=COLOR_CARD, foreground=COLOR_TEXT_OFF, padding=[8, 4], font=('Segoe UI', 9, 'bold'))
        self.style.map("TNotebook.Tab", background=[("selected", COLOR_ACCENT)], foreground=[("selected", "#000")])
        self.style.configure("TFrame", background=COLOR_BG)
        self.style.configure("Card.TLabelframe", background=COLOR_BG, foreground=COLOR_ACCENT, bordercolor=COLOR_ACCENT)
        self.style.configure("Card.TLabelframe.Label", background=COLOR_BG, foreground=COLOR_ACCENT, font=('Consolas', 10, 'bold'))
        self.style.configure("Treeview", background=COLOR_CARD, foreground="#fff", fieldbackground=COLOR_CARD, rowheight=20, font=('Segoe UI', 8))
        self.style.configure("Treeview.Heading", background=COLOR_INPUT_BG, foreground=COLOR_ACCENT, font=('Segoe UI', 8, 'bold'))
        self.style.map("Treeview", background=[("selected", COLOR_ACCENT)], foreground=[("selected", "#000")])

        header_frame = tk.Frame(self.root, bg=COLOR_BG)
        header_frame.pack(fill="x", pady=3)
        tk.Label(header_frame, text=self.t("app.header"), bg=COLOR_BG, fg=COLOR_ACCENT, font=('Impact', 18)).pack()

        language_frame = tk.Frame(header_frame, bg=COLOR_BG)
        language_frame.pack(fill="x", padx=10, pady=(0, 2))
        tk.Label(language_frame, text=self.t("language.selector"), bg=COLOR_BG, fg=COLOR_TEXT_OFF, font=('Segoe UI', 8, 'bold')).pack(side="right", padx=(5, 0))
        self.idioma_selector = ttk.Combobox(
            language_frame,
            state="readonly",
            width=10,
            values=(self.t("language.spanish"), self.t("language.english")),
            font=('Segoe UI', 8),
        )
        self.idioma_selector.set(self.t("language.spanish" if self.idioma == "es" else "language.english"))
        self.idioma_selector.pack(side="right")
        self.idioma_selector.bind("<<ComboboxSelected>>", self.cambiar_idioma)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=6, pady=3)

        self.tab_bot = ttk.Frame(self.notebook)
        self.tab_layout = ttk.Frame(self.notebook)
        self.tab_despliegue = ttk.Frame(self.notebook)
        self.tab_log = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_bot, text=self.t("tab.instances"))
        self.notebook.add(self.tab_layout, text=self.t("tab.layout"))
        self.notebook.add(self.tab_despliegue, text=self.t("tab.deploy"))
        self.notebook.add(self.tab_log, text=self.t("tab.log"))

        self.setup_tab_log()
        self.setup_tab_bot()
        self.setup_tab_layout()
        self.setup_tab_despliegue()

        self.log_status(self.t("log.crud_ready"))

        self.running_monitor = True
        self.monitor_thread = threading.Thread(target=self.monitor_foco_ventanas, daemon=True)
        self.monitor_thread.start()

    def cambiar_idioma(self, event=None):
        if self.reiniciando:
            return
        idioma_nuevo = "en" if self.idioma_selector.get() == self.t("language.english") else "es"
        if idioma_nuevo == self.idioma:
            return
        self.config["IDIOMA"] = idioma_nuevo
        self.guardar_config()
        self.reiniciando = True
        self.idioma_selector.configure(state="disabled")
        self.mostrar_alerta(self.t("language.restart.title"), self.t("language.restart.message"))
        self.root.after(700, self.reiniciar_aplicacion)

    def reiniciar_aplicacion(self):
        self.running_monitor = False
        for bot in list(self.instancias_activas.values()):
            bot.stop()

        if getattr(sys, "frozen", False):
            comando = [sys.executable, *sys.argv[1:]]
            directorio = os.path.dirname(sys.executable)
        else:
            comando = [sys.executable, os.path.abspath(__file__), *sys.argv[1:]]
            directorio = os.path.dirname(os.path.abspath(__file__))

        try:
            subprocess.Popen(comando, cwd=directorio)
        except Exception as error:
            self.reiniciando = False
            self.idioma_selector.configure(state="readonly")
            self.mostrar_alerta(
                self.t("popup.critical_error"),
                self.t("log.restart_error", error=error),
                es_error=True,
            )
            return

        self.root.destroy()

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

        tk.Button(popup, text=self.t("button.ok"), bg=COLOR_CARD, fg=COLOR_ACCENT, activebackground=COLOR_ACCENT, activeforeground="#000", font=('Segoe UI', 9, 'bold'), relief="groove", width=15, command=popup.destroy).pack(pady=(15, 10))

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

        tk.Button(btn_frame, text=self.t("button.yes_delete"), bg="#330000", fg="#ff0000", activebackground="#ff0000", activeforeground="#fff", font=('Segoe UI', 9, 'bold'), relief="groove", width=15, command=on_yes).pack(side="left", padx=10)
        tk.Button(btn_frame, text=self.t("button.cancel"), bg=COLOR_CARD, fg=COLOR_ACCENT, activebackground=COLOR_ACCENT, activeforeground="#000", font=('Segoe UI', 9, 'bold'), relief="groove", width=15, command=on_no).pack(side="left", padx=10)

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
                            self.log_status(self.t("log.auto_paused", nickname=bot.apodo))
                            cambio_detectado = True
                    else:
                        if bot.paused and bot.forced_pause and not bot.manual_pause:
                            bot.resume(); bot.forced_pause = False
                            self.log_status(self.t("log.auto_resumed", nickname=bot.apodo))
                            cambio_detectado = True
                if cambio_detectado: self.root.after(0, self.actualizar_tabla_visual)
            except Exception: pass

    # --- TAB BOT (SISTEMA CRUD) ---
    def setup_tab_bot(self):
        scroll_wrapper = ScrollableFrame(self.tab_bot, COLOR_BG)
        scroll_wrapper.pack(fill="both", expand=True)
        container = scroll_wrapper.scrollable_frame

        # 1. LISTA DE PERFILES E INSTANCIAS (READ)
        frame_lista = ttk.LabelFrame(container, text=self.t("frame.instances"), style="Card.TLabelframe")
        frame_lista.pack(fill="x", padx=10, pady=3)
        
        self.tabla_instancias = ttk.Treeview(frame_lista, columns=("apodo", "modo", "ventana", "delay", "estado"), show="headings", height=5)
        for col, key, w in [("apodo","column.nickname",100), ("modo","column.mode",95), ("ventana","column.window",150), ("delay","column.delay",55), ("estado","column.status",95)]:
            txt = self.t(key)
            self.tabla_instancias.heading(col, text=txt); self.tabla_instancias.column(col, width=w, anchor="center")
        self.tabla_instancias.pack(fill="x", padx=5, pady=5)
        self.tabla_instancias.bind("<<TreeviewSelect>>", self.cargar_datos_seleccionados)

        # 2. FORMULARIO DE EDICIÓN (CREATE / UPDATE)
        frame_form = ttk.LabelFrame(container, text=self.t("frame.profile"), style="Card.TLabelframe")
        frame_form.pack(fill="x", padx=10, pady=3)
        
        self.modo_var = tk.StringVar(value="MISION_Q")

        # Fila 1: Apodo y Ventana
        f1 = tk.Frame(frame_form, bg=COLOR_BG); f1.pack(fill="x", padx=10, pady=3)
        tk.Label(f1, text=self.t("label.nickname"), bg=COLOR_BG, fg=COLOR_ACCENT, font=('Segoe UI', 9, 'bold'), width=10).pack(side="left")
        self.entry_apodo = tk.Entry(f1, width=12, bg=COLOR_INPUT_BG, fg="#fff", insertbackground=COLOR_ACCENT, borderwidth=0, font=('Segoe UI', 9))
        self.entry_apodo.pack(side="left", padx=5)
        
        tk.Label(f1, text=self.t("label.window"), bg=COLOR_BG, fg=COLOR_ACCENT, font=('Segoe UI', 9, 'bold'), width=10).pack(side="left", padx=(10,0))
        self.combo_ventanas = ttk.Combobox(f1, state="readonly", width=24, font=('Segoe UI', 9))
        self.combo_ventanas.pack(side="left", padx=5, fill="x", expand=True)
        tk.Button(f1, text="🔄", bg=COLOR_CARD, fg=COLOR_ACCENT, relief="groove", command=self.actualizar_combo).pack(side="left", padx=2)

        # Fila 2: Modos
        f2 = tk.Frame(frame_form, bg=COLOR_BG); f2.pack(fill="x", padx=10, pady=1)
        def on_mode_change():
            self.actualizar_radio_colores()
        self.rb_mision = tk.Radiobutton(f2, text=self.t("mode.mission"), variable=self.modo_var, value="MISION_Q", bg=COLOR_BG, fg=COLOR_TEXT_ON, selectcolor="#000", font=('Segoe UI', 9, 'bold'), command=on_mode_change)
        self.rb_mision.pack(side="left", padx=5)
        self.rb_farma = tk.Radiobutton(f2, text=self.t("mode.farm"), variable=self.modo_var, value="FARMA_EXP", bg=COLOR_BG, fg=COLOR_TEXT_OFF, selectcolor="#000", font=('Segoe UI', 9, 'bold'), command=on_mode_change)
        self.rb_farma.pack(side="left", padx=5)
        self.rb_summon = tk.Radiobutton(f2, text=self.t("mode.boss"), variable=self.modo_var, value="SUMMON_BOSS", bg=COLOR_BG, fg=COLOR_TEXT_OFF, selectcolor="#000", font=('Segoe UI', 9, 'bold'), command=on_mode_change)
        self.rb_summon.pack(side="left", padx=5)
        self.mode_tooltips = [
            ToolTip(self.rb_mision, self.t("tooltip.mode.mission")),
            ToolTip(self.rb_farma, self.t("tooltip.mode.farm")),
            ToolTip(self.rb_summon, self.t("tooltip.mode.boss")),
        ]

        # Fila 3: Delay y Ulti
        f3 = tk.Frame(frame_form, bg=COLOR_BG); f3.pack(fill="x", padx=10, pady=3)
        tk.Label(f3, text=self.t("label.delay"), bg=COLOR_BG, fg=COLOR_ACCENT, font=('Segoe UI', 9, 'bold')).pack(side="left")
        self.entry_delay = tk.Entry(f3, width=5, bg=COLOR_INPUT_BG, fg=COLOR_ACCENT, insertbackground=COLOR_ACCENT, borderwidth=0, font=('Consolas', 10, 'bold'))
        self.entry_delay.insert(0, "5"); self.entry_delay.pack(side="left", padx=5)
        self.check_ulti = tk.Checkbutton(f3, text=self.t("check.ultimate"), variable=self.ulti_var, bg=COLOR_BG, fg=COLOR_TEXT_OFF, selectcolor="#000", state="disabled", activebackground=COLOR_BG, activeforeground=COLOR_SECONDARY, font=('Segoe UI', 9, 'bold'), command=on_mode_change)
        self.check_ulti.pack(side="left", padx=15)

        # Botones CRUD
        btn_crud_frame = tk.Frame(frame_form, bg=COLOR_BG); btn_crud_frame.pack(fill="x", padx=10, pady=3)
        tk.Button(btn_crud_frame, text=self.t("button.new"), bg=COLOR_CARD, fg="#fff", font=('Segoe UI', 8, 'bold'), relief="groove", command=self.limpiar_formulario).pack(side="left", fill="x", expand=True, padx=2)
        tk.Button(btn_crud_frame, text=self.t("button.save_profile"), bg=COLOR_ACCENT, fg="#000", font=('Segoe UI', 8, 'bold'), relief="flat", command=self.guardar_o_actualizar_perfil).pack(side="left", fill="x", expand=True, padx=2)
        tk.Button(btn_crud_frame, text=self.t("button.delete"), bg="#330000", fg="#ff0000", font=('Segoe UI', 8, 'bold'), relief="groove", command=self.eliminar_perfil_seleccionado).pack(side="left", fill="x", expand=True, padx=2)

        # 3. CONTROL DE EJECUCIÓN
        frame_exec = ttk.LabelFrame(container, text=self.t("frame.execution"), style="Card.TLabelframe")
        frame_exec.pack(fill="x", padx=10, pady=3)
        
        btn_exec_frame = tk.Frame(frame_exec, bg=COLOR_BG); btn_exec_frame.pack(pady=3, fill="x", padx=8)

        self.btn_iniciar = tk.Button(btn_exec_frame, text=self.t("button.start"), font=('Segoe UI', 8, 'bold'), relief="flat", command=self.iniciar_instancia)
        self.btn_iniciar.pack(side="left", fill="x", expand=True, padx=2)

        self.btn_pausar = tk.Button(btn_exec_frame, text=self.t("button.pause"), font=('Segoe UI', 8, 'bold'), relief="flat", command=self.pausar_instancia)
        self.btn_pausar.pack(side="left", fill="x", expand=True, padx=2)

        self.btn_reanudar = tk.Button(btn_exec_frame, text=self.t("button.resume"), font=('Segoe UI', 8, 'bold'), relief="flat", command=self.reanudar_instancia)
        self.btn_reanudar.pack(side="left", fill="x", expand=True, padx=2)

        self.btn_detener = tk.Button(btn_exec_frame, text=self.t("button.stop"), font=('Segoe UI', 8, 'bold'), relief="flat", command=self.detener_instancia)
        self.btn_detener.pack(side="left", fill="x", expand=True, padx=2)

        # 4. PANICO
        btn_panico = tk.Button(container, text=self.t("button.panic"),
                               bg="#cc0000", fg="#ffffff", font=('Segoe UI', 9, 'bold'), 
                               relief="flat", activebackground="#ff3333", 
                               pady=3, command=self.boton_de_panico)
        btn_panico.pack(fill="x", padx=10, pady=(3, 3))

        self.actualizar_combo()
        self.actualizar_tabla_visual()

        estado_uia = self.t("status.uia_ready") if UIA_AVAILABLE else self.t("status.uia_missing")
        self.log_status(self.t("log.initialized", version=APP_VERSION, uia=estado_uia))

        ruta_abs_json = os.path.abspath(self.config_file)
        if os.path.exists(self.config_file):
            self.log_status(self.t("log.config_found", path=ruta_abs_json))
        else:
            self.log_status(self.t("log.config_missing", path=ruta_abs_json))

    def setup_tab_log(self):
        frame_log = ttk.LabelFrame(self.tab_log, text=self.t("frame.log"), style="Card.TLabelframe")
        frame_log.pack(fill="both", expand=True, padx=10, pady=10)
        self.txt_log = tk.Text(
            frame_log,
            bg="#020502",
            fg=COLOR_ACCENT,
            font=('Consolas', 8),
            state='disabled',
            borderwidth=0,
            height=5,
        )
        self.txt_log.pack(fill="both", expand=True, padx=5, pady=5)

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
        self.log_status(self.t("log.form_cleared"))

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
            self.mostrar_alerta(self.t("popup.attention"), self.t("popup.nickname_required"))
            return
        if apodo in RESERVED_CONFIG_SECTIONS:
            self.mostrar_alerta(self.t("popup.attention"), self.t("popup.reserved_name", nickname=apodo))
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
                self.log_status(self.t("log.updated_live", nickname=bot.apodo))
            except Exception as e:
                self.log_status(self.t("log.error", error=e))

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
        self.log_status(self.t("log.saved_profile", nickname=apodo))
        self.actualizar_tabla_visual()

    def eliminar_perfil_seleccionado(self):
        if not self.tabla_instancias.selection():
            self.mostrar_alerta(self.t("popup.attention"), self.t("popup.select_profile_delete"))
            return

        item = self.tabla_instancias.selection()[0]
        valores = self.tabla_instancias.item(item, "values")
        apodo = str(valores[0])

        hwnd_val = self.item_a_hwnd.get(item)
        if isinstance(hwnd_val, int) and hwnd_val in self.instancias_activas:
            self.mostrar_alerta(self.t("popup.attention"), self.t("popup.running_profile"))
            return

        if apodo in self.config:
            if self.pedir_confirmacion(self.t("popup.confirm_delete"), self.t("popup.confirm_delete_message", nickname=apodo)):
                del self.config[apodo]
                self.guardar_config()
                self.log_status(self.t("log.deleted_profile", nickname=apodo))
                self.actualizar_tabla_visual()
                self.limpiar_formulario()
        else:
            self.mostrar_alerta(self.t("popup.attention"), self.t("popup.invalid_profile"))

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
            if es_ventana_mir4(hwnd): ventanas.append(f"{win32gui.GetWindowText(hwnd)} (HWND: {hwnd})")
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
            estado = self.t("status.auto_paused") if (bot.paused and bot.forced_pause) else (self.t("status.paused") if bot.paused else self.t("status.running"))
            if not bot.is_alive() or not bot.running: estado = self.t("status.finished")
            
            try:
                titulo_ventana = win32gui.GetWindowText(hwnd) or f"HWND {hwnd}"
            except:
                titulo_ventana = f"HWND {hwnd}"
                
            item = self.tabla_instancias.insert("", tk.END, values=(bot.apodo, self.modo_visible(bot.modo), titulo_ventana, f"{bot.delay_personalizado}s", estado))
            self.item_a_hwnd[item] = hwnd
            if bot.apodo == apodo_seleccionado: self.tabla_instancias.selection_set(item)
            apodos_activos.append(bot.apodo)

        for section in self.config.keys():
            if section in RESERVED_CONFIG_SECTIONS: continue
            if section not in apodos_activos:
                modo = self.config[section].get("modo", "MISION_Q")
                delay = self.config[section].get("delay", 5.0)
                ventana_t = self.config[section].get("ventana_titulo", "Pendiente")
                item = self.tabla_instancias.insert("", tk.END, values=(section, self.modo_visible(modo), ventana_t, f"{delay}s", self.t("status.saved")))
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
                
        self.mostrar_alerta(self.t("popup.attention"), self.t("popup.select_window"));
        return None

    # --- CONTROL DE EJECUCIÓN ---
    def iniciar_instancia(self):
        apodo = self.entry_apodo.get().strip()
        if not apodo:
            self.mostrar_alerta(self.t("popup.attention"), self.t("popup.nickname_start"))
            return

        # Asegurarnos de guardar el perfil antes de iniciar
        self.guardar_o_actualizar_perfil()

        sel = self.combo_ventanas.get()
        if not sel: 
            self.mostrar_alerta(self.t("popup.attention"), self.t("popup.no_mir4_window"))
            return
            
        try:
            hwnd = int(sel.split("(HWND: ")[1].replace(")", ""))
            if hwnd in self.instancias_activas and self.instancias_activas[hwnd].is_alive():
                self.log_status(self.t("log.hwnd_running", hwnd=hwnd)); return

            modo = self.modo_var.get()
            delay = float(self.entry_delay.get())
            usar_ulti = self.ulti_var.get() if modo == "FARMA_EXP" else False

            bot = BotInstance(hwnd, modo, delay, usar_ulti, apodo)
            self.instancias_activas[hwnd] = bot
            bot.start()
            self.log_status(self.t("log.started", nickname=bot.apodo))
            self.actualizar_tabla_visual()
        except Exception as e: self.log_status(self.t("log.error", error=e))

    def pausar_instancia(self):
        hwnd = self.obtener_hwnd_seleccionado()
        if hwnd and hwnd in self.instancias_activas:
            bot = self.instancias_activas[hwnd]; bot.manual_pause = True; bot.forced_pause = False; bot.pause()
            self.log_status(self.t("log.paused", nickname=bot.apodo)); self.actualizar_tabla_visual()

    def reanudar_instancia(self):
        hwnd = self.obtener_hwnd_seleccionado()
        if hwnd and hwnd in self.instancias_activas:
            bot = self.instancias_activas[hwnd]; bot.manual_pause = False; bot.forced_pause = False; bot.resume()
            self.log_status(self.t("log.resumed", nickname=bot.apodo)); self.actualizar_tabla_visual()

    def detener_instancia(self):
        hwnd = self.obtener_hwnd_seleccionado()
        if hwnd and hwnd in self.instancias_activas:
            bot = self.instancias_activas[hwnd]; bot.stop(); del self.instancias_activas[hwnd]
            self.log_status(self.t("log.stopped", nickname=bot.apodo)); self.actualizar_tabla_visual()

    # --- TAB LAYOUT ---
    def setup_tab_layout(self):
        frame_grid = ttk.LabelFrame(self.tab_layout, text=self.t("frame.layout"), style="Card.TLabelframe")
        frame_grid.pack(fill="both", expand=True, padx=10, pady=10)

        layout_config = self.config.get('LAYOUT', {})
        saved_offset = layout_config.get('offset', 0)

        self.label_offset = ttk.Label(frame_grid, text=self.t("label.offset", value=saved_offset), background=COLOR_BG, foreground=COLOR_ACCENT, font=('Segoe UI', 10, 'bold'))
        self.label_offset.pack(pady=8)

        self.offset_var = tk.IntVar(value=saved_offset)

        def on_offset_change(v):
            val = int(float(v))
            self.label_offset.config(text=self.t("label.offset", value=val))
            if 'LAYOUT' not in self.config: self.config['LAYOUT'] = {}
            self.config['LAYOUT']['offset'] = val
            self.guardar_config()

        self.slider = ttk.Scale(frame_grid, from_=0, to=20, orient='horizontal', variable=self.offset_var, command=on_offset_change)
        self.slider.pack(fill="x", padx=30, pady=10)

        frame_fixed = ttk.LabelFrame(frame_grid, text=self.t("frame.fixed_size"), style="Card.TLabelframe")
        frame_fixed.pack(fill="x", padx=15, pady=(2, 5))
        fixed_row = tk.Frame(frame_fixed, bg=COLOR_BG)
        fixed_row.pack(fill="x", padx=8, pady=5)

        tk.Label(fixed_row, text=self.t("label.width"), bg=COLOR_BG, fg=COLOR_ACCENT, font=('Segoe UI', 9, 'bold')).pack(side="left")
        self.entry_layout_width = tk.Entry(fixed_row, width=7, bg=COLOR_INPUT_BG, fg="#fff", insertbackground=COLOR_ACCENT, borderwidth=0, font=('Consolas', 10, 'bold'))
        self.entry_layout_width.insert(0, str(layout_config.get('fixed_width', 800)))
        self.entry_layout_width.pack(side="left", padx=(4, 12))

        tk.Label(fixed_row, text=self.t("label.height"), bg=COLOR_BG, fg=COLOR_ACCENT, font=('Segoe UI', 9, 'bold')).pack(side="left")
        self.entry_layout_height = tk.Entry(fixed_row, width=7, bg=COLOR_INPUT_BG, fg="#fff", insertbackground=COLOR_ACCENT, borderwidth=0, font=('Consolas', 10, 'bold'))
        self.entry_layout_height.insert(0, str(layout_config.get('fixed_height', 450)))
        self.entry_layout_height.pack(side="left", padx=(4, 12))

        tk.Button(fixed_row, text=self.t("button.apply_fixed"), bg=COLOR_CARD, fg=COLOR_SECONDARY, font=('Segoe UI', 8, 'bold'), relief="groove", command=self.aplicar_tamano_fijo).pack(side="left", fill="x", expand=True)

        frame_custom = ttk.LabelFrame(frame_grid, text=self.t("frame.custom_distribution"), style="Card.TLabelframe")
        frame_custom.pack(fill="x", padx=15, pady=5)
        custom_row = tk.Frame(frame_custom, bg=COLOR_BG)
        custom_row.pack(fill="x", padx=8, pady=5)

        tk.Label(custom_row, text=self.t("label.columns"), bg=COLOR_BG, fg=COLOR_ACCENT, font=('Segoe UI', 9, 'bold')).pack(side="left")
        self.entry_layout_columns = tk.Entry(custom_row, width=5, bg=COLOR_INPUT_BG, fg="#fff", insertbackground=COLOR_ACCENT, borderwidth=0, font=('Consolas', 10, 'bold'))
        self.entry_layout_columns.insert(0, str(layout_config.get('columns', 2)))
        self.entry_layout_columns.pack(side="left", padx=(4, 12))

        tk.Label(custom_row, text=self.t("label.rows"), bg=COLOR_BG, fg=COLOR_ACCENT, font=('Segoe UI', 9, 'bold')).pack(side="left")
        self.entry_layout_rows = tk.Entry(custom_row, width=5, bg=COLOR_INPUT_BG, fg="#fff", insertbackground=COLOR_ACCENT, borderwidth=0, font=('Consolas', 10, 'bold'))
        self.entry_layout_rows.insert(0, str(layout_config.get('rows', 2)))
        self.entry_layout_rows.pack(side="left", padx=(4, 12))

        tk.Button(custom_row, text=self.t("button.apply_grid"), bg=COLOR_CARD, fg=COLOR_SECONDARY, font=('Segoe UI', 8, 'bold'), relief="groove", command=self.aplicar_distribucion_personalizada).pack(side="left", fill="x", expand=True)

        tk.Button(frame_grid, text=self.t("button.arrange"), bg=COLOR_ACCENT, fg="#000", font=('Segoe UI', 10, 'bold'), relief="flat", activebackground=COLOR_SECONDARY, command=self.ordenar_grid_ventanas).pack(pady=(12, 6), fill="x", padx=25)
        tk.Button(frame_grid, text=self.t("button.minimize"), bg=COLOR_CARD, fg="#fff", font=('Segoe UI', 10, 'bold'), relief="flat", activebackground=COLOR_DISABLED_FG, command=self.minimizar_grid_ventanas).pack(pady=(0, 12), fill="x", padx=25)

    def _leer_entero_layout(self, entry, nombre):
        try:
            valor = int(entry.get().strip())
        except ValueError:
            self.mostrar_alerta(self.t("popup.invalid_value"), self.t("popup.invalid_layout", name=nombre))
            return None
        if valor <= 0:
            self.mostrar_alerta(self.t("popup.invalid_value"), self.t("popup.positive_layout", name=nombre))
            return None
        return valor

    def _guardar_layout_valores(self, **valores):
        if 'LAYOUT' not in self.config:
            self.config['LAYOUT'] = {}
        self.config['LAYOUT'].update(valores)
        self.guardar_config()

    def _obtener_area_trabajo(self):
        rect = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0, 0)))['Work']
        return rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]

    def _mover_ventanas_layout(self, v_list, posiciones, mensaje):
        try:
            for hwnd, x, y, ancho, alto in posiciones:
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.MoveWindow(hwnd, x, y, ancho, alto, True)
                win32gui.SetForegroundWindow(hwnd)
                time.sleep(0.05)

            self.root.after(100, lambda: self.root.focus_force())
            self.log_status(self.t("log.layout_applied", message=mensaje, count=len(v_list)))
        except Exception as e:
            self.log_status(self.t("log.layout_error", error=e))

    def ordenar_grid_ventanas(self):
        v_list = obtener_ventanas_mir4()
        v_list.sort()
        if not v_list:
            self.log_status(self.t("log.no_windows"))
            return

        w_x, w_y, w_w, w_h = self._obtener_area_trabajo()
        num = len(v_list)
        cols = int(num ** 0.5)
        if cols * cols < num:
            cols += 1
        rows = (num + cols - 1) // cols
        win_w = w_w // cols
        win_h = w_h // rows
        offset = self.offset_var.get()
        posiciones = []
        for i, hwnd in enumerate(v_list):
            r, c = i // cols, i % cols
            posiciones.append((hwnd, w_x + (c * win_w) - offset, w_y + (r * win_h), win_w + (offset * 2), win_h + offset))

        self._guardar_layout_valores(offset=offset)
        self._mover_ventanas_layout(v_list, posiciones, self.t("log.layout_auto"))

    def aplicar_tamano_fijo(self):
        ancho = self._leer_entero_layout(self.entry_layout_width, "El ancho")
        alto = self._leer_entero_layout(self.entry_layout_height, "El alto")
        if ancho is None or alto is None:
            return

        v_list = obtener_ventanas_mir4()
        v_list.sort()
        if not v_list:
            self.log_status(self.t("log.no_windows"))
            return

        w_x, w_y, w_w, w_h = self._obtener_area_trabajo()
        columnas = w_w // ancho
        filas = w_h // alto
        capacidad = columnas * filas
        if capacidad == 0 or len(v_list) > capacidad:
            self.mostrar_alerta(self.t("popup.invalid_value"), self.t("popup.size_unavailable", width=ancho, height=alto, count=capacidad))
            return

        posiciones = []
        offset = self.offset_var.get()
        for i, hwnd in enumerate(v_list):
            fila, columna = i // columnas, i % columnas
            posiciones.append((hwnd, w_x + columna * ancho - offset, w_y + fila * alto, ancho + (offset * 2), alto + offset))

        self._guardar_layout_valores(fixed_width=ancho, fixed_height=alto, offset=offset)
        self._mover_ventanas_layout(v_list, posiciones, self.t("log.layout_fixed", width=ancho, height=alto))

    def aplicar_distribucion_personalizada(self):
        columnas = self._leer_entero_layout(self.entry_layout_columns, "Las columnas")
        filas = self._leer_entero_layout(self.entry_layout_rows, "Las filas")
        if columnas is None or filas is None:
            return

        v_list = obtener_ventanas_mir4()
        v_list.sort()
        if not v_list:
            self.log_status(self.t("log.no_windows"))
            return

        w_x, w_y, w_w, w_h = self._obtener_area_trabajo()
        espacios = columnas * filas
        if len(v_list) > espacios:
            self.mostrar_alerta(self.t("popup.invalid_value"), self.t("popup.distribution_insufficient", columns=columnas, rows=filas, spaces=espacios, count=len(v_list)))
            return
        if columnas > w_w or filas > w_h:
            self.mostrar_alerta(self.t("popup.invalid_value"), self.t("popup.distribution_invalid"))
            return

        ancho = w_w // columnas
        alto = w_h // filas
        offset = self.offset_var.get()
        posiciones = []
        for i, hwnd in enumerate(v_list):
            fila, columna = i // columnas, i % columnas
            posiciones.append((hwnd, w_x + columna * ancho - offset, w_y + fila * alto, ancho + (offset * 2), alto + offset))

        self._guardar_layout_valores(columns=columnas, rows=filas, offset=offset)
        self._mover_ventanas_layout(v_list, posiciones, self.t("log.layout_custom", columns=columnas, rows=filas))

    def minimizar_grid_ventanas(self):
        v_list = obtener_ventanas_mir4()
        v_list.sort()
        if not v_list:
            self.log_status(self.t("log.no_windows_minimize"))
            return
        try:
            for hwnd in v_list:
                win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            self.log_status(self.t("log.minimized", count=len(v_list)))
        except Exception as e: self.log_status(self.t("log.error", error=e))

    # --- TAB DESPLIEGUE ---
    def setup_tab_despliegue(self):
        scroll_wrapper = ScrollableFrame(self.tab_despliegue, COLOR_BG)
        scroll_wrapper.pack(fill="both", expand=True)
        container = scroll_wrapper.scrollable_frame

        frame_steam = ttk.LabelFrame(container, text=self.t("frame.steam"), style="Card.TLabelframe")
        frame_steam.pack(fill="x", padx=15, pady=(10, 5))
        tk.Label(frame_steam, text=self.t("label.launcher_path"), bg=COLOR_BG, fg=COLOR_ACCENT, font=('Segoe UI', 9, 'bold')).pack(anchor="w", padx=15, pady=(5,0))
        self.ent_steam = tk.Entry(frame_steam, bg=COLOR_INPUT_BG, fg="#fff", borderwidth=0, font=('Segoe UI', 9))
        steam_path = self.config.get('RUTAS', {}).get('steam', r"C:\Program Files (x86)\Steam\steam.exe")
        self.ent_steam.insert(0, steam_path)
        self.ent_steam.pack(fill="x", padx=15, pady=2)
        btn_steam_frame = tk.Frame(frame_steam, bg=COLOR_BG)
        btn_steam_frame.pack(fill="x", padx=15, pady=(5, 10))
        tk.Button(btn_steam_frame, text=self.t("button.save_steam"), bg=COLOR_CARD, fg=COLOR_SECONDARY, font=('Segoe UI', 9, 'bold'), relief="groove", command=self.guardar_rutas_interfaz).pack(side="left", fill="x", expand=True, padx=5)
        tk.Button(btn_steam_frame, text=self.t("button.start_steam"), bg="#0054a6", fg="#fff", font=('Segoe UI', 10, 'bold'), relief="flat", command=self.lanzar_steam).pack(side="left", fill="x", expand=True, padx=5)

        frame_ruta = ttk.LabelFrame(container, text=self.t("frame.launcher_path"), style="Card.TLabelframe")
        frame_ruta.pack(fill="x", padx=15, pady=5)
        self.ent_launcher = tk.Entry(frame_ruta, bg=COLOR_INPUT_BG, fg="#fff", borderwidth=0, font=('Segoe UI', 9))
        self.ent_launcher.pack(fill="x", padx=15, pady=(10,5))

        frame_coord = ttk.LabelFrame(container, text=self.t("frame.coordinates"), style="Card.TLabelframe")
        frame_coord.pack(fill="x", padx=15, pady=5)

        f1 = tk.Frame(frame_coord, bg=COLOR_BG); f1.pack(fill="x", padx=15, pady=5)
        tk.Label(f1, text="GAME 1 -> X:", bg=COLOR_BG, fg=COLOR_ACCENT, font=('Consolas', 10, 'bold'), width=12, anchor="w").pack(side="left")
        self.ent_g1_x = tk.Entry(f1, width=8, bg=COLOR_INPUT_BG, fg=COLOR_ACCENT, insertbackground=COLOR_ACCENT, borderwidth=0, font=('Consolas', 11, 'bold')); self.ent_g1_x.pack(side="left", padx=5)
        tk.Label(f1, text="Y:", bg=COLOR_BG, fg=COLOR_ACCENT, font=('Consolas', 10, 'bold')).pack(side="left", padx=(10,0))
        self.ent_g1_y = tk.Entry(f1, width=8, bg=COLOR_INPUT_BG, fg=COLOR_ACCENT, insertbackground=COLOR_ACCENT, borderwidth=0, font=('Consolas', 11, 'bold')); self.ent_g1_y.pack(side="left", padx=5)
        tk.Button(f1, text=self.t("button.capture"), bg=COLOR_CARD, fg="#fff", font=('Segoe UI', 8, 'bold'), relief="flat", command=lambda: self.iniciar_captura(self.ent_g1_x, self.ent_g1_y)).pack(side="right", padx=5)

        f2 = tk.Frame(frame_coord, bg=COLOR_BG); f2.pack(fill="x", padx=15, pady=5)
        tk.Label(f2, text="GAME 2 -> X:", bg=COLOR_BG, fg=COLOR_SECONDARY, font=('Consolas', 10, 'bold'), width=12, anchor="w").pack(side="left")
        self.ent_g2_x = tk.Entry(f2, width=8, bg=COLOR_INPUT_BG, fg=COLOR_SECONDARY, insertbackground=COLOR_ACCENT, borderwidth=0, font=('Consolas', 11, 'bold')); self.ent_g2_x.pack(side="left", padx=5)
        tk.Label(f2, text="Y:", bg=COLOR_BG, fg=COLOR_SECONDARY, font=('Consolas', 10, 'bold')).pack(side="left", padx=(10,0))
        self.ent_g2_y = tk.Entry(f2, width=8, bg=COLOR_INPUT_BG, fg=COLOR_SECONDARY, insertbackground=COLOR_ACCENT, borderwidth=0, font=('Consolas', 11, 'bold')); self.ent_g2_y.pack(side="left", padx=5)
        tk.Button(f2, text=self.t("button.capture"), bg=COLOR_CARD, fg="#fff", font=('Segoe UI', 8, 'bold'), relief="flat", command=lambda: self.iniciar_captura(self.ent_g2_x, self.ent_g2_y)).pack(side="right", padx=5)

        frame_extra = ttk.LabelFrame(container, text=self.t("frame.fine_tuning"), style="Card.TLabelframe")
        frame_extra.pack(fill="x", padx=15, pady=5)

        f3 = tk.Frame(frame_extra, bg=COLOR_BG); f3.pack(fill="x", padx=15, pady=5)
        tk.Label(f3, text=self.t("label.title_class"), bg=COLOR_BG, fg=COLOR_ACCENT, font=('Segoe UI', 9, 'bold'), width=16, anchor="w").pack(side="left")
        self.ent_titulo_launcher = tk.Entry(f3, bg=COLOR_INPUT_BG, fg="#fff", insertbackground=COLOR_ACCENT, borderwidth=0, font=('Segoe UI', 9))
        self.ent_titulo_launcher.pack(side="left", fill="x", expand=True, padx=5)
        tk.Label(frame_extra, text=self.t("label.launcher_hint"), bg=COLOR_BG, fg=COLOR_TEXT_OFF, font=('Segoe UI', 8, 'italic')).pack(anchor="w", padx=20)

        f5 = tk.Frame(frame_extra, bg=COLOR_BG); f5.pack(fill="x", padx=15, pady=5)
        tk.Label(f5, text=self.t("label.launcher_wait"), bg=COLOR_BG, fg=COLOR_ACCENT, font=('Segoe UI', 9, 'bold'), width=30, anchor="w").pack(side="left")
        self.ent_delay_pre_click = tk.Entry(f5, width=6, bg=COLOR_INPUT_BG, fg=COLOR_ACCENT, insertbackground=COLOR_ACCENT, borderwidth=0, font=('Consolas', 11, 'bold'))
        self.ent_delay_pre_click.pack(side="left", padx=5)

        f4 = tk.Frame(frame_extra, bg=COLOR_BG); f4.pack(fill="x", padx=15, pady=(0,10))
        tk.Label(f4, text=self.t("label.game_wait"), bg=COLOR_BG, fg=COLOR_ACCENT, font=('Segoe UI', 9, 'bold'), width=30, anchor="w").pack(side="left")
        self.ent_delay_launch = tk.Entry(f4, width=6, bg=COLOR_INPUT_BG, fg=COLOR_ACCENT, insertbackground=COLOR_ACCENT, borderwidth=0, font=('Consolas', 11, 'bold'))
        self.ent_delay_launch.pack(side="left", padx=5)

        frame_btn = tk.Frame(container, bg=COLOR_BG); frame_btn.pack(fill="x", padx=15, pady=15)
        tk.Button(frame_btn, text=self.t("button.save_launcher"), bg=COLOR_CARD, fg=COLOR_SECONDARY, font=('Segoe UI', 10, 'bold'), relief="groove", command=self.guardar_config_launcher).pack(side="left", fill="x", expand=True, padx=5)
        tk.Button(frame_btn, text=self.t("button.start_uia"), bg=COLOR_ACCENT, fg="#000", font=('Segoe UI', 11, 'bold'), relief="flat", activebackground=COLOR_SECONDARY, command=self.lanzar_game1_game2).pack(side="left", fill="x", expand=True, padx=5)

        self.cargar_config_launcher()

    def boton_de_panico(self):
        try:
            self.log_status(self.t("log.panic_started"))
            ejecutables = ["Mir4G.exe", "Mir4Launcher.exe", "Mir4GClient.exe", "Mir4Client.exe", "Mir4.exe", "Mir4S.exe", "Mir4-Win64-Shipping.exe", "Mir4G-Win64-Shipping.exe"]
            for exe in ejecutables:
                subprocess.run(f"taskkill /F /IM {exe} /T", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            for hwnd, bot in list(self.instancias_activas.items()):
                bot.stop()
            self.instancias_activas.clear()
            self.actualizar_tabla_visual()
            self.log_status(self.t("log.panic_finished"))

            popup = tk.Toplevel(self.root)
            popup.title(self.t("popup.panic_title"))
            popup.geometry("380x180")
            popup.configure(bg=COLOR_BG)
            popup.resizable(False, False)
            popup.transient(self.root)
            popup.grab_set()

            x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 190
            y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 90
            popup.geometry(f"+{x}+{y}")

            tk.Label(popup, text=self.t("popup.panic_header"), bg=COLOR_BG, fg=COLOR_CAPTURA, font=('Segoe UI', 14, 'bold')).pack(pady=(15, 5))
            tk.Label(popup, text=self.t("popup.panic_message"), bg=COLOR_BG, fg="#ffffff", font=('Segoe UI', 10)).pack(pady=10)
            btn_ok = tk.Button(popup, text=self.t("button.ok"), bg=COLOR_CARD, fg=COLOR_ACCENT, activebackground=COLOR_ACCENT, activeforeground="#000", font=('Segoe UI', 9, 'bold'), relief="groove", width=15, command=popup.destroy)
            btn_ok.pack(pady=(5, 10))

        except Exception as e:
            self.log_status(self.t("log.panic_error", error=e))

    def cerrar_ventanas_steam(self):
        nombres_proceso = {"steam.exe", "steamwebhelper.exe"}
        cerradas = 0

        def callback(hwnd, _):
            nonlocal cerradas
            if not win32gui.IsWindowVisible(hwnd):
                return True

            proceso = None
            try:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                proceso = win32api.OpenProcess(
                    win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ,
                    False,
                    pid,
                )
                ruta_proceso = win32process.GetModuleFileNameEx(proceso, 0)
                if os.path.basename(ruta_proceso).lower() in nombres_proceso:
                    win32api.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                    cerradas += 1
            except Exception:
                pass
            finally:
                if proceso:
                    win32api.CloseHandle(proceso)
            return True

        win32gui.EnumWindows(callback, None)
        self.log_status(self.t("log.steam_closed", count=cerradas))

    def esperar_mir4_y_cerrar_steam(self, ventanas_anteriores):
        limite = time.time() + 120
        while time.time() < limite:
            ventanas_actuales = set(obtener_ventanas_mir4())
            if ventanas_actuales - ventanas_anteriores:
                self.cerrar_ventanas_steam()
                return
            time.sleep(0.5)
        self.log_status(self.t("log.mir4_timeout"))

    def iniciar_captura(self, entry_x, entry_y):
        if self.capturando_activo: return
        self.capturando_activo = True
        self.log_status(self.t("log.capture_started"))
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
                    self.root.after(0, self._terminar_captura, entry_x, entry_y, "0", "0", original_bg_x, original_bg_y, False, self.t("capture.outside_window"))
                    return
            else:
                self.root.after(0, self._terminar_captura, entry_x, entry_y, str(screen_x), str(screen_y), original_bg_x, original_bg_y, False, self.t("log.launcher_not_found"))
        except Exception as e:
            self.root.after(0, self._terminar_captura, entry_x, entry_y, "0", "0", original_bg_x, original_bg_y, False, self.t("log.error", error=e))

    def _actualizar_texto_captura(self, entry_x, entry_y, x, y):
        entry_x.delete(0, tk.END); entry_x.insert(0, str(x))
        entry_y.delete(0, tk.END); entry_y.insert(0, str(y))

    def _terminar_captura(self, entry_x, entry_y, x, y, bg_x, bg_y, exito, msg_extra=""):
        self.capturando_activo = False
        entry_x.configure(bg=bg_x); entry_y.configure(bg=bg_y)
        if exito:
            entry_x.delete(0, tk.END); entry_x.insert(0, x)
            entry_y.delete(0, tk.END); entry_y.insert(0, y)
            self.log_status(self.t("log.coordinates_captured", x=x, y=y))
        else:
            self.log_status(self.t("log.capture_failed", message=msg_extra))

    def guardar_rutas_interfaz(self):
        if 'RUTAS' not in self.config: self.config['RUTAS'] = {}
        self.config['RUTAS']['steam'] = self.ent_steam.get()
        self.guardar_config(); self.log_status(self.t("log.steam_updated"))

    def lanzar_steam(self):
        ruta = self.ent_steam.get()
        if os.path.exists(ruta):
            try:
                ventanas_anteriores = set(obtener_ventanas_mir4())
                subprocess.Popen([ruta, "-applaunch", "1623660"])
                threading.Thread(
                    target=self.esperar_mir4_y_cerrar_steam,
                    args=(ventanas_anteriores,),
                    daemon=True,
                ).start()
                self.log_status(self.t("log.steam_request"))
            except Exception as e: self.log_status(self.t("log.steam_error", error=e))
        else: self.log_status(self.t("log.steam_missing"))

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
            self.log_status(self.t("log.coordinates_error"))
            return

        self.guardar_config()
        self.log_status(self.t("log.launcher_saved"))

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
            self.log_status(self.t("log.anti_ban_missing"))
            self.mostrar_alerta(self.t("popup.critical_error"), self.t("popup.critical_error_message"), es_error=True)
            return
        try:
            ruta = self.ent_launcher.get()
            g1_x = int(self.ent_g1_x.get()); g1_y = int(self.ent_g1_y.get())
            g2_x = int(self.ent_g2_x.get()); g2_y = int(self.ent_g2_y.get())
            titulo_launcher = self.ent_titulo_launcher.get()
            delay_pre_click = int(float(self.ent_delay_pre_click.get()))
            delay = int(float(self.ent_delay_launch.get()))
            if not os.path.exists(ruta): self.log_status(self.t("log.invalid_path")); return
            self.log_status(self.t("log.safe_sequence"))
            threading.Thread(target=self._hilo_lanzamiento_uia, args=(ruta, g1_x, g1_y, g2_x, g2_y, titulo_launcher, delay_pre_click, delay), daemon=True).start()
        except ValueError: self.log_status(self.t("log.coordinates_error"))
        except Exception as e: self.log_status(self.t("log.error", error=e))

    def uia_click(self, hwnd, target_x, target_y):
        try:
            abs_x, abs_y = win32gui.ClientToScreen(hwnd, (target_x, target_y))
            desktop = Desktop(backend="uia"); launcher = desktop.window(handle=hwnd)
            self.log_status(self.t("log.uia_scan", x=abs_x, y=abs_y))

            buttons = launcher.descendants(control_type="Button")
            for btn in buttons:
                rect = btn.rectangle()
                if rect.left <= abs_x <= rect.right and rect.top <= abs_y <= rect.bottom:
                    if btn.is_enabled():
                        self.log_status(self.t("log.uia_button"))
                        btn.invoke()
                        return True

            self.log_status(self.t("log.uia_generic"))
            controls = launcher.descendants()
            for ctrl in controls:
                try:
                    rect = ctrl.rectangle()
                    if rect.left <= abs_x <= rect.right and rect.top <= abs_y <= rect.bottom:
                        if ctrl.is_enabled():
                            try:
                                self.log_status(self.t("log.uia_control", class_name=ctrl.element_info.class_name))
                                ctrl.invoke()
                                return True
                            except Exception:
                                pass
                except Exception:
                    continue

            self.log_status(self.t("log.uia_not_found"))
            return False
        except Exception as e:
            self.log_status(self.t("log.uia_error", error=e))
            return False

    def _hilo_lanzamiento_uia(self, ruta, g1_x, g1_y, g2_x, g2_y, titulo_launcher, delay_pre_click, delay):
        try:
            self.log_status(self.t("log.launcher_open"))
            subprocess.Popen(ruta)

            self.log_status(self.t("log.launcher_search", title=titulo_launcher))
            hwnd_launcher = esperar_ventana(titulo_launcher, timeout=30)
            if not hwnd_launcher:
                self.log_status(self.t("log.launcher_not_found"))
                return

            self.log_status(self.t("log.window_found", hwnd=hwnd_launcher))
            self.log_status(self.t("log.wait_render", seconds=delay_pre_click))
            time.sleep(delay_pre_click)

            self.log_status(self.t("log.press_game", game="Game 1"))
            if not self.uia_click(hwnd_launcher, g1_x, g1_y): return

            self.log_status(self.t("log.wait_game", game="Game 1"))
            if not esperar_ventana("Mir4G", timeout=90):
                self.log_status(self.t("log.game_slow", game="Game 1", next_game="Game 2"))

            self.log_status(self.t("log.wait_seconds", seconds=delay))
            time.sleep(delay)

            hwnd_launcher = esperar_ventana(titulo_launcher, timeout=15)
            if not hwnd_launcher:
                self.log_status(self.t("log.game_launcher_missing", game="Game 2"))
                return

            self.log_status(self.t("log.press_game", game="Game 2"))
            if not self.uia_click(hwnd_launcher, g2_x, g2_y): return

            self.log_status(self.t("log.wait_game", game="Game 2"))
            if esperar_ventana("Mir4G", timeout=90):
                self.log_status(self.t("log.deploy_complete"))
            else:
                self.log_status(self.t("log.deploy_timeout", game="Game 2"))

        except Exception as e:
            self.log_status(self.t("log.launcher_error", error=e))

    # --- FUNCIÓN DE GUARDADO JSON ---
    def guardar_config(self):
        config_dir = os.path.dirname(self.config_file) or "."
        temp_path = None
        try:
            fd, temp_path = tempfile.mkstemp(prefix=".config_", suffix=".tmp", dir=config_dir)
            with os.fdopen(fd, 'w', encoding='utf-8') as configfile:
                json.dump(self.config, configfile, indent=4, ensure_ascii=False)
                configfile.flush()
                os.fsync(configfile.fileno())

            if os.path.exists(self.config_file):
                shutil.copy2(self.config_file, self.config_file + ".bak")
            os.replace(temp_path, self.config_file)
            temp_path = None
        finally:
            if temp_path and os.path.exists(temp_path):
                os.unlink(temp_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
