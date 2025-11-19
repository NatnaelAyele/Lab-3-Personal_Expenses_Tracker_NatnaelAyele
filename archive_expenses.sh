#!/bin/bash

# define directory paths
DIR="$HOME/Lab-3-Personal_Expenses_Tracker_NatnaelAyele"
ARCHIVE_DIR="$DIR/archives"
LOG_FILE="$ARCHIVE_DIR/archive_log.txt"

# check if the parent directory exists
if [ -d "$DIR" ]; then

    # create the 'archives' directory inside the parent directory if it doesn't exist
    mkdir -p "$ARCHIVE_DIR"

    # search for files that start with expenses and are .txt file inside the parent directory
    if compgen -G "$DIR/expenses*.txt" > /dev/null; then

	# move each expenses files from the parent directory to 'archives' directory and log the operation to a log file inside 'archcives' directory with timestamp 
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


# validates the date accepted from user
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


# prompts user for date, if the date is valid it searches for an expense file with that date inside 'archives/'. If the expense file exists it display the content of the file

search_files() {
    read -p "Enter the date in YYYY-MM-DD format: " date

     # is_valid_date() to check validity of the date
     if ! is_valid_date "$date"; then
        echo "Invalid date format. Please use YYYY-MM-DD and make sure it is a real date."
        return
    fi

    # loop through archives directory searching for a file that contains the specified date
    for file in "$ARCHIVE_DIR"/*"$date".txt; do

	# if a file exist with that date display its content
        if [ -f "$file" ]; then
            echo "=========================================================="
            cat "$file"
            echo "=========================================================="
	 
	 # if none found print 'no file found'
        else
            echo "No files found for $date"
        fi
    done
}


# an infinite loop that asks if user wants to serach for file, if yes, it calls the appropriate function to allow search. if no, it exits the program
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
