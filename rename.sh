#!/bin/bash

for file in *; do
    if [ -f "$file" ]; then
        # Get the file extension
        extension="${file##*.}"
        
        # Generate Unix timestamp
        timestamp=$(date +%s)
        
        # Rename the file
        mv "$file" "${timestamp}.${extension}"
    fi
done
