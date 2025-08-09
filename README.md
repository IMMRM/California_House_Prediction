# California Housing Price Prediction 🏡

## 📌 Project Overview  
This project predicts **California housing prices** using a **Machine Learning pipeline** with automated **data ingestion, preprocessing, training, and retraining**. It supports **real-time retraining** when new data arrives in the PostgreSQL database.  

---

## 🛠️ Tech Stack  
- **Python** – Core programming language  
- **FastAPI** – API for triggering retraining  
- **PostgreSQL (AWS RDS)** – Data storage  
- **scikit-learn** – Model building  
- **MLflow** – Experiment tracking  
- **DVC & DagsHub** – Data & model versioning  
- **Docker** – Containerization  
- **Grafana** – Monitoring model metrics  
- **GitHub Actions** – CI/CD automation  

## ⚙️ Workflow  

1. **Data Extraction**  
   - Pulls housing data from an external source into **AWS PostgreSQL**.  

2. **Data Preprocessing**  
   - Cleans, scales, and handles outliers.  

3. **Model Training**  
   - Trains a regression model and saves it with a timestamp.  
   - Tracks experiments in **MLflow**.  
   - Pushes models to **DVC/DagsHub**.  

4. **Retraining Trigger**  
   - When new data arrives in PostgreSQL, a FastAPI endpoint triggers retraining automatically.  

5. **Monitoring**  
   - Metrics visualized in **Grafana**.  

## 🔄 CI/CD & Version Control  

- **GitHub Repository** – Stores project code.  
- **DagsHub** – Stores datasets & models with versioning.  
- **DockerHub** – Hosts project container image.  
- **GitHub Actions** – Automates testing & deployment.  

---

## 🚀 How to Run  

1. **Clone the repository**  
   ```bash
   git clone <repo-url>
   cd california_housing_prediction
2. **Install dependencies**
    pip install -r requirements.txt
3. **Run the FastAPI Server**
    uvicorn app:app --reload

