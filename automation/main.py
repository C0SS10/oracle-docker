from drive.drive_service import DriveService
from workflows.folder_workflow import FolderWorkflow
from config.settings import settings


def main():
    drive = DriveService(settings.GOOGLE_CREDENTIALS)

    folders = drive.get_folders(settings.GOOGLE_PARENT_ID)
    if not folders:
        print("⚠️ No se encontraron carpetas.")
        return

    workflow = FolderWorkflow(drive, settings.BASE_DUMP)

    for folder in folders:
        workflow.process_folder(folder)

    print("\n🎉 Proceso completado.")


if __name__ == "__main__":
    main()
