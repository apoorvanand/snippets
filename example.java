import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;

public class PropertiesExample {
    public static void main(String[] args) throws IOException {
        // Load the properties file
        Properties props = new Properties();
        FileInputStream fis = new FileInputStream("path/to/properties/file.properties");
        props.load(fis);

        // Iterate over the property names and set them as environment variables
        for (Object key : props.keySet()) {
            String keyStr = (String) key;
            String value = props.getProperty(keyStr);
            System.setEnvironmentVariable(keyStr, value);
        }
    }
}
