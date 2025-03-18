To connect to AWS MSK using AWS SDK v2 with Pod Identity authorization in AWS EKS, you'll need to use the appropriate environment variables that are automatically injected by the EKS Pod Identity Agent. Here's a Java implementation that works with the EKS Pod Identity mechanism:

## Producer Code

```java
package com.example.msk;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;
import software.amazon.awssdk.services.sts.StsClient;
import software.amazon.awssdk.services.sts.model.GetCallerIdentityResponse;

import java.util.Properties;
import java.util.concurrent.ExecutionException;

public class MSKProducer {
    private static final String TOPIC = "my-topic";
    private static final String BOOTSTRAP_SERVERS = "BOOTSTRAP_SERVER_ENDPOINT:9098";

    public static void main(String[] args) {
        // Verify AWS identity using Pod Identity
        try (StsClient stsClient = StsClient.create()) {
            GetCallerIdentityResponse identity = stsClient.getCallerIdentity();
            System.out.println("Using IAM identity: " + identity.arn());
        }

        // Configure Kafka producer with IAM authentication
        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, BOOTSTRAP_SERVERS);
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        
        // MSK IAM authentication settings
        props.put("security.protocol", "SASL_SSL");
        props.put("sasl.mechanism", "AWS_MSK_IAM");
        props.put("sasl.jaas.config", "software.amazon.msk.auth.iam.IAMLoginModule required;");
        props.put("sasl.client.callback.handler.class", "software.amazon.msk.auth.iam.IAMClientCallbackHandler");

        try (KafkaProducer producer = new KafkaProducer<>(props)) {
            for (int i = 0; i  record = new ProducerRecord<>(TOPIC, key, value);
                producer.send(record, (metadata, exception) -> {
                    if (exception == null) {
                        System.out.printf("Produced record to topic %s partition %s offset %s%n",
                                metadata.topic(), metadata.partition(), metadata.offset());
                    } else {
                        System.err.println("Failed to produce to Kafka: " + exception.getMessage());
                        exception.printStackTrace();
                    }
                }).get();
            }
            
            producer.flush();
            System.out.println("10 messages were produced to topic " + TOPIC);
        } catch (InterruptedException | ExecutionException e) {
            System.err.println("Error producing messages: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

## Consumer Code

```java
package com.example.msk;

import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.serialization.StringDeserializer;
import software.amazon.awssdk.services.sts.StsClient;
import software.amazon.awssdk.services.sts.model.GetCallerIdentityResponse;

import java.time.Duration;
import java.util.Collections;
import java.util.Properties;

public class MSKConsumer {
    private static final String TOPIC = "my-topic";
    private static final String BOOTSTRAP_SERVERS = "BOOTSTRAP_SERVER_ENDPOINT:9098";
    private static final String GROUP_ID = "my-consumer-group";

    public static void main(String[] args) {
        // Verify AWS identity using Pod Identity
        try (StsClient stsClient = StsClient.create()) {
            GetCallerIdentityResponse identity = stsClient.getCallerIdentity();
            System.out.println("Using IAM identity: " + identity.arn());
        }

        // Configure Kafka consumer with IAM authentication
        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, BOOTSTRAP_SERVERS);
        props.put(ConsumerConfig.GROUP_ID_CONFIG, GROUP_ID);
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        
        // MSK IAM authentication settings
        props.put("security.protocol", "SASL_SSL");
        props.put("sasl.mechanism", "AWS_MSK_IAM");
        props.put("sasl.jaas.config", "software.amazon.msk.auth.iam.IAMLoginModule required;");
        props.put("sasl.client.callback.handler.class", "software.amazon.msk.auth.iam.IAMClientCallbackHandler");

