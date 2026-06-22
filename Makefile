# Photo-Sorter Makefile
# Команды: make <target>

.PHONY: help install run sort archive rename clean

help:
	@echo "Доступные команды:"
	@echo "  make install   - Установить зависимости"
	@echo "  make run       - Запустить основное меню сортировки"
	@echo "  make sort      - Запустить сортировку (прямой вызов)"
	@echo "  make archive   - Запустить архивацию по месяцам"
	@echo "  make rename    - Запустить переименование файлов"
	@echo "  make clean     - Очистить временные файлы"

install:
	pip install Pillow exifread

run:
	python main.py

sort:
	python -c "from src.sorter import sort_all_simple; sort_all_simple()"

archive:
	python scripts/archive_years.py

rename:
	python scripts/rename_cyrillic.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Очищено"
