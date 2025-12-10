import re
from pathlib import Path

class DumpMetadata:
    @staticmethod
    def extract(zip_filename: str):
        match = re.match(r"([A-Za-z0-9]+)_(\d{8})\.zip", zip_filename)
        if not match:
            raise ValueError(f"Formato inválido de ZIP: {zip_filename}")

        return match.group(1), match.group(2)

    @staticmethod
    def detect_dump_files(prefix: str, date: str, folder: Path):
        expected = [
            f"{prefix}_CV_{date}.dmp",
            f"{prefix}_GR_{date}.dmp",
            f"{prefix}_IN_{date}.dmp",
        ]

        found = [f for f in expected if (folder / f).exists()]
        if not found:
            raise FileNotFoundError("No se encontraron dumps válidos.")

        return found
