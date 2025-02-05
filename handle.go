package main

import (
	"archive/zip"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
)

func extractFolderContainingFile(sourceZip, destinationPath, filename string) error {
	// Open the zip file
	reader, err := zip.OpenReader(sourceZip)
	if err != nil {
		return fmt.Errorf("failed to open zip file: %v", err)
	}
	defer reader.Close()

	// Search for the specific file and its containing folder
	var targetFolder string
	for _, file := range reader.File {
		if strings.HasSuffix(file.Name, filename) {
			targetFolder = filepath.Dir(file.Name) // Get the folder containing the file
			break
		}
	}

	if targetFolder == "" && filename != "" {
		return fmt.Errorf("file '%s' not found in the archive", filename)
	}

	// Extract files from the target folder or root if targetFolder is empty
	for _, file := range reader.File {
		if targetFolder == "" || strings.HasPrefix(file.Name, targetFolder) {
			// Get the relative path of the file within the target folder or root
			var relPath string
			if targetFolder != "" {
				relPath, err = filepath.Rel(targetFolder, file.Name)
				if err != nil {
					return fmt.Errorf("failed to get relative path: %v", err)
				}
			} else {
				relPath = file.Name // If at root, use the full name as relative path
			}

			// Construct the full path for extraction
			path := filepath.Join(destinationPath, relPath)

			if file.FileInfo().IsDir() {
				// Create directory
				err := os.MkdirAll(path, os.ModePerm)
				if err != nil {
					return fmt.Errorf("failed to create directory: %v", err)
				}
				continue
			}

			// Create the containing folder
			err := os.MkdirAll(filepath.Dir(path), os.ModePerm)
			if err != nil {
				return fmt.Errorf("failed to create directory: %v", err)
			}

			// Create and write to the file
			outFile, err := os.OpenFile(path, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, file.Mode())
			if err != nil {
				return fmt.Errorf("failed to create file: %v", err)
			}

			rc, err := file.Open()
			if err != nil {
				outFile.Close()
				return fmt.Errorf("failed to open file in zip: %v", err)
			}

			_, err = io.Copy(outFile, rc)
			outFile.Close()
			rc.Close()

			if err != nil {
				return fmt.Errorf("failed to write file contents: %v", err)
			}
		}
	}

	fmt.Printf("Successfully extracted folder containing '%s' to '%s'\n", filename, destinationPath)
	return nil
}

func main() {
	sourceZip := "path/to/your/archive.zip"
	destinationPath := "path/to/extraction/directory"
	filename := "specific_file.txt"

	err := extractFolderContainingFile(sourceZip, destinationPath, filename)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
	}
}
