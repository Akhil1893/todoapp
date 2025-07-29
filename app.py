from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import re
import json
from sms_parser import SMSParser
from expense_categorizer import ExpenseCategorizer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

# Initialize parsers
sms_parser = SMSParser()
categorizer = ExpenseCategorizer()

# Database Models
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)  # 'debit' or 'credit'
    merchant = db.Column(db.String(100))
    category = db.Column(db.String(50))
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)
    bank = db.Column(db.String(50))
    account_number = db.Column(db.String(20))
    balance = db.Column(db.Float)
    raw_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'transaction_type': self.transaction_type,
            'merchant': self.merchant,
            'category': self.category,
            'date': self.date.isoformat() if self.date else None,
            'description': self.description,
            'bank': self.bank,
            'account_number': self.account_number,
            'balance': self.balance,
            'raw_message': self.raw_message,
            'created_at': self.created_at.isoformat()
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/parse-sms', methods=['POST'])
def parse_sms():
    try:
        data = request.get_json()
        sms_text = data.get('sms_text', '')
        
        if not sms_text:
            return jsonify({'error': 'SMS text is required'}), 400
        
        # Parse the SMS
        parsed_data = sms_parser.parse(sms_text)
        
        if not parsed_data:
            return jsonify({'error': 'Could not parse SMS message'}), 400
        
        # Categorize the expense
        category = categorizer.categorize(parsed_data.get('merchant', ''), parsed_data.get('description', ''))
        parsed_data['category'] = category
        
        # Save to database
        transaction = Transaction(
            amount=parsed_data['amount'],
            transaction_type=parsed_data['transaction_type'],
            merchant=parsed_data.get('merchant'),
            category=category,
            date=parsed_data['date'],
            description=parsed_data.get('description'),
            bank=parsed_data.get('bank'),
            account_number=parsed_data.get('account_number'),
            balance=parsed_data.get('balance'),
            raw_message=sms_text
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'transaction': transaction.to_dict(),
            'message': 'Transaction parsed and saved successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        transaction_type = request.args.get('type')
        category = request.args.get('category')
        
        query = Transaction.query
        
        if transaction_type:
            query = query.filter(Transaction.transaction_type == transaction_type)
        
        if category:
            query = query.filter(Transaction.category == category)
        
        transactions = query.order_by(Transaction.date.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'transactions': [t.to_dict() for t in transactions.items],
            'total': transactions.total,
            'pages': transactions.pages,
            'current_page': page
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    try:
        # Monthly spending
        monthly_query = db.session.query(
            db.func.strftime('%Y-%m', Transaction.date).label('month'),
            db.func.sum(Transaction.amount).label('total')
        ).filter(Transaction.transaction_type == 'debit').group_by('month').all()
        
        monthly_data = [{'month': m[0], 'amount': float(m[1])} for m in monthly_query]
        
        # Category-wise spending
        category_query = db.session.query(
            Transaction.category,
            db.func.sum(Transaction.amount).label('total')
        ).filter(Transaction.transaction_type == 'debit').group_by(Transaction.category).all()
        
        category_data = [{'category': c[0] or 'Uncategorized', 'amount': float(c[1])} for c in category_query]
        
        # Top merchants
        merchant_query = db.session.query(
            Transaction.merchant,
            db.func.sum(Transaction.amount).label('total')
        ).filter(Transaction.transaction_type == 'debit').group_by(Transaction.merchant).order_by(db.func.sum(Transaction.amount).desc()).limit(10).all()
        
        merchant_data = [{'merchant': m[0] or 'Unknown', 'amount': float(m[1])} for m in merchant_query]
        
        return jsonify({
            'monthly_spending': monthly_data,
            'category_spending': category_data,
            'top_merchants': merchant_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bulk-import', methods=['POST'])
def bulk_import():
    try:
        data = request.get_json()
        sms_messages = data.get('messages', [])
        
        if not sms_messages:
            return jsonify({'error': 'No messages provided'}), 400
        
        successful = 0
        failed = 0
        errors = []
        
        for sms_text in sms_messages:
            try:
                parsed_data = sms_parser.parse(sms_text)
                
                if parsed_data:
                    category = categorizer.categorize(parsed_data.get('merchant', ''), parsed_data.get('description', ''))
                    
                    transaction = Transaction(
                        amount=parsed_data['amount'],
                        transaction_type=parsed_data['transaction_type'],
                        merchant=parsed_data.get('merchant'),
                        category=category,
                        date=parsed_data['date'],
                        description=parsed_data.get('description'),
                        bank=parsed_data.get('bank'),
                        account_number=parsed_data.get('account_number'),
                        balance=parsed_data.get('balance'),
                        raw_message=sms_text
                    )
                    
                    db.session.add(transaction)
                    successful += 1
                else:
                    failed += 1
                    errors.append(f"Could not parse: {sms_text[:50]}...")
                    
            except Exception as e:
                failed += 1
                errors.append(f"Error processing message: {str(e)}")
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'successful': successful,
            'failed': failed,
            'errors': errors[:10]  # Return only first 10 errors
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)