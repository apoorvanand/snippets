package main

import (
	"fmt"
	"html/template"
	"log"
	"net/http"
	"os"
	"path/filepath"
)

type PageWrapper struct {
	Title   string
	Content template.HTML
}

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

		// Capture the original response
		crw := &customResponseWriter{ResponseWriter: w}
		h.ServeHTTP(crw, r)

		// Wrap the content with navigation and footer
		wrapper := PageWrapper{
			Title:   "My Custom Website",
			Content: template.HTML(crw.body),
		}

		tmpl := template.Must(template.New("wrapper").Parse(`
			<!DOCTYPE html>
			<html>
			<head>
				<title>{{.Title}}</title>
				<style>
					nav { background-color: #f1f1f1; padding: 10px; }
					nav a { margin-right: 10px; }
					footer { background-color: #f1f1f1; padding: 10px; text-align: center; }
				</style>
			</head>
			<body>
				<nav>
					<a href="/">Home</a>
					<a href="/about.html">About</a>
					<a href="/contact.html">Contact</a>
				</nav>
				<main>
					{{.Content}}
				</main>
				<footer>
					<p>&copy; 2023 My Custom Website. All rights reserved.</p>
				</footer>
			</body>
			</html>
		`))

		tmpl.Execute(w, wrapper)
	}
}

type customResponseWriter struct {
	http.ResponseWriter
	body string
}

func (crw *customResponseWriter) Write(b []byte) (int, error) {
	crw.body += string(b)
	return len(b), nil
}
