from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.image import Image
from kivymd.uix.list import OneLineIconListItem
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from register import RegisterScreen
from firebase_config import db  
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.graphics import Color, Rectangle
import requests
from firebase_admin import credentials, firestore, auth
from firebase_config import auth_client
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.textfield import MDTextField
from usuariosregistor import LoginScreen, UsuariosCreados
#from statistics_screen import StatisticsScreen

Window.size = (360, 640)

Builder.load_string("""
<MainScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        canvas.before:
            Color:
                rgba: [13/255, 155/255, 203/255, 1]
            Rectangle:
                pos: self.pos
                size: self.size
        Image:
            source: 'assets/Logo.jpg'
            size_hint: (1, 1)
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            allow_stretch: True
            keep_ratio: True
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(50)
            MDRaisedButton:
                text: "Inicio"
                size_hint: (0.3, 1)
                md_bg_color: app.theme_cls.primary_color
                pos_hint: {"center_x": 0.5}
                on_release:
                    app.root.current = 'login_screen'

<HomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        canvas.before:
            Color:
                rgba: app.theme_cls.primary_color
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(50)  
            MDRaisedButton:
                text: "Ver Registros"
                size_hint: (0.3, 1)  
                md_bg_color: app.theme_cls.primary_color
                pos_hint: {"center_x": 0.5}
                on_release:
                    app.root.current = 'view_records'
            MDRaisedButton:
                text: "Crear Nuevo Registro"
                size_hint: (0.3, 1) 
                md_bg_color: app.theme_cls.primary_color
                pos_hint: {"center_x": 0.5}
                on_release:
                    app.root.current = 'create_records'
            MDRaisedButton:
                text: "Ingresar Factura"
                size_hint: (0.3, 1)  
                md_bg_color: app.theme_cls.primary_color
                pos_hint: {"center_x": 0.5}
                on_release:
                    app.root.current = 'invoice_screen'

<ViewRecordsScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        canvas.before:
            Color:
                rgba: app.theme_cls.primary_color  
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(150)
            padding: dp(10)
            spacing: dp(10)
            canvas.before:
                Color:
                    rgba: app.theme_cls.primary_color  
                Rectangle:
                    pos: self.pos
                    size: self.size
            MDLabel:
                text: "REGISTROS"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1  
                font_style: "H4"
                size_hint_y: None
                height: self.texture_size[1]
                halign: "center"
                bold: True
        MDScrollView:
            id: scroll_view
            MDList:
                id: client_list
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(50)  
            padding: dp(10)
            spacing: dp(10)
            MDRaisedButton:
                text: "Volver"
                size_hint: (1, 1)
                md_bg_color: app.theme_cls.primary_color
                pos_hint: {"center_x": 0.5}
                on_release:
                    app.root.current = 'home_screen'

<ClientDetailsScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)
        canvas.before:
            Color:
                rgba: 0.98, 0.98, 0.98, 1  
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(150)
            padding: dp(10)
            spacing: dp(10)
            canvas.before:
                Color:
                    rgba: app.theme_cls.primary_color
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(20), dp(20), dp(0), dp(0)]
            MDLabel:
                text: "REGISTRO"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1  
                font_style: "H4"
                size_hint_y: None
                height: self.texture_size[1]
                halign: "center"
                bold: True
            MDLabel:
                id: client_name_label
                text: "Detalles del Cliente"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1  
                font_style: "H5"
                size_hint_y: None
                height: self.texture_size[1]
                halign: "center"
                bold: True
        MDScrollView:
            id: scroll_view
            MDList:
                id: client_details_list
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(50)
            padding: dp(10)
            spacing: dp(10)
            MDRaisedButton:
                text: "Volver"
                size_hint: (0.3, 1)
                md_bg_color: app.theme_cls.primary_color
                pos_hint: {"center_x": 0.5}
                on_release:
                    app.root.current = 'view_records'
            MDRaisedButton:
                text: "Modificar"
                size_hint: (0.3, 1)
                md_bg_color: app.theme_cls.primary_color
                pos_hint: {"center_x": 0.5}
                on_release:
                    root.modify_client_details()
            MDRaisedButton:
                text: "Eliminar"
                size_hint: (0.3, 1)
                md_bg_color: app.theme_cls.error_color
                pos_hint: {"center_x": 0.5}
                on_release:
                    root.remove_client_from_list()

<ModifyRecordsScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)
        MDLabel:
            text: "MODIFICAR REGISTRO"
            font_style: "H5"
            halign: 'center'
            size_hint_y: None
            height: self.texture_size[1]
        ScrollView:
            size_hint: (1, 1)
            do_scroll_x: False
            do_scroll_y: True
            bar_width: dp(10)
            GridLayout:
                cols: 1
                spacing: dp(10)
                padding: dp(10)
                size_hint_y: None
                height: self.minimum_height
                # Sección de datos del cliente
                MDTextField:
                    id: client_name
                    hint_text: "Nombre Completo"
                    size_hint_y: None
                    height: dp(40)
                MDTextField:
                    id: contact_number
                    hint_text: "Número de Contacto"
                    size_hint_y: None
                    height: dp(40)
                MDTextField:
                    id: address
                    hint_text: "Dirección"
                    size_hint_y: None
                    height: dp(40)
                MDTextField:
                    id: service_type
                    hint_text: "Tipo de Servicio"
                    size_hint_y: None
                    height: dp(40)
                MDTextField:
                    id: service_date
                    hint_text: "Fecha del Servicio"
                    size_hint_y: None
                    height: dp(40)
                MDTextField:
                    id: tire_condition_before
                    hint_text: "Estado de Neumáticos Antes"
                    size_hint_y: None
                    height: dp(40)
                MDTextField:
                    id: tire_condition_after
                    hint_text: "Estado de Neumáticos Después"
                    size_hint_y: None
                    height: dp(40)
                MDTextField:
                    id: service_cost
                    hint_text: "Costo del Servicio"
                    size_hint_y: None
                    height: dp(40)
                MDTextField:
                    id: invoice_number
                    hint_text: "Número de Factura"
                    size_hint_y: None
                    height: dp(40)
                MDLabel:
                    text: "Artículos utilizados"
                    font_style: "H6"
                    halign: 'center'
                    size_hint_y: None
                    height: self.texture_size[1]
                GridLayout:
                    id: items_grid
                    cols: 1
                    spacing: dp(10)
                    padding: dp(10)
                    size_hint_y: None
                    height: self.minimum_height
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(50)
            spacing: dp(20)
            padding: [0, dp(10), 0, 0]
            pos_hint: {"center_x": .5}
            MDRaisedButton:
                text: "Guardar"
                size_hint_x: None
                width: dp(100)
                on_release: root.save_modified_data()
            MDRaisedButton:
                text: "Cancelar"
                size_hint_x: None
                width: dp(100)
                on_release: app.root.current = 'client_details_screen'

<InvoiceScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        canvas.before:
            Color:
                rgba: [0.1, 0.6, 0.8, 1]  
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(20),]
        MDLabel:
            text: "Ingresar Factura"
            font_style: "H4"
            halign: 'center'
            theme_text_color: "Primary"
            size_hint_y: None
            height: self.texture_size[1]
        MDTextField:
            id: invoice_number
            hint_text: "Número de Factura"
            size_hint_y: None
            height: dp(40)
        MDTextField:
            id: item_quantity
            hint_text: "Cantidad de Artículos"
            size_hint_y: None
            height: dp(40)
            on_text_validate: root.generate_item_fields(self.text)
        ScrollView:
            id: items_scroll
            size_hint: (1, 0.6)
            do_scroll_x: False
            do_scroll_y: True
            bar_width: dp(10)
            GridLayout:
                id: items_grid
                cols: 1
                spacing: dp(10)
                padding: dp(10)
                size_hint_y: None
                height: self.minimum_height
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(50)
            spacing: dp(20)

            MDRaisedButton:
                text: "Guardar y Volver"
                on_release:
                    root.save_invoice()
<InvoiceScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        canvas.before:
            Color:
                rgba: [1, 1, 1, 1] 
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(20),]
        MDLabel:
            text: "INGRESAR FACTURA"
            font_style: "H4"
            halign: 'center'
            theme_text_color: "Primary"
            size_hint_y: None
            height: self.texture_size[1]
            bold: True  
        MDTextField:
            id: invoice_number
            hint_text: "Número de Factura"
            size_hint_y: None
            height: dp(40)
        MDTextField:
            id: item_quantity
            hint_text: "Cantidad de Artículos"
            size_hint_y: None
            height: dp(40)
            on_text_validate: root.generate_item_fields(self.text)
        ScrollView:
            id: items_scroll
            size_hint: (1, 0.6)
            do_scroll_x: False
            do_scroll_y: True
            bar_width: dp(10)
            GridLayout:
                id: items_grid
                cols: 1
                spacing: dp(10)
                padding: dp(10)
                size_hint_y: None
                height: self.minimum_height
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(50)
            spacing: dp(20)
            MDRaisedButton:
                text: "Guardar"
                on_release:
                    root.save_invoice()
            MDRaisedButton:
                text: "Volver"
                on_release:
                    app.root.current = 'home_screen'
<InventoryScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        canvas.before:
            Color:
                rgba: app.theme_cls.primary_color
            Rectangle:
                pos: self.pos
                size: self.size
        MDLabel:
            text: "Inventario"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1  
            font_style: "H4"
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
            bold: True
        MDScrollView:
            id: inventory_scroll
            MDList:
                id: inventory_list
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(50)  
            padding: dp(10)
            spacing: dp(10)
            MDRaisedButton:
                text: "Volver"
                size_hint: (1, 1)
                md_bg_color: app.theme_cls.primary_color
                pos_hint: {"center_x": 0.5}
                on_release:
                    app.root.current = 'home_screen'
<ItemDetailsScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        MDLabel:
            text: "Detalles del Artículo"
            font_style: "H4"
            halign: 'center'
        MDScrollView:
            MDList:
                id: item_details_list
        MDRaisedButton:
            text: "Volver"
            size_hint: (1, 0.1)
            on_release:
                app.root.current = 'inventory_screen'
        MDRaisedButton:
            text: "Modificar"
            size_hint: (1, 0.1)
            on_release:
                root.modify_item_details()
        MDRaisedButton:
            text: "Eliminar de la lista"
            size_hint: (1, 0.1)
            md_bg_color: app.theme_cls.error_color
            on_release:
                root.remove_item_from_list()
<ModifyItemScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        MDLabel:
            text: "Modificar Artículo"
            font_style: "H4"
            halign: 'center'
        MDTextField:
            id: item_name
            hint_text: "Nombre del Artículo"
        MDTextField:
            id: item_quantity
            hint_text: "Cantidad"
        MDTextField:
            id: item_cost
            hint_text: "Costo"
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)
            MDRaisedButton:
                text: "Guardar"
                on_release:
                    root.save_modified_item()
            MDRaisedButton:
                text: "Cancelar"
                on_release:
                    app.root.current = 'item_details_screen'
""")

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        logo = Image(source='assets/Logo.jpg', size_hint=(0.6, 0.6), allow_stretch=True, keep_ratio=True)
        logo.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        button_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        button_box.add_widget(MDRaisedButton(text="Inicio", on_release=self.go_to_home, size_hint=(0.3, 1)))
        layout.add_widget(logo)
        layout.add_widget(button_box)
        self.add_widget(layout)
    def go_to_home(self, instance):
        self.manager.current = 'login_screen'

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        button_box1 = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        button_box1.add_widget(MDRaisedButton(text="Ver Registros", on_release=self.go_to_view_records, size_hint=(0.3, 1)))
        button_box2 = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        button_box2.add_widget(MDRaisedButton(text="Crear Nuevo Registro", on_release=self.go_to_create_record, size_hint=(0.3, 1)))
        button_box3 = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        button_box3.add_widget(MDRaisedButton(text="Ingresar Factura", on_release=self.go_to_invoice_screen, size_hint=(0.3, 1)))
        button_box4 = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        button_box4.add_widget(MDRaisedButton(text="Ver Inventario", on_release=self.go_to_inventory_screen, size_hint=(0.3, 1)))
        #button_box5 = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        #button_box5.add_widget(MDRaisedButton(text="Ver Estadísticas", on_release=self.go_to_statistics_screen, size_hint=(0.3, 1)))
        #layout.add_widget(button_box5)
        layout.add_widget(button_box1)
        layout.add_widget(button_box2)
        layout.add_widget(button_box3)
        layout.add_widget(button_box4)
        self.add_widget(layout)
    def go_to_view_records(self, instance):
        self.manager.current = 'view_records'
    def go_to_create_record(self, instance):
        self.manager.current = 'create_records'
    def go_to_invoice_screen(self, instance):
        self.manager.current = 'invoice_screen'
    def go_to_inventory_screen(self, instance):
        self.manager.current = 'inventory_screen'
    #def go_to_statistics_screen(self, instance):
        #self.manager.current = 'statistics_screen'

