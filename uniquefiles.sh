#!/bin/zsh

# Check if any arguments are provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <file1> [file2 ...]"
    exit 1
fi

# Function to generate a unique filename
generate_unique_filename() {
    local base_file="$1"
    local index="$2"
    local filename=$(basename "$base_file")
    local extension="${filename##*.}"
    local basename="${filename%.*}"
    
    echo "${basename}_copy_${index}.${extension}"
}

# Iterate through all provided files
for file in "$@"; do
    # Check if file exists
    if [[ ! -f "$file" ]]; then
        echo "File $file does not exist. Skipping."
        continue
    fi
    
    # Make 100 copies of each file
    for i in {1..100}; do
        unique_filename=$(generate_unique_filename "$file" "$i")
        cp "$file" "$unique_filename"
        echo "Created copy: $unique_filename"
    done
done
