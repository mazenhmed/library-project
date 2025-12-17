from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.imagelist import MDSmartTile
from kivymd.uix.textfield import MDTextField
from kivymd.toast import toast
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from database import Database
import arabic_reshaper
from bidi.algorithm import get_display
import os
from kivy.clock import Clock

# Helper for Arabic Text
def reshape_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text, base_dir='R')

def set_toolbar_font(toolbar):
    if not toolbar:
        return
    # Recursive search for MDLabel to set font
    to_check = [toolbar]
    while to_check:
        widget = to_check.pop(0)
        if isinstance(widget, MDLabel):
            widget.font_name = FONT_PATH
        if hasattr(widget, 'children'):
            to_check.extend(widget.children)

# Absolute path to font
FONT_PATH = os.path.join(os.path.dirname(__file__), 'assets', 'fonts', 'arial.ttf')

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def on_enter(self):
        Clock.schedule_once(self.update_ui)

    def update_ui(self, dt):
        if 'toolbar' in self.ids:
            self.ids.toolbar.title = reshape_text("المكتبة المتكاملة")
            set_toolbar_font(self.ids.toolbar)
        
        # Clear existing widgets to refresh
        self.ids.content_layout.clear_widgets()
        
        # Welcome
        self.ids.content_layout.add_widget(MDLabel(
            text=reshape_text("مرحباً بكم في المكتبة المتكاملة"),
            halign="center",
            bold=True,
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(50),
            font_name=FONT_PATH
        ))

        # Ads Section
        app = MDApp.get_running_app()
        ads = app.api.get_ads()
        if ads:
            self.ids.content_layout.add_widget(MDLabel(text=reshape_text("الإعلانات"), halign="right", bold=True, size_hint_y=None, height=dp(40), font_name=FONT_PATH, theme_text_color="Custom", text_color=(0, 0.5, 0.5, 1)))
            ads_scroll = ScrollView(size_hint_y=None, height=dp(140))
            ads_grid = MDGridLayout(rows=1, spacing=dp(15), size_hint_x=None, padding=dp(10))
            ads_grid.bind(minimum_width=ads_grid.setter('width'))
            
            for ad in ads:
                card = MDCard(size_hint=(None, None), size=(dp(220), dp(110)), padding=dp(10), radius=[15], elevation=4)
                card.add_widget(MDLabel(text=reshape_text(ad['title']), halign="center", font_name=FONT_PATH, bold=True))
                ads_grid.add_widget(card)
            
            ads_scroll.add_widget(ads_grid)
            self.ids.content_layout.add_widget(ads_scroll)

        # Offers Section
        offers = app.api.get_offers()
        if offers:
            self.ids.content_layout.add_widget(MDLabel(text=reshape_text("العروض"), halign="right", bold=True, size_hint_y=None, height=dp(40), font_name=FONT_PATH, theme_text_color="Custom", text_color=(1, 0.5, 0, 1)))
            offers_scroll = ScrollView(size_hint_y=None, height=dp(140))
            offers_grid = MDGridLayout(rows=1, spacing=dp(15), size_hint_x=None, padding=dp(10))
            offers_grid.bind(minimum_width=offers_grid.setter('width'))
            
            for offer in offers:
                card = MDCard(size_hint=(None, None), size=(dp(220), dp(110)), padding=dp(10), radius=[15], elevation=4, md_bg_color=(1, 0.95, 0.9, 1))
                card.add_widget(MDLabel(text=reshape_text(f"{offer['title']}\n{offer['discount']}"), halign="center", font_name=FONT_PATH, theme_text_color="Custom", text_color=(0.8, 0.2, 0, 1)))
                offers_grid.add_widget(card)
            
            offers_scroll.add_widget(offers_grid)
            self.ids.content_layout.add_widget(offers_scroll)

        # Categories Grid
        self.ids.content_layout.add_widget(MDLabel(text=reshape_text("الأقسام"), halign="right", bold=True, size_hint_y=None, height=dp(40), font_name=FONT_PATH, theme_text_color="Primary"))
        
        grid = MDGridLayout(cols=2, spacing=dp(15), size_hint_y=None, padding=dp(5))
        grid.bind(minimum_height=grid.setter('height'))
        
        categories = app.api.get_categories()
        for cat in categories:
            card = MDCard(
                orientation='vertical',
                size_hint_y=None,
                height=dp(130),
                radius=[20],
                elevation=3,
                on_release=lambda x, c=cat: self.open_category(c),
                padding=dp(10)
            )
            card.add_widget(MDIconButton(icon=cat['icon'] or 'book', pos_hint={'center_x': 0.5}, icon_size="56sp", theme_text_color="Custom", text_color=app.theme_cls.primary_color))
            card.add_widget(MDLabel(text=reshape_text(cat['name']), halign="center", bold=True, font_name=FONT_PATH))
            grid.add_widget(card)
            
        self.ids.content_layout.add_widget(grid)

    def build_ui(self):
        # Initial setup only, content loaded in update_ui
        pass

    def open_category(self, category):
        app = MDApp.get_running_app()
        app.current_category = category
        self.manager.current = 'products'

