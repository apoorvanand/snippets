javac -cp "$SPARK_JARS" -d build/classes src/com/example/MySparkApp.java
jar cvf my-spark-app.jar -C build/classes/ .
spark-submit --class com.example.MySparkApp --master local[2] my-spark-app.jar
