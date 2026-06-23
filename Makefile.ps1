param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

switch ($Command) {
    "help" {
        Write-Host "Доступные команды:"
        Write-Host "  .\Makefile.ps1 install   - Установить зависимости"
        Write-Host "  .\Makefile.ps1 run       - Запустить основное меню"
        Write-Host "  .\Makefile.ps1 sort      - Запустить сортировку"
        Write-Host "  .\Makefile.ps1 archive   - Запустить архивацию"
        Write-Host "  .\Makefile.ps1 rename    - Запустить переименование"
        Write-Host "  .\Makefile.ps1 clean     - Очистить временные файлы"
    }
    "install" {
        pip install Pillow exifread
    }
    "run" {
        python main.py
    }
    "sort" {
        python -c "from src.sorter import sort_all_simple; sort_all_simple()"
    }
    "archive" {
        python scripts/archive_photos.py
    }
    "rename" {
        python scripts/rename_cyrillic.py
    }
    "clean" {
        Get-ChildItem -Recurse -Include __pycache__,*.pyc | Remove-Item -Recurse -Force
        Write-Host "Очищено."
    }
}
