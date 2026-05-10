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
            for o in cust.orders:
                o.is_paid = True
            app.db.save()
            app.root.get_screen('debtlist').update_list()
            app.root.get_screen('paidhistory').update_list()

    def mark_as_unpaid(self):
        app = App.get_running_app()
        cust = app.db.get_customer(self.customer_id)
        if cust:
            for o in cust.orders:
                o.is_paid = False
            app.db.save()
            app.root.get_screen('paidhistory').update_list()
            app.root.get_screen('debtlist').update_list()

    def confirm_delete(self):
        content = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15))
        content.add_widget(Label(text="Delete this customer and all records?", halign='center', color=(0.88, 0.91, 0.95, 1)))
        btns = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        yes = Button(text="DELETE", background_color=(0.8, 0.2, 0.2, 1), background_normal='', bold=True)
        no = Button(text="CANCEL", background_color=(0.2, 0.26, 0.36, 1), background_normal='', bold=True)
        btns.add_widget(no)
        btns.add_widget(yes)
        content.add_widget(btns)
        popup = Popup(title="Confirm Deletion", content=content, size_hint=(0.85, 0.3),
                      title_align='center', background='', background_color=(0.1, 0.13, 0.19, 1),
                      separator_color=(0.22, 0.58, 0.27, 1))
        yes.bind(on_release=lambda x: self.execute_delete(popup))
        no.bind(on_release=popup.dismiss)
        popup.open()

    def execute_delete(self, popup):
        app = App.get_running_app()
        app.db.customers = [c for c in app.db.customers if c.id != self.customer_id]
        app.db.save()
        popup.dismiss()
        app.root.get_screen('paidhistory').update_list()
        app.root.get_screen('debtlist').update_list()

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
    def on_pre_enter(self):
        self.update_list()

    def update_list(self, search=''):
        app = App.get_running_app()
        if 'rv' not in self.ids:
            return
        customers = app.db.search_customers(search) if search else app.db.customers
        active = [c for c in customers if c.unpaid_total() > 0]
        self.ids.rv.data = [
            {
                'customer_id': c.id,
                'text': f"[b]{c.name}[/b]",
                'address_text': c.address,
                'debt_text': f"₱ {c.unpaid_total():.2f}"
            } for c in active
        ]

class PaidHistoryScreen(Screen):
    def on_pre_enter(self):
        self.update_list()

    def update_list(self, search=''):
        app = App.get_running_app()
        if 'rv' not in self.ids:
            return
        customers = app.db.search_customers(search) if search else app.db.customers
        paid = [c for c in customers if any(o.is_paid for o in c.orders) and c.unpaid_total() == 0]
        self.ids.rv.data = [
            {
                'customer_id': c.id,
                'text': f"[b]{c.name}[/b]",
                'address_text': c.address,
                'debt_text': "SETTLED"
            } for c in paid
        ]