class ViewRecordsScreen(Screen):
    def on_pre_enter(self, *args):
        self.load_clients()
    def load_clients(self):
        self.ids.client_list.clear_widgets()
        clients_ref = db.collection('clientes')
        docs = clients_ref.stream()
        for doc in docs:
            client_data = doc.to_dict()
            if client_data.get('removed_from_list', False):
                continue
            client_name = client_data.get('cliente', {}).get('nombre_completo', 'No Name')
            item = OneLineIconListItem(text=client_name, on_release=self.show_client_details)
            item.client_id = doc.id 
            self.ids.client_list.add_widget(item)
    def show_client_details(self, instance):
        client_id = instance.client_id
        self.manager.current = 'client_details_screen'
        self.manager.get_screen('client_details_screen').load_client_details(client_id)
    def go_back(self):
        self.manager.current = 'home_screen'


class ClientDetailsScreen(Screen):
    def load_client_details(self, client_id):
        self.client_id = client_id  
        self.ids.client_details_list.clear_widgets()
        client_ref = db.collection('clientes').document(client_id)
        client_doc = client_ref.get()

        if client_doc.exists:
            client_data = client_doc.to_dict()
            cliente = client_data.get('cliente', {})
            vehiculo_servicios = client_data.get('vehiculo_servicios', {})  # Cambiado de 'servicios' a 'vehiculo_servicios'
            financieros = client_data.get('financieros', {})
            stock = client_data.get('stock', {}).get('articulos', [])

            # Mostrar los datos correctos
            details = {
                'Nombre Completo': cliente.get('nombre_completo', 'N/A'),
                'Número de Contacto': cliente.get('numero_contacto', 'N/A'),
                'Dirección': cliente.get('direccion', 'N/A'),
                'Tipo de Servicio': vehiculo_servicios.get('tipo_servicio', 'N/A'),
                'Fecha del Servicio': vehiculo_servicios.get('fecha_servicio', 'N/A'),
                'Estado de Neumáticos Antes': vehiculo_servicios.get('estado_neumaticos_antes', 'N/A'),
                'Estado de Neumáticos Después': vehiculo_servicios.get('estado_neumaticos_despues', 'N/A'),
                'Costo del Servicio': financieros.get('costo_servicio', 'N/A'),
                'Número de Factura': financieros.get('numero_factura', 'N/A')
            }

            # Añadir los detalles a la lista
            for key, value in details.items():
                self.ids.client_details_list.add_widget(OneLineIconListItem(text=f"{key}: {value}"))

            if stock:
                self.ids.client_details_list.add_widget(OneLineIconListItem(text="Artículos en Stock:"))
                for i, item in enumerate(stock, start=1):
                    item_details = f"Artículo {i}: {item.get('nombre', 'N/A')} - Cantidad: {item.get('cantidad', 'N/A')}"
                    self.ids.client_details_list.add_widget(OneLineIconListItem(text=item_details))

    def modify_client_details(self):
        modify_screen = self.manager.get_screen('modify_records_screen')
        client_ref = db.collection('clientes').document(self.client_id)
        client_doc = client_ref.get()

        if client_doc.exists:
            client_data = client_doc.to_dict()
            cliente = client_data.get('cliente', {})
            vehiculo_servicios = client_data.get('vehiculo_servicios', {})  # Cambiado de 'servicios' a 'vehiculo_servicios'
            financieros = client_data.get('financieros', {})
            stock = client_data.get('stock', {}).get('articulos', [])

            # Mostrar los datos en la pantalla de modificación
            modify_screen.ids.client_name.text = cliente.get('nombre_completo', '')
            modify_screen.ids.contact_number.text = cliente.get('numero_contacto', '')
            modify_screen.ids.address.text = cliente.get('direccion', '')
            modify_screen.ids.service_type.text = vehiculo_servicios.get('tipo_servicio', '')
            modify_screen.ids.service_date.text = vehiculo_servicios.get('fecha_servicio', '')
            modify_screen.ids.tire_condition_before.text = vehiculo_servicios.get('estado_neumaticos_antes', '')
            modify_screen.ids.tire_condition_after.text = vehiculo_servicios.get('estado_neumaticos_despues', '')
            modify_screen.ids.service_cost.text = str(financieros.get('costo_servicio', ''))
            modify_screen.ids.invoice_number.text = financieros.get('numero_factura', '')

            modify_screen.ids.items_grid.clear_widgets()
            for item in stock:
                item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
                item_name = MDTextField(text=item.get('nombre', ''), size_hint_x=0.5)
                item_quantity = MDTextField(text=str(item.get('cantidad', '')), size_hint_x=0.2, input_filter='int')
                item_cost = MDTextField(text=str(item.get('costo', '')), size_hint_x=0.3, input_filter='float')
                item_layout.add_widget(item_name)
                item_layout.add_widget(item_quantity)
                item_layout.add_widget(item_cost)
                modify_screen.ids.items_grid.add_widget(item_layout)

        self.manager.current = 'modify_records_screen'

    def remove_client_from_list(self):
        """Muestra el cuadro de diálogo de confirmación antes de eliminar un cliente."""
        confirm_dialog = MDDialog(
            title="Confirmación",
            text="¿Estás seguro de eliminar este registro?",
            buttons=[
                MDRaisedButton(
                    text="Cancelar",
                    on_release=lambda x: confirm_dialog.dismiss()
                ),
                MDRaisedButton(
                    text="Eliminar",
                    on_release=lambda x: self.confirm_removal(confirm_dialog)
                ),
            ],
        )
        confirm_dialog.open()

    def confirm_removal(self, dialog):
        """Confirma la eliminación del cliente."""
        dialog.dismiss()

        # Marcar el cliente como eliminado
        client_ref = db.collection('clientes').document(self.client_id)
        client_ref.set({'removed_from_list': True}, merge=True)

        # Recargar la lista de clientes y volver a la pantalla anterior
        self.manager.get_screen('view_records').load_clients()
        self.manager.current = 'view_records'


