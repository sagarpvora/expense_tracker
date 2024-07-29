from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///expense.db"
db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(200), default="General")
    amount = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc),nullable=False)

    def __repr__(self):
        return '<Expense %r>' % self.id


@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        expense_name = request.form['name']
        expense_desc = request.form['description']
        expense_cat = request.form['category']
        expense_amount = request.form['amount']
        date = request.form['date_created']
        date_created = datetime.strptime(date, '%Y-%m-%d')
        date_created = datetime.combine(date_created, datetime.now(timezone.utc).time())
        date_created = date_created.replace(tzinfo=timezone.utc)
        new_expense = Expense(name=expense_name,description=expense_desc,category=expense_cat,amount=expense_amount,date_created=date_created)

        try:
            db.session.add(new_expense)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"There was a problem in adding your expense : {e}"
    else:
        # exp = Expense.query.order_by(Expense.date_created).all()
        latest_expenses = Expense.query.order_by(Expense.date_created.desc()).limit(2).all()
        return render_template('index.html', expenses=latest_expenses)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Expense.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem in deleting your expense"

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    expense_to_update = Expense.query.get_or_404(id)

    if request.method == 'POST':
        expense_to_update.name = request.form['name']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem in updating your expense"
    else:
        return render_template('update.html', expense=expense_to_update)
    
@app.route('/summary', methods=['GET','POST'])
def summary(id):
    if request.method == 'POST':
        pass
    else:
        exp = Expense.query.order_by(Expense.date_created).all()
        return render_template('index.html', expense=exp)
if __name__ == "__main__":
    app.run(debug=True)

