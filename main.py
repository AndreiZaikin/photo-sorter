from src.sorter import sort_all_simple, clean_empty_dirs


def main_menu():
    print("\n" + "=" * 50)
    print("  МЕНЮ")
    print("=" * 50)
    print("  1. Сортировать ВСЁ (фото + видео + неопознанные)")
    print("  2. Удалить пустые папки в исходной директории")
    print("  3. Выход")
    print("-" * 50)

    choice = input("Выберите пункт (1-3): ").strip()

    if choice == "1":
        sort_all_simple()
    elif choice == "2":
        clean_empty_dirs()
    elif choice == "3":
        print("Выход.")
    else:
        print("Неверный ввод.")


if __name__ == "__main__":
    main_menu()
