from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.tab import MDTabs
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from firebase_config import db
import uuid
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox

# Cargar el archivo KV
Builder.load_string("""
<RegisterScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        canvas.before:
            Color:
                rgba: 0.6, 0.8, 1, 1  # Celeste suave
            Rectangle:
                pos: self.pos
                size: self.size

        MDTabs:
            id: tabs

            TabCliente:
                title: 'Cliente'
                id: cliente_tab

            TabVehiculoServicios:
                title: 'Vehículo y Servicios'
                id: vehiculo_servicios_tab

            TabFinancieros:
                title: 'Detalles Financieros'
                id: financieros_tab

            TabStock:
                title: 'Stock de Neumáticos y Accesorios'
                id: stock_tab

        MDRaisedButton:
            text: "Guardar Registro"
            size_hint_y: None
            height: dp(50)
            pos_hint: {"center_x": 0.5}
            md_bg_color: app.theme_cls.primary_color
            on_release:
                root.save_to_firestore()

        MDRaisedButton:
            text: "Volver a la Pantalla Principal"
            size_hint_y: None
            height: dp(50)
            pos_hint: {"center_x": 0.5}
            md_bg_color: app.theme_cls.primary_color
            on_release:
                root.go_to_home()

<TabCliente>:
    ScrollView:
        do_scroll_x: False
        do_scroll_y: True
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            spacing: dp(10)
            padding: dp(10)

            MDTextField:
                id: client_name
                hint_text: "Nombre completo"
                required: True
                helper_text: "Ejemplo: Juan Pérez"
                helper_text_mode: "on_focus"

            MDTextField:
                id: client_contact
                hint_text: "Número de contacto"
                required: True
                input_filter: 'int'
                helper_text: "Ingrese el número sin espacios ni guiones"
                helper_text_mode: "on_focus"

            MDTextField:
                id: client_address
                hint_text: "Dirección"
                required: True
                helper_text: "Ejemplo: Calle Falsa 123"
                helper_text_mode: "on_focus"

<TabVehiculoServicios>:
    ScrollView:
        do_scroll_x: False
        do_scroll_y: True
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            spacing: dp(10)
            padding: dp(10)

            # Campos restantes de la ventana Vehículo
            MDTextField:
                id: vehicle_type
                hint_text: "Tipo de Vehículo"
                required: True
                helper_text: "Ejemplo: Auto, Moto, Camión"
                helper_text_mode: "on_focus"

            # Campos restantes de la ventana Servicios Realizados
            MDTextField:
                id: service_type
                hint_text: "Tipo de Servicio"
                required: True
                helper_text: "Ejemplo: Cambio de aceite, alineación"
                helper_text_mode: "on_focus"

            MDTextField:
                id: service_date
                hint_text: "Fecha del Servicio (DD/MM/AAAA)"
                required: True
                helper_text: "Formato: Día/Mes/Año"
                helper_text_mode: "on_focus"
                on_text: root.format_date(self)

            MDTextField:
                id: tire_status_before
                hint_text: "Estado Antes del Servicio"
                required: True
                helper_text: "Condición antes del servicio"
                helper_text_mode: "on_focus"

            MDTextField:
                id: tire_status_after
                hint_text: "Estado Después del Servicio"
                required: True
                helper_text: "Condición después del servicio"
                helper_text_mode: "on_focus"

<TabFinancieros>:
    ScrollView:
        do_scroll_x: False
        do_scroll_y: True
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            spacing: dp(10)
            padding: dp(10)

            MDTextField:
                id: service_cost
                hint_text: "Costo del Servicio"
                required: True
                input_filter: 'float'
                helper_text: "Ingrese el monto total en la moneda local"
                helper_text_mode: "on_focus"

            MDTextField:
                id: invoice_number
                hint_text: "Número de Factura/Recibo"
                required: True
                helper_text: "Número único para identificar el recibo"
                helper_text_mode: "on_focus"

<TabStock>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)

        MDRaisedButton:
            text: "Seleccionar Artículo"
            size_hint_y: None
            height: dp(50)
            on_release: root.open_item_selection_dialog()

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
""")