class ProductsScreen(MDScreen):
    def on_enter(self):
        Clock.schedule_once(self.update_ui)

    def update_ui(self, dt):
        self.ids.grid.clear_widgets()
        app = MDApp.get_running_app()
        category = app.current_category
        
        if 'toolbar' in self.ids:
            self.ids.toolbar.title = reshape_text("المنتجات")
            set_toolbar_font(self.ids.toolbar)
        
        self.ids.title.text = reshape_text(f"منتجات {category['name']}")
        self.ids.title.font_name = FONT_PATH
        
        products = app.api.get_products(category['name'])
        
        if not products:
            self.ids.grid.add_widget(MDLabel(text=reshape_text("لا توجد منتجات"), halign="center", font_name=FONT_PATH))
            return

        for p in products:
            card = MDCard(orientation='vertical', size_hint_y=None, height=dp(200), padding=dp(10), radius=[15], elevation=3)
            
            # Image placeholder
            card.add_widget(MDIconButton(icon="book-open-variant", pos_hint={'center_x': 0.5}, icon_size="64sp"))
            
            card.add_widget(MDLabel(text=reshape_text(p['name']), halign="center", bold=True, font_name=FONT_PATH))
            card.add_widget(MDLabel(text=f"{p['price']} RY", halign="center", theme_text_color="Secondary"))
            
            btn = MDFillRoundFlatButton(
                text=reshape_text("إضافة للسلة"),
                pos_hint={'center_x': 0.5},
                on_release=lambda x, prod=p: self.add_to_cart(prod),
                font_name=FONT_PATH
            )
            card.add_widget(btn)
            self.ids.grid.add_widget(card)

    def add_to_cart(self, product):
        app = MDApp.get_running_app()
        app.cart.append(product)
        toast(reshape_text(f"تم إضافة {product['name']}"))

class CartScreen(MDScreen):
    def on_enter(self):
        Clock.schedule_once(self.update_cart_ui)

    def update_cart_ui(self, dt):
        self.ids.cart_list.clear_widgets()
        app = MDApp.get_running_app()
        
        if 'toolbar' in self.ids:
            self.ids.toolbar.title = reshape_text("سلة المشتريات")
            set_toolbar_font(self.ids.toolbar)
        
        total = 0
        for item in app.cart:
            card = MDCard(orientation='horizontal', size_hint_y=None, height=dp(80), padding=dp(10), spacing=dp(10))
            card.add_widget(MDIconButton(icon="book", pos_hint={'center_y': 0.5}))
            
            box = MDBoxLayout(orientation='vertical')
            box.add_widget(MDLabel(text=reshape_text(item['name']), bold=True, font_name=FONT_PATH))
            box.add_widget(MDLabel(text=f"{item['price']} RY", theme_text_color="Secondary"))
            card.add_widget(box)
            
            total += item['price']
            self.ids.cart_list.add_widget(card)
            
        self.ids.total_label.text = reshape_text(f"الإجمالي: {total} ريال")
        self.ids.total_label.font_name = FONT_PATH

    def checkout(self):
        app = MDApp.get_running_app()
        if not app.cart:
            toast(reshape_text("السلة فارغة"))
            return
        
        # Calculate total and items count
        total = sum(item['price'] for item in app.cart)
        items_count = len(app.cart)
        
        # Save order to DB
        # Save order to DB via API
        if app.api.add_order(total, items_count):
             toast(reshape_text("تم الطلب بنجاح!"))
        else:
             toast(reshape_text("فشل في إرسال الطلب"))
        app.cart = []
        self.on_enter()

class AdminScreen(MDScreen):
    def on_enter(self):
        Clock.schedule_once(self.set_admin_text)

    def set_admin_text(self, dt):
        if 'toolbar' in self.ids:
            self.ids.toolbar.title = reshape_text("الإدارة")
            set_toolbar_font(self.ids.toolbar)
        self.ids.user.hint_text = reshape_text("اسم المستخدم")
        self.ids.pwd.hint_text = reshape_text("كلمة المرور")
        self.ids.login_btn.text = reshape_text("تسجيل الدخول")

    def login(self, username, password):
        app = MDApp.get_running_app()
        user_data = app.api.login(username, password)
        if user_data and user_data.get('isLoggedIn'):
            toast(reshape_text("تم تسجيل الدخول"))
            app.change_screen('admin_dashboard')
        else:
            toast(reshape_text("بيانات خاطئة"))

class AdminDashboardScreen(MDScreen):
    def on_enter(self):
        Clock.schedule_once(self.set_text)

    def set_text(self, dt):
        if 'toolbar' in self.ids:
            self.ids.toolbar.title = reshape_text("لوحة التحكم")
            set_toolbar_font(self.ids.toolbar)
        self.ids.btn_add_product.text = reshape_text("إضافة منتج")
        self.ids.btn_add_category.text = reshape_text("إضافة قسم")
        self.ids.btn_manage_ads.text = reshape_text("إدارة الإعلانات")
        self.ids.btn_manage_offers.text = reshape_text("إدارة العروض")
        self.ids.btn_generate_report.text = reshape_text("تحميل التقرير (PDF)")
        self.ids.btn_logout.text = reshape_text("تسجيل الخروج")

    def generate_report(self):
        try:
            from reportlab.pdfgen import canvas
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            from reportlab.lib.pagesizes import A4
        except ImportError:
            toast(reshape_text("مكتبة التقرير غير متوفرة"))
            return

        app = MDApp.get_running_app()
        stats = app.api.get_stats()
        
        # File path
        from kivy.utils import platform
        if platform == 'android':
            from android.storage import primary_external_storage_path
            dir_path = primary_external_storage_path()
            download_dir = os.path.join(dir_path, 'Download')
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)
            file_path = os.path.join(download_dir, 'library_report.pdf')
        else:
            # Save to Desktop on Windows
            desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
            file_path = os.path.join(desktop, 'library_report.pdf')

        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4
        
        # Register Font
        try:
            pdfmetrics.registerFont(TTFont('Arabic', FONT_PATH))
        except:
            pass # Font might already be registered or path issue

        def draw_arabic(text, x, y, font_size=14):
            reshaped = arabic_reshaper.reshape(text)
            bidi_text = get_display(reshaped, base_dir='R')
            c.setFont('Arabic', font_size)
            c.drawRightString(x, y, bidi_text)

        # Title
        draw_arabic("تقرير المكتبة المتكاملة", width - 50, height - 50, 24)
        
        y = height - 100
        line_height = 30
        
        # General Stats
        draw_arabic(f"عدد الأقسام: {stats['categories_count']}", width - 50, y)
        y -= line_height
        draw_arabic(f"عدد المنتجات: {stats['products_count']}", width - 50, y)
        y -= line_height
        draw_arabic(f"عدد الطلبات: {stats['orders_count']}", width - 50, y)
        y -= line_height
        draw_arabic(f"عدد الإعلانات: {stats['ads_count']}", width - 50, y)
        y -= line_height
        draw_arabic(f"عدد العروض: {stats['offers_count']}", width - 50, y)
        y -= line_height * 2
        
        # Products per Category
        draw_arabic("تفاصيل الأقسام:", width - 50, y, 18)
        y -= line_height
        
        for cat_name, count in stats['products_per_category']:
            draw_arabic(f"- {cat_name}: {count} منتج", width - 70, y)
            y -= line_height

        c.save()
        toast(reshape_text(f"تم حفظ التقرير في: {file_path}"))

    def logout(self):
        app = MDApp.get_running_app()
        app.change_screen('home')
        toast(reshape_text("تم تسجيل الخروج"))

class AddProductScreen(MDScreen):
    def on_enter(self):
        Clock.schedule_once(self.set_text)

    def set_text(self, dt):
        if 'toolbar' in self.ids:
            self.ids.toolbar.title = reshape_text("إضافة منتج")
            set_toolbar_font(self.ids.toolbar)
        self.ids.name.hint_text = reshape_text("اسم المنتج")
        self.ids.price.hint_text = reshape_text("السعر")
        self.ids.category.hint_text = reshape_text("اسم القسم")
        self.ids.btn_add.text = reshape_text("إضافة")

    def add_product(self, name, price, category_name):
        if not name or not price or not category_name:
            toast(reshape_text("يرجى ملء جميع الحقول"))
            return

        app = MDApp.get_running_app()
        try:
            if app.api.add_product(name, price, category_name):
                toast(reshape_text("تم إضافة المنتج بنجاح"))
                self.ids.name.text = ""
                self.ids.price.text = ""
                self.ids.category.text = ""
            else:
                toast(reshape_text("حدث خطأ، تأكد من اسم القسم"))
        except ValueError:
            toast(reshape_text("السعر يجب أن يكون رقماً"))

class AddCategoryScreen(MDScreen):
    def on_enter(self):
        Clock.schedule_once(self.set_text)

    def set_text(self, dt):
        if 'toolbar' in self.ids:
            self.ids.toolbar.title = reshape_text("إضافة قسم")
            set_toolbar_font(self.ids.toolbar)
        self.ids.name.hint_text = reshape_text("اسم القسم")
        self.ids.icon.hint_text = reshape_text("أيقونة (اختياري)")
        self.ids.btn_add.text = reshape_text("إضافة")

    def add_category(self, name, icon):
        if not name:
            toast(reshape_text("يرجى إدخال اسم القسم"))
            return

        app = MDApp.get_running_app()
        if app.api.add_category(name, icon):
            toast(reshape_text("تم إضافة القسم بنجاح"))
            self.ids.name.text = ""
            self.ids.icon.text = ""
        else:
            toast(reshape_text("القسم موجود مسبقاً أو حدث خطأ"))

class ManageAdsScreen(MDScreen):
    def on_enter(self):
        Clock.schedule_once(self.update_ui)

    def update_ui(self, dt):
        if 'toolbar' in self.ids:
            self.ids.toolbar.title = reshape_text("إدارة الإعلانات")
            set_toolbar_font(self.ids.toolbar)
        self.ids.title.hint_text = reshape_text("عنوان الإعلان")
        self.ids.desc.hint_text = reshape_text("الوصف")
        self.ids.btn_add.text = reshape_text("إضافة إعلان")
        
        self.load_ads()

    def load_ads(self):
        self.ids.ads_list.clear_widgets()
        app = MDApp.get_running_app()
        ads = app.api.get_ads()
        for ad in ads:
            item = MDCard(orientation='horizontal', size_hint_y=None, height=dp(80), padding=dp(10), spacing=dp(10))
            item.add_widget(MDLabel(text=reshape_text(ad['title']), font_name=FONT_PATH))
            btn = MDIconButton(icon="delete", on_release=lambda x, a_id=ad['id']: self.delete_ad(a_id))
            item.add_widget(btn)
            self.ids.ads_list.add_widget(item)

    def add_ad(self, title, desc):
        if not title or not desc:
            toast(reshape_text("يرجى ملء البيانات"))
            return
        app = MDApp.get_running_app()
        if app.api.add_ad(title, desc):
            toast(reshape_text("تم إضافة الإعلان"))
            self.ids.title.text = ""
            self.ids.desc.text = ""
            self.load_ads()
        else:
            toast(reshape_text("حدث خطأ"))

    def delete_ad(self, ad_id):
        app = MDApp.get_running_app()
        if app.api.delete_ad(ad_id):
            toast(reshape_text("تم حذف الإعلان"))
            self.load_ads()
        else:
            toast(reshape_text("حدث خطأ"))

class ManageOffersScreen(MDScreen):
    def on_enter(self):
        Clock.schedule_once(self.update_ui)

    def update_ui(self, dt):
        if 'toolbar' in self.ids:
            self.ids.toolbar.title = reshape_text("إدارة العروض")
            set_toolbar_font(self.ids.toolbar)
        self.ids.title.hint_text = reshape_text("عنوان العرض")
        self.ids.discount.hint_text = reshape_text("الخصم (مثال: 50%)")
        self.ids.btn_add.text = reshape_text("إضافة عرض")
        
        self.load_offers()

    def load_offers(self):
        self.ids.offers_list.clear_widgets()
        app = MDApp.get_running_app()
        offers = app.api.get_offers()
        for offer in offers:
            item = MDCard(orientation='horizontal', size_hint_y=None, height=dp(80), padding=dp(10), spacing=dp(10))
            item.add_widget(MDLabel(text=reshape_text(f"{offer['title']} - {offer['discount']}"), font_name=FONT_PATH))
            btn = MDIconButton(icon="delete", on_release=lambda x, o_id=offer['id']: self.delete_offer(o_id))
            item.add_widget(btn)
            self.ids.offers_list.add_widget(item)

    def add_offer(self, title, discount):
        if not title or not discount:
            toast(reshape_text("يرجى ملء البيانات"))
            return
        app = MDApp.get_running_app()
        if app.api.add_offer(title, discount):
            toast(reshape_text("تم إضافة العرض"))
            self.ids.title.text = ""
            self.ids.discount.text = ""
            self.load_offers()
        else:
            toast(reshape_text("حدث خطأ"))

    def delete_offer(self, offer_id):
        app = MDApp.get_running_app()
        if app.api.delete_offer(offer_id):
            toast(reshape_text("تم حذف العرض"))
            self.load_offers()
        else:
            toast(reshape_text("حدث خطأ"))
