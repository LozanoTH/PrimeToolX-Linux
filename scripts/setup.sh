#!/usr/bin/env bash
# Instalación de PrimeToolX Linux (Arch / Debian / Fedora)
set -e

echo "==> Instalando dependencias del sistema..."
if command -v pacman >/dev/null 2>&1; then
    sudo pacman -S --needed --noconfirm python tk libusb usbutils python-pyusb
elif command -v apt-get >/dev/null 2>&1; then
    sudo apt-get install -y python3 python3-venv python3-tk libusb-1.0-0 usbutils
elif command -v dnf >/dev/null 2>&1; then
    sudo dnf install -y python3 python3-tkinter libusb usbutils
fi

echo "==> Entorno virtual del proyecto..."
python3 -m venv .venv
./.venv/bin/pip install --upgrade pip
./.venv/bin/pip install -r requirements.txt

echo "==> Motores de código abierto (mtkclient / edl)..."
if [ ! -d /opt/mtkclient ]; then
    sudo git clone --depth 1 https://github.com/bkerler/mtkclient /opt/mtkclient
else
    echo "    /opt/mtkclient ya existe"
fi

if [ ! -d /opt/edl ]; then
    sudo git clone --depth 1 https://github.com/bkerler/edl /opt/edl
else
    echo "    /opt/edl ya existe"
fi

# mtkclient en su propio venv (usa USB con libusb)
sudo python3 -m venv /opt/mtkvenv
sudo /opt/mtkvenv/bin/pip install --upgrade pip
sudo /opt/mtkvenv/bin/pip install pyusb pycryptodomex

echo "==> Permisos USB (udev):"
sudo tee /etc/udev/rules.d/99-primetoolx.rules <<'EOF'
SUBSYSTEM=="usb", ATTR{idVendor}=="0e8d", MODE="0666", GROUP="users"
SUBSYSTEM=="usb", ATTR{idVendor}=="05c6", MODE="0666", GROUP="users"
SUBSYSTEM=="usb", ATTR{idVendor}=="18d1", MODE="0666", GROUP="users"
EOF
sudo udevadm control --reload-rules

echo ""
echo "Listo. Para modelos/DA propietarios, coloca la carpeta _internal"
echo "de PrimeToolX en ~/Descargas/PrimeToolX26.7.2/_internal (opcional)."
echo "Ejecuta:  ./run.sh"