func Unzip(src, dest string) error {
    r, err := zip.OpenReader(src)
    if err != nil {
        return err
    }
    defer r.Close()

    os.MkdirAll(dest, 0755)

    for _, f := range r.File {
        fpath := filepath.Join(dest, f.Name)

        // Check for ZipSlip vulnerability
        if !strings.HasPrefix(fpath, filepath.Clean(dest)+string(os.PathSeparator)) {
            return fmt.Errorf("invalid file path: %s", fpath)
        }

        if f.FileInfo().IsDir() {
            os.MkdirAll(fpath, os.ModePerm)
            continue
        }

        if err = os.MkdirAll(filepath.Dir(fpath), os.ModePerm); err != nil {
            return err
        }

        outFile, err := os.OpenFile(fpath, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, f.Mode())
        if err != nil {
            return err
        }

        rc, err := f.Open()
        if err != nil {
            outFile.Close()
            return err
        }

        _, err = io.Copy(outFile, rc)
        outFile.Close()
        rc.Close()

        if err != nil {
            return err
        }
    }
    return nil
}
