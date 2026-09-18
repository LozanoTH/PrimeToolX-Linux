import os
import subprocess
import sys
import customtkinter as ctk

from core import config
from core.engine import MTK_PYTHON, MTK_SCRIPT, EDL_PYTHON, EDL_SCRIPT

COLOR_FONDO = "#21201e"

class PanelDrivers(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLOR_FONDO)

        self.label_titulo = ctk.CTkLabel(self, text="Drivers y entorno Linux", font=("Consolas", 20, "bold"))
        self.label_titulo.pack(pady=(30, 6))

        self.label_sub = ctk.CTkLabel(self, text="En Linux no se instalan drivers .inf: se usan reglas udev y librerías libusb",
                                      font=("Consolas", 12), text_color="#9aa0a5")
        self.label_sub.pack()

        self.frame_estado = ctk.CTkFrame(self, width=800, fg_color="#16191c", corner_radius=10)
        self.frame_estado.pack(pady=20, padx=40, fill="both", expand=True)

        self.label_check = ctk.CTkLabel(self.frame_estado, text=self._chequear(), justify="left", anchor="w",
                                        font=("Consolas", 12), text_color="#c9ced3")
        self.label_check.pack(padx=18, pady=16, fill="both", expand=True)

        self.boton_reglas = ctk.CTkButton(self, text="Instalar reglas udev (MediaTek/Qualcomm)", width=320, height=40,
                                          fg_color="#0060b0", hover_color="#0b7ad0", font=("Consolas", 13),
                                          command=self._instalar_udev)
        self.boton_reglas.pack(pady=(0, 10))

        self.label_udev = ctk.CTkLabel(self, text="", font=("Consolas", 12), text_color="#9fe870")
        self.label_udev.pack()

    def _chequear(self):
        lineas = []
        lineas.append("COMPROBACIÓN DEL ENTORNO")
        lineas.append("  mtkclient motor : " + ("OK" if os.path.exists(MTK_SCRIPT) else "FALTA") + f"  ({MTK_SCRIPT})")
        lineas.append("  mtkclient python: " + ("OK" if os.path.exists(MTK_PYTHON) else "FALTA") + f"  ({MTK_PYTHON})")
        lineas.append("  edl (Qualcomm)  : " + ("OK" if os.path.exists(EDL_SCRIPT) else "FALTA") + f"  ({EDL_SCRIPT})")
        lineas.append("  libusb Python   : " + ("OK" if self._pyok("import usb") else "FALTA"))
        lineas.append("  customtkinter   : " + ("OK" if self._pyok("import customtkinter") else "FALTA"))
        lineas.append("")
        lineas.append("  Paquetes Arch (pacman):")
        lineas.append("    libusb, usbutils, gtk3, python-pyusb, tk")
        lineas.append("")
        lineas.append("  Fuente de modelos: " + config.ruta_datos())
        lineas.append("  Fuente de DA     : " + (config.localizar_app_original() or "no encontrada (opcional)"))
        return "\n".join(lineas)

    def _pyok(self, codigo):
        try:
            r = subprocess.run([sys.executable, "-c", codigo],
                               capture_output=True)
            return r.returncode == 0
        except Exception:
            return False

    def _instalar_udev(self):
        reglas = (
            'SUBSYSTEM=="usb", ATTR{idVendor}=="0e8d", MODE="0666", GROUP="users"\n'
            'SUBSYSTEM=="usb", ATTR{idVendor}=="05c6", MODE="0666", GROUP="users"\n'
            'SUBSYSTEM=="usb", ATTR{idVendor}=="18d1", MODE="0666", GROUP="users"\n'
            'SUBSYSTEM=="usb", ATTR{idVendor}=="12d1", MODE="0666", GROUP="users"\n'
        )
        try:
            ruta = "/etc/udev/rules.d/99-primetoolx.rules"
            subprocess.run(["sudo", "tee", ruta], input=reglas.encode(), check=False)
            subprocess.run(["sudo", "udevadm", "control", "--reload-rules"], check=False)
            self.label_udev.configure(text="Reglas udev instaladas y recargadas ✔", text_color="#9fe870")
        except Exception as e:
            self.label_udev.configure(text=f"Error: {e}", text_color="#e07070")