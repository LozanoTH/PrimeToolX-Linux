import os
import signal
import subprocess
import threading
import shlex

# Rutas de los motores externos. Se pueden cambiar con variables de entorno
# (p. ej.: PRIMETOOLX_MTK_PYTHON=/usr/bin/python3).
MTK_PYTHON = os.environ.get("PRIMETOOLX_MTK_PYTHON", "/opt/mtkvenv/bin/python")
MTK_SCRIPT = os.environ.get("PRIMETOOLX_MTK_SCRIPT", "/opt/mtkclient/mtk.py")
EDL_PYTHON = os.environ.get("PRIMETOOLX_EDL_PYTHON", "/usr/bin/python3")
EDL_SCRIPT = os.environ.get("PRIMETOOLX_EDL_SCRIPT", "/opt/edl/edl.py")

class MotorMtk:
    """Ejecuta mtkclient nativo (el mismo motor que usa PrimeToolX)."""

    def __init__(self, log_callback=None, status_callback=None):
        self.log = log_callback or (lambda t: None)
        self.status = status_callback or (lambda s: None)
        self.proc = None
        self._cancelled = False

    def accion_disponible(self):
        return os.path.exists(MTK_PYTHON) and os.path.exists(MTK_SCRIPT)

    def construir_comando(self, comando_base, loader=None, extra=None):
        cmd = [MTK_PYTHON, MTK_SCRIPT] + shlex.split(comando_base)
        if loader:
            cmd += ["--loader", loader]
        if extra:
            cmd += shlex.split(extra)
        return cmd

    def ejecutar(self, cmd, timeout_espera=None):
        """Ejecuta el comando y transmite la salida en vivo. Devuelve returncode."""
        self._cancelled = False
        env = os.environ.copy()
        self.status("Iniciando...")
        self.log("$ " + " ".join(cmd))
        try:
            self.proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1, env=env,
                preexec_fn=os.setsid,
            )
        except Exception as e:
            self.log(f"[ERROR] No se pudo lanzar: {e}")
            self.status("Error al iniciar")
            return -1

        def lector():
            for linea in self.proc.stdout:
                t = linea.rstrip("\n")
                self.log(t)
                if self._cancelled:
                    break

        hilo = threading.Thread(target=lector, daemon=True)
        hilo.start()

        if timeout_espera:
            try:
                self.proc.wait(timeout=timeout_espera)
            except subprocess.TimeoutExpired:
                self.stop()
                self.log("[AVISO] Tiempo de espera agotado, proceso detenido.")
                return -2
        else:
            self.proc.wait()

        hilo.join(timeout=2)
        rc = self.proc.returncode
        self.status("Proceso terminado (rc=%s)" % rc if rc == 0 else "Error en el proceso (rc=%s)" % rc)
        return rc

    def stop(self):
        if self.proc and self.proc.poll() is None:
            self.log("Deteniendo proceso...")
            try:
                os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
            except Exception:
                self.proc.terminate()


EDL_PYTHON = os.environ.get("PRIMETOOLX_EDL_PYTHON", "/usr/bin/python3")
EDL_SCRIPT = os.environ.get("PRIMETOOLX_EDL_SCRIPT", "/opt/edl/edl.py")

class MotorEDL:
    """Ejecuta la herramienta edl nativa para Qualcomm/Samsung EDL Mode."""

    def __init__(self, log_callback=None, status_callback=None):
        self.log = log_callback or (lambda t: None)
        self.status = status_callback or (lambda s: None)
        self.proc = None
        self._cancelled = False

    def accion_disponible(self):
        return os.path.exists(EDL_PYTHON) and os.path.exists(EDL_SCRIPT)

    def construir_comando(self, comando, loader=None, extra=None):
        cmd = [EDL_PYTHON, EDL_SCRIPT]
        if loader:
            cmd += ["--loader", loader]
        cmd += shlex.split(comando)
        if extra:
            cmd += shlex.split(extra)
        return cmd

    def ejecutar(self, cmd, timeout_espera=None):
        self._cancelled = False
        env = os.environ.copy()
        self.status("Iniciando...")
        self.log("$ " + " ".join(cmd))
        try:
            self.proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1, env=env,
                preexec_fn=os.setsid,
            )
        except Exception as e:
            self.log(f"[ERROR] No se pudo lanzar: {e}")
            self.status("Error al iniciar")
            return -1

        def lector():
            for linea in self.proc.stdout:
                t = linea.rstrip("\n")
                self.log(t)
                if self._cancelled:
                    break

        hilo = threading.Thread(target=lector, daemon=True)
        hilo.start()
        self.proc.wait()
        hilo.join(timeout=2)
        rc = self.proc.returncode
        self.status("Proceso terminado (rc=%s)" % rc if rc == 0 else "Error en el proceso (rc=%s)" % rc)
        return rc

    def stop(self):
        if self.proc and self.proc.poll() is None:
            self.log("Deteniendo proceso...")
            try:
                os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
            except Exception:
                self.proc.terminate()