class ModifyRecordsScreen(Screen):
    inventory_screen = None  # Referencia para el inventario
    warning_dialog = None  # Referencia para la advertencia

    def __init__(self, **kwargs):
        super(ModifyRecordsScreen, self).__init__(**kwargs)
        from main import InventoryScreen  # Importación de InventoryScreen

        if not self.inventory_screen:
            # Crear instancia para acceder al inventario una vez
            self.inventory_screen = InventoryScreen()
            self.inventory_screen.load_inventory()  # Cargar inventario

    def reduce_inventory(self, modified_data):
        """
        Actualiza el inventario restando o sumando la diferencia de cantidades cuando se modifica el registro.
        """
        for articulo in modified_data['stock']['articulos']:
            nombre = articulo['nombre']
            cantidad_modificada = int(articulo['cantidad'])
            cantidad_previa = int(articulo.get('cantidad_previa', 0))  # Agregar una cantidad previa para comparar

            # Buscar el artículo en el inventario
            for item in self.inventory_screen.ids.inventory_list.children:
                split_text = item.text.split(' - ')
                if len(split_text) >= 2:  # Verificar que hay al menos dos partes después de la división
                    item_name = split_text[0]
                    item_details = split_text[1]

                    if item_name == nombre:
                        try:
                            cantidad_actual = int(item_details.split(': ')[1].split(' ')[0])
                        except (IndexError, ValueError):
                            print(f"Error al extraer la cantidad de: {item.text}")
                            continue  # Continuar con el siguiente artículo si hay un error

                        # Calcular la diferencia entre la cantidad modificada y la cantidad previa
                        diferencia = cantidad_modificada - cantidad_previa

                        # Actualizar la cantidad en el inventario según la diferencia
                        nueva_cantidad = cantidad_actual - diferencia

                        item.item_data['cantidad'] = nueva_cantidad

                        # Actualizar la cantidad en la base de datos
                        self.inventory_screen.update_inventory_item(item.item_data)
                        break

    def check_inventory_quantity(self, item_name, quantity):
        """
        Verifica si la cantidad ingresada es mayor a la disponible en el inventario.
        """
        try:
            cantidad_ingresada = int(quantity)
        except ValueError:
            return  # Si no es un número válido, no hacer nada

        # Buscar la cantidad disponible en el inventario
        for item in self.inventory_screen.ids.inventory_list.children:
            split_text = item.text.split(' - ')
            if len(split_text) >= 2:
                nombre = split_text[0]
                if nombre == item_name:
                    try:
                        cantidad_disponible = int(split_text[1].split(': ')[1].split(' ')[0])
                    except (IndexError, ValueError):
                        print(f"Error al obtener la cantidad de inventario para: {item_name}")
                        return

                    if cantidad_ingresada > cantidad_disponible:
                        self.show_inventory_warning(item_name, cantidad_disponible)
                    return

    def show_inventory_warning(self, item_name, cantidad_disponible):
        """
        Mostrar un cuadro de advertencia si la cantidad supera el inventario disponible.
        """
        if not self.warning_dialog:
            self.warning_dialog = MDDialog(
                title="Cantidad Insuficiente",
                text=f"No hay suficiente cantidad en el inventario.",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda x: self.warning_dialog.dismiss()
                    )
                ]
            )
        self.warning_dialog.text = f"No hay suficiente cantidad en el inventario."
        self.warning_dialog.open()

    def save_modified_data(self):
        client_id = self.manager.get_screen('client_details_screen').client_id
        modified_data = {
            'cliente': {
                'nombre_completo': self.ids.client_name.text,
                'numero_contacto': self.ids.contact_number.text,
                'direccion': self.ids.address.text,
            },
            'servicios': {
                'tipo_servicio': self.ids.service_type.text,
                'fecha_servicio': self.ids.service_date.text,
                'estado_neumaticos_antes': self.ids.tire_condition_before.text,
                'estado_neumaticos_despues': self.ids.tire_condition_after.text,
            },
            'financieros': {
                'costo_servicio': self.ids.service_cost.text,
                'numero_factura': self.ids.invoice_number.text,
            },
            'stock': {
                'articulos': []
            }
        }

        for item_layout in self.ids.items_grid.children:
            item_name = item_layout.children[2].text
            item_quantity = item_layout.children[1].text
            item_cost = item_layout.children[0].text
            document_id = getattr(item_layout, 'document_id', None)

            modified_data['stock']['articulos'].append({
                'nombre': item_name,
                'cantidad': item_quantity,
                'costo': item_cost,
                'document_id': document_id,
            })

        self.reduce_inventory(modified_data)

        db.collection('clientes').document(client_id).set(modified_data, merge=True)
        self.inventory_screen.load_inventory()
        client_details_screen = self.manager.get_screen('client_details_screen')
        client_details_screen.load_client_details(client_id)
        self.manager.current = 'client_details_screen'

