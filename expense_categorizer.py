import re

class ExpenseCategorizer:
    def __init__(self):
        # Define category mappings
        self.category_keywords = {
            'Food & Dining': [
                'restaurant', 'cafe', 'food', 'pizza', 'burger', 'swiggy', 'zomato',
                'dominos', 'kfc', 'mcdonalds', 'subway', 'starbucks', 'dunkin',
                'dining', 'meal', 'lunch', 'dinner', 'breakfast', 'snacks',
                'biryani', 'chinese', 'indian', 'continental', 'fast food',
                'bakery', 'ice cream', 'juice', 'coffee', 'tea'
            ],
            
            'Transportation': [
                'uber', 'ola', 'taxi', 'cab', 'metro', 'bus', 'train', 'flight',
                'petrol', 'diesel', 'fuel', 'gas', 'parking', 'toll', 'transport',
                'auto', 'rickshaw', 'railway', 'airlines', 'indigo', 'spicejet',
                'vistara', 'air india', 'goair', 'redbus', 'irctc', 'rapido'
            ],
            
            'Shopping': [
                'amazon', 'flipkart', 'myntra', 'ajio', 'nykaa', 'shopping',
                'mall', 'store', 'retail', 'purchase', 'buy', 'shop',
                'clothing', 'fashion', 'electronics', 'mobile', 'laptop',
                'shoes', 'bag', 'watch', 'jewellery', 'cosmetics',
                'big bazaar', 'dmart', 'reliance', 'lifestyle', 'pantaloons'
            ],
            
            'Entertainment': [
                'movie', 'cinema', 'pvr', 'inox', 'netflix', 'amazon prime',
                'hotstar', 'spotify', 'youtube', 'gaming', 'game', 'entertainment',
                'concert', 'show', 'theatre', 'music', 'streaming', 'subscription',
                'bookmyshow', 'paytm movies', 'fun', 'recreation'
            ],
            
            'Healthcare': [
                'hospital', 'clinic', 'doctor', 'medical', 'pharmacy', 'medicine',
                'health', 'dental', 'eye', 'checkup', 'treatment', 'surgery',
                'apollo', 'fortis', 'max', 'medanta', 'aiims', 'care',
                'diagnostic', 'lab', 'test', 'x-ray', 'scan', 'physiotherapy'
            ],
            
            'Utilities': [
                'electricity', 'water', 'gas', 'internet', 'broadband', 'wifi',
                'mobile', 'recharge', 'bill', 'utility', 'maintenance',
                'rent', 'emi', 'loan', 'insurance', 'premium', 'policy',
                'airtel', 'jio', 'vi', 'bsnl', 'tata', 'reliance'
            ],
            
            'Education': [
                'school', 'college', 'university', 'education', 'course', 'fee',
                'tuition', 'coaching', 'training', 'workshop', 'seminar',
                'book', 'study', 'exam', 'certification', 'online course',
                'udemy', 'coursera', 'byju', 'unacademy', 'vedantu'
            ],
            
            'Travel': [
                'hotel', 'resort', 'accommodation', 'booking', 'travel', 'trip',
                'vacation', 'holiday', 'tour', 'sightseeing', 'tourist',
                'makemytrip', 'goibibo', 'yatra', 'cleartrip', 'trivago',
                'oyo', 'treebo', 'fab', 'zostel', 'airbnb'
            ],
            
            'Groceries': [
                'grocery', 'vegetables', 'fruits', 'milk', 'bread', 'rice',
                'dal', 'oil', 'spices', 'supermarket', 'market', 'fresh',
                'organic', 'bigbasket', 'grofers', 'dunzo', 'blinkit',
                'zepto', 'instamart', 'nature\'s basket', 'spencer\'s'
            ],
            
            'Personal Care': [
                'salon', 'spa', 'beauty', 'haircut', 'massage', 'facial',
                'manicure', 'pedicure', 'grooming', 'personal care',
                'barber', 'parlour', 'wellness', 'fitness', 'gym',
                'yoga', 'meditation', 'therapy'
            ],
            
            'Financial Services': [
                'bank', 'atm', 'withdrawal', 'transfer', 'payment', 'charge',
                'fee', 'penalty', 'interest', 'loan', 'credit card', 'debit card',
                'mutual fund', 'investment', 'trading', 'stock', 'sip',
                'insurance', 'policy', 'premium', 'tax', 'gst'
            ],
            
            'Donations & Charity': [
                'donation', 'charity', 'ngo', 'temple', 'church', 'mosque',
                'gurudwara', 'religious', 'social', 'cause', 'fundraiser',
                'help', 'support', 'relief', 'disaster', 'covid'
            ]
        }
        
        # Merchant-specific mappings (for exact matches)
        self.merchant_mappings = {
            # Food delivery
            'swiggy': 'Food & Dining',
            'zomato': 'Food & Dining',
            'dominos': 'Food & Dining',
            'kfc': 'Food & Dining',
            'mcdonalds': 'Food & Dining',
            'subway': 'Food & Dining',
            'starbucks': 'Food & Dining',
            
            # Transportation
            'uber': 'Transportation',
            'ola': 'Transportation',
            'rapido': 'Transportation',
            'irctc': 'Transportation',
            'redbus': 'Transportation',
            
            # Shopping
            'amazon': 'Shopping',
            'flipkart': 'Shopping',
            'myntra': 'Shopping',
            'ajio': 'Shopping',
            'nykaa': 'Shopping',
            
            # Entertainment
            'netflix': 'Entertainment',
            'amazon prime': 'Entertainment',
            'hotstar': 'Entertainment',
            'spotify': 'Entertainment',
            'bookmyshow': 'Entertainment',
            
            # Utilities
            'airtel': 'Utilities',
            'jio': 'Utilities',
            'vi': 'Utilities',
            'bsnl': 'Utilities',
            
            # Groceries
            'bigbasket': 'Groceries',
            'grofers': 'Groceries',
            'blinkit': 'Groceries',
            'dunzo': 'Groceries',
            'zepto': 'Groceries',
            
            # Travel
            'makemytrip': 'Travel',
            'goibibo': 'Travel',
            'yatra': 'Travel',
            'oyo': 'Travel',
            'airbnb': 'Travel'
        }

    def categorize(self, merchant, description=''):
        """Categorize transaction based on merchant name and description"""
        if not merchant and not description:
            return 'Others'
        
        # Combine merchant and description for analysis
        text_to_analyze = f"{merchant} {description}".lower()
        
        # First check for exact merchant matches
        merchant_lower = merchant.lower() if merchant else ''
        if merchant_lower in self.merchant_mappings:
            return self.merchant_mappings[merchant_lower]
        
        # Check for partial merchant matches
        for known_merchant, category in self.merchant_mappings.items():
            if known_merchant in merchant_lower:
                return category
        
        # Check keywords in both merchant and description
        category_scores = {}
        
        for category, keywords in self.category_keywords.items():
            score = 0
            for keyword in keywords:
                # Count occurrences of keyword
                score += text_to_analyze.count(keyword.lower())
                
                # Give extra weight to exact word matches
                if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', text_to_analyze):
                    score += 2
            
            if score > 0:
                category_scores[category] = score
        
        # Return category with highest score
        if category_scores:
            return max(category_scores.items(), key=lambda x: x[1])[0]
        
        # Special cases based on common patterns
        if self._is_transfer(text_to_analyze):
            return 'Transfers'
        elif self._is_cash_withdrawal(text_to_analyze):
            return 'Cash Withdrawal'
        elif self._is_bill_payment(text_to_analyze):
            return 'Bill Payments'
        
        return 'Others'

    def _is_transfer(self, text):
        """Check if transaction is a transfer"""
        transfer_keywords = ['transfer', 'sent', 'p2p', 'upi transfer', 'fund transfer']
        return any(keyword in text for keyword in transfer_keywords)

    def _is_cash_withdrawal(self, text):
        """Check if transaction is cash withdrawal"""
        withdrawal_keywords = ['atm', 'cash withdrawal', 'withdraw', 'atm withdrawal']
        return any(keyword in text for keyword in withdrawal_keywords)

    def _is_bill_payment(self, text):
        """Check if transaction is bill payment"""
        bill_keywords = ['bill payment', 'electricity bill', 'water bill', 'gas bill', 'phone bill']
        return any(keyword in text for keyword in bill_keywords)

    def get_all_categories(self):
        """Get list of all available categories"""
        categories = list(self.category_keywords.keys())
        categories.extend(['Transfers', 'Cash Withdrawal', 'Bill Payments', 'Others'])
        return sorted(set(categories))

    def add_custom_rule(self, merchant_pattern, category):
        """Add custom categorization rule"""
        self.merchant_mappings[merchant_pattern.lower()] = category

    def get_category_suggestions(self, merchant, description=''):
        """Get top 3 category suggestions with confidence scores"""
        text_to_analyze = f"{merchant} {description}".lower()
        category_scores = {}
        
        for category, keywords in self.category_keywords.items():
            score = 0
            for keyword in keywords:
                score += text_to_analyze.count(keyword.lower())
                if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', text_to_analyze):
                    score += 2
            
            if score > 0:
                category_scores[category] = score
        
        # Sort by score and return top 3
        sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
        
        suggestions = []
        total_score = sum(category_scores.values()) if category_scores else 1
        
        for category, score in sorted_categories[:3]:
            confidence = (score / total_score) * 100
            suggestions.append({
                'category': category,
                'confidence': round(confidence, 2)
            })
        
        return suggestions