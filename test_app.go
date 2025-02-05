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
			targetFolder = filepath.Dir(file.Name)
			break
		}
	}

	if targetFolder == "" && filename != "" {
		targetFolder = "." // Handle files at the root level of the ZIP archive
	}

	if targetFolder == "" {
		return fmt.Errorf("file '%s' not found in the archive", filename)
	}

	// Extract files from the target folder
	for _, file := range reader.File {
		if (targetFolder == "." && !strings.Contains(file.Name, "/")) || strings.HasPrefix(file.Name, targetFolder) {
			// Get the relative path of the file within the target folder
			var relPath string
			if targetFolder == "." {
				relPath = file.Name // Use full name for root-level files
			} else {
				var err error
				relPath, err = filepath.Rel(targetFolder, file.Name)
				if err != nil {
					return fmt.Errorf("failed to get relative path: %v", err)
				}
			}

			// Construct the full path for extraction
			path := filepath.Join(destinationPath, relPath)

			if file.FileInfo().IsDir() {
				// Create directory
				os.MkdirAll(path, os.ModePerm)
				continue
			}

			// Create the containing folder
			if err := os.MkdirAll(filepath.Dir(path), os.ModePerm); err != nil {
				return fmt.Errorf("failed to create directory: %v", err)
			}

			// Create the file
			outFile, err := os.OpenFile(path, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, file.Mode())
			if err != nil {
				return fmt.Errorf("failed to create file: %v", err)
			}

			// Open the file in the zip
			rc, err := file.Open()
			if err != nil {
				outFile.Close()
				return fmt.Errorf("failed to open file in zip: %v", err)
			}

			// Copy the contents
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
