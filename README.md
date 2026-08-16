
```markdown
# SabandijaBot-MIR4 🐍

Automatización y gestión de instancias para MIR4 (Reptil Edition).

## 🚀 Características
* **Soporte Multicuenta:** Control de múltiples ventanas del juego de forma independiente.
* **Modos de Operación:** Misión Q (Auto), Farma EXP (AFK) con opción de Ultimate, y Summon Boss.
* **Despliegue Seguro:** Lanzamiento de clientes mediante UIAutomation para evitar bloqueos.
* **Gestión de Perfiles:** Guarda y carga configuraciones personalizadas para cada personaje.
* **Ajuste de Ventanas:** Ordena automáticamente las pantallas del juego en un grid ordenado.
* **Ayuda de Modos:** Muestra una explicación al pasar el mouse sobre Misión Q, Farma EXP o Summon Boss.

## 🛠️ Requisitos
Necesitas tener instalado Python 3.12+ y las dependencias del proyecto:
```bash
pip install -r requirements.txt

```

## 📦 Compilación a ejecutable (.exe)

Para generar el archivo ejecutable independiente:

```bash
py -m PyInstaller --noconsole --onefile --uac-admin --icon=sabandijab0tico.ico --name SabandijaBot MisionQQ4.py

```

## ⚙️ Uso

1. Ejecuta `MisionQQ4.py` para las pruebas. El `.exe` compilado solicita permisos de **Administrador** al iniciarse.
2. Configura las rutas de tu launcher y las coordenadas de inicio en la pestaña **Despliegue**.
3. Selecciona la ventana del juego, define el modo de bot y haz clic en **Iniciar bot**.

### Idioma

El selector **Idioma / Language** está disponible en la cabecera. Español (`es`) es el idioma predeterminado y también se puede seleccionar **English**. El idioma se guarda en `config.json` mediante la clave `IDIOMA`; al cambiarlo, el bot se reinicia automáticamente para aplicar el idioma a toda la interfaz.
