import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.core.window import Window
from database import Database
from screens import HomeScreen, DebtListScreen, CustomerDetailScreen, PaidHistoryScreen

# Softinput mode ensures the keyboard doesn't cover text fields
Window.softinput_mode = "below_target"

class DEERApp(App):
    current_customer_id = None

    def build(self):
        self.db = Database()
        self.db.load()

        # Load KV files
        kv_path = os.path.join(os.path.dirname(__file__), 'kv_files')
        for kv in ['home.kv', 'debtlist.kv', 'customerdetail.kv', 'paidhistory.kv']:
            Builder.load_file(os.path.join(kv_path, kv))

        self.sm = ScreenManager(transition=SlideTransition())
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(DebtListScreen(name='debtlist'))
        self.sm.add_widget(PaidHistoryScreen(name='paidhistory'))
        self.sm.add_widget(CustomerDetailScreen(name='customerdetail'))

        # Bind the Android Back Button
        Window.bind(on_keyboard=self.on_key)
        return self.sm

    def on_key(self, window, key, *args):
        """Handles the Android Back Button (Key 27)."""
        if key == 27:
            if self.sm.current == 'home':
                return False  # Let Android close the app
            
            self.sm.transition.direction = 'right'
            if self.sm.current in ['debtlist', 'paidhistory']:
                self.sm.current = 'home'
            else:
                self.sm.current = 'debtlist'
            return True
        return False

    def on_pause(self):
        """Saves data when the app is minimized (e.g., phone call)."""
        self.db.save()
        return True

    def on_stop(self):
        """Final save when the app is fully closed."""
        self.db.save()

if __name__ == '__main__':
    DEERApp().run()