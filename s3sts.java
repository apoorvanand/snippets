import software.amazon.awssdk.auth.credentials.AwsBasicCredentials;
import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider;
import software.amazon.awssdk.regions.Region;   

import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.PutObjectRequest;   

import software.amazon.awssdk.services.sts.StsClient;
import software.amazon.awssdk.services.sts.model.AssumeRoleRequest;
import software.amazon.awssdk.services.sts.model.AssumeRoleResponse;
import software.amazon.awssdk.services.sts.model.Credentials;

import   
 java.io.File;

public class S3UploadWithRole {
    public static void main(String[] args) {
        String roleArn = "arn:aws:iam::your-account-id:role/YourRole";
        String roleSessionName = "MySession";
        String bucketName = "your-bucket-name";
        String keyName = "your-file-key";
        String filePath = "/path/to/your/file";

        // Assume role
        StsClient stsClient = StsClient.builder().region(Region.US_EAST_1).build(); // Replace with your desired region
        AssumeRoleRequest assumeRoleRequest = AssumeRoleRequest.builder()
                .roleArn(roleArn)
                .roleSessionName(roleSessionName)
                .build();
        AssumeRoleResponse assumeRoleResponse = stsClient.assumeRole(assumeRoleRequest);   

        Credentials credentials = assumeRoleResponse.credentials();   


        // Create S3 client with temporary credentials
        S3Client s3Client = S3Client.builder()
                .region(Region.US_EAST_1) // Replace with your desired region
                .credentialsProvider(StaticCredentialsProvider.create(
                        AwsBasicCredentials.create(credentials.accessKeyId(), credentials.secretAccessKey(), credentials.sessionToken())))
                .build();

        // Upload file
        try {
            PutObjectRequest putObjectRequest = PutObjectRequest.builder()
                    .bucket(bucketName)
                    .key(keyName)
                    .build();

            s3Client.putObject(putObjectRequest, RequestBody.fromFile(new   
 File(filePath)));
            System.out.println("File uploaded successfully");
        } catch (Exception e) {
            System.err.println("Error uploading file: " + e.getMessage());
        }
    }
}