class TabCliente(Screen, MDTabsBase):
    def get_cliente_data(self):
        return {
            'nombre_completo': self.ids.client_name.text,
            'numero_contacto': self.ids.client_contact.text,
            'direccion': self.ids.client_address.text,
        }

class TabVehiculoServicios(Screen, MDTabsBase):
    def get_vehiculo_servicios_data(self):
        return {
            'tipo_vehiculo': self.ids.vehicle_type.text,
            'tipo_servicio': self.ids.service_type.text,
            'fecha_servicio': self.ids.service_date.text,
            'estado_neumaticos_antes': self.ids.tire_status_before.text,
            'estado_neumaticos_despues': self.ids.tire_status_after.text,
        }

    def format_date(self, instance):
        text = instance.text
        if len(text) == 2 or len(text) == 5:
            if not text.endswith('/'):
                instance.text = f"{text}/"

class TabFinancieros(Screen, MDTabsBase):
    def get_financieros_data(self):
        return {
            'costo_servicio': self.ids.service_cost.text,
            'numero_factura': self.ids.invoice_number.text,
        }

class TabStock(Screen, MDTabsBase):
    dialog = None
    inventory_screen = None  # Referencia para el inventario
    warning_dialog = None  # Referencia para la advertencia

    def open_item_selection_dialog(self):
        if not self.dialog:
            from main import InventoryScreen  # Asegúrate de tener la importación de InventoryScreen
            
            if not self.inventory_screen:
                self.inventory_screen = InventoryScreen()  # Crear instancia para acceder al inventario una vez
                self.inventory_screen.load_inventory()  # Cargar inventario

            # Solo toma los nombres de los artículos (suponiendo que los items tienen más detalles)
            items = [item.text.split(' - ')[0] for item in self.inventory_screen.ids.inventory_list.children]

            # Crear la lista de ítems, mostrando solo el nombre del artículo
            self.dialog = MDDialog(
                title="Seleccionar Artículos",
                type="confirmation",
                items=[
                    OneLineIconListItem(
                        text=item,
                        on_release=lambda x=item: self.toggle_item_selection(x)
                    ) for item in items
                ],
                buttons=[
                    MDFlatButton(text="Cancelar", on_release=lambda x: self.dialog.dismiss()),
                    MDRaisedButton(text="Aceptar", on_release=self.add_selected_items)
                ],
            )
        self.dialog.open()

    def toggle_item_selection(self, item):
        # Añadir un atributo 'selected' al item para manejar la selección
        if hasattr(item, 'selected'):
            item.selected = not item.selected
        else:
            item.selected = True
        # Cambiar el color de fondo del ítem si está seleccionado
        item.bg_color = (0, 1, 0, 0.3) if item.selected else (1, 1, 1, 1)

    def add_selected_items(self, *args):
        # Agrega los artículos seleccionados a la interfaz principal
        for item in self.dialog.items:
            if hasattr(item, 'selected') and item.selected:  # Si el artículo está seleccionado
                item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
                
                item_name = MDTextField(text=item.text, size_hint_x=0.5, readonly=True)
                item_quantity = MDTextField(hint_text="Cantidad", size_hint_x=0.2, input_filter='int')

                # Vincular la función de verificación de cantidad
                item_quantity.bind(text=lambda instance, value: self.check_inventory_quantity(item.text, value))
                
                item_layout.add_widget(item_name)
                item_layout.add_widget(item_quantity)
                
                self.ids.items_grid.add_widget(item_layout)
        self.dialog.dismiss()

    def get_stock_data(self):
        stock_data = {
            'articulos': []
        }
        for item_layout in self.ids.items_grid.children:
            item_name = item_layout.children[1].text  # Nombre del artículo
            item_quantity = item_layout.children[0].text  # Cantidad

            stock_data['articulos'].append({
                'nombre': item_name,
                'cantidad': item_quantity
            })
        return stock_data

    def reduce_inventory(self, stock_data):
        # Actualiza el inventario reduciendo las cantidades
        for articulo in stock_data['articulos']:
            nombre = articulo['nombre']
            cantidad_reducir = int(articulo['cantidad'])

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

                        nueva_cantidad = max(0, cantidad_actual - cantidad_reducir)  # Evitar cantidades negativas
                        item.item_data['cantidad'] = nueva_cantidad

                        # Actualizar la cantidad en la base de datos
                        self.inventory_screen.update_inventory_item(item.item_data)
                        break

    def check_inventory_quantity(self, item_name, quantity):
        # Verifica si la cantidad ingresada es mayor a la disponible en el inventario
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
        # Mostrar un cuadro de advertencia si la cantidad supera el inventario disponible
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

