import subprocess
import time

class WaitForKaypachaCommand:
    def __init__(self, container_name: str):
        self.container_name = container_name

    def execute(self):
        print(f"⏳ Esperando a que Kaypacha termine en el contenedor: {self.container_name}")

        process = subprocess.Popen(
            ["docker", "logs", "-f", self.container_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        for line in process.stdout:
            if "Kaypacha finished successfully" in line:
                process.kill()
                return

            if "Error running Kaypacha" in line or "❌" in line:
                process.kill()
                return