class InvoiceScreen(Screen):
    def generate_item_fields(self, quantity):
        try:
            quantity = int(quantity)
        except ValueError:
            return
        self.ids.items_grid.clear_widgets()
        for i in range(quantity):
            item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
            item_name = TextInput(hint_text=f"Artículo {i+1}", size_hint_x=0.5, multiline=False)
            item_quantity = TextInput(hint_text="Cantidad", size_hint_x=0.2, multiline=False)
            item_cost = TextInput(hint_text="Costo", size_hint_x=0.3, multiline=False)
            item_layout.add_widget(item_name)
            item_layout.add_widget(item_quantity)
            item_layout.add_widget(item_cost)
            self.ids.items_grid.add_widget(item_layout)
    def save_invoice(self):
        invoice_data = {
            'numero_factura': self.ids.invoice_number.text,
            'articulos': []
        }
        for item_layout in self.ids.items_grid.children:
            item_name = item_layout.children[2].text  # Nombre del artículo
            item_quantity = item_layout.children[1].text  # Cantidad del artículo
            item_cost = item_layout.children[0].text  # Costo del artículo
            invoice_data['articulos'].append({
                'nombre': item_name,
                'cantidad': item_quantity,
                'costo': item_cost
            })
        db.collection('inventario').add(invoice_data)
        self.ids.invoice_number.text = ""
        self.ids.item_quantity.text = ""
        self.ids.items_grid.clear_widgets()
        self.show_confirmation_dialog()
    def show_confirmation_dialog(self):
        confirm_dialog = MDDialog(
            title="Confirmación",
            text="Los datos se guardaron correctamente.",
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: confirm_dialog.dismiss()
                ),
            ],
        )
        confirm_dialog.open()
