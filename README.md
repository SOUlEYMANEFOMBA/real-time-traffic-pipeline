# 🚦 Real-Time Traffic Pipeline

## 🧠 Problem Statement

Urban road congestion is a growing challenge in major cities, leading to significant time loss, increased fuel consumption, and air pollution.  
Access to **real-time traffic data** is essential for smarter decision-making, optimizing travel routes, and improving urban transport policies.

## 🎯 Project Objective

This project aims to build an **end-to-end real-time data pipeline** that collects, processes, stores, and visualizes traffic data using the **TomTom Traffic API**.

The pipeline will allow users to:
- Monitor real-time traffic conditions
- Identify congestion hotspots
- Generate actionable insights via a live dashboard

---

## 🔧 Tech Stack

| Stage                      | Technology                          |
|---------------------------|--------------------------------------|
| Data Ingestion            | Kafka + Python Producer (TomTom API)|
| Data Processing           | Apache Spark                         |
| Storage                   | Google BigQuery                      |
| Data Transformation       | dbt Cloud                            |
| Data Visualization        | Looker Studio (or Power BI)          |
| Orchestration             | Apache Airflow (Dockerized)          |
| Containerization          | Docker + Docker Compose              |

---

## 🗺️ Architecture Diagram

![architecture](./assets/architecture.png)

---

## 🚀 Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/<your-user>/real-time-traffic-pipeline.git
cd real-time-traffic-pipeline

# 2. Start the Dockerized environment
docker-compose up --build

# 3. Trigger the main DAG via Airflow UI
# Access at: http://localhost:8080

# 4. View your dashboard in Looker Studio (connected to BigQuery)
