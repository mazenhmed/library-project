from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window
from screens import HomeScreen, ProductsScreen, CartScreen, AdminScreen, AdminDashboardScreen, AddProductScreen, AddCategoryScreen, ManageAdsScreen, ManageOffersScreen
from api_client import APIClient
import arabic_reshaper
from bidi.algorithm import get_display
import os

# Set window size for mobile simulation
Window.size = (360, 640)

# Absolute path to font, ensuring forward slashes for KV
FONT_PATH = os.path.join(os.path.dirname(__file__), 'assets', 'fonts', 'arial.ttf').replace('\\', '/')

# Register Arabic Font globally
from kivy.core.text import LabelBase
LabelBase.register(name="Roboto", fn_regular=FONT_PATH, fn_bold=FONT_PATH)
LabelBase.register(name="Roboto-Bold", fn_regular=FONT_PATH)
LabelBase.register(name="Roboto-Medium", fn_regular=FONT_PATH)
LabelBase.register(name="Roboto-Regular", fn_regular=FONT_PATH)
LabelBase.register(name="Roboto-Light", fn_regular=FONT_PATH)
LabelBase.register(name="Roboto-Thin", fn_regular=FONT_PATH)
LabelBase.register(name="Roboto-Black", fn_regular=FONT_PATH)

