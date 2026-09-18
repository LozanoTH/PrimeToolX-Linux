import customtkinter as ctk

from core.engine import MotorMtk, MTK_PYTHON, MTK_SCRIPT

COLOR_FONDO = "#21201e"
COLOR_ACTIVO = "#34322f"

class PanelInicio(ctk.CTkFrame):
    """Pantalla de inicio: estado del entorno, motor mtkclient y accesos rapidos."""

    def __init__(self, parent):
        super().__init__(parent, fg_color=COLOR_FONDO)
        self.app = self  # placeholder

        self.label_titulo = ctk.CTkLabel(self, text="PrimeToolX Linux", font=("Consolas", 26, "bold"))
        self.label_titulo.pack(pady=(40, 4))

        self.label_sub = ctk.CTkLabel(self, text="Fork nativo para Linux  •  26.7.2  •  Comunidad GSM", font=("Consolas", 13), text_color="#717171")
        self.label_sub.pack()

        self.frame_estado = ctk.CTkFrame(self, width=760, height=200, fg_color="#16191c", corner_radius=10)
        self.frame_estado.pack(pady=30, padx=30, fill="both", expand=True)

        texto = self._estado_texto()
        self.label_estado = ctk.CTkLabel(self.frame_estado, text=texto, justify="left", anchor="w",
                                         font=("Consolas", 13), text_color="#c9ced3")
        self.label_estado.pack(padx=20, pady=20)

        self.boton_herramientas = ctk.CTkButton(self, text="Abrir Herramientas", width=220, height=42,
                                                 fg_color="#0060b0", hover_color="#0b7ad0",
                                                 font=("Consolas", 14), command=self._abrir)
        self.boton_herramientas.pack(pady=(0, 8))

        sp = ctk.CTkFrame(self, height=1, fg_color="#333333")
        sp.pack(fill="x", padx=200, pady=10)

        self.label_notas = ctk.CTkLabel(self,
            text="Operaciones via mtkclient nativo (MediaTek) sin Wine.\n"
                 "Render por customtkinter. Datos de modelos: base de datos original PrimeToolX.",
            font=("Consolas", 11), text_color="#9aa0a5", justify="center")
        self.label_notas.pack(side="bottom", pady=18)

    def _estado_texto(self):
        m = MotorMtk()
        lineas = []
        lineas.append("MOTOR MTKCLIENT")
        lineas.append("  mtkclient : " + ("DISPONIBLE" if m.accion_disponible() else "NO INSTALADO"))
        lineas.append("  script    : " + MTK_SCRIPT)
        lineas.append("  python    : " + MTK_PYTHON)
        return "\n".join(lineas)

    def _abrir(self):
        from app.principal import PrimeToolXLinux
        root = self.after
        # Acceso al padre real: navega hacia arriba
        w = self
        while w is not None and not isinstance(w, PrimeToolXLinux):
            w = w.master
        if w is not None:
            w.abrir_ventana("herramientas")