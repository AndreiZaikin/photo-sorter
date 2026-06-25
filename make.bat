@echo off
if "%1"=="" goto help
if "%1"=="install" goto install
if "%1"=="menu" goto menu
if "%1"=="sort" goto sort
if "%1"=="rename" goto rename
if "%1"=="archive" goto archive
if "%1"=="clean" goto clean
goto help

:help
echo Available commands:
echo   make.bat install   - Install dependencies
echo   make.bat menu      - Run interactive menu
echo   make.bat sort      - Sort photos and videos
echo   make.bat rename    - Rename files (transliteration)
echo   make.bat archive   - Archive by months
echo   make.bat clean     - Remove empty folders
goto :eof

:install
pip install Pillow exifread
goto :eof

:menu
python main.py
goto :eof

:sort
python -c "from src.sorter import sort_all_simple; sort_all_simple()"
goto :eof

:rename
python -c "from src.renamer import rename_files; rename_files()"
goto :eof

:archive
python -c "from src.archiver import archive_photos; archive_photos()"
goto :eof

:clean
python -c "from src.sorter import clean_empty_dirs; clean_empty_dirs()"
goto :eof
