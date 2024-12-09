package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strings"
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
	http.HandleFunc("/", wrapHandler(fs))

	// Start the server
	fmt.Println("Server is running on http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func wrapHandler(h http.Handler) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		// Add custom header
		w.Header().Set("X-Custom-Header", "MyCustomValue")

		// Serve the file
		filePath := filepath.Join("custom_html_directory", r.URL.Path)
		content, err := ioutil.ReadFile(filePath)
		if err != nil {
			h.ServeHTTP(w, r)
			return
		}

		// Inject custom navigation and footer
		modifiedContent := injectCustomContent(content)

		w.Write(modifiedContent)
	}
}

func injectCustomContent(content []byte) []byte {
	customNav := `
		<nav style="background-color: #f1f1f1; padding: 10px;">
			<a href="/">Home</a>
			<a href="/about.html">About</a>
			<a href="/contact.html">Contact</a>
		</nav>
	`
	customFooter := `
		<footer style="background-color: #f1f1f1; padding: 10px; text-align: center;">
			<p>&copy; 2023 My Custom Website. All rights reserved.</p>
		</footer>
	`

	// Insert custom navigation after <body>
	bodyIndex := bytes.Index(content, []byte("<body>"))
	if bodyIndex != -1 {
		content = append(content[:bodyIndex+6], append([]byte(customNav), content[bodyIndex+6:]...)...)
	}

	// Insert custom footer before </body>
	bodyEndIndex := bytes.LastIndex(content, []byte("</body>"))
	if bodyEndIndex != -1 {
		content = append(content[:bodyEndIndex], append([]byte(customFooter), content[bodyEndIndex:]...)...)
	}

	return content
}
