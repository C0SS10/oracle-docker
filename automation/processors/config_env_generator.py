from pathlib import Path

class EnvGenerator:
    @staticmethod
    def create(prefix: str, date: str, dump_files: list[str], project_root: Path):
        scienti_path = project_root / "scienti"
        scienti_path.mkdir(exist_ok=True)

        env_file = scienti_path / ".config.env"

        dump_joined = ",".join(dump_files)

        content = f"""#!/bin/bash

export CVLAC_USER="{prefix}_CV"
export GRUPLAC_USER="{prefix}_GR"
export INSTITULAC_USER="{prefix}_IN"
export ORACLE_PWD="password"

export DUMP_PATH="$HOME/dump"
export DUMP_DATE="{date}"
export DUMP_FILES="{dump_joined}"

export HUNABKU_PORT=9090
"""

        env_file.write_text(content)
        return env_file
