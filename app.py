from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from database import get_db_connection, initialize_database
from auth import hash_password, verify_password
from knowledge_base import search_knowledge
from datetime import datetime
from rag_pipeline import run_rag


app = Flask(__name__)
app.secret_key = "supportai-secret-key-change-this"

# Initialize database
initialize_database()


# =====================================================
# HOME PAGE
# =====================================================

@app.route("/")
def home():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("index.html")
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # Check empty fields
        if not email or not password:
            return render_template(
                "login.html",
                error="Please enter email and password."
            )

        # Connect to database
        conn = get_db_connection()

        user = conn.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,)
        ).fetchone()

        conn.close()

        # User not found
        if user is None:
            return render_template(
                "login.html",
                error="Account not found. Please check your email."
            )

        # Verify password
        if not verify_password(password, user["password_hash"]):
            return render_template(
                "login.html",
                error="Incorrect password."
            )

        # Create session
        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        session["user_email"] = user["email"]

        # Login successful
        return redirect(url_for("home"))

    return render_template("login.html")
# =====================================================
# SIGNUP
# =====================================================

# =====================================================
# SIGNUP
# =====================================================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # Check empty fields
        if not name or not email or not password:
            return render_template(
                "signup.html",
                error="Please fill in all fields."
            )

        # Check password confirmation
        if password != confirm_password:
            return render_template(
                "signup.html",
                error="Passwords do not match."
            )

        # Check password length
        if len(password) < 6:
            return render_template(
                "signup.html",
                error="Password must contain at least 6 characters."
            )

        # Hash password
        password_hash = hash_password(password)

        conn = get_db_connection()

        try:

            cursor = conn.execute(
                """
                INSERT INTO users
                (name, email, password_hash, role, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    name,
                    email,
                    password_hash,
                    "customer",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
            )

            conn.commit()

            # Get newly created user's ID
            user_id = cursor.lastrowid

        except Exception:

            conn.close()

            return render_template(
                "signup.html",
                error="Email already registered."
            )

        conn.close()

        # Login user automatically
        session["user_id"] = user_id
        session["user_name"] = name
        session["user_email"] = email

        # Go to dashboard
        return redirect(url_for("home"))

    return render_template("signup.html")



# =====================================================
# CLASSIFICATION AGENT
# =====================================================

def classify_ticket(query):

    text = query.lower()

    # Payment
    if any(word in text for word in [
        "payment",
        "paid",
        "transaction",
        "deducted",
        "charged",
        "upi",
        "credit card",
        "debit card"
    ]):
        return "Payment"

    # Refund
    elif any(word in text for word in [
        "refund",
        "money back",
        "reimbursement"
    ]):
        return "Refund"

    # Delivery
    elif any(word in text for word in [
        "delivery",
        "delivered",
        "package",
        "shipping",
        "shipment"
    ]):
        return "Delivery"

    # Order
    elif any(word in text for word in [
        "order",
        "purchase",
        "cancel order"
    ]):
        return "Order"

    # Account
    elif any(word in text for word in [
        "password",
        "login",
        "log in",
        "account",
        "sign in"
    ]):
        return "Account"

    # Technical
    elif any(word in text for word in [
        "vpn",
        "server",
        "application",
        "app",
        "website",
        "error",
        "crash",
        "network"
    ]):
        return "Technical"

    # Security
    elif any(word in text for word in [
        "fraud",
        "hacked",
        "unauthorized",
        "stolen",
        "security",
        "scam"
    ]):
        return "Security"

    else:
        return "General"


# =====================================================
# PRIORITY AGENT
# =====================================================

def calculate_priority(query, category):

    text = query.lower()

    # Critical issues
    critical_words = [
        "fraud",
        "hacked",
        "unauthorized",
        "stolen",
        "security",
        "scam"
    ]

    # High priority issues
    high_words = [
        "payment deducted",
        "payment failed",
        "urgent",
        "not received",
        "account locked"
    ]

    if any(word in text for word in critical_words):
        return "Critical", 95

    elif category == "Security":
        return "Critical", 90

    elif any(word in text for word in high_words):
        return "High", 80

    elif category in ["Payment", "Refund"]:
        return "High", 75

    elif category in ["Technical", "Delivery"]:
        return "Medium", 55

    else:
        return "Low", 30


# =====================================================
# RESOLUTION AGENT
# =====================================================

def generate_resolution(query, category):

    resolutions = {

        "Payment":
        "Please verify the payment transaction status and "
        "transaction reference. If the payment was successful "
        "but the order was not created, the amount will be "
        "processed according to the refund policy.",

        "Refund":
        "Please provide the order or transaction reference. "
        "The refund status can then be verified and the expected "
        "refund timeline can be provided.",

        "Delivery":
        "Please check the latest shipment tracking information. "
        "If the package has not arrived within the expected "
        "delivery period, the delivery team can investigate it.",

        "Order":
        "Please provide your order ID so that the order status "
        "can be verified. If required, the cancellation or "
        "modification process can be initiated.",

        "Account":
        "Please use the account recovery or password reset "
        "option. If you are still unable to access your account, "
        "the support team can verify the account.",

        "Technical":
        "Please restart the application or service and verify "
        "your network connection. If the issue continues, "
        "technical support should investigate the problem.",

        "Security":
        "This issue may involve account or transaction security. "
        "Please avoid sharing sensitive information and contact "
        "the security support team for immediate verification.",

        "General":
        "Your query has been received. A support agent will "
        "review the issue and provide the appropriate assistance."
    }

    return resolutions.get(
        category,
        resolutions["General"]
    )


# =====================================================
# ESCALATION AGENT
# =====================================================

def determine_escalation(priority, category):

    if priority == "Critical":
        return "Escalated to Human Agent"

    if category == "Security":
        return "Escalated to Human Agent"

    return "Handled by AI"


# =====================================================
# SUBMIT TICKET
# =====================================================
# =====================================================
# SUBMIT TICKET
# =====================================================

@app.route("/submit", methods=["POST"])
def submit_ticket():

    data = request.get_json()

    customer_name = data.get(
        "customer_name",
        ""
    ).strip()

    query = data.get(
        "query",
        ""
    ).strip()

    department = data.get(
        "department",
        ""
    ).strip()

    # ---------------------------------------------
    # VALIDATION
    # ---------------------------------------------

    if not customer_name or not query:

        return jsonify({
            "success": False,
            "message": "Customer name and query are required."
        }), 400

    # ---------------------------------------------
    # AI PIPELINE + RAG
    # ---------------------------------------------

    # 1. Ticket Classification
    category = classify_ticket(query)

    # 2. Priority Agent
    priority, priority_score = calculate_priority(
        query,
        category
    )

    # 3. RAG Pipeline
    rag_result = run_rag(query)

    # 4. RAG Resolution
    resolution = rag_result["resolution"]["response"]

    # 5. Escalation Agent
    escalation = determine_escalation(
        priority,
        category
    )

    # ---------------------------------------------
    # CREATE TICKET ID
    # ---------------------------------------------

    ticket_id = (
        "TKT-" +
        datetime.now().strftime("%Y%m%d%H%M%S")
    )

    created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # ---------------------------------------------
    # SAVE TO DATABASE
    # ---------------------------------------------

    conn = get_db_connection()

    conn.execute(
        """
        INSERT INTO tickets
        (
            ticket_id,
            customer_name,
            query,
            department,
            category,
            priority,
            priority_score,
            resolution,
            escalation,
            feedback,
            status,
            created_at
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,

        (
            ticket_id,
            customer_name,
            query,
            department,
            category,
            priority,
            priority_score,
            resolution,
            escalation,
            "No Feedback",
            "Open",
            created_at
        )
    )

    conn.commit()
    conn.close()

    # ---------------------------------------------
    # SEND RESULT TO FRONTEND
    # ---------------------------------------------

    return jsonify({

        "success": True,

        "ticket_id": ticket_id,

        "category": category,

        "priority": priority,

        "priority_score": priority_score,

        "resolution": resolution,

        "escalation": escalation,

        "rag": {

            "retrieved_documents":
                rag_result["retrieved_documents"],

            "context":
                rag_result["context"],

            "confidence":
                rag_result["resolution"]["confidence"]

        }

    })  
# =====================================================
# GET ALL TICKETS
# =====================================================

@app.route("/tickets")
def get_tickets():

    conn = get_db_connection()

    tickets = conn.execute(
        """
        SELECT *
        FROM tickets
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    return jsonify([
        dict(ticket)
        for ticket in tickets
    ])



 

# =====================================================
# FEEDBACK
# =====================================================

@app.route(
    "/feedback/<ticket_id>",
    methods=["POST"]
)
def submit_feedback(ticket_id):

    data = request.get_json()

    feedback = data.get(
        "feedback",
        "No Feedback"
    )

    conn = get_db_connection()

    # Update ticket
    conn.execute(
        """
        UPDATE tickets

        SET feedback = ?

        WHERE ticket_id = ?
        """,

        (
            feedback,
            ticket_id
        )
    )

    # Store feedback separately
    conn.execute(
        """
        INSERT INTO feedback
        (
            ticket_id,
            rating,
            comment,
            created_at
        )

        VALUES (?, ?, ?, ?)
        """,

        (
            ticket_id,
            feedback,
            "",
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
    )

    conn.commit()
    conn.close()

    return jsonify({
        "success": True
    })

# ==============================
# RAG TEST ROUTE
# ==============================
@app.route("/test-rag")
def test_rag():

    result = run_rag(
        "payment deducted but order not confirmed"
    )

    return {
        "success": True,
        "rag_result": result
    }

# ==============================
# LOGOUT
# ==============================

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))






# =====================================================
# RUN APPLICATION
# =====================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
    