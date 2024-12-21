import pandas as pd
import pdfplumber

# Initialize a DataFrame to store transaction data
columns = ['Date', 'Description', 'Amount', 'Type']
transactions = pd.DataFrame(columns=columns)

# Function to extract data from a PDF and save as a CSV
def pdf_to_csv(pdf_path, csv_path):
    with pdfplumber.open(pdf_path) as pdf:
        rows = []
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split("\n")
            for line in lines:
                # Attempt to extract date, description, and amount from each line
                parts = line.split()
                if len(parts) >= 3 and parts[0].isdigit():
                    try:
                        date = parts[0]
                        amount = float(parts[-1].replace("$", "").replace(",", ""))
                        description = " ".join(parts[1:-1])
                        type_ = 'Deposit' if amount > 0 else 'Withdrawal'
                        rows.append([date, description, abs(amount), type_])
                    except ValueError:
                        pass
        
        # Create a DataFrame and save it to a CSV file
        df = pd.DataFrame(rows, columns=columns)
        df.to_csv(csv_path, index=False)
        print(f"Data extracted and saved to {csv_path}")

# Function to categorize transactions into specific names
def categorize(description):
    description = description.lower()
    # Define all unique categories based on your list
    categories = {
        'rna abduallah': 'Rna Abduallah Ja',
        'venmo instant pmt': 'Venmo Instant Pmt',
        'zelle from flores giulia': 'Zelle From Flores Giulia',
        'wt fed#03389 trade bank of iraq': 'WT Fed#03389 Trade Bank of Iraq',
        'preauthorized deposit from wells fargo bank na': 'Preauthorized Deposit from Wells Fargo Bank NA',
        'deposit from st. olaf college': 'Deposit from St. Olaf College',
        'deposit from performance savings': 'Deposit from Performance Savings',
        'zelle money received from yohana lasuba': 'Zelle Money Received from Yohana Lasuba',
        'zelle money received from sardar qaidi': 'Zelle Money Received from Sardar Qaidi',
        'zelle money received from jihene bejaoui': 'Zelle Money Received from Jihene Bejaoui',
        'monthly interest paid': 'Monthly Interest Paid',
        'dd doordash davesh': 'DD Doordash Davesh',
        'dd doordash restau': 'DD Doordash Restau',
        'dd *doordashdashpa': 'DD *Doordashdashpa',
        'holy land brand': 'Holy Land Brand',
        'discover e-payment': 'Discover E-Payment',
        'zelle to saji': 'Zelle to Saji',
        'uber trip': 'Uber Trip',
        'rocket money premium': 'Rocket Money Premium',
        'kwik-trip': 'Kwik-Trip',
        'madinas automotive': 'Madinas Automotive',
        'apple.com/bill': 'Apple.Com/Bill',
        'dd *doordash popey': 'DD *Doordash Popey',
        'dd *doordash walgr': 'DD *Doordash Walgr',
        'mint mobile': 'Mint Mobile',
        'prairie market': 'Prairie Market',
        'wire trans svc charge': 'Wire Trans Svc Charge',
        'tst* st paul brewing': 'Tst* St Paul Brewing',
        'microsoft*ultimate': 'Microsoft*Ultimate',
        'bsaw-minneapolis': 'Bsaw-Minneapolis',
        'usefull httpswww.usef': 'Usefull Httpswww.Usef',
        'zelle to ghanim abdu': 'Zelle to Ghanim Abdu',
        'el triunfo': 'El Triunfo',
        'interstate parking': 'Interstate Parking',
        'culvers of northfield': 'Culvers of Northfield',
        'ameritas insurance': 'Ameritas Insurance',
        'aldi': 'Aldi',
        'progressive insurance': 'Progressive Insurance',
        'st olaf clg cage': 'St Olaf Clg Cage',
        'c n s vending': 'C N S Vending',
        'snack soda vending': 'Snack Soda Vending',
        'tst* fairfield inn': 'Tst* Fairfield Inn',
        'ziggy\'s': 'Ziggy\'s',
        'mnrd-dundas': 'Mnrd-Dundas',
        'vioc oil change': 'Vioc Oil Change',
        'walgreens store': 'Walgreens Store',
        'capital one mobile payment': 'Capital One Mobile Payment',
        'down town tobacco': 'Down Town Tobacco',
        'forget me not flor': 'Forget Me Not Flor',
        'the blast': 'The Blast',
        'tobacco field': 'Tobacco Field',
        'olaf coll bookstore': 'Olaf Coll Bookstore',
        'dollar general': 'Dollar General',
        'costco whse': 'Costco WHSE',
        'dairy queen': 'Dairy Queen',
        'mcdonald\'s': 'McDonald\'s',
        'coco\'s': 'Coco\'s',
        'carbone\'s pizza': 'Carbone\'s Pizza',
        'target': 'Target',
        'content bookstore': 'Content Bookstore',
        'bath & body works': 'Bath & Body Works',
        'froggy bottoms': 'Froggy Bottoms',
        'northfield liquor store': 'Northfield Liquor Store',
        'gong loco': 'Gong Loco',
        'fj #576': 'FJ #576'
    }
    # Match the description to a category
    for keyword, category in categories.items():
        if keyword in description:
            return category
    return 'Uncategorized'

# Function to add transactions from a CSV file
def add_transactions_from_csv(csv_path):
    global transactions
    data = pd.read_csv(csv_path)
    data['Category'] = data['Description'].apply(categorize)
    transactions = pd.concat([transactions, data], ignore_index=True)

# Function to summarize analytics and save as CSV
def summarize():
    # Category Summary
    category_summary = transactions.groupby(['Category'])['Amount'].sum().reset_index()
    category_summary.to_csv('Category_Summary.csv', index=False)
    print("\nCategory Summary:")
    print(category_summary)

    # Spending Trends by Date
    spending_trends = transactions.groupby(['Date'])['Amount'].sum().reset_index()
    spending_trends.to_csv('Spending_Trends.csv', index=False)
    print("\nSpending Trends by Date:")
    print(spending_trends)

# Add transactions from the CSV
add_transactions_from_csv('August_Statements.csv')
add_transactions_from_csv('September_Statements.csv')
add_transactions_from_csv('October_Statements.csv')
add_transactions_from_csv('November_Statements.csv')

# Display analytics and save as CSV
summarize()