class CustomerDetailScreen(Screen):
    edit_mode = False

    def on_pre_enter(self):
        app = App.get_running_app()
        self.edit_mode = not bool(app.current_customer_id)
        self.apply_mode_ui()
        self.refresh_ui()

    def call_customer(self):
        phone = self.ids.phone_input.text.strip()
        if phone:
            webbrowser.open(f"tel:{phone}")

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        self.apply_mode_ui()
        if not self.edit_mode:
            self.refresh_ui()

    def apply_mode_ui(self):
        app = App.get_running_app()
        is_new = app.current_customer_id is None
        editable = (is_new or self.edit_mode)
        self.ids.name_input.disabled = not editable
        self.ids.phone_input.disabled = not editable
        self.ids.address_input.disabled = not editable
        self.ids.edit_toggle_btn.opacity = 0 if is_new else 1
        self.ids.edit_actions.height = dp(50) if self.edit_mode and not is_new else 0
        self.ids.edit_actions.opacity = 1 if self.edit_mode and not is_new else 0
        self.ids.edit_toggle_btn.text = "CANCEL" if self.edit_mode else "EDIT"
        self.ids.new_order_section.height = dp(240) if is_new or self.edit_mode else 0
        self.ids.new_order_section.opacity = 1 if is_new or self.edit_mode else 0
        self.ids.phone_input.hint_text = 'Add Phone Number (Optional)' if (is_new or self.edit_mode) else ''

    def refresh_ui(self):
        app = App.get_running_app()
        # Reset basic fields
        if not app.current_customer_id:
            for f in ['name_input', 'phone_input', 'address_input']:
                self.ids[f].text = ''
            self.ids.history_container.clear_widgets()
            self.ids.balance_label.text = "BALANCE: ₱0.00"
            return

        cust = app.db.get_customer(app.current_customer_id)
        if cust:
            self.ids.name_input.text = cust.name
            self.ids.phone_input.text = cust.phone
            self.ids.address_input.text = cust.address
            
            # Rebuild Transaction History Rows
            container = self.ids.history_container
            container.clear_widgets()
            
            for o in cust.orders:
                status_color = "4caf50" if o.is_paid else "ef5350"
                status_text = "(Paid)" if o.is_paid else "(Unpaid)"
                
                row_text = f"• {o.date}: {o.description} - [b]₱{o.amount:.2f}[/b] [color={status_color}]{status_text}[/color]"
                
                # Create a clickable button for each row
                btn = Button(
                    text=row_text,
                    markup=True,
                    size_hint_y=None,
                    height=dp(40),
                    background_normal='',
                    background_color=(0, 0, 0, 0),
                    halign='left',
                    valign='middle',
                    font_size='13sp'
                )
                btn.bind(size=btn.setter('text_size'))
                # Bind the specific order to the toggle function
                btn.bind(on_release=lambda x, order=o: self.toggle_order_status(order))
                
                container.add_widget(btn)

            self.ids.balance_label.text = f"BALANCE: ₱{cust.unpaid_total():.2f}"

    def toggle_order_status(self, order):
        """Toggles a specific order's paid status and refreshes screen."""
        order.is_paid = not order.is_paid
        App.get_running_app().db.save()
        self.refresh_ui()

    def update_customer_info(self):
        app = App.get_running_app()
        cust = app.db.get_customer(app.current_customer_id)
        if cust:
            cust.name = self.ids.name_input.text.strip()
            cust.phone = self.ids.phone_input.text.strip()
            cust.address = self.ids.address_input.text.strip()
            app.db.save()
            self.edit_mode = False
            self.apply_mode_ui()
            self.refresh_ui()

    def delete_customer(self):
        content = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15))
        content.add_widget(Label(text="Delete this customer and all records?", halign='center', color=(0.88, 0.91, 0.95, 1)))
        btns = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        yes = Button(text="DELETE", background_color=(0.8, 0.2, 0.2, 1), background_normal='', bold=True)
        no = Button(text="CANCEL", background_color=(0.2, 0.26, 0.36, 1), background_normal='', bold=True)
        btns.add_widget(no)
        btns.add_widget(yes)
        content.add_widget(btns)
        popup = Popup(title="Confirm Deletion", content=content, size_hint=(0.85, 0.3),
                      title_align='center', background='', background_color=(0.1, 0.13, 0.19, 1),
                      separator_color=(0.22, 0.58, 0.27, 1))
        app = App.get_running_app()
        def do_delete(x):
            app.db.customers = [c for c in app.db.customers if c.id != app.current_customer_id]
            app.db.save()
            popup.dismiss()
            self.manager.transition.direction = "right"
            self.manager.current = 'debtlist'
        yes.bind(on_release=do_delete)
        no.bind(on_release=popup.dismiss)
        popup.open()

    def add_order(self):
        from models import Customer, Order
        app = App.get_running_app()
        name = self.ids.name_input.text.strip()
        if not name:
            return
        cust = app.db.get_customer(app.current_customer_id) if app.current_customer_id else next(
            (c for c in app.db.customers if c.name.lower() == name.lower()), None)
        if not cust:
            cust = Customer(name=name, phone=self.ids.phone_input.text, address=self.ids.address_input.text)
            app.db.customers.append(cust)
        app.current_customer_id = cust.id
        try:
            amt = float(self.ids.order_total.text)
            if amt > 0:
                cust.orders.append(Order(amount=amt, description=self.ids.order_desc.text or "General"))
        except:
            pass
        app.db.save()
        self.ids.order_desc.text = ''
        self.ids.order_total.text = ''
        self.edit_mode = False
        self.apply_mode_ui()
        self.refresh_ui()

    def back(self):
        self.manager.transition.direction = "right"
        self.manager.current = 'home' if App.get_running_app().current_customer_id is None else 'debtlist'
