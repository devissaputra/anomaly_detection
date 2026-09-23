# Ethics and Limits

This project uses a public handwritten-digit dataset and does not make decisions about people.

The main caution is methodological. An anomaly score does not mean that an example is wrong, dangerous, or invalid. It only means that the model finds it unusual relative to the training data.

In a real anomaly-detection system, thresholds should be chosen with the cost of false alarms and missed anomalies in mind.
