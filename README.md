#  EnergySentinel – Real-Time Energy Anomaly Detection Platform

An end-to-end **real-time Azure Data Engineering platform** that simulates industrial energy monitoring using a modern streaming lakehouse architecture with **live anomaly detection powered by a pre-trained Machine Learning model**.

---

#  Project Overview

This project demonstrates how to build a **production-style streaming data platform** on Microsoft Azure.

The system simulates industrial sensor telemetry in real time and processes it to:

- Monitor industrial equipment continuously
- Validate incoming streaming data
- Build a Delta Lakehouse using Medallion Architecture
- Perform real-time anomaly detection using a pre-trained Machine Learning model
- Enable business analytics and interactive dashboards

---

# 🏗️ Architecture

![Architecture](https://github.com/AhmedRefat1412/EnergySentinel-Real-Time-Energy-Anomaly-Detection-Platform-on-Azure/blob/main/EnergySentinel%20.drawio.png)

---

# ⚡ Streaming Pipeline (Core Flow)

##  Data Simulation

Azure Function simulates industrial machine telemetry every second.

Generated metrics include:

- Voltage
- Current
- Power Consumption
- Temperature
- Frequency
- Power Factor

Random anomalies are intentionally injected into the generated telemetry to simulate realistic equipment failures and evaluate the anomaly detection model.

---

##  Pipeline Flow

### 1- Data Ingestion (Azure Event Hubs)

- Azure Function publishes telemetry events.
- Azure Event Hubs receives the streaming data.
- Serves as the real-time messaging layer for the platform.

---

### 2- Stream Processing (Azure Databricks)

PySpark Structured Streaming consumes events from Azure Event Hubs.

Each incoming micro-batch is processed in parallel:

- Raw events are stored in the **Bronze Layer**.
- The pre-trained LightGBM model is loaded from Azure Data Lake Storage.
- Real-time anomaly predictions are generated.
- Prediction results are stored in the **Platinum Layer**.

This design enables simultaneous raw data ingestion and machine learning inference without interrupting the streaming pipeline.

---

### 3- Silver Layer

The Silver notebook reads data from the Bronze layer and applies Data Quality validation.

Validation includes:

- Null checks
- Duplicate removal
- Range validation
- Timestamp validation
- Sensor validation

Invalid records are redirected to a **Quarantine** table, while clean records are promoted to the Silver layer.

---

### 4- Gold Layer

Business-ready analytical tables are generated from the Silver layer.

Generated tables include:

- Plant Summary
- Sensor Summary
- Hourly Trends

These tables are optimized for reporting and analytics.

---

### 5- Query Layer

Business datasets are exposed using:

- Synapse Serverless SQL

---

### 6- Visualization

Power BI connects to Synapse Serverless SQL to provide interactive dashboards for monitoring industrial equipment and energy consumption in real time.

---

# 🧠 Machine Learning

**Model**

LightGBM Classifier

The anomaly detection model was trained **offline** using historical sensor data collected from the streaming pipeline.

After collecting enough telemetry in the Bronze layer, the historical data was exported as a CSV dataset and used locally to train the LightGBM model.

Once training was completed:

- The trained model was serialized
- Uploaded to Azure Data Lake Storage
- Loaded automatically by Azure Databricks during stream processing

The streaming pipeline performs **online inference only**.

No online retraining is executed.

### 🎯 Purpose

- Detect abnormal equipment behavior
- Predict potential equipment failures
- Support predictive maintenance

---

# 🔄 Offline Training Workflow

The anomaly detection model is trained only once using historical streaming data.

Workflow:

1. Streaming data is collected in local by using consumer script 
2. Historical data is exported as a CSV dataset.
3. The LightGBM model is trained locally.
4. The trained model is uploaded to Azure Data Lake Storage.
5. Azure Databricks loads the model during stream processing.
6. Every incoming streaming event is evaluated in real time without retraining.

This approach separates model training from online inference, following common production Machine Learning practices.

---

# 🏗️ Medallion Architecture

## 🥉 Bronze Layer

- Raw streaming events from Azure Event Hubs
- Stored as Delta tables
- No transformations applied
- Acts as the historical source for downstream processing and model training

---

## 🥈 Silver Layer

Validated and trusted datasets.

Responsibilities:

- Data cleaning
- Schema enforcement
- Duplicate removal
- Data Quality validation
- Invalid records moved to Quarantine

---

## 🥇 Gold Layer

Business-ready analytical datasets.

Includes:

- Plant KPIs
- Sensor KPIs
- Hourly Aggregations

Optimized for reporting and business analytics.

---

## 💎 Platinum Layer

Streaming Machine Learning predictions.

Each incoming streaming event is evaluated using the pre-trained LightGBM model.

Stores:

- Prediction
- Prediction Confidence
- Anomaly Status

---

# ✅ Data Quality Framework

Every incoming event passes through automated validation before being promoted to the Silver layer.

Validation includes:

- Missing values
- Duplicate events
- Invalid sensor IDs
- Invalid timestamps
- Out-of-range values
- Schema validation

Invalid records are automatically written into a Quarantine table for further investigation.

---

#  Orchestration (Azure Data Factory)

Azure Data Factory orchestrates the platform by:

- Scheduling the Silver notebook
- Scheduling the Gold notebook

---

# 📊 Real-Time Dashboard (Power BI)

Dashboard includes:

- Live Energy Consumption
- Plant Performance
- Temperature Monitoring
- Voltage Trends
- Current Trends
- Equipment Health
- Anomaly Detection
- Hourly Analytics

---

#  Storage & Analytics Layer

- Azure Data Lake Storage Gen2
- Delta Lake
- Azure Databricks
- Synapse Serverless SQL
- Power BI

---

# 🛠️ Tech Stack

- Microsoft Azure
- Azure Functions
- Azure Event Hubs
- Azure Databricks
- PySpark Structured Streaming
- Delta Lake
- Azure Data Lake Storage Gen2
- Azure Data Factory
- Synapse Serverless SQL
- Power BI
- LightGBM
- Python
- Git
- GitHub Actions