        try (KafkaConsumer consumer = new KafkaConsumer<>(props)) {
            consumer.subscribe(Collections.singletonList(TOPIC));
            System.out.println("Subscribed to topic: " + TOPIC);

            while (true) {
                ConsumerRecords records = consumer.poll(Duration.ofMillis(100));
                for (ConsumerRecord record : records) {
                    System.out.printf("Consumed record with key %s and value %s, partition %s, offset %s%n",
                            record.key(), record.value(), record.partition(), record.offset());
                }
            }
        }
    }
}
```

## Maven Dependencies

Add these dependencies to your `pom.xml`:

```xml

    
    
        software.amazon.awssdk
        sts
        2.21.30
    
    
    
    
        org.apache.kafka
        kafka-clients
        3.5.1
    
    
    
    
        software.amazon.msk
        aws-msk-iam-auth
        1.1.6
    
    
    
    
        org.slf4j
        slf4j-api
        2.0.9
    
    
        org.slf4j
        slf4j-simple
        2.0.9
    

```

The AWS SDK v2 for Java automatically uses the Pod Identity credentials through the default credential provider chain. When your application runs in an EKS pod with Pod Identity configured, the EKS Pod Identity Agent injects the necessary environment variables (`AWS_CONTAINER_CREDENTIALS_FULL_URI` and `AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE`), and the AWS SDK will automatically use these to obtain temporary credentials from the EKS Pod Identity Agent REST endpoint.

Make sure you're using AWS SDK for Java v2 version 2.21.30 or later, as this version supports EKS Pod Identity.

Citations:
[1] https://docs.aws.amazon.com/eks/latest/userguide/pod-id-minimum-sdk.html
[2] https://sdk.amazonaws.com/java/api/latest/software/amazon/awssdk/services/eks/model/PodIdentityAssociation.html
[3] https://aws.amazon.com/blogs/containers/amazon-eks-pod-identity-a-new-way-for-applications-on-eks-to-obtain-iam-credentials/
[4] https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html
[5] https://www.pulumi.com/registry/packages/aws/api-docs/eks/podidentityassociation/
[6] https://stackoverflow.com/questions/69819087/how-connect-to-msk-cluster-from-eks-cluster
[7] https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/deploy-a-sample-java-microservice-on-amazon-eks-and-expose-the-microservice-using-an-application-load-balancer.html
[8] https://github.com/aws/aws-sdk-js/issues/4566
[9] https://stackoverflow.com/questions/66712022/accessing-msk-cluster-from-a-service-running-in-eks
[10] https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials.html
[11] https://sdk.amazonaws.com/java/api/latest/
[12] https://github.com/aws/aws-sdk-java/issues/3062
[13] https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/home.html
[14] https://github.com/aws/aws-msk-iam-auth
[15] https://stackoverflow.com/questions/74407121/aws-msk-iam-authentication-failure-access-denied-spring-boot
[16] https://migratorydata.com/docs/server/deployment/aws/eks-msk/
[17] https://repost.aws/knowledge-center/eks-pods-iam-role-service-accounts

---
```
<dependencies>
    <!-- AWS SDK v2 Core -->
    <dependency>
        <groupId>software.amazon.awssdk</groupId>
        <artifactId>sts</artifactId>
        <version>2.21.30</version>
    </dependency>
    
    <!-- Apache Kafka Client -->
    <dependency>
        <groupId>org.apache.kafka</groupId>
        <artifactId>kafka-clients</artifactId>
        <version>3.5.1</version>
    </dependency>
    
    <!-- AWS MSK IAM Auth Library -->
    <dependency>
        <groupId>software.amazon.msk</groupId>
        <artifactId>aws-msk-iam-auth</artifactId>
        <version>1.1.6</version>
    </dependency>
    
    <!-- SLF4J for logging -->
    <dependency>
        <groupId>org.slf4j</groupId>
        <artifactId>slf4j-api</artifactId>
        <version>2.0.9</version>
    </dependency>
    <dependency>
        <groupId>org.slf4j</groupId>
        <artifactId>slf4j-simple</artifactId>
        <version>2.0.9</version>
    </dependency>
</dependencies>

```
