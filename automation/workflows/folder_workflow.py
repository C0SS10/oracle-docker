from pathlib import Path

from commands.wait_for_complete_command import WaitForKaypachaCommand
from commands.docker_down_command import DockerDownCommand
from commands.docker_up_command import DockerUpCommand
from orchestrator.command_executor import CommandExecutor
from drive.drive_service import DriveService
from processors.config_env_generator import EnvGenerator
from processors.dump_metadata import DumpMetadata
from processors.zip_processor import ZipProcessor


class FolderWorkflow:
    def __init__(self, drive: DriveService, base_dump: Path, project_root: Path):
        self.drive = drive
        self.base_dump = base_dump
        self.project_root = project_root

    def process_folder(self, folder):
        folder_name = folder["name"]
        folder_id = folder["id"]

        local_folder = self.base_dump / folder_name
        local_folder.mkdir(exist_ok=True)

        print(f"\n📁 Carpeta: {folder_name}")

        files = self.drive.get_files(folder_id)
        if not files:
            print("  ⚠️ Vacía.")
            return None

        zip_file = None

        for file in files:
            file_path = local_folder / file["name"]
            print(f"  ⬇️ Descargando: {file['name']}")
            self.drive.download_file(file["id"], file_path)

            if file["name"].endswith(".zip"):
                zip_file = file_path

        if not zip_file:
            print("  ⚠️ No hay ZIP → no se genera .config.env")
            return None

        ZipProcessor.unzip(zip_file, local_folder)

        prefix, date = DumpMetadata.extract(zip_file.name)
        dump_files = DumpMetadata.detect_dump_files(prefix, date, local_folder)

        env_file = EnvGenerator.create(
            prefix=prefix,
            date=date,
            dump_files=dump_files,
            project_root=Path(__file__).resolve().parents[2],
            dump_folder=local_folder,
        )

        if env_file:
            executor = CommandExecutor()

            compose_file = self.project_root / "scienti" / "docker-compose.yml"

            executor.add(DockerUpCommand(compose_file=compose_file, env_file=env_file))
            executor.add(WaitForKaypachaCommand(container_name="scienti-oracle-docker-1"))
            executor.add(DockerDownCommand(compose_file=compose_file, env_file=env_file))

            executor.run()

        return env_file
