import google.generativeai as genai
import snowflake.connector
import os
import sqlparse

# --- CONFIGURATION ---

# Securely load your Gemini API key from environment variable
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    print("❌ Error: GOOGLE_API_KEY environment variable is not set.")
    exit()

# Snowflake credentials
SNOWFLAKE_ACCOUNT = "zbymzkr-jmb03693"
SNOWFLAKE_USER = 'tanish123'
SNOWFLAKE_PASSWORD = 'Boomchika@#123'
SNOWFLAKE_WAREHOUSE = 'COMPUTE_WH'
SNOWFLAKE_DATABASE = 'GARDEN_PLANTS'
SNOWFLAKE_SCHEMA = 'FRUITS'

# --- FUNCTIONS ---

def connect_snowflake():
    """Establish connection to Snowflake."""
    return snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )

def explain_sql(sql):
    """Explains an SQL query using Google's Gemini model."""
    prompt = f"Explain the following SQL query in simple English:\n{sql}"
    try:
        # CORRECTED: Use a current model name
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error getting explanation: {str(e)}"

def estimate_cost(conn, sql):
    """Estimates cost of query based on EXPLAIN plan steps."""
    try:
        cursor = conn.cursor(snowflake.connector.DictCursor)
        cursor.execute(f"EXPLAIN {sql}")
        plan = cursor.fetchall()
        num_steps = len(plan)

        # Simple estimation based on number of steps
        if num_steps < 5:
            return f"Estimated Cost Category: 🟢 Low (based on {num_steps} steps)"
        elif 5 <= num_steps < 15:
            return f"Estimated Cost Category: 🟡 Medium (based on {num_steps} steps)"
        else:
            return f"Estimated Cost Category: 🔴 High (based on {num_steps} steps)"
    except Exception as e:
        return f"Error estimating cost: {str(e)}"

def lint_sql(sql):
    """Basic SQL linting for common inefficiencies."""
    issues = []
    if "SELECT *" in sql.upper():
        issues.append("⚠️ Avoid using 'SELECT *'. Specify needed columns.")
    if "JOIN" in sql.upper() and " ON " not in sql.upper():
        issues.append("⚠️ JOIN without ON clause may result in a cartesian product.")
    if "WHERE" not in sql.upper():
        issues.append("⚠️ Query lacks a WHERE clause — may cause full table scan.")
    return issues if issues else ["✅ No major issues detected."]

# --- MAIN EXECUTION ---

if __name__ == "__main__":
    user_query = input("Enter your SQL query:\n")

    print("\n--- 🧠 AI Explanation ---")
    print(explain_sql(user_query))

    print("\n--- 🧼 Linting Feedback ---")
    for issue in lint_sql(user_query):
        print("-", issue)

    print("\n--- 💸 Query Cost Estimate ---")
    try:
        with connect_snowflake() as conn:
            print(estimate_cost(conn, user_query))
    except Exception as e:
        print(f"Error connecting to Snowflake: {str(e)}")