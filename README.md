# UPI Expense Tracker

A comprehensive web application that automatically tracks your expenses by parsing bank SMS messages. Perfect for the UPI era where people struggle to keep track of their digital transactions.

## Features

### 🏦 Multi-Bank Support
- **SBI (State Bank of India)**
- **HDFC Bank**
- **ICICI Bank**
- **Axis Bank**
- **Paytm Payments Bank**
- **PhonePe**
- **Google Pay**
- **Generic UPI patterns**

### 📱 SMS Parsing
- Automatically extracts transaction details from SMS messages
- Supports both debit and credit transactions
- Extracts merchant names, amounts, dates, and account balances
- Handles various SMS formats from different banks

### 🏷️ Smart Categorization
- **Automatic categorization** based on merchant names and transaction descriptions
- **13+ categories** including:
  - Food & Dining
  - Transportation
  - Shopping
  - Entertainment
  - Healthcare
  - Utilities
  - Education
  - Travel
  - Groceries
  - Personal Care
  - Financial Services
  - Donations & Charity
  - Others

### 📊 Analytics & Insights
- **Monthly spending trends** with interactive charts
- **Category-wise breakdown** with pie charts
- **Top merchants** analysis
- **Summary cards** showing total spent, received, and monthly expenses
- **Transaction history** with filtering options

### 💻 User-Friendly Interface
- **Modern, responsive design** built with Bootstrap 5
- **Real-time parsing** of SMS messages
- **Bulk import** functionality for multiple SMS messages
- **Transaction details** modal with complete information
- **Filtering and pagination** for transaction history

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd upi-expense-tracker
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

## Usage

### Adding Single SMS
1. Navigate to the **"Add SMS"** section
2. Paste your bank SMS message in the text area
3. Click **"Parse SMS"** to automatically extract transaction details
4. The transaction will be saved and categorized automatically

### Bulk Import
1. Go to the **"Bulk Import"** section
2. Paste multiple SMS messages (one per line)
3. Click **"Import Messages"** to process all messages at once
4. View the import results showing successful and failed parsing attempts

### Viewing Analytics
1. Visit the **"Dashboard"** to see:
   - Summary cards with key metrics
   - Monthly spending trend chart
   - Category breakdown pie chart
   - Top merchants list

### Transaction History
1. Check the **"Transactions"** section for:
   - Complete transaction history
   - Filter by transaction type (debit/credit)
   - Filter by category
   - Pagination for large datasets
   - Detailed transaction information

## Sample SMS Formats

### SBI Bank
```
SBI: Your A/c XXXX1234 debited by Rs.500.00 on 15-01-24 to SWIGGY* Info: UPI/SWIGGY. Avl Bal Rs.25000.00
```

### HDFC Bank
```
HDFC Bank: Rs.1200.00 debited from A/c XXXX5678 on 15-01-24 at AMAZON PAY. UPI Ref No 123456789. Avl Bal: INR 45000.00
```

### ICICI Bank
```
ICICI: Rs.800.00 debited from A/c XXXX9012 on 15-01-24 to UBER INDIA. UPI txn. Avl bal Rs.35000.00
```

## API Endpoints

### Parse SMS
- **POST** `/api/parse-sms`
- Parse a single SMS message and save transaction

### Get Transactions
- **GET** `/api/transactions`
- Retrieve transaction history with pagination and filters

### Analytics
- **GET** `/api/analytics`
- Get analytics data for dashboard

### Bulk Import
- **POST** `/api/bulk-import`
- Import multiple SMS messages at once

## Database Schema

The application uses SQLite database with the following transaction model:

```python
class Transaction:
    id: Integer (Primary Key)
    amount: Float (Required)
    transaction_type: String (debit/credit)
    merchant: String
    category: String
    date: DateTime (Required)
    description: Text
    bank: String
    account_number: String
    balance: Float
    raw_message: Text
    created_at: DateTime
```

## Architecture

### Backend (Flask)
- **app.py**: Main Flask application with API routes
- **sms_parser.py**: SMS parsing logic for different bank formats
- **expense_categorizer.py**: Automatic expense categorization system
- **SQLAlchemy**: Database ORM for transaction storage

### Frontend (Vanilla JavaScript)
- **Bootstrap 5**: Responsive UI framework
- **Chart.js**: Interactive charts for analytics
- **Font Awesome**: Icons
- **Custom CSS**: Modern styling and animations

## Supported Banks & Patterns

The SMS parser supports regex patterns for:

1. **Major Banks**: SBI, HDFC, ICICI, Axis Bank
2. **Payment Apps**: Paytm, PhonePe, Google Pay
3. **Generic UPI**: Fallback patterns for other banks
4. **Transaction Types**: Both debit and credit transactions
5. **Data Extraction**: Amount, merchant, date, balance, account details

## Categorization Logic

The expense categorizer uses:

1. **Keyword Matching**: Merchant names and descriptions
2. **Exact Merchant Mapping**: Pre-defined merchant categories
3. **Pattern Recognition**: Common transaction patterns
4. **Confidence Scoring**: Multiple keyword matches for accuracy

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Future Enhancements

- [ ] Mobile app version
- [ ] Export functionality (PDF, Excel)
- [ ] Budget setting and alerts
- [ ] Receipt attachment
- [ ] Multi-user support
- [ ] Bank API integration
- [ ] Machine learning for better categorization
- [ ] Expense forecasting
- [ ] Custom category creation
- [ ] Recurring transaction detection

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please create an issue in the repository or contact the development team.

---

**Built with ❤️ for the UPI generation to better track their digital expenses!**
