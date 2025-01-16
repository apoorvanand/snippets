package main

import (
    "archive/zip"
    "io"
    "net/http"
    "os"
    "path/filepath"
)

func main() {
    http.HandleFunc("/upload", handleUpload)
    http.ListenAndServe(":8080", nil)
}

func handleUpload(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    file, header, err := r.FormFile("zipfile")
    if err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }
    defer file.Close()

    destPath := r.FormValue("destination")
    if destPath == "" {
        http.Error(w, "Destination path is required", http.StatusBadRequest)
        return
    }

    tempFile, err := os.CreateTemp("", "upload-*.zip")
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    defer os.Remove(tempFile.Name())
    defer tempFile.Close()

    _, err = io.Copy(tempFile, file)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    err = extractAndReplace(tempFile.Name(), destPath)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    w.WriteHeader(http.StatusOK)
    w.Write([]byte("File extracted and contents replaced successfully"))
}

func extractAndReplace(zipPath, destPath string) error {
    err := os.RemoveAll(destPath)
    if err != nil {
        return err
    }

    err = os.MkdirAll(destPath, 0755)
    if err != nil {
        return err
    }

    zipReader, err := zip.OpenReader(zipPath)
    if err != nil {
        return err
    }
    defer zipReader.Close()

    for _, file := range zipReader.File {
        filePath := filepath.Join(destPath, file.Name)

        if file.FileInfo().IsDir() {
            os.MkdirAll(filePath, file.Mode())
            continue
        }

        err = os.MkdirAll(filepath.Dir(filePath), 0755)
        if err != nil {
            return err
        }

        dstFile, err := os.OpenFile(filePath, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, file.Mode())
        if err != nil {
            return err
        }
        defer dstFile.Close()

        srcFile, err := file.Open()
        if err != nil {
            return err
        }
        defer srcFile.Close()

        _, err = io.Copy(dstFile, srcFile)
        if err != nil {
            return err
        }
    }

    return nil
}
