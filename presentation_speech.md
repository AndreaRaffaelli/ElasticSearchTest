# Presentation

## Elasticsearch Scalability Through Replication

### 1. Introduction

Let's dive into Elasticsearch, but not as a database. It's a search engine, perfect for full-text search, log analysis and real-time data handling. The best part? It's scalable and flexible, which is exactly what we're focusing on today.

---

### 2. Architecture Overview

Elasticsearch is built on a distributed architecture, Apache Lucene. This means it uses clusters made up of multiple nodes. Each of these nodes can hold data, but the data is split into smaller chunks called shards, which are mapped on Lucene Indexes. Eeach shard gets replicated: this setup helps in both data storage and processing.

---

### 3. Sharding for Scalability

Sharding is a key feature for scalability in Elasticsearch. By breaking indexes, huge data collections, into shards, Elasticsearch can process these shards in parallel, making it incredibly efficient. Plus, if you need more power, you can add more nodes – that's elastic scaling in action, also known as horizontal scaling.

---

### 4. Replication for Reliability

Replication is all about reliability. Replica shards are copies of your data that provide failover protection in case a node goes down. They also help balance read loads across the cluster, and with multi-cluster replication, you can even replicate data across different geographic locations.

---

### 5. Data Consistency and Availability

Elasticsearch handles data consistency with *In Sync Replicas policy*, the same used in Apache Kafka and widely recognized as winnining. This means you can write on the system with a pool of $f$ replicas always in sync, this makes the cluster fault-tolerant till $f$ faults. Data is available immediately after writing, since the primary doesn't wait for replicas to acknowledge the write.

---

### 6. Drawbacks

Of course, there are some challenges. Elasticsearch doesn't use consistent hashing, which fixes a priori the number of partition available and if you need a new partitio makes you move all your data on a new index. 
Furthermore, the *ISRs policy* can lead in writes and reads that might not be acknowledged properly, and there can be misses in consistency. If the leader gets in a network parition, it keeps committing writes without having the chance to repair. 

It's important to be aware of these potential pitfalls.

---

### 7. Testing Replication and High Availability

Our testing focused on ensuring the cluster can handle replication and maintain high availability. We set up a cluster with 3 master nodes and 3 data nodes, using tools like EsRally for provisoning and testing and cURL for monitoring.

---

### 8. Replication Tests

We conducted several tests, starting with index creation and data insertion to check if documents were properly replicated across nodes. We also simulated a node failure to test failover, ensuring the data remained available and the cluster health was maintained. Once the failed node was restored, we confirmed that the cluster stabilized as expected.

---

### 9. High Availability Tests

High availability is crucial, so we tested how the cluster behaved with one or more nodes offline. Our goal was to ensure continuous data accessibility and consistency. We also performed high-volume read/write operations to see if the system balanced the load effectively across resources.

---

### 10. Test Execution and Results

Our test setup included three remote cloud machines, each with 16 GB of RAM, 8-core x86 processors, and 160 GB SSDs. We also used a small coordinator node for executing the tests via bash scripts and SSH commands. The results? All tests were successful and met our expectations, as the documentation promised.

---

### 11. Conclusion

That's a wrap! I really enjoyed putting together this presentation, and I hope you found it informative and engaging. Elasticsearch is a powerful tool, and understanding its scalability through replication can open up a lot of possibilities.

---

Thank you for your time!
