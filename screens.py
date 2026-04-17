import webbrowser
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import StringProperty
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class SelectableButton(RecycleDataViewBehavior, Button):
    index = None
    customer_id = None
    address_text = StringProperty("")
    debt_text = StringProperty("")
    
    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.customer_id = data.get('customer_id')
        self.text = data.get('text', '')
        self.address_text = data.get('address_text', '')
        self.debt_text = data.get('debt_text', '')
        return super().refresh_view_attrs(rv, index, data)

    def mark_as_paid(self):
        app = App.get_running_app()
        cust = app.db.get_customer(self.customer_id)
        if cust:
            for o in cust.orders: o.is_paid = True
            app.db.save()
            app.root.get_screen('debtlist').update_list()

    def mark_as_unpaid(self):
        app = App.get_running_app()
        cust = app.db.get_customer(self.customer_id)
        if cust:
            for o in cust.orders: o.is_paid = False
            app.db.save()
            app.root.get_screen('paidhistory').update_list()

    def confirm_delete(self):
        content = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15))
        content.add_widget(Label(text="Delete this customer and all records?", halign='center'))
        btns = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        yes = Button(text="DELETE", background_color=(0.8, 0.2, 0.2, 1), background_normal='', bold=True)
        no = Button(text="CANCEL", background_color=(0.3, 0.3, 0.3, 1), background_normal='', bold=True)
        btns.add_widget(no); btns.add_widget(yes)
        content.add_widget(btns)
        popup = Popup(title="Confirm Deletion", content=content, size_hint=(0.85, 0.3), title_align='center')
        yes.bind(on_release=lambda x: self.execute_delete(popup))
        no.bind(on_release=popup.dismiss)
        popup.open()

    def execute_delete(self, popup):
        app = App.get_running_app()
        app.db.customers = [c for c in app.db.customers if c.id != self.customer_id]
        app.db.save()
        popup.dismiss()
        if app.root.current == 'paidhistory': app.root.get_screen('paidhistory').update_list()
        else: app.root.get_screen('debtlist').update_list()

    def on_release(self):
        app = App.get_running_app()
        app.root.transition.direction = "left"
        app.current_customer_id = self.customer_id
        app.root.current = 'customerdetail'

class HomeScreen(Screen):
    def add_new_debt(self):
        self.manager.transition.direction = "left"
        App.get_running_app().current_customer_id = None
        self.manager.current = 'customerdetail'
    def show_debts(self):
        self.manager.transition.direction = "left"
        self.manager.current = 'debtlist'

class DebtListScreen(Screen):
    def on_pre_enter(self): self.update_list()
    def update_list(self, search=''):
        app = App.get_running_app()
        if 'rv' not in self.ids: return
        customers = app.db.search_customers(search) if search else app.db.customers
        active = [c for c in customers if c.unpaid_total() > 0]
        self.ids.rv.data = [{'customer_id': c.id, 'text': f"[b]{c.name}[/b]", 'address_text': f"{c.address}", 'debt_text': f"₱ {c.unpaid_total():.2f}"} for c in active]

class PaidHistoryScreen(Screen):
    def on_pre_enter(self): self.update_list()
    def update_list(self, search=''):
        app = App.get_running_app()
        if 'rv' not in self.ids: return
        customers = app.db.search_customers(search) if search else app.db.customers
        paid = [c for c in customers if len(c.orders) > 0 and c.unpaid_total() == 0]
        self.ids.rv.data = [{'customer_id': c.id, 'text': f"[b]{c.name}[/b]", 'address_text': f"{c.address}", 'debt_text': "SETTLED"} for c in paid]

class CustomerDetailScreen(Screen):
    edit_mode = False
    def on_pre_enter(self):
        app = App.get_running_app()
        self.edit_mode = not bool(app.current_customer_id)
        self.apply_mode_ui(); self.refresh_ui()

    def call_customer(self):
        phone = self.ids.phone_input.text.strip()
        if phone: webbrowser.open(f"tel:{phone}")

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        self.apply_mode_ui()
        if not self.edit_mode: self.refresh_ui()

    def apply_mode_ui(self):
        app = App.get_running_app()
        is_new = app.current_customer_id is None
        editable = (is_new or self.edit_mode)
        self.ids.name_input.disabled = self.ids.phone_input.disabled = self.ids.address_input.disabled = not editable
        self.ids.edit_toggle_btn.opacity = 0 if is_new else 1
        self.ids.edit_actions.height = dp(50) if self.edit_mode and not is_new else 0
        self.ids.edit_actions.opacity = 1 if self.edit_mode and not is_new else 0
        self.ids.edit_toggle_btn.text = "CANCEL" if self.edit_mode else "EDIT"
        self.ids.new_order_section.height = dp(240) if is_new or self.edit_mode else 0
        self.ids.new_order_section.opacity = 1 if is_new or self.edit_mode else 0

    def refresh_ui(self):
        app = App.get_running_app()
        if not app.current_customer_id:
            for f in ['name_input', 'phone_input', 'address_input', 'history_label']: self.ids[f].text = ''
            return
        cust = app.db.get_customer(app.current_customer_id)
        if cust:
            self.ids.name_input.text, self.ids.phone_input.text, self.ids.address_input.text = cust.name, cust.phone, cust.address
            h = "".join([f"• {o.date}: {o.description} - [b]₱{o.amount:.2f}[/b] {'[color=888888](Paid)[/color]' if o.is_paid else ''}\n" for o in cust.orders])
            self.ids.history_label.text = h + f"\n[b][color=2E7D32]BALANCE: ₱{cust.unpaid_total():.2f}[/color][/b]"

    def update_customer_info(self):
        app = App.get_running_app()
        cust = app.db.get_customer(app.current_customer_id)
        if cust:
            cust.name, cust.phone, cust.address = self.ids.name_input.text.strip(), self.ids.phone_input.text.strip(), self.ids.address_input.text.strip()
            app.db.save(); self.edit_mode = False; self.apply_mode_ui(); self.refresh_ui()

    def delete_customer(self):
        app = App.get_running_app()
        app.db.customers = [c for c in app.db.customers if c.id != app.current_customer_id]
        app.db.save(); self.manager.transition.direction = "right"; self.manager.current = 'debtlist'

    def add_order(self):
        from models import Customer, Order
        app = App.get_running_app()
        name = self.ids.name_input.text.strip()
        if not name: return
        cust = app.db.get_customer(app.current_customer_id) if app.current_customer_id else next((c for c in app.db.customers if c.name.lower() == name.lower()), None)
        if not cust:
            cust = Customer(name=name, phone=self.ids.phone_input.text, address=self.ids.address_input.text)
            app.db.customers.append(cust)
        app.current_customer_id = cust.id
        try:
            amt = float(self.ids.order_total.text)
            if amt > 0: cust.orders.append(Order(amount=amt, description=self.ids.order_desc.text or "General"))
        except: pass
        app.db.save(); self.ids.order_desc.text = self.ids.order_total.text = ''; self.edit_mode = False; self.apply_mode_ui(); self.refresh_ui()

    def back(self):
        self.manager.transition.direction = "right"
        self.manager.current = 'home' if App.get_running_app().current_customer_id is None else 'debtlist'