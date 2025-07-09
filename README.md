# aiproject_KIPI_BY_TANISH

# 💡 SQL Insight Assistant

This Python-based project provides an intelligent assistant that:

- 🧠 Explains SQL queries using **Google Gemini (Gemini Pro)**
- 🧼 Lints queries for common anti-patterns (like `SELECT *`)
- 💸 Estimates the query cost using **Snowflake's EXPLAIN plan**

---

## 🚀 Features

- **AI-Powered SQL Explanation**  
  Uses Google’s Gemini model to explain SQL in plain English.

- **Basic SQL Linting**  
  Flags common issues like missing `WHERE` clause or cross joins.

- **Snowflake Query Cost Estimation**  
  Uses `EXPLAIN` plans to estimate how costly a query is based on number of execution steps.

---

## 🛠️ Setup Instructions

### 1. 🔑 Prerequisites

- Python 3.8+
- A **Snowflake account** with access credentials
- A **Google Cloud API key** with access to the **Generative Language API (Gemini)**

### 2. 📦 Install Dependencies

```bash
pip install google-generativeai snowflake-connector-python sqlparse