class RegisterScreen(Screen):
    def save_to_firestore(self):
        try:
            # Obtener referencias a las pestañas
            cliente_tab = self.ids.cliente_tab
            vehiculo_servicios_tab = self.ids.vehiculo_servicios_tab
            financieros_tab = self.ids.financieros_tab
            stock_tab = self.ids.stock_tab

            # Obtener los datos de cada pestaña
            cliente_data = cliente_tab.get_cliente_data()
            vehiculo_servicios_data = vehiculo_servicios_tab.get_vehiculo_servicios_data()
            financieros_data = financieros_tab.get_financieros_data()
            stock_data = stock_tab.get_stock_data()

            # Lista para almacenar los campos incompletos
            incomplete_fields = []

            # Verificar cada campo en cada pestaña
            for tab_name, data in {
                "Cliente": cliente_data,
                "Vehículo y Servicios": vehiculo_servicios_data,
                "Financieros": financieros_data,
                "Stock": stock_data
            }.items():
                for key, value in data.items():
                    if isinstance(value, str) and not value.strip():
                        incomplete_fields.append(f"{key} en {tab_name}")

            # Si hay campos incompletos, mostrar diálogo y salir del método
            if incomplete_fields:
                self.show_incomplete_fields_dialog(incomplete_fields)
                return

            # Reducir el inventario antes de guardar los datos en Firestore
            stock_tab.reduce_inventory(stock_data)

            # Si todos los campos están completos, guardar en Firestore
            cliente_id = str(uuid.uuid4())  # Generar un ID único para cada cliente

            cliente_document = {
                'cliente': cliente_data,
                'vehiculo_servicios': vehiculo_servicios_data,
                'financieros': financieros_data,
                'stock': stock_data,
            }

            db.collection('clientes').document(cliente_id).set(cliente_document)
            print("Datos guardados en Firestore bajo el cliente:", cliente_id)
            
            # Limpiar los campos después de guardar
            self.clear_fields()
            
            # Volver a la pestaña de Cliente
            self.ids.tabs.switch_tab("Cliente")
            
            # Mostrar un diálogo de confirmación
            self.show_confirmation_dialog()

        except AttributeError as e:
            print(f"Error: las pestañas no contienen los elementos esperados: {e}")
        except Exception as e:
            print(f"Error al guardar en Firestore: {e}")

    def show_incomplete_fields_dialog(self, fields):
        # Crear el mensaje de campos incompletos
        fields_str = '\n'.join(fields)
        dialog = MDDialog(
            title="Campos Incompletos",
            text=f"Por favor, completa los siguientes campos:\n{fields_str}",
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def clear_fields(self):
        # Limpiar todos los campos de texto en todas las pestañas
        for tab in [
            self.ids.cliente_tab,
            self.ids.vehiculo_servicios_tab,
            self.ids.financieros_tab,
            self.ids.stock_tab
        ]:
            for child in tab.ids.values():
                if isinstance(child, MDTextField):
                    child.text = ""

        # Limpiar los elementos añadidos en el tab de Stock
        stock_tab = self.ids.stock_tab
        stock_tab.ids.items_grid.clear_widgets()

    def show_confirmation_dialog(self):
        # Mostrar un diálogo de confirmación después de guardar los datos
        dialog = MDDialog(
            title="Registro Guardado",
            text="Los datos se han guardado correctamente.",
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def go_to_home(self):
        # Cambiar la pantalla activa a la pantalla principal
        self.manager.current = 'home_screen'