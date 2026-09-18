import os
import json
import shutil

APP_ORIGEN = os.path.expanduser("~/Descargas/PrimeToolX26.7.2/_internal")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def localizar_app_original():
    """Localiza la carpeta _internal de la app original (no la descarga, solo la referencia)."""
    for ruta in [APP_ORIGEN,
                 "/opt/PrimeToolX26.7.2/_internal",
                 "/opt/PrimeToolX/_internal"]:
        if os.path.isdir(ruta):
            return ruta
    return None

def ruta_datos():
    """Carpeta de datos del repo (JSON de modelos)."""
    return os.path.join(BASE_DIR, "data")

def ruta_cache():
    """Carpeta donde dejamos los DA extraídos (copias de trabajo)."""
    cache = os.path.join(BASE_DIR, "cache", "da")
    os.makedirs(cache, exist_ok=True)
    return cache

def cargar_modelos_mtk():
    for ruta in [os.path.join(ruta_datos(), "modelos_mediatek.json"),
                 os.path.join(localizar_app_original() or "", "mobs", "data", "modelos_mediatek.json")]:
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as f:
                return json.load(f)
    return {}

def cargar_modelos_samsung():
    for ruta in [os.path.join(ruta_datos(), "modelos_samsung.json"),
                 os.path.join(localizar_app_original() or "", "mobs", "data", "modelos_samsung.json")]:
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as f:
                return json.load(f)
    return {}

def buscar_da_en_app(nombre_base):
    """Busca un archivo DA (.bin, .prime) o loader por nombre en carpetas de la app original."""
    orig = localizar_app_original()
    nombres = []
    if nombre_base.lower().endswith((".bin", ".prime", ".elf")):
        nombres = [nombre_base]
    else:
        nombres = [nombre_base + ".bin", nombre_base + ".prime", nombre_base + ".elf"]

    carpetas = []
    raiz_mobs = os.path.join(orig, "mobs")
    for root, dirs, files in os.walk(raiz_mobs):
        if os.path.basename(root) in ("DA", "mtk_loads", "loaders", "scripts"):
            carpetas.append(root)
    carpetas.append(os.path.join(raiz_mobs, "mtk_loads"))
    carpetas.append(os.path.join(orig, "edl_sb", "loaders"))

    for carpeta in set(carpetas):
        for nom in nombres:
            ruta = os.path.join(carpeta, nom)
            if os.path.isfile(ruta):
                return ruta
    return None

def extraer_da_prim(e):
    """Convierte un .prime de PrimeTool en un archivo usable (DA .bin o ELF) si hace falta."""
    destino = os.path.join(ruta_cache(), os.path.basename(e))
    if not os.path.exists(destino):
        data = open(e, 'rb').read()
        marcador = data.find(b'MTK_DOWNLOAD_AGENT')
        if marcador > 0:
            data = data[marcador:]
        elif data[:4] == b'\x7fELF':
            pass  # ya es ELF directo
        else:
            # .prime de EDL: el ELF suele empezar con 0x7f ELF poco después del prefijo
            idx = data.find(b'\x7fELF')
            if idx > 0:
                data = data[idx:]
        with open(destino, 'wb') as f:
            f.write(data)
    return destino if os.path.exists(destino) else e

def preparar_loader(nombre_loader):
    """Devuelve la ruta del loader (DA/ELF) lista para usarse, o None."""
    if not nombre_loader or str(nombre_loader).lower() == "off":
        return None
    ruta = buscar_da_en_app(nombre_loader)
    if ruta is None:
        return None
    if ruta.lower().endswith((".prime",)):
        return extraer_da_prim(ruta)
    if ruta.lower().endswith((".bin", ".elf")):
        destino = os.path.join(ruta_cache(), os.path.basename(ruta))
        if not os.path.exists(destino):
            shutil.copy(ruta, destino)
        return destino
    return ruta