#!/bin/bash

DIR="$HOME/Lab-3-Personal_Expenses_Tracker_NatnaelAyele"
ARCHIVE_DIR="$DIR/archives"
LOG_FILE="$ARCHIVE_DIR/archive_log.txt"


if [ -d "$DIR" ]; then
    mkdir -p "$ARCHIVE_DIR"
    if compgen -G "$DIR/expenses*.txt" > /dev/null; then
    	for file in "$DIR"/expenses*.txt; do
            	mv "$file" "$ARCHIVE_DIR"
            	echo "[$(date '+%Y-%m-%d %H:%M:%S')] Archived $file" >> "$LOG_FILE"
    done
    echo "archived successfuly!!!"
    else
	    echo "Everything is up-to-date"
    fi
else
    echo "Directory Not found"
fi


is_valid_date() {
    # Check the pattern first: YYYY-MM-DD
    if [[ ! $1 =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        return 1
    fi

    # Check if it's a real calendar date
    if ! date -d "$1" >/dev/null 2>&1; then
        return 1
    fi

    return 0
}


search_files() {
    read -p "Enter the date in YYYY-MM-DD format: " date


     if ! is_valid_date "$date"; then
        echo "Invalid date format. Please use YYYY-MM-DD and make sure it is a real date."
        return
    fi

    for file in "$ARCHIVE_DIR"/*"$date".txt; do
        if [ -f "$file" ]; then
            echo "=========================================================="
            cat "$file"
            echo "=========================================================="
        else
            echo "No files found for $date"
        fi
    done
}

while true; do
    read -p "Want to search files from the archive (y/n): " choice
    choice=$(echo "$choice" | tr 'A-Z' 'a-z')

    case "$choice" in
        y)
            search_files
            ;;
        n)
            break
            ;;
        *)
            echo "Invalid option."
            ;;
    esac
done 
