from pathlib import Path

class EnvGenerator:
    @staticmethod
    def create(prefix: str, date: str, dump_files: list[str], project_root: Path):
        dump_files_joined = ",".join(dump_files)
        home_name = Path.home().as_posix()
        dump_abs = f"{home_name}/dump"

        env_content = f"""#!/bin/bash

export CVLAC_USER="{prefix}_CV"
export GRUPLAC_USER="{prefix}_GR"
export INSTITULAC_USER="{prefix}_IN"
export ORACLE_PWD="colavudea"

export DUMP_PATH="{dump_abs}"
export DUMP_DATE="{date}"
export DUMP_FILES="{dump_files_joined}"

export HUNABKU_PORT=9090
"""

        env_path = project_root / "scienti" / "config.env"
        env_path.write_text(env_content)

        print(f"📝 Archivo config.env generado en: {env_path}")
        return env_path
