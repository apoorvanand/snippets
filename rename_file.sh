#!/bin/bash

# Find all files with whitespace in their names
find . -type f -name "* *" -print0 | while IFS= read -r -d '' file; do
  # Remove whitespace and replace with underscore
  new_name=$(echo "${file}" | sed 's/ /_/g')
  # Rename the file
  mv -- "$file" "$new_name"
done
