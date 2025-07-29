import re
from datetime import datetime
from dateutil import parser as date_parser

class SMSParser:
    def __init__(self):
        # Define patterns for different banks
        self.patterns = {
            # SBI Pattern
            'sbi': {
                'pattern': r'(?i)(?:sbi|state bank).*?(?:debited|credited).*?rs\.?\s*(\d+(?:,\d+)*(?:\.\d{2})?).*?(?:at|to)\s+([^.]+?).*?(?:on|dated?)\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                'amount_group': 1,
                'merchant_group': 2,
                'date_group': 3,
                'bank': 'SBI'
            },
            
            # HDFC Pattern
            'hdfc': {
                'pattern': r'(?i)hdfc.*?(?:debited|credited).*?inr\s*(\d+(?:,\d+)*(?:\.\d{2})?).*?(?:at|to)\s+([^.]+?).*?(?:on|dated?)\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                'amount_group': 1,
                'merchant_group': 2,
                'date_group': 3,
                'bank': 'HDFC'
            },
            
            # ICICI Pattern
            'icici': {
                'pattern': r'(?i)icici.*?(?:debited|credited).*?rs\.?\s*(\d+(?:,\d+)*(?:\.\d{2})?).*?(?:at|to)\s+([^.]+?).*?(?:on|dated?)\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                'amount_group': 1,
                'merchant_group': 2,
                'date_group': 3,
                'bank': 'ICICI'
            },
            
            # Axis Bank Pattern
            'axis': {
                'pattern': r'(?i)axis.*?(?:debited|credited).*?rs\.?\s*(\d+(?:,\d+)*(?:\.\d{2})?).*?(?:at|to)\s+([^.]+?).*?(?:on|dated?)\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                'amount_group': 1,
                'merchant_group': 2,
                'date_group': 3,
                'bank': 'Axis Bank'
            },
            
            # Generic UPI Pattern
            'upi_generic': {
                'pattern': r'(?i)(?:debited|credited).*?rs\.?\s*(\d+(?:,\d+)*(?:\.\d{2})?).*?(?:upi|vpa|to)\s+([^.]+?).*?(?:on|dated?)\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                'amount_group': 1,
                'merchant_group': 2,
                'date_group': 3,
                'bank': 'Generic'
            },
            
            # Paytm Pattern
            'paytm': {
                'pattern': r'(?i)paytm.*?(?:debited|credited).*?rs\.?\s*(\d+(?:,\d+)*(?:\.\d{2})?).*?(?:to|at)\s+([^.]+?).*?(?:on|dated?)\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                'amount_group': 1,
                'merchant_group': 2,
                'date_group': 3,
                'bank': 'Paytm'
            },
            
            # PhonePe Pattern
            'phonepe': {
                'pattern': r'(?i)phonepe.*?(?:debited|credited).*?rs\.?\s*(\d+(?:,\d+)*(?:\.\d{2})?).*?(?:to|at)\s+([^.]+?).*?(?:on|dated?)\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                'amount_group': 1,
                'merchant_group': 2,
                'date_group': 3,
                'bank': 'PhonePe'
            },
            
            # Google Pay Pattern
            'gpay': {
                'pattern': r'(?i)(?:google pay|gpay).*?(?:debited|credited).*?rs\.?\s*(\d+(?:,\d+)*(?:\.\d{2})?).*?(?:to|at)\s+([^.]+?).*?(?:on|dated?)\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                'amount_group': 1,
                'merchant_group': 2,
                'date_group': 3,
                'bank': 'Google Pay'
            }
        }
        
        # Balance extraction patterns
        self.balance_patterns = [
            r'(?i)(?:balance|bal|available)\s*(?:is|:)?\s*rs\.?\s*(\d+(?:,\d+)*(?:\.\d{2})?)',
            r'(?i)(?:avl bal|available balance)\s*rs\.?\s*(\d+(?:,\d+)*(?:\.\d{2})?)',
        ]
        
        # Account number patterns
        self.account_patterns = [
            r'(?i)(?:a\/c|account|acc)\s*(?:no\.?|number)?\s*(?:ending|xxxx)?(\d{4,})',
            r'(?i)(?:card|ac)\s*(?:ending|xxxx)(\d{4})',
        ]

    def parse(self, sms_text):
        """Parse SMS text and extract transaction details"""
        try:
            # Clean the SMS text
            sms_text = self._clean_text(sms_text)
            
            # Determine transaction type
            transaction_type = self._get_transaction_type(sms_text)
            
            # Try each pattern
            for bank_name, pattern_info in self.patterns.items():
                match = re.search(pattern_info['pattern'], sms_text)
                
                if match:
                    # Extract basic information
                    amount_str = match.group(pattern_info['amount_group'])
                    merchant = match.group(pattern_info['merchant_group']).strip()
                    date_str = match.group(pattern_info['date_group'])
                    
                    # Parse amount (remove commas)
                    amount = float(amount_str.replace(',', ''))
                    
                    # Parse date
                    transaction_date = self._parse_date(date_str)
                    
                    # Extract additional information
                    balance = self._extract_balance(sms_text)
                    account_number = self._extract_account_number(sms_text)
                    
                    # Clean merchant name
                    merchant = self._clean_merchant_name(merchant)
                    
                    return {
                        'amount': amount,
                        'transaction_type': transaction_type,
                        'merchant': merchant,
                        'date': transaction_date,
                        'description': sms_text,
                        'bank': pattern_info['bank'],
                        'account_number': account_number,
                        'balance': balance
                    }
            
            # If no pattern matches, try generic extraction
            return self._generic_parse(sms_text)
            
        except Exception as e:
            print(f"Error parsing SMS: {e}")
            return None

    def _clean_text(self, text):
        """Clean and normalize SMS text"""
        # Remove extra whitespaces
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters that might interfere
        text = text.replace('\n', ' ').replace('\r', ' ')
        return text.strip()

    def _get_transaction_type(self, text):
        """Determine if transaction is debit or credit"""
        debit_keywords = ['debited', 'debit', 'spent', 'paid', 'purchase', 'withdrawn']
        credit_keywords = ['credited', 'credit', 'received', 'refund', 'cashback']
        
        text_lower = text.lower()
        
        for keyword in debit_keywords:
            if keyword in text_lower:
                return 'debit'
        
        for keyword in credit_keywords:
            if keyword in text_lower:
                return 'credit'
        
        return 'debit'  # Default to debit

    def _parse_date(self, date_str):
        """Parse date string to datetime object"""
        try:
            # Try different date formats
            formats = [
                '%d/%m/%Y', '%d-%m-%Y', '%d/%m/%y', '%d-%m-%y',
                '%Y-%m-%d', '%d.%m.%Y', '%d.%m.%y'
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            
            # Use dateutil parser as fallback
            return date_parser.parse(date_str)
            
        except Exception:
            # Return current date if parsing fails
            return datetime.now()

    def _extract_balance(self, text):
        """Extract account balance from SMS"""
        for pattern in self.balance_patterns:
            match = re.search(pattern, text)
            if match:
                balance_str = match.group(1)
                try:
                    return float(balance_str.replace(',', ''))
                except ValueError:
                    continue
        return None

    def _extract_account_number(self, text):
        """Extract account number from SMS"""
        for pattern in self.account_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return None

    def _clean_merchant_name(self, merchant):
        """Clean and normalize merchant name"""
        # Remove common prefixes/suffixes
        merchant = re.sub(r'(?i)(?:upi|vpa|@)', '', merchant)
        merchant = re.sub(r'[*]+', '', merchant)
        merchant = merchant.strip()
        
        # Capitalize properly
        merchant = ' '.join(word.capitalize() for word in merchant.split())
        
        return merchant

    def _generic_parse(self, text):
        """Generic parsing for unrecognized formats"""
        try:
            # Look for amount
            amount_match = re.search(r'rs\.?\s*(\d+(?:,\d+)*(?:\.\d{2})?)', text, re.IGNORECASE)
            if not amount_match:
                return None
            
            amount = float(amount_match.group(1).replace(',', ''))
            
            # Look for date
            date_match = re.search(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', text)
            transaction_date = self._parse_date(date_match.group(1)) if date_match else datetime.now()
            
            # Determine transaction type
            transaction_type = self._get_transaction_type(text)
            
            # Extract merchant (this is tricky for generic parsing)
            merchant = "Unknown Merchant"
            
            return {
                'amount': amount,
                'transaction_type': transaction_type,
                'merchant': merchant,
                'date': transaction_date,
                'description': text,
                'bank': 'Unknown',
                'account_number': self._extract_account_number(text),
                'balance': self._extract_balance(text)
            }
            
        except Exception:
            return None