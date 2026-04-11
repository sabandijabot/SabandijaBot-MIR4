# incrementar_version.py
import os

archivo_ver = "version.txt"
if os.path.exists(archivo_ver):
    with open(archivo_ver, "r") as f:
        try:
            version = int(f.read().strip())
        except:
            version = 0
else:
    version = 0

nueva_version = version + 1
with open(archivo_ver, "w") as f:
    f.write(str(nueva_version))

print(f">>> Versión actualizada a: 2.0.{nueva_version}")