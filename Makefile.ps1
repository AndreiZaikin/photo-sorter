param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

switch ($Command) {
    "help" {
        Write-Host "Available commands:"
        Write-Host "  .\Makefile.ps1 install   - Install dependencies"
        Write-Host "  .\Makefile.ps1 menu      - Run interactive menu"
        Write-Host "  .\Makefile.ps1 sort      - Sort photos and videos"
        Write-Host "  .\Makefile.ps1 rename    - Rename files (transliteration)"
        Write-Host "  .\Makefile.ps1 archive   - Archive by months"
        Write-Host "  .\Makefile.ps1 clean     - Remove empty folders"
    }
    "install" {
        pip install Pillow exifread
    }
    "menu" {
        python main.py
    }
    "sort" {
        python -c "from src.sorter import sort_all_simple; sort_all_simple()"
    }
    "rename" {
        python -c "from src.renamer import rename_files; rename_files()"
    }
    "archive" {
        python -c "from src.archiver import archive_photos; archive_photos()"
    }
    "clean" {
        python -c "from src.sorter import clean_empty_dirs; clean_empty_dirs()"
    }
}
