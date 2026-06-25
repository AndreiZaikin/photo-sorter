from src.sorter import sort_all_simple, clean_empty_dirs
from src.renamer import rename_files
from src.archiver import archive_photos


def main_menu():
    print("\n" + "=" * 50)
    print("  PHOTO-SORTER")
    print("=" * 50)
    print("  1. Сортировать фото и видео")
    print("  2. Переименовать файлы (транслитерация)")
    print("  3. Архивировать по месяцам")
    print("  4. Удалить пустые папки")
    print("  5. Выход")
    print("-" * 50)

    choice = input("Выберите пункт (1-5): ").strip()

    if choice == "1":
        sort_all_simple()
    elif choice == "2":
        rename_files()
    elif choice == "3":
        archive_photos()
    elif choice == "4":
        clean_empty_dirs()
    elif choice == "5":
        print("Выход.")
    else:
        print("Неверный ввод.")


if __name__ == "__main__":
    main_menu()