class InventoryScreen(Screen):
    def on_pre_enter(self, *args):
        self.load_inventory()  # Recarga el inventario cada vez que la pantalla se muestra
    def load_inventory(self):
        self.ids.inventory_list.clear_widgets()
        invoices = db.collection('inventario').stream()
        for invoice in invoices:
            invoice_data = invoice.to_dict()
            for item in invoice_data['articulos']:
                item['document_id'] = invoice.id  # Guardar el ID del documento
                item_name = item.get('nombre', 'Desconocido')
                item_quantity = item.get('cantidad', 'Desconocida')
                item_cost = item.get('costo', 'No especificado')
                if item.get('removed_from_list', False):
                    continue
                item_widget = OneLineIconListItem(text=f"{item_name} - Cantidad: {item_quantity} - Costo: ${item_cost}")
                item_widget.item_data = item  
                item_widget.on_release = lambda instance=item_widget: self.show_item_details(instance)
                self.ids.inventory_list.add_widget(item_widget)

    def show_item_details(self, instance):
        item_data = instance.item_data
        self.manager.get_screen('item_details_screen').load_item_details(item_data)
        self.manager.current = 'item_details_screen'
    def update_inventory_item(self, item_data):
        document_id = item_data['document_id']
        inventory_ref = db.collection('inventario').document(document_id)
        invoice_data = inventory_ref.get().to_dict()
        for item in invoice_data['articulos']:
            if item['nombre'] == item_data['nombre']:
                item['cantidad'] = item_data['cantidad']  # Actualiza la cantidad
                break
        inventory_ref.set(invoice_data, merge=True)
        self.load_inventory()

