package main

import (
	"archive/zip"
	"fmt"
	"io"
	"os"
	"path/filepath"
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
		if filepath.Base(file.Name) == filename {
			targetFolder = filepath.Dir(file.Name)
			break
		}
	}

	if targetFolder == "" {
		return fmt.Errorf("file '%s' not found in the archive", filename)
	}

	// Extract files from the target folder while preserving structure
	for _, file := range reader.File {
		if strings.HasPrefix(file.Name, targetFolder) {
			// Construct the full path for extraction
			extractedPath := filepath.Join(destinationPath, file.Name)

			if file.FileInfo().IsDir() {
				// Create directory
				err := os.MkdirAll(extractedPath, os.ModePerm)
				if err != nil {
					return fmt.Errorf("failed to create directory: %v", err)
				}
				continue
			}

			// Create parent directories if needed
			err := os.MkdirAll(filepath.Dir(extractedPath), os.ModePerm)
			if err != nil {
				return fmt.Errorf("failed to create parent directories: %v", err)
			}

			// Create and write to the file
			outFile, err := os.OpenFile(extractedPath, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, file.Mode())
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
