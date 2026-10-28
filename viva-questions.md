# Viva Questions and Answers: Web Log Analysis

1. **What is a web server log?**  
   A text record of requests handled by a web server, often including IP address, timestamp, request path, HTTP status and response size.

2. **Why analyze web logs?**  
   To understand traffic, identify popular pages, count errors and spot unusual patterns.

3. **What is Big Data?**  
   Data whose volume, velocity or variety can make conventional processing difficult; suitable tools depend on the scale and task.

4. **What is MapReduce?**  
   A programming model that maps input records to intermediate key-value pairs and reduces values with the same key.

5. **What does the mapper do in this project?**  
   It emits a selected field such as a page path as the key and `1` as the value for each request.

6. **What does the reducer do?**  
   It sums values for identical keys to produce counts.

7. **What is an HTTP status code?**  
   A three-digit server response code. For example, 200 generally means success, 404 means not found, and 500 indicates a server error.

8. **What is the difference between 4xx and 5xx?**  
   4xx codes indicate a client-side request error; 5xx codes indicate a server-side error.

9. **Why are invalid log lines skipped?**  
   They do not match the expected format and cannot be reliably parsed into the required fields.

10. **Which technologies are used?**  
    Python, Streamlit, pandas and Matplotlib. Hadoop Streaming is described as an optional distributed execution extension.

11. **Does the main application run on Hadoop?**  
    No. It demonstrates MapReduce-style aggregation locally in Python. A configured Hadoop Streaming environment is required for actual Hadoop execution.

12. **What are the project outputs?**  
    Request totals, unique IP count, error count, bytes transferred, popular pages, status-code charts and downloadable CSVs.

13. **What is the limitation of the sample data?**  
    It is synthetic and small, so it does not represent real production traffic or prove distributed scalability.

14. **How can this project be extended?**  
    Run mapper/reducer scripts using Hadoop Streaming, use a larger log file, and add time-series or anomaly analysis.

15. **What is the conclusion?**  
    Web logs can be parsed and aggregated to reveal useful traffic patterns. MapReduce offers a model for scaling such aggregation to distributed data processing.
