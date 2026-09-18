import customtkinter as ctk

from core import config
from app.panel_qualcomm import PanelQualcomm
from app.panel_mediatek import PanelMediaTek

COLOR_FONDO = "#21201e"
COLOR_ACTIVO = "#34322f"

class PanelDispositivos(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLOR_FONDO)

        self.frame_superior = ctk.CTkFrame(self, height=50, fg_color=COLOR_FONDO)
        self.frame_superior.pack(side="top", fill="x", pady=(10, 0))
        self.frame_superior.pack_propagate(False)

        self.boton_qualcomm = ctk.CTkButton(self.frame_superior, text="Qualcomm", font=("Consolas", 13),
                                            width=130, height=30, hover_color="#2C2A27", corner_radius=5,
                                            command=self.abrir_qualcomm)
        self.boton_qualcomm.pack(side="left", padx=(10, 5))

        self.boton_mediatek = ctk.CTkButton(self.frame_superior, text="MediaTek", font=("Consolas", 13),
                                            width=120, height=30, hover_color="#2C2A27", corner_radius=5,
                                            command=self.abrir_mediatek)
        self.boton_mediatek.pack(side="left", padx=5)

        self.frame_contenido = ctk.CTkFrame(self, fg_color=COLOR_FONDO)
        self.frame_contenido.pack(side="left", pady=(0, 10), expand=True, fill="both")
        self.frame_contenido.pack_propagate(False)

        self.abrir_mediatek()

    def ocultar(self):
        for w in self.frame_contenido.winfo_children():
            w.destroy()

    def resaltar(self, activo):
        self.boton_qualcomm.configure(fg_color=COLOR_ACTIVO if activo == "qc" else COLOR_FONDO)
        self.boton_mediatek.configure(fg_color=COLOR_ACTIVO if activo == "mtk" else COLOR_FONDO)

    def abrir_qualcomm(self):
        self.ocultar()
        p = PanelQualcomm(self.frame_contenido)
        p.pack(expand=True, fill="both")
        self.resaltar("qc")

    def abrir_mediatek(self):
        self.ocultar()
        p = PanelMediaTek(self.frame_contenido)
        p.pack(expand=True, fill="both")
        self.resaltar("mtk")