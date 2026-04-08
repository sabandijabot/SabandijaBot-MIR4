# 🐍 SABANDIJA B0T - REPTIL EDITION

![Status](https://img.shields.io/badge/Status-Active-39ff14?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-2.0.0--reptil-ccff00?style=for-the-badge)

Macro especializado para la automatización y optimización de tareas en el ecosistema de **MIR4**. Esta versión "Reptil" ha sido rediseñada con una interfaz neón y lógica mejorada para el manejo de instancias múltiples.

## 🚀 Funcionalidades Principales

* **MISIÓN Q (AUTO):** Ciclo automatizado para completar misiones rápidas de manera eficiente.
* **FARMA EXP (AFK):** Sistema de rotación de objetivos y ataque básico para leveleo desatendido.
* **LANZAR ULTI [R]:** Opción integrada exclusivamente para el modo Farma, permitiendo el uso de habilidades definitivas según el delay configurado.
* **RECTIL LAYOUT:** Herramienta de arquitectura de ventanas para organizar múltiples instancias de MIR4 en cascada automáticamente.

## 🛠️ Requisitos Técnicos

* **Sistema Operativo:** Windows 10/11 (Se requiere ejecutar como Administrador para interactuar con la ventana del juego).
* **Lenguaje:** Python 3.10+.
* **Librerías:** `tkinter`, `pywin32`.

## 📥 Instalación y Uso

### Para Usuarios (Ejecutable)
1.  Dirígete a la sección de **[RELEASES](https://github.com/sabandijabot/SabandijaBot-MIR4/releases)** de este repositorio.
2.  Descarga el archivo `MisionQQ.exe`.
3.  Ejecuta el bot, selecciona la ventana de MIR4 y configura tu modo de caza.

### Para Desarrolladores (Código Fuente)
Si deseas modificar el comportamiento del bot para **IDYNSOFT C.A.**:

1.  Clona el repositorio:
    ```bash
    git clone [https://github.com/sabandijabot/SabandijaBot-MIR4.git](https://github.com/sabandijabot/SabandijaBot-MIR4.git)
    ```
2.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
3.  Ejecuta el script:
    ```bash
    python MisionQQ.py
    ```

## ⚠️ Advertencia de Seguridad
Este software es una herramienta de automatización basada en el envío de mensajes de red nativos de Windows (`PostMessage`). Úsalo bajo tu propia responsabilidad y asegúrate de cumplir con los términos de servicio del juego para evitar sanciones en tu cuenta.
