from pathlib import Path
from drive.drive_service import DriveService
from workflows.folder_workflow import FolderWorkflow
from config.settings import settings


def main():
    drive_service = DriveService(settings.GOOGLE_CREDENTIALS)

    folders = drive_service.get_folders(settings.GOOGLE_PARENT_ID)
    if not folders:
        print("⚠️ No se encontraron carpetas.")
        return

    project_root = Path(__file__).resolve().parents[1]
    workflow = FolderWorkflow(
        drive=drive_service,
        base_dump=Path.home() / "dump",
        project_root=project_root
    )

    for folder in folders:
        workflow.process_folder(folder)

    print("\n🎉 Proceso completado.")


if __name__ == "__main__":
    main()
