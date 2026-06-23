@echo off
if "%1"=="" goto help
if "%1"=="install" goto install
if "%1"=="run" goto run
if "%1"=="sort" goto sort
if "%1"=="archive" goto archive
if "%1"=="rename" goto rename
if "%1"=="clean" goto clean
goto help

:help
echo Available commands:
echo   make.bat install   - Install dependencies
echo   make.bat run       - Run main menu
echo   make.bat sort      - Run sorter
echo   make.bat archive   - Archive by months
echo   make.bat rename    - Rename files
echo   make.bat clean     - Remove temp files
goto :eof

:install
pip install Pillow exifread
goto :eof

:run
python main.py
goto :eof

:sort
python -c "from src.sorter import sort_all_simple; sort_all_simple()"
goto :eof

:archive
python scripts/archive_photos.py
goto :eof

:rename
python scripts/rename_cyrillic.py
goto :eof

:clean
del /s /q *.pyc 2>nul
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
echo Done.
goto :eof
