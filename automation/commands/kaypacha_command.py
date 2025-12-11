import subprocess
from .base_command import Command

class SqlToMongoCommand(Command):
    def __init__(self, prefix: str, dump_date: str, mongo_model="product", max_threads=2):
        self.prefix = prefix
        self.dump_date = dump_date
        self.mongo_model = mongo_model
        self.max_threads = max_threads

    def execute(self):
        print("🔄 Ejecutando migración SQL → MongoDB...")

        # Database name format: scienti_<institution>_<date>
        mongo_dbname = f"scienti_{self.prefix.lower()}_{self.dump_date}"

        cmd = [
            "kaypacha_scienti",
            "--mongo_dbname", mongo_dbname,
            "--model", self.mongo_model,
            "--max_threads", str(self.max_threads),
            "--cvlac_user", f"{self.prefix}_CV",
            "--gruplac_user", f"{self.prefix}_GR",
            "--institulac_user", f"{self.prefix}_IN",
            "--checkpoint"
        ]

        print("▶ Executing:", " ".join(cmd))

        subprocess.run(cmd, check=True)
