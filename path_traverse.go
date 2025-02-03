package main

import (
    "archive/zip"
    "fmt"
    "io"
    "os"
    "path/filepath"
    "strings"
)

// extractFile extracts a single file from a ZIP archive.
func extractFile(zf *zip.File, dest string) error {
    rc, err := zf.Open()
    if err != nil {
        return err
    }
    defer rc.Close()

    // Create the destination file
    filePath := filepath.Join(dest, zf.Name)
    if err := os.MkdirAll(filepath.Dir(filePath), os.ModePerm); err != nil {
        return err
    }

    outFile, err := os.Create(filePath)
    if err != nil {
        return err
    }
    defer outFile.Close()

    // Copy the file content
    _, err = io.Copy(outFile, rc)
    return err
}

// extractFolder extracts all files from a specific folder in a ZIP archive.
func extractFolder(zf *zip.Reader, folderPath, dest string) error {
    for _, file := range zf.File {
        if strings.HasPrefix(file.Name, folderPath) {
            if err := extractFile(file, dest); err != nil {
                return err
            }
        }
    }
    return nil
}

// findFileAndExtractFolder searches for a specific file in the ZIP archive
// and extracts the folder containing that file.
func findFileAndExtractFolder(zipPath, fileName, dest string) error {
    // Open the ZIP file
    r, err := zip.OpenReader(zipPath)
    if err != nil {
        return err
    }
    defer r.Close()

    var folderPath string
    found := false

    // Search for the specific file
    for _, file := range r.File {
        if filepath.Base(file.Name) == fileName {
            folderPath = filepath.Dir(file.Name) + "/"
            found = true
            break
        }
    }

    if !found {
        return fmt.Errorf("file %s not found in the ZIP archive", fileName)
    }

    // Extract the folder containing the file
    if err := extractFolder(&r.Reader, folderPath, dest); err != nil {
        return err
    }

    fmt.Printf("Extracted folder %s to %s\n", folderPath, dest)
    return nil
}

func main() {
    zipPath := "path/to/your/archive.zip"
    fileName := "yourfile.txt"
    dest := "path/to/extract/folder"

    if err := findFileAndExtractFolder(zipPath, fileName, dest); err != nil {
        fmt.Println("Error:", err)
    }
}
