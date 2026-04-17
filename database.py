import json
import os
from kivy.app import App
from models import Customer

class Database:
    def __init__(self):
        app = App.get_running_app()
        # Android-safe path
        self.db_path = os.path.join(app.user_data_dir, 'debts.json')
        self.customers = []
        self.load()

    def load(self):
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.customers = [Customer.from_dict(item) for item in data]
            except Exception as e:
                print(f"Load error: {e}")
                self.customers = []

    def save(self):
        try:
            data = [c.to_dict() for c in self.customers]
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Save error: {e}")

    def add_customer(self, customer):
        # Update existing or add new
        for i, c in enumerate(self.customers):
            if c.id == customer.id:
                self.customers[i] = customer
                self.save()
                return
        self.customers.append(customer)
        self.save()

    def get_customer(self, cust_id):
        return next((c for c in self.customers if c.id == cust_id), None)

    def get_unpaid_debts(self):
        # Returns everyone; filtering is done in the list update
        return self.customers

    def search_customers(self, query):
        q = query.lower()
        return [c for c in self.customers if q in c.name.lower()]