class ItemDetailsScreen(Screen):
    def load_item_details(self, item_data):
        self.item_data = item_data 
        self.ids.item_details_list.clear_widgets()
        details_to_display = ['nombre', 'cantidad', 'costo']
        for key in details_to_display:
            value = item_data.get(key, 'No especificado')
            self.ids.item_details_list.add_widget(OneLineIconListItem(text=f"{key.capitalize()}: {value}"))
    def modify_item_details(self):
        modify_screen = self.manager.get_screen('modify_item_screen')
        modify_screen.load_item_data(self.item_data)
        self.manager.current = 'modify_item_screen'
    def remove_item_from_list(self):
        inventory_ref = db.collection('inventario').document(self.item_data['document_id'])
        invoice_data = inventory_ref.get().to_dict()
        for item in invoice_data['articulos']:
            if item['nombre'] == self.item_data['nombre']:
                item['removed_from_list'] = True
                break
        inventory_ref.set(invoice_data, merge=True)
        self.manager.get_screen('inventory_screen').load_inventory()
        self.manager.current = 'inventory_screen'

class ModifyItemScreen(Screen):
    def load_item_data(self, item_data):
        self.item_data = item_data
        self.ids.item_name.text = item_data.get('nombre', '')
        self.ids.item_quantity.text = str(item_data.get('cantidad', ''))
        self.ids.item_cost.text = item_data.get('costo', '')
    def save_modified_item(self):
        updated_name = self.ids.item_name.text
        updated_quantity = self.ids.item_quantity.text
        updated_cost = self.ids.item_cost.text
        inventory_ref = db.collection('inventario')
        document_id = self.item_data['document_id']
        invoice_ref = inventory_ref.document(document_id)
        invoice_data = invoice_ref.get().to_dict()
        for item in invoice_data['articulos']:
            if item['nombre'] == self.item_data['nombre']:
                item['nombre'] = updated_name
                item['cantidad'] = updated_quantity
                item['costo'] = updated_cost
                break
        invoice_ref.set(invoice_data, merge=True)
        self.item_data['nombre'] = updated_name
        self.item_data['cantidad'] = updated_quantity
        self.item_data['costo'] = updated_cost
        self.manager.get_screen('item_details_screen').load_item_details(self.item_data)
        self.manager.get_screen('inventory_screen').load_inventory()
        self.manager.current = 'item_details_screen'      
class MyApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main_screen'))
        sm.add_widget(HomeScreen(name='home_screen'))
        sm.add_widget(RegisterScreen(name='create_records'))
        sm.add_widget(ViewRecordsScreen(name='view_records'))
        sm.add_widget(ClientDetailsScreen(name='client_details_screen'))
        sm.add_widget(ModifyRecordsScreen(name='modify_records_screen'))
        sm.add_widget(UsuariosCreados(name='usuarios_screen'))
        sm.add_widget(LoginScreen(name='login_screen'))
        sm.add_widget(InvoiceScreen(name='invoice_screen'))
        sm.add_widget(InventoryScreen(name='inventory_screen'))
        sm.add_widget(ItemDetailsScreen(name='item_details_screen'))
        sm.add_widget(ModifyItemScreen(name='modify_item_screen'))
        
        return sm
if __name__ == '__main__':
    MyApp().run()
