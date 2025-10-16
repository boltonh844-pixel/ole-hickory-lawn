from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- Home Page ---
@app.route('/')
def home():
    return render_template('index.html')

# --- Contact Form Submission ---
@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # You can later add email sending logic here
    print(f"📩 Contact form from {name} ({email}): {message}")
    return jsonify({"status": "success", "message": "Thanks for reaching out! We'll be in touch soon."})

# --- Quote Request ---
@app.route('/get-quote', methods=['POST'])
def get_quote():
    data = request.json
    print("🧾 New Quote Request:", data)
    # You could store this in a database or email it later
    return jsonify({"status": "received", "message": "Your quote request has been submitted!"})

# --- Live Chat Endpoint ---
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').lower()

    # --- Simple AI-style auto-responses ---
    if "quote" in user_message:
        reply = "Sure! You can request a quick quote by clicking the 'Quote' button above."
    elif "seed" in user_message or "grass" in user_message:
        reply = "We use premium cool-season grass blends perfect for Virginia lawns."
    elif "date" in user_message or "available" in user_message:
        reply = "We currently have open slots this week for new clients — would you like to book a visit?"
    elif "hello" in user_message or "hi" in user_message:
        reply = "Hey there! 👋 Welcome to Ole Hickory — how can we help with your lawn today?"
    else:
        reply = "Thanks for reaching out! A team member will follow up soon."

    print(f"💬 Chat message received: {user_message}")
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)