KV = f'''
ScreenManager:
    HomeScreen:
        name: 'home'
    ProductsScreen:
        name: 'products'
    CartScreen:
        name: 'cart'
    AdminScreen:
        name: 'admin'
    AdminDashboardScreen:
        name: 'admin_dashboard'
    AddProductScreen:
        name: 'add_product'
    AddCategoryScreen:
        name: 'add_category'
    ManageAdsScreen:
        name: 'manage_ads'
    ManageOffersScreen:
        name: 'manage_offers'

<HomeScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            id: toolbar
            right_action_items: [["cart", lambda x: app.change_screen('cart')], ["account", lambda x: app.change_screen('admin')]]
            elevation: 4
            title_font_name: '{FONT_PATH}'

        ScrollView:
            MDBoxLayout:
                id: content_layout
                orientation: 'vertical'
                padding: dp(10)
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height

<ProductsScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            id: toolbar
            left_action_items: [["arrow-left", lambda x: app.change_screen('home')]]
            elevation: 4
            title_font_name: '{FONT_PATH}'
            
        MDLabel:
            id: title
            text: ""
            halign: "center"
            bold: True
            size_hint_y: None
            height: dp(50)
            font_name: '{FONT_PATH}'
            
        ScrollView:
            MDGridLayout:
                id: grid
                cols: 1
                spacing: dp(10)
                padding: dp(10)
                size_hint_y: None
                height: self.minimum_height

<CartScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            id: toolbar
            left_action_items: [["arrow-left", lambda x: app.change_screen('home')]]
            elevation: 4
            title_font_name: '{FONT_PATH}'
            
        ScrollView:
            MDBoxLayout:
                id: cart_list
                orientation: 'vertical'
                spacing: dp(10)
                padding: dp(10)
                size_hint_y: None
                height: self.minimum_height
                
        MDCard:
            size_hint_y: None
            height: dp(100)
            padding: dp(20)
            elevation: 10
            
            MDBoxLayout:
                orientation: 'vertical'
                MDLabel:
                    id: total_label
                    text: "الإجمالي: 0 ريال"
                    halign: "right"
                    bold: True
                    font_name: '{FONT_PATH}'
                
                MDFillRoundFlatButton:
                    text: "إتمام الشراء"
                    pos_hint: {{'center_x': 0.5}}
                    on_release: root.checkout()
                    font_name: '{FONT_PATH}'

<AdminScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        
        MDTopAppBar:
            id: toolbar
            left_action_items: [["arrow-left", lambda x: app.change_screen('home')]]
            pos_hint: {{'top': 1}}
            title_font_name: '{FONT_PATH}'
            
        MDBoxLayout:
            orientation: 'vertical'
            spacing: dp(20)
            pos_hint: {{'center_y': 0.5}}
            adaptive_height: True
            
            MDTextField:
                id: user
                icon_right: "account"
                font_name: '{FONT_PATH}'
                font_name_hint_text: '{FONT_PATH}'
                base_direction: 'rtl'
                halign: 'right'
                
            MDTextField:
                id: pwd
                icon_right: "key"
                password: True
                font_name: '{FONT_PATH}'
                font_name_hint_text: '{FONT_PATH}'
                base_direction: 'rtl'
                halign: 'right'
                
            MDFillRoundFlatButton:
                id: login_btn
                pos_hint: {{'center_x': 0.5}}
                on_release: root.login(user.text, pwd.text)
                font_name: '{FONT_PATH}'

<AdminDashboardScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        
        MDTopAppBar:
            id: toolbar
            left_action_items: [["arrow-left", lambda x: app.change_screen('admin')]]
            pos_hint: {{'top': 1}}
            title_font_name: '{FONT_PATH}'
            
        MDBoxLayout:
            orientation: 'vertical'
            spacing: dp(20)
            pos_hint: {{'center_y': 0.5}}
            adaptive_height: True
            
            MDFillRoundFlatButton:
                id: btn_add_product
                pos_hint: {{'center_x': 0.5}}
                on_release: app.change_screen('add_product')
                font_name: '{FONT_PATH}'
                
            MDFillRoundFlatButton:
                id: btn_add_category
                pos_hint: {{'center_x': 0.5}}
                on_release: app.change_screen('add_category')
                font_name: '{FONT_PATH}'

            MDFillRoundFlatButton:
                id: btn_manage_ads
                pos_hint: {{'center_x': 0.5}}
                on_release: app.change_screen('manage_ads')
                font_name: '{FONT_PATH}'

            MDFillRoundFlatButton:
                id: btn_manage_offers
                pos_hint: {{'center_x': 0.5}}
                on_release: app.change_screen('manage_offers')
                font_name: '{FONT_PATH}'

            MDFillRoundFlatButton:
                id: btn_generate_report
                pos_hint: {{'center_x': 0.5}}
                on_release: root.generate_report()
                font_name: '{FONT_PATH}'
                
            MDFillRoundFlatButton:
                id: btn_logout
                pos_hint: {{'center_x': 0.5}}
                on_release: root.logout()
                font_name: '{FONT_PATH}'
                md_bg_color: 1, 0, 0, 1

<AddProductScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        
        MDTopAppBar:
            id: toolbar
            left_action_items: [["arrow-left", lambda x: app.change_screen('admin_dashboard')]]
            pos_hint: {{'top': 1}}
            title_font_name: '{FONT_PATH}'
            
        MDBoxLayout:
            orientation: 'vertical'
            spacing: dp(20)
            pos_hint: {{'center_y': 0.5}}
            adaptive_height: True
            
            MDTextField:
                id: name
                font_name: '{FONT_PATH}'
                font_name_hint_text: '{FONT_PATH}'
                base_direction: 'rtl'
                halign: 'right'
                
            MDTextField:
                id: price
                input_filter: 'float'
                font_name: '{FONT_PATH}'
                font_name_hint_text: '{FONT_PATH}'
                base_direction: 'rtl'
                halign: 'right'
                
            MDTextField:
                id: category
                font_name: '{FONT_PATH}'
                font_name_hint_text: '{FONT_PATH}'
                base_direction: 'rtl'
                halign: 'right'
                
            MDFillRoundFlatButton:
                id: btn_add
                pos_hint: {{'center_x': 0.5}}
                on_release: root.add_product(name.text, price.text, category.text)
                font_name: '{FONT_PATH}'

<AddCategoryScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        
        MDTopAppBar:
            id: toolbar
            left_action_items: [["arrow-left", lambda x: app.change_screen('admin_dashboard')]]
            pos_hint: {{'top': 1}}
            title_font_name: '{FONT_PATH}'
            
        MDBoxLayout:
            orientation: 'vertical'
            spacing: dp(20)
            pos_hint: {{'center_y': 0.5}}
            adaptive_height: True
            
            MDTextField:
                id: name
                font_name: '{FONT_PATH}'
                font_name_hint_text: '{FONT_PATH}'
                base_direction: 'rtl'
                halign: 'right'
                
            MDTextField:
                id: icon
                font_name: '{FONT_PATH}'
                font_name_hint_text: '{FONT_PATH}'
                base_direction: 'rtl'
                halign: 'right'
                
            MDFillRoundFlatButton:
                id: btn_add
                pos_hint: {{'center_x': 0.5}}
                on_release: root.add_category(name.text, icon.text)
                font_name: '{FONT_PATH}'

<ManageAdsScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            id: toolbar
            left_action_items: [["arrow-left", lambda x: app.change_screen('admin_dashboard')]]
            title_font_name: '{FONT_PATH}'
            
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(20)
            spacing: dp(10)
            adaptive_height: True
            
            MDTextField:
                id: title
                font_name: '{FONT_PATH}'
                font_name_hint_text: '{FONT_PATH}'
                base_direction: 'rtl'
                halign: 'right'
            
            MDTextField:
                id: desc
                font_name: '{FONT_PATH}'
                font_name_hint_text: '{FONT_PATH}'
                base_direction: 'rtl'
                halign: 'right'
                
            MDFillRoundFlatButton:
                id: btn_add
                pos_hint: {{'center_x': 0.5}}
                on_release: root.add_ad(title.text, desc.text)
                font_name: '{FONT_PATH}'
                
        ScrollView:
            MDBoxLayout:
                id: ads_list
                orientation: 'vertical'
                spacing: dp(10)
                padding: dp(10)
                size_hint_y: None
                height: self.minimum_height

<ManageOffersScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            id: toolbar
            left_action_items: [["arrow-left", lambda x: app.change_screen('admin_dashboard')]]
            title_font_name: '{FONT_PATH}'
            
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(20)
            spacing: dp(10)
            adaptive_height: True
            
            MDTextField:
                id: title
                font_name: '{FONT_PATH}'
                font_name_hint_text: '{FONT_PATH}'
                base_direction: 'rtl'
                halign: 'right'
            
            MDTextField:
                id: discount
                font_name: '{FONT_PATH}'
                font_name_hint_text: '{FONT_PATH}'
                base_direction: 'rtl'
                halign: 'right'
                
            MDFillRoundFlatButton:
                id: btn_add
                pos_hint: {{'center_x': 0.5}}
                on_release: root.add_offer(title.text, discount.text)
                font_name: '{FONT_PATH}'
                
        ScrollView:
            MDBoxLayout:
                id: offers_list
                orientation: 'vertical'
                spacing: dp(10)
                padding: dp(10)
                size_hint_y: None
                height: self.minimum_height
'''

class LibraryApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Orange"
        self.theme_cls.theme_style = "Light"
        
        # App State
        self.cart = []
        self.current_category = None
        self.api = APIClient()
        
        return Builder.load_string(KV)

    def change_screen(self, screen_name):
        self.root.current = screen_name

if __name__ == '__main__':
    LibraryApp().run()
