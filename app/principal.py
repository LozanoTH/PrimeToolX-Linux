import customtkinter as ctk
from app.panel_inicio import PanelInicio
from app.panel_devices import PanelDispositivos
from app.panel_drivers import PanelDrivers

COLOR_FONDO = "#21201e"
COLOR_ACTIVO = "#34322f"
COLOR_HOVER = "#2C2A27"

class PrimeToolXLinux(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1150x680")
        self.minsize(900, 560)
        self.resizable(True, True)
        self.title("PrimeToolX Linux 26.7.2")
        self.configure(fg_color=COLOR_FONDO)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_lateral = ctk.CTkFrame(self, width=80, fg_color=COLOR_FONDO)
        self.frame_lateral.grid(row=0, column=0, sticky="nsw")
        self.frame_lateral.grid_propagate(False)
        self.frame_lateral.configure(height=680)

        self.frame_ventanas = ctk.CTkFrame(self, fg_color=COLOR_FONDO)
        self.frame_ventanas.grid(row=0, column=1, sticky="nsew")
        self.frame_ventanas.grid_propagate(False)
        self.frame_ventanas.configure(width=1070, height=680)

        self.boton_inicio = ctk.CTkButton(self.frame_lateral, text="Inicio", width=60, height=45,
                                          fg_color=COLOR_FONDO, hover_color=COLOR_HOVER,
                                          command=lambda: self.abrir_ventana("inicio"))
        self.boton_inicio.pack(side="top", pady=10)

        self.boton_herramienta = ctk.CTkButton(self.frame_lateral, text="Herramientas", width=60, height=45,
                                               fg_color=COLOR_FONDO, hover_color=COLOR_HOVER,
                                               command=lambda: self.abrir_ventana("herramientas"))
        self.boton_herramienta.pack(side="top", pady=0)

        self.boton_drivers = ctk.CTkButton(self.frame_lateral, text="Drivers", width=60, height=45,
                                            fg_color=COLOR_FONDO, hover_color=COLOR_HOVER,
                                            command=lambda: self.abrir_ventana("drivers"))
        self.boton_drivers.pack(side="top", pady=10)

        self.paneles = {
            "inicio": PanelInicio(self.frame_ventanas),
            "herramientas": PanelDispositivos(self.frame_ventanas),
            "drivers": PanelDrivers(self.frame_ventanas),
        }

        self.abrir_ventana("herramientas")

    def cambiar_boton(self, activo):
        for nombre, boton in [("inicio", self.boton_inicio),
                              ("herramientas", self.boton_herramienta),
                              ("drivers", self.boton_drivers)]:
            boton.configure(fg_color=COLOR_ACTIVO if activo == nombre else COLOR_FONDO)

    def abrir_ventana(self, nombre):
        for widget in self.frame_ventanas.winfo_children():
            widget.pack_forget()
        self.paneles[nombre].pack(expand=True, fill="both")
        self.cambiar_boton(nombre)