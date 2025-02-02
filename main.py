from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import Clock
import json
import os

# Глобальные переменные
score = 0
click_power = 1
auto_clickers = 0
auto_clicker_power = 1

# Цены на улучшения
click_power_price = 10
auto_clicker_price = 50
auto_clicker_power_price = 100

# Путь для сохранения данных
SAVE_FILE = "save.json"

class ClickerGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 10
        self.padding = 20
        self.load_data()

        # Основной интерфейс
        self.score_label = Label(text=f"Score: {score}", font_size=40, size_hint=(1, 0.2))
        self.add_widget(self.score_label)

        self.click_button = Button(text="Click Me!", font_size=30, size_hint=(1, 0.3), background_color=(0.2, 0.6, 1, 1))
        self.click_button.bind(on_press=self.handle_click)
        self.add_widget(self.click_button)

        self.shop_button = Button(text="Shop", font_size=30, size_hint=(1, 0.2), background_color=(0.9, 0.5, 0.2, 1))
        self.shop_button.bind(on_press=self.open_shop)
        self.add_widget(self.shop_button)

        self.exit_button = Button(text="Exit", font_size=30, size_hint=(1, 0.2), background_color=(0.8, 0.2, 0.2, 1))
        self.exit_button.bind(on_press=self.exit_game)
        self.add_widget(self.exit_button)

        # Автокликеры
        Clock.schedule_interval(self.auto_click, 1)

    def handle_click(self, instance):
        global score
        score += click_power
        self.update_score()

    def auto_click(self, dt):
        global score
        score += auto_clickers * auto_clicker_power
        self.update_score()

    def open_shop(self, instance):
        global score, click_power, auto_clickers, auto_clicker_power
        content = BoxLayout(orientation="vertical", spacing=10)
        popup = Popup(title="Shop", content=content, size_hint=(0.8, 0.8))

        # Улучшение силы клика
        self.upgrade_click_power_btn = Button(
            text=f"Upgrade Click Power (+1) - Cost: {click_power_price}",
            size_hint=(1, 0.2),
            background_color=(0.2, 0.8, 0.2, 1)
        )
        self.upgrade_click_power_btn.bind(on_press=lambda x: self.upgrade_click_power(popup))
        content.add_widget(self.upgrade_click_power_btn)

        # Покупка автокликера
        self.buy_auto_clicker_btn = Button(
            text=f"Buy Auto Clicker (+1) - Cost: {auto_clicker_price}",
            size_hint=(1, 0.2),
            background_color=(0.8, 0.2, 0.2, 1)
        )
        self.buy_auto_clicker_btn.bind(on_press=lambda x: self.buy_auto_clicker(popup))
        content.add_widget(self.buy_auto_clicker_btn)

        # Улучшение силы автокликера
        self.upgrade_auto_clicker_power_btn = Button(
            text=f"Upgrade Auto Clicker Power (+1) - Cost: {auto_clicker_power_price}",
            size_hint=(1, 0.2),
            background_color=(0.8, 0.8, 0.2, 1)
        )
        self.upgrade_auto_clicker_power_btn.bind(on_press=lambda x: self.upgrade_auto_clicker_power(popup))
        content.add_widget(self.upgrade_auto_clicker_power_btn)

        # Кнопка закрытия магазина
        close_btn = Button(text="Close Shop", size_hint=(1, 0.2), background_color=(0.5, 0.5, 0.5, 1))
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)

        popup.open()

    def update_score(self):
        self.score_label.text = f"Score: {score}"

    def upgrade_click_power(self, popup):
        global score, click_power, click_power_price
        if score >= click_power_price:
            score -= click_power_price
            click_power += 1
            click_power_price = int(click_power_price * 1.2)
            self.update_score()
            # Обновляем текст кнопки напрямую через атрибут
            self.upgrade_click_power_btn.text = f"Upgrade Click Power (+1) - Cost: {click_power_price}"
        else:
            self.show_popup("Not enough points!")

    def buy_auto_clicker(self, popup):
        global score, auto_clickers, auto_clicker_price
        if score >= auto_clicker_price:
            score -= auto_clicker_price
            auto_clickers += 1
            auto_clicker_price = int(auto_clicker_price * 1.2)
            self.update_score()
            # Обновляем текст кнопки напрямую через атрибут
            self.buy_auto_clicker_btn.text = f"Buy Auto Clicker (+1) - Cost: {auto_clicker_price}"
        else:
            self.show_popup("Not enough points!")

    def upgrade_auto_clicker_power(self, popup):
        global score, auto_clicker_power, auto_clicker_power_price
        if score >= auto_clicker_power_price:
            score -= auto_clicker_power_price
            auto_clicker_power += 1
            auto_clicker_power_price = int(auto_clicker_power_price * 1.2)
            self.update_score()
            # Обновляем текст кнопки напрямую через атрибут
            self.upgrade_auto_clicker_power_btn.text = f"Upgrade Auto Clicker Power (+1) - Cost: {auto_clicker_power_price}"
        else:
            self.show_popup("Not enough points!")

    def show_popup(self, message):
        popup = Popup(title="Info", content=Label(text=message), size_hint=(0.6, 0.4))
        popup.open()

    def load_data(self):
        global score, click_power, auto_clickers, auto_clicker_power, click_power_price, auto_clicker_price, auto_clicker_power_price
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as file:
                data = json.load(file)
                score = data.get("score", 0)
                click_power = data.get("click_power", 1)
                auto_clickers = data.get("auto_clickers", 0)
                auto_clicker_power = data.get("auto_clicker_power", 1)
                click_power_price = data.get("click_power_price", 10)
                auto_clicker_price = data.get("auto_clicker_price", 50)
                auto_clicker_power_price = data.get("auto_clicker_power_price", 100)

    def save_data(self):
        data = {
            "score": score,
            "click_power": click_power,
            "auto_clickers": auto_clickers,
            "auto_clicker_power": auto_clicker_power,
            "click_power_price": click_power_price,
            "auto_clicker_price": auto_clicker_price,
            "auto_clicker_power_price": auto_clicker_power_price
        }
        with open(SAVE_FILE, "w") as file:
            json.dump(data, file)

    def exit_game(self, instance):
        # Сохраняем данные перед выходом
        self.save_data()
        App.get_running_app().stop()  # Завершаем приложение

class ClickerApp(App):
    def build(self):
        return ClickerGame()

    def on_stop(self):
        # Сохраняем данные при выходе
        self.root.save_data()

if __name__ == "__main__":
    ClickerApp().run()
