from main import app
from main.models import Item, User
from flask import render_template, redirect, url_for, request, jsonify, flash
from main.forms import RegisterForm
from main import db
from main.Call_api import get_bot_response, evaluate_code

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/hoidap', methods=['GET', 'POST'])
def ask_question():
    if request.method == 'POST':
        data = request.get_json()
        question = data.get('question')

        if not question:
            return jsonify({"error": "No question provided"}), 400

        # gọi Call_api 
        answer = get_bot_response(question)

        return jsonify({"answer": answer})
    return render_template('Q&A.html')

@app.route('/kiemtracode', methods=['GET', 'POST'])
def check_code():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file:
                if file.filename.endswith('.py'):
                    try:
                        code = file.read().decode('utf-8')
                        respond = evaluate_code(code=code)
                        return jsonify({"respond": respond})
                    except Exception as e:
                        return jsonify({"output": f"Error: {e}"})
    return render_template('check_code.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('home_page'))
    if form.errors != {}: # nếu như ko có lỗi từ việc xác nhận
        for err_msg in form.errors.values():
            flash(f'Có lỗi trong việc tạo user: {err_msg}')
    return render_template('register.html', form=form)