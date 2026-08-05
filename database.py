import mysql.connector

# -----------------------------
# MySQL Connection
# -----------------------------

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ujala123",
    database="llm_token_tracker"
)

# -----------------------------
# Save Request
# -----------------------------

def save_request(
    model,
    prompt,
    response,
    input_tokens,
    output_tokens,
    thinking_tokens,
    total_tokens,
    estimated_cost
):

    cursor = connection.cursor()

    sql = """
    INSERT INTO requests
    (
        model,
        prompt,
        response,
        input_tokens,
        output_tokens,
        thinking_tokens,
        total_tokens,
        estimated_cost
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        model,
        prompt,
        response,
        input_tokens,
        output_tokens,
        thinking_tokens,
        total_tokens,
        estimated_cost
    )

    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


# -----------------------------
# Get History
# -----------------------------

def get_history():

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM requests
        ORDER BY id DESC
    """)

    history = cursor.fetchall()

    cursor.close()

    return history
def get_analytics():

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            COUNT(*) AS total_requests,
            SUM(input_tokens) AS total_input_tokens,
            SUM(output_tokens) AS total_output_tokens,
            SUM(thinking_tokens) AS total_thinking_tokens,
            SUM(total_tokens) AS total_tokens,
            SUM(estimated_cost) AS total_cost
        FROM requests
    """)

    analytics = cursor.fetchone()

    cursor.close()

    return analytics
def most_used_model():

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT model,
               COUNT(*) AS count
        FROM requests
        GROUP BY model
        ORDER BY count DESC
        LIMIT 1
    """)

    model = cursor.fetchone()

    cursor.close()

    return model
def delete_request(request_id):

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM requests WHERE id = %s",
        (request_id,)
    )

    connection.commit()

    cursor.close()