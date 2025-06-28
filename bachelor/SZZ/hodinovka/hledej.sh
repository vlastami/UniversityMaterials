#!/bin/bash

# Funkce pro výpis použití skriptu
usage() {
    echo "Usage: $0 input_directory output_csv_file extension1 extension2 ..."
    exit 1
}

# Kontrola počtu parametrů
if [ "$#" -lt 3 ]; then
    usage
fi

input_directory=$1
output_csv_file=$2
shift 2
extensions=("$@")

# Kontrola, zda je zadaný vstupní adresář platný
if [ ! -d "$input_directory" ]; then
    echo "Error: Input directory does not exist."
    exit 1
fi

# Inicializace CSV souboru
echo "Path,Size" > "$output_csv_file"

# Vyhledávání obrázků podle zadaných přípon a ukládání do CSV souboru
for ext in "${extensions[@]}"; do
    find "$input_directory" -type f -iname "*.$ext" -exec stat --format="%n,%s" {} + >> "$output_csv_file"
done
