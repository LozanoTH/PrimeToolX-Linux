import threading
import customtkinter as ctk

from core import config
from core.engine import MotorEDL

COLOR_FONDO = "#21201e"
COLOR_SUB = "#16191c"
COLOR_SUB2 = "#12151a"

class PanelQualcomm(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLOR_FONDO)
        self.db = config.cargar_modelos_samsung()
        self.marca_actual = None
        self.modelo_actual = None
        self.motor = MotorEDL(self._log, self._status)

        self.frame_botones = ctk.CTkFrame(self, fg_color=COLOR_FONDO)
        self.frame_botones.pack(side="top", fill="x", padx=10, pady=(4, 4))

        self.botones_marca = {}
        for marca in self.db.keys():
            b = ctk.CTkButton(self.frame_botones, text=marca.capitalize(), width=100, height=30,
                              font=("Consolas", 13), fg_color="#161a1e", hover_color="#21201e",
                              corner_radius=5, command=lambda m=marca: self.seleccionar_marca(m))
            b.pack(side="left", padx=(0, 6), pady=4)
            self.botones_marca[marca] = b

        self.frame_mitad = ctk.CTkFrame(self, fg_color=COLOR_FONDO)
        self.frame_mitad.pack(expand=True, fill="both", padx=10, pady=(0, 8))

        self.frame_lista = ctk.CTkFrame(self.frame_mitad, width=430, fg_color=COLOR_SUB, corner_radius=8)
        self.frame_lista.pack(side="left", fill="both", expand=True)

        self.label_marca = ctk.CTkLabel(self.frame_lista, text="Selecciona una marca", font=("Consolas", 14, "bold"), text_color="#c9ced3")
        self.label_marca.pack(pady=6)

        self.entrada_buscar = ctk.CTkEntry(self.frame_lista, placeholder_text="Buscar modelo...", font=("Consolas", 12))
        self.entrada_buscar.pack(fill="x", padx=8, pady=(0, 4))
        self.entrada_buscar.bind("<KeyRelease>", lambda e: self._filtrar())

        self.scroll = ctk.CTkScrollableFrame(self.frame_lista, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=6, pady=(0, 6))

        self.frame_detalle = ctk.CTkFrame(self.frame_mitad, width=600, fg_color=COLOR_SUB2, corner_radius=8)
        self.frame_detalle.pack(side="right", fill="both", expand=True)

        self.label_detalle = ctk.CTkLabel(self.frame_detalle, text="Selecciona un modelo de la lista",
                                           font=("Consolas", 13), text_color="#c9ced3", justify="left", anchor="nw")
        self.label_detalle.pack(padx=14, pady=10, fill="y")

        self.frame_consola_tit = ctk.CTkFrame(self.frame_detalle, fg_color="transparent")
        self.frame_consola_tit.pack(fill="x", padx=14, pady=(0, 4))
        ctk.CTkLabel(self.frame_consola_tit, text="Consola", font=("Consolas", 12, "bold"), text_color="#e3c54d").pack(side="left")
        self.label_estado = ctk.CTkLabel(self.frame_consola_tit, text="Listo", font=("Consolas", 11), text_color="#9aa0a5")
        self.label_estado.pack(side="right")

        self.texto_consola = ctk.CTkTextbox(self.frame_detalle, height=150, fg_color="#0b0d0f", text_color="#9fe870",
                                             font=("Consolas", 11), wrap="word")
        self.texto_consola.pack(fill="both", expand=True, padx=14, pady=(0, 8))

        self.frame_accion = ctk.CTkFrame(self, fg_color=COLOR_SUB, corner_radius=8)
        self.frame_accion.pack(fill="x", padx=10, pady=(0, 8))
        self.label_comando = ctk.CTkLabel(self.frame_accion, text="edl ...", font=("Consolas", 12), text_color="#c9ced3")
        self.label_comando.pack(side="left", padx=12, pady=10, fill="x", expand=True)
        self.boton_detener = ctk.CTkButton(self.frame_accion, text="Detener", width=90, height=32,
                                           fg_color="#5a1010", hover_color="#7a1414", command=self._detener)
        self.boton_detener.pack(side="right", padx=6, pady=8)
        self.boton_ejecutar = ctk.CTkButton(self.frame_accion, text="Ejecutar", width=110, height=32,
                                            fg_color="#0060b0", hover_color="#0b7ad0", font=("Consolas", 13),
                                            command=self._ejecutar)
        self.boton_ejecutar.pack(side="right", padx=6, pady=8)

        self._consejo = None

        if self.db:
            self.seleccionar_marca(list(self.db.keys())[0])

    def seleccionar_marca(self, marca):
        self.marca_actual = marca
        self.modelo_actual = None
        for m, b in self.botones_marca.items():
            b.configure(fg_color="#34322f" if m == marca else "#161a1e")
        self.label_marca.configure(text=marca.capitalize())
        self.entrada_buscar.delete(0, "end")
        self._filtrar()

    def _filtrar(self):
        for w in self.scroll.winfo_children():
            w.destroy()
        modelos = self.db.get(self.marca_actual, []) or []
        texto = self.entrada_buscar.get().strip().lower()
        for m in modelos:
            etiqueta = f"{m.get('nombre','')}  {m.get('variante','')}"
            if texto and texto not in etiqueta.lower():
                continue
            b = ctk.CTkButton(self.scroll, text=etiqueta, anchor="w", height=36,
                              fg_color="transparent", hover_color="#2a2d30", text_color="#d5d9dc",
                              font=("Consolas", 12), command=lambda mm=m: self.seleccionar_modelo(mm))
            b.pack(fill="x", pady=1)

    def seleccionar_modelo(self, m):
        self.modelo_actual = m
        datos = [
            ("MODELO", f"{m.get('nombre','')}"),
            ("VARIANTE", f"{m.get('variante','')}"),
            ("SOPORTE", f"{m.get('soporta','')}"),
            ("CHIPSET", f"{m.get('chipset','')}"),
            ("CONEXION", f"{m.get('conexion','')}"),
            ("METODO", f"{m.get('metodo','')}"),
            ("LOADER", f"{m.get('loader','off')}"),
            ("INSTRUCCIONES", f"{m.get('instruccion','')}"),
        ]
        self.label_detalle.configure(text="\n".join(f"> {k}: {v}" for k, v in datos))

        loader = config.preparar_loader(m.get('loader'))
        cmd = self.motor.construir_comando("printgpt", loader)
        self.label_comando.configure(text=" ".join(cmd))
        self._log(f"[Modelo seleccionado] {m.get('nombre')} {m.get('variante')}")

    def _ejecutar(self):
        if not self.modelo_actual:
            self._log("[AVISO] Selecciona un modelo primero")
            return
        loader = config.preparar_loader(self.modelo_actual.get('loader'))
        cmd = self.motor.construir_comando("printgpt", loader)
        if not self.motor.accion_disponible():
            self._log("[ERROR] edl no está instalado. Corre: cd /opt/edl && pip install -r requirements.txt")
            return
        self._log("[INFO] Qualcomm EDL requiere el dispositivo en modo EDL (9008) o Sahara.")
        self.boton_ejecutar.configure(state="disabled")
        self.texto_consola.delete("1.0", "end")

        def run():
            rc = self.motor.ejecutar(cmd)
            self.after(0, lambda: self.boton_ejecutar.configure(state="normal"))
        threading.Thread(target=run, daemon=True).start()

    def _detener(self):
        self.motor.stop()
        self._log("[INFO] Orden de detención enviada.")

    def _log(self, t):
        def insertar():
            self.texto_consola.insert("end", t + "\n")
            self.texto_consola.see("end")
        try:
            self.after(0, insertar)
        except Exception:
            pass

    def _status(self, s):
        try:
            self.after(0, lambda: self.label_estado.configure(text=s))
        except Exception:
            pass