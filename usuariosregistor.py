import requests
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from firebase_admin import auth
from firebase_config import auth_client, db
from kivy.metrics import dp
from kivy.core.window import Window
from kivymd.uix.button import MDRaisedButton
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.image import Image
from kivymd.uix.list import OneLineIconListItem
from kivy.uix.textinput import TextInput

# Añade tu clave API de Firebase aquí
FIREBASE_API_KEY = "AIzaSyABKdIoKDpDLDGx_BXHVM7oTjECUjDd6qg"

Builder.load_string('''
<LoginScreen>:
    BoxLayout:
        orientation: "vertical"
        padding: dp(20)
        spacing: dp(20)
        canvas.before:
            Color:
                rgba: 0.6, 0.8, 1, 1  # Fondo azul claro
            Rectangle:
                pos: self.pos
                size: self.size
        MDLabel:
            text: "Iniciar Sesión"
            halign: "center"
            theme_text_color: "Custom"
            text_color: [0, 0, 0, 1]  # Texto negro
            font_style: "H5"

        MDTextField:
            id: email
            hint_text: "Correo Electrónico"
            mode: "line"
            size_hint_y: None
            height: dp(48)
            line_color_focus: [1, 1, 1, 1]  # Línea blanca al enfocarse
            text_color: [1, 1, 1, 1]  # Texto blanco
            hint_text_color: [1, 1, 1, 0.6]  # Texto de hint color gris claro
            background_color: [0, 0, 0, 1]  # Fondo negro

        BoxLayout:
            size_hint_y: None
            height: dp(48)

            MDTextField:
                id: password
                hint_text: "Contraseña"
                mode: "line"
                password: True
                size_hint_y: None
                height: dp(48)
                line_color_focus: [1, 1, 1, 1]
                text_color: [1, 1, 1, 1]
                hint_text_color: [1, 1, 1, 0.6]
                background_color: [0, 0, 0, 1]

            MDIconButton:
                icon: "eye-off"
                theme_text_color: "Custom"
                text_color: [1, 1, 1, 1]  # Icono blanco
                on_release: root.toggle_password_visibility("password")

        MDRaisedButton:
            text: "Ingresar"
            size_hint: (0.7, None) 
            height: dp(48)
            md_bg_color: [1, 1, 1, 1]  # Fondo blanco
            text_color: [0, 0, 0, 1]  # Texto negro
            pos_hint: {"center_x": 0.5}
            on_release: root.login_user()

        MDRaisedButton:
            text: "Registrarse"
            size_hint: (0.7, None) 
            height: dp(48)
            md_bg_color: [1, 1, 1, 1]
            text_color: [0, 0, 0, 1]
            pos_hint: {"center_x": 0.5}
            on_release: root.manager.current = "usuarios_screen"

<UsuariosCreados>:
    BoxLayout:
        orientation: "vertical"
        padding: dp(20)
        spacing: dp(20)
        canvas.before:
            Color:
                rgba: 0.6, 0.8, 1, 1 # Fondo azul claro
            Rectangle:
                pos: self.pos
                size: self.size

        MDLabel:
            text: "Registrarse"
            halign: "center"
            theme_text_color: "Custom"
            text_color: [0, 0, 0, 1]  # Texto blanco
            font_style: "H5"

        MDTextField:
            id: email
            hint_text: "Correo Electrónico"
            mode: "line"
            size_hint_y: None
            height: dp(48)
            line_color_focus: [1, 1, 1, 1]  # Línea blanca al enfocarse
            text_color: [1, 1, 1, 1]  # Texto blanco
            hint_text_color: [1, 1, 1, 0.6]  # Texto de hint color gris claro
            background_color: [0, 0, 0, 1]  # Fondo negro

        BoxLayout:
            size_hint_y: None
            height: dp(48)

            MDTextField:
                id: password
                hint_text: "Contraseña"
                mode: "line"
                password: True
                size_hint_y: None
                height: dp(48)
                line_color_focus: [1, 1, 1, 1]
                text_color: [1, 1, 1, 1]
                hint_text_color: [1, 1, 1, 0.6]
                background_color: [0, 0, 0, 1]

            MDIconButton:
                icon: "eye-off"
                theme_text_color: "Custom"
                text_color: [1, 1, 1, 1]  # Icono blanco
                on_release: root.toggle_password_visibility("password")

        BoxLayout:
            size_hint_y: None
            height: dp(48)

            MDTextField:
                id: confirm_password
                hint_text: "Confirmar Contraseña"
                mode: "line"
                password: True
                size_hint_y: None
                height: dp(48)
                line_color_focus: [1, 1, 1, 1]
                text_color: [1, 1, 1, 1]
                hint_text_color: [1, 1, 1, 0.6]
                background_color: [0, 0, 0, 1]

            MDIconButton:
                icon: "eye-off"
                theme_text_color: "Custom"
                text_color: [1, 1, 1, 1]  # Icono blanco
                on_release: root.toggle_password_visibility("confirm_password")

        MDRaisedButton:
            text: "Crear Cuenta"
            size_hint: (0.7, None)
            height: dp(48)
            md_bg_color: [1, 1, 1, 1]
            text_color: [0, 0, 0, 1]
            pos_hint: {"center_x": 0.5}
            on_release: root.register_user()

        MDRaisedButton:
            text: "Volver a Inicio de Sesión"
            size_hint: (0.7, None)
            height: dp(48)
            md_bg_color: [1, 1, 1, 1]
            text_color: [0, 0, 0, 1]
            pos_hint: {"center_x": 0.5}
            on_release: root.manager.current = "login_screen"
''')


class LoginScreen(Screen):
    password_visible = False  # Estado de visibilidad de la contraseña

    def toggle_password_visibility(self, field):
        # Cambia el estado de visibilidad de la contraseña
        self.password_visible = not self.password_visible
        self.ids[field].password = not self.password_visible

        # Cambia el ícono del botón
        icon_button = self.ids[field].parent.children[0]  # Accede al MDIconButton
        if self.password_visible:
            icon_button.icon = "eye"
        else:
            icon_button.icon = "eye-off"

    def login_user(self):
        email = self.ids.email.text
        password = self.ids.password.text

        if not email or not password:
            MDDialog(title="Error", text="Por favor, completa todos los campos.").open()
            return

        try:
            # Verificar las credenciales usando la API REST de Firebase
            response = requests.post(
                f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}",
                json={"email": email, "password": password, "returnSecureToken": True}
            )
            response_data = response.json()

            if response.status_code == 200:
                # Si la autenticación es exitosa
                id_token = response_data["idToken"]
                MDDialog(title="Éxito", text="Inicio de sesión exitoso").open()
                self.manager.current = "home_screen"
            else:
                MDDialog(title="Error", text="USUARIO/CONTRASEÑA incorrectos, intentelo de nuevo").open()
        except Exception as e:
            MDDialog(title="Error", text=str(e)).open()

class UsuariosCreados(Screen):
    password_visible = False  # Estado de visibilidad de la contraseña

    def toggle_password_visibility(self, field):
        # Cambia el estado de visibilidad de la contraseña
        self.password_visible = not self.password_visible
        self.ids[field].password = not self.password_visible

        # Cambia el ícono del botón
        icon_button = self.ids[field].parent.children[0]  # Accede al MDIconButton
        if self.password_visible:
            icon_button.icon = "eye"
        else:
            icon_button.icon = "eye-off"

    def register_user(self):
        email = self.ids.email.text
        password = self.ids.password.text
        confirm_password = self.ids.confirm_password.text

        if not email or not password or not confirm_password:
            MDDialog(title="Error", text="Por favor, completa todos los campos.").open()
            return

        if password != confirm_password:
            MDDialog(title="Error", text="Las contraseñas no coinciden.").open()
            return

        try:
            user = auth.create_user(email=email, password=password)
            db.collection("users").document(user.uid).set({"email": email})
            MDDialog(title="Éxito", text="Registro exitoso, redirigiendo al inicio...").open()
            self.manager.current = "home_screen"  # Redirige al home_screen
        except Exception as e:
            MDDialog(title="Error", text=str(e)).open()

class MyApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login_screen'))
        sm.add_widget(UsuariosCreados(name='usuarios_screen'))
        return sm

if __name__ == '__main__':
    MyApp().run()
