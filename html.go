package main

import (
    "fmt"
    "log"
    "net/http"
    "os"
    "path/filepath"
)

func main() {
    // Get the current working directory
    cwd, err := os.Getwd()
    if err != nil {
        log.Fatal(err)
    }

    // Specify the custom directory to serve files from
    customDir := filepath.Join(cwd, "custom_html_directory")

    // Create a file server handler
    fs := http.FileServer(http.Dir(customDir))

    // Handle requests to the root URL
    http.Handle("/", http.StripPrefix("/", fs))

    // Start the server
    fmt.Println("Server is running on http://localhost:8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
