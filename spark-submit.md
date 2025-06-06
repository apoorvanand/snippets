Great! If you're running a **PySpark job** with `spark-submit` in **cluster mode**, here’s how to do it depending on your **cluster manager** (e.g., YARN, Standalone, Kubernetes).

---

## ✅ General Syntax for PySpark (cluster mode):

```bash
spark-submit \
  --master <cluster-manager> \
  --deploy-mode cluster \
  --name my-pyspark-job \
  --executor-memory 4G \
  --num-executors 4 \
  --executor-cores 2 \
  your_script.py \
  [your-script-args]
```

---

## 🧩 1. Example: Cluster Mode on Spark Standalone

```bash
spark-submit \
  --master spark://<spark-master-host>:7077 \
  --deploy-mode cluster \
  --name pyspark-cluster-job \
  --executor-memory 2G \
  --num-executors 3 \
  --executor-cores 2 \
  my_pyspark_script.py
```

> Your script must be accessible on the cluster (i.e., use full path or submit with `--archives` or `--files` if needed).

---

## 🧩 2. Example: Cluster Mode on YARN

```bash
spark-submit \
  --master yarn \
  --deploy-mode cluster \
  --name pyspark-yarn-job \
  --executor-memory 2G \
  --num-executors 4 \
  --executor-cores 2 \
  my_pyspark_script.py
```

> You must run this from a node that can talk to YARN (e.g., an edge node or dev machine with Hadoop config).

---

## 🧩 3. Example: Cluster Mode on Kubernetes

```bash
spark-submit \
  --master k8s://https://<k8s-api>:6443 \
  --deploy-mode cluster \
  --name pyspark-k8s-job \
  --conf spark.kubernetes.container.image=your-docker-image \
  --conf spark.executor.instances=3 \
  local:///opt/spark/my_pyspark_script.py
```

> Your PySpark script must be **inside the Docker image** if running in Kubernetes `cluster` mode.

---

## 🛠️ Notes for PySpark Jobs

### ✅ Dependencies?

* Use `--py-files` for zipped `.py` modules.
* Use `--files` to ship configs.
* Use `--archives` to ship virtualenv or Conda environments (esp. for Python 3).

### ✅ Example with dependencies:

```bash
spark-submit \
  --master yarn \
  --deploy-mode cluster \
  --py-files my_libs.zip \
  --files config.yaml \
  my_pyspark_script.py arg1 arg2
```

---

## 🔍 Logs and Monitoring

* **YARN:** use `yarn logs -applicationId <id>`
* **Standalone:** visit `http://<master>:8080`
* **K8s:** `kubectl logs` + Spark history server

