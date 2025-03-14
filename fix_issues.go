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

	// First, extract all files from the target folder to the destination root
	for _, file := range reader.File {
		if targetFolder == "" || strings.HasPrefix(file.Name, targetFolder) {
			// Get the path relative to the target folder
			var relPath string
			if targetFolder != "" {
				relPath, err = filepath.Rel(targetFolder, file.Name)
				if err != nil {
					return fmt.Errorf("failed to get relative path: %v", err)
				}
			} else {
				relPath = file.Name
			}

			// Extract to root destination
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

	// Now, also maintain the subfolder structure by copying the entire subfolder to the root
	if targetFolder != "" {
		// Create the target folder at the root
		subfolderPath := filepath.Join(destinationPath, filepath.Base(targetFolder))
		err := os.MkdirAll(subfolderPath, os.ModePerm)
		if err != nil {
			return fmt.Errorf("failed to create subfolder at root: %v", err)
		}

		// Copy files to maintain the subfolder structure
		for _, file := range reader.File {
			if strings.HasPrefix(file.Name, targetFolder) {
				// Get the path relative to the target folder
				relPath, err := filepath.Rel(targetFolder, file.Name)
				if err != nil {
					return fmt.Errorf("failed to get relative path: %v", err)
				}

				// Extract to subfolder at root
				path := filepath.Join(subfolderPath, relPath)

				if file.FileInfo().IsDir() {
					// Create directory
					err := os.MkdirAll(path, os.ModePerm)
					if err != nil {
						return fmt.Errorf("failed to create directory in subfolder: %v", err)
					}
					continue
				}

				// Create the containing folder
				err = os.MkdirAll(filepath.Dir(path), os.ModePerm)
				if err != nil {
					return fmt.Errorf("failed to create directory in subfolder: %v", err)
				}

				// Skip if the file already exists (from the first extraction)
				if _, err := os.Stat(path); err == nil {
					continue
				}

				// Create and write to the file
				outFile, err := os.OpenFile(path, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, file.Mode())
				if err != nil {
					return fmt.Errorf("failed to create file in subfolder: %v", err)
				}

				rc, err := file.Open()
				if err != nil {
					outFile.Close()
					return fmt.Errorf("failed to open file in zip for subfolder: %v", err)
				}

				_, err = io.Copy(outFile, rc)
				outFile.Close()
				rc.Close()

				if err != nil {
					return fmt.Errorf("failed to write file contents to subfolder: %v", err)
				}
			}
		}
	}

	fmt.Printf("Successfully extracted contents to '%s' and maintained subfolder structure\n", destinationPath)
	return nil
}

func main() {
	if len(os.Args) < 4 {
		fmt.Println("Usage: program sourceZip destinationPath filename")
		fmt.Println("Example: program archive.zip ./extracted index.html")
		os.Exit(1)
	}

	sourceZip := os.Args[1]
	destinationPath := os.Args[2]
	filename := os.Args[3]

	err := extractFolderContainingFile(sourceZip, destinationPath, filename)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		os.Exit(1)
	}
}
