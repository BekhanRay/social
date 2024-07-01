#!/bin/bash

src_directory="apps"

# Найти все поддиректории с именем migrations внутри директории src
migrations_directories=$(find "$src_directory" -type d -name migrations)

<<<<<<< HEAD
for dir in $migrations_directories; do
=======
for dir in $migrations_directories;do
>>>>>>> 7315cff (Initial commit)
    echo "Deleting migrations in $dir"
    
    # Удалить все файлы с расширением .py, кроме __init__.py
    find "$dir" -type f -name "*.py" -not -name "__init__.py" -delete
    
    # Удалить все файлы с расширением .pyc
    find "$dir" -type f -name "*.pyc" -delete
done

echo "Migrations deleted successfully."