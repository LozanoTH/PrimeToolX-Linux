# PrimeToolX Linux — fork nativo

Versión nativa para **Linux** (sin Wine) de PrimeToolX 26.7.2: herramienta de
servicio GSM para teléfonos MediaTek y Qualcomm/Samsung, construida sobre
motores de código abierto.

## Qué hace

- **MediaTek**: borrado de `frp` / `persistent` por modelo, usando el motor
  **mtkclient** nativo (el mismo que la app original invoca internamente).
- **Qualcomm/Samsung**: operación en modo EDL con cargadores Firehose vía la
  herramienta **edl** nativa.
- Extrae automáticamente los DA/loaders `.prime` (contenedores GSM_PRIME) a
  `.bin`/`.elf` utilizables, sin modificar los archivos originales.
- Los JSON de modelos de los principales fabricantes se incluyen en `data/`.

> **Aviso legal**: la app original **PrimeToolX** es software propietario de
> GSM Prime. Este proyecto es un *rescatador de funcionalidad*: reimplementa
> su interfaz en Python 3 + customtkinter y delega el trabajo de bajo nivel en
> motores GPLv3. **No se incluye ni redistribuye ningún binario propietario**
> (`.exe`, `.prime`, `.elf`, DA) de la app original.

## Requisitos

- Linux (probado en Arch) + Python 3.10+
- Paquetes del sistema: `tk` + `libusb` + `usbutils`
- Rutas de motores externos (configurables por variables de entorno):
  - `/opt/mtkclient/mtk.py` (mtkclient) con su venv `/opt/mtkvenv`
  - `/opt/edl/edl.py` (herramienta edl) con python del proyecto

## Instalación

Automatizado:

```bash
cd PrimeToolX-Linux
./scripts/setup.sh       # instala sistema + venv + motores + udev
```

Manual:

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt

# motores de código abierto (una vez):
sudo python3 -m venv /opt/mtkvenv
sudo /opt/mtkvenv/bin/pip install pyusb pycryptodomex
sudo git clone --depth 1 https://github.com/bkerler/mtkclient /opt/mtkclient
sudo git clone --depth 1 https://github.com/bkerler/edl /opt/edl
```

Opcional — **datos propietarios**: para operar sobre modelos con DA propio
(no incluidos por defecto), coloca la carpeta `_internal` de PrimeToolX en
`~/Descargas/PrimeToolX26.7.2/_internal`. La app la usará para localizar DA.

## Ejecutar

```bash
./run.sh            # lanza la interfaz
./main.py           # equivalente
```

## Configuración

Las rutas de los motores se pueden redefinir sin tocar el código:

```bash
export PRIMETOOLX_MTK_PYTHON=/usr/bin/python3
export PRIMETOOLX_MTK_SCRIPT=/opt/mtkclient/mtk.py
export PRIMETOOLX_EDL_PYTHON=/usr/bin/python3
export PRIMETOOLX_EDL_SCRIPT=/opt/edl/edl.py
./run.sh
```

## Permisos USB (udev)

```bash
sudo tee /etc/udev/rules.d/99-primetoolx.rules <<'EOF'
SUBSYSTEM=="usb", ATTR{idVendor}=="0e8d", MODE="0666"
SUBSYSTEM=="usb", ATTR{idVendor}=="05c6", MODE="0666"
EOF
sudo udevadm control --reload-rules
```

En Arch descarga el driver `cdc_acm` si captura el preloader:
`sudo modprobe -r cdc_acm`.

## Estructura

```
PrimeToolX-Linux/
├── main.py               # punto de entrada
├── app/                  # interfaz (paneles: inicio, mediatek, qualcomm, drivers)
├── core/                 # núcleo: config (JSON+DA) y engine (mtkclient/edl)
├── data/                 # JSON de modelos (MediaTek y Qualcomm/Samsung)
├── scripts/setup.sh      # instalación automática
└── cache/                # DA extraídos en tiempo de ejecución (gitignored)
```

## Créditos

- **GSM Prime** — app original y base de datos de modelos de la que se extrajo `data/`.
- **B. Kerler** — [mtkclient](https://github.com/bkerler/mtkclient) y [edl](https://github.com/bkerler/edl), ambos GPLv3.

## Licencia

GPLv3. Ver `LICENSE`.