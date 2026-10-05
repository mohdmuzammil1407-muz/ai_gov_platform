
# AI Digital Governance Platform – Complete Technical Viva Guide

## 1. Project Overview

The AI Digital Governance Platform is an intelligent complaint management system that automatically classifies complaints, assigns departments, and prioritizes cases using Artificial Intelligence and Machine Learning.

This system integrates:

- React Frontend
- Flask Backend
- MongoDB Database
- AI Models using TF‑IDF, FAISS, Sentence Transformers, and Logistic Regression

---

## 2. System Architecture

### 3‑Layer Architecture

Frontend Layer:
- Built using React.js
- Provides user interface for complaint submission
- Staff and admin dashboards

Backend Layer:
- Built using Flask (Python)
- Handles API requests
- Connects AI models
- Stores data in MongoDB

Database Layer:
- MongoDB NoSQL database
- Stores users, complaints, staff, departments

AI Layer:
- Department classification model
- Semantic similarity search using FAISS
- Priority prediction using Logistic Regression

Architecture Flow:

User → Frontend → Flask Backend → AI Model → MongoDB → Staff Dashboard

---

## 3. Complete Workflow

Step 1: User submits complaint

Step 2: Backend receives complaint text

Step 3: AI department classification begins

Step 4: Text converted into vector using TF‑IDF

Step 5: Semantic similarity calculated using FAISS index

Step 6: Best matching department predicted

Step 7: Priority prediction model assigns priority

Step 8: Complaint stored in MongoDB

Step 9: Staff dashboard displays complaint

Step 10: Staff resolves complaint

---

## 4. Artificial Intelligence Models Used

This project uses multiple AI models:

Model 1: Department Classification

Algorithms Used:
- TF‑IDF Vectorization
- FAISS Similarity Search
- Sentence Transformer (MiniLM‑L6‑v2)

Model 2: Priority Prediction

Algorithm Used:
- Logistic Regression

---

## 5. Dataset Used

Dataset file:
backend/ai/complaints_dataset.csv

Structure:

text, department

Example:

"Street light not working", Electricity
"Garbage not collected", Sanitation

Priority dataset:

backend/ai/priority_dataset.csv

Structure:

description, priority

Example:

"Fire accident", High
"Road pothole", Medium

---

## 6. Model Training Process

Department Model Training:

Step 1: Load dataset

Step 2: Text preprocessing

Step 3: TF‑IDF vectorization

Formula:

TF‑IDF = Term Frequency × Inverse Document Frequency

Step 4: Convert text to vector form

Step 5: Store vectors in FAISS index

Step 6: Save model components:

- tfidf.pkl
- faiss_index.pkl
- labels.pkl

Semantic Model Training:

Uses Sentence Transformer:

Model: all‑MiniLM‑L6‑v2

This converts text into 384‑dimensional vectors

Stored in FAISS index

---

## 7. Priority Model Training

Uses Logistic Regression

Steps:

Step 1: Load priority dataset

Step 2: Convert text using TF‑IDF

Step 3: Train Logistic Regression model

Step 4: Save model

priority_model.pkl

---

## 8. Prediction Process

Department Prediction:

User complaint → TF‑IDF → FAISS search → best matching department

Priority Prediction:

Complaint → TF‑IDF → Logistic Regression → priority level

---

## 9. Algorithms Used

TF‑IDF Vectorizer

Converts text into numerical vectors

FAISS (Facebook AI Similarity Search)

Performs fast similarity search

Sentence Transformer (BERT‑based model)

Creates semantic embeddings

Logistic Regression

Predicts complaint priority

---

## 10. Train Test Concept

Dataset split concept:

Training Data: used to train model

Testing Data: used to evaluate accuracy

Training builds prediction capability

Testing evaluates performance

---

## 11. Model Accuracy

Department model accuracy depends on dataset similarity matching.

Priority model accuracy typically:

85% to 95%

Factors affecting accuracy:

Dataset size
Dataset quality
Feature extraction quality

---

## 12. MongoDB Database Structure

Collections:

users

staff

complaints

Complaint document:

complaint_id
text
department
priority
status

---

## 13. Backend AI Integration

Backend file:

backend/ai/predict.py

Loads trained models

Uses model.predict()

Returns predicted department

---

## 14. Technologies Used

Frontend:
React
Tailwind CSS

Backend:
Python
Flask

AI:
Scikit‑learn
TF‑IDF
FAISS
Sentence Transformers

Database:
MongoDB

---

## 15. Why these Algorithms Used

TF‑IDF:

Simple and effective text vectorization

FAISS:

Fast similarity search

Sentence Transformer:

Captures semantic meaning

Logistic Regression:

Fast and accurate classification

---

## 16. Advantages

Fully automated complaint classification

Fast processing

High accuracy

Scalable system

Real‑world AI implementation

---

## 17. Viva Questions and Answers

Q: Which AI algorithms used?
A: TF‑IDF, FAISS, Sentence Transformer, Logistic Regression

Q: Why TF‑IDF used?
A: Converts text into numerical vectors

Q: Why FAISS used?
A: Fast similarity search

Q: Which ML model used?
A: Logistic Regression

Q: Which NLP model used?
A: Sentence Transformer

---

## 18. Conclusion

This project demonstrates real‑world application of Artificial Intelligence in governance systems.

It integrates:

Machine Learning
Natural Language Processing
Semantic Search
Database Integration

to create a fully intelligent complaint management system.
