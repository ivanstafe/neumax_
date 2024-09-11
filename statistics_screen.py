from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.core.text import Label as CoreLabel
from firebase_config import db  # Importar Firestore

class PieGraph(Widget):
    def __init__(self, data, labels=[], title="", **kwargs):
        super(PieGraph, self).__init__(**kwargs)
        self.data = data
        self.labels = labels
        self.title = title
        self.bind(pos=self.update_graph, size=self.update_graph)

    def update_graph(self, *args):
        print(f"Actualizando gráfico {self.title} con datos: {self.data} y etiquetas: {self.labels}")
        self.canvas.clear()

        if len(self.data) == 0 or sum(self.data) == 0:
            print(f"No hay datos para dibujar el gráfico {self.title}.")
            return  # Si no hay datos o son todos ceros, no intentamos dibujar

        total = sum(self.data)
        angle_start = 0
        radius = min(self.width, self.height) / 2 - 50
        center_x = self.center_x
        center_y = self.center_y
        legend_x = self.x + self.width - 100  # Ajustar la posición de la leyenda al lado derecho del gráfico
        legend_y = self.top - 40  # Comienza desde arriba de la pantalla

        # Colores para los sectores
        colors = [(0.2, 0.6, 1, 1), (0.3, 0.3, 0.3, 1), (0.5, 1, 0.5, 1), (1, 0.6, 0.2, 1)]
        
        with self.canvas:
            for i, value in enumerate(self.data):
                if value == 0:
                    continue  # Si el valor es 0, no dibujar

                angle_end = angle_start + (value / total) * 360
                Color(*colors[i % len(colors)])  # Cambiar color según el índice
                Ellipse(pos=(center_x - radius, center_y - radius), size=(2 * radius, 2 * radius),
                        angle_start=angle_start, angle_end=angle_end)
                angle_start = angle_end

                # Dibujar leyenda
                Color(*colors[i % len(colors)])
                Rectangle(pos=(legend_x, legend_y), size=(20, 20))  # Cuadro de color para la leyenda
                Color(0, 0, 0, 1)  # Color negro para el texto
                legend_text = f"{self.labels[i]}: {self.data[i]}"
                self.draw_legend_text(legend_text, legend_x + 30, legend_y + 5)
                legend_y -= 30  # Espacio entre cada leyenda

    def draw_legend_text(self, text, x, y):
        label = CoreLabel(text=text, font_size=12, color=(0, 0, 0, 1))
        label.refresh()
        texture = label.texture
        self.canvas.add(Rectangle(texture=texture, pos=(x, y), size=texture.size))


class StatisticsScreen(Screen):
    def __init__(self, **kwargs):
        super(StatisticsScreen, self).__init__(**kwargs)

        # Envolver todo en un ScrollView para manejar el scroll
        scroll_view = ScrollView(size_hint=(1, 1))

        layout = BoxLayout(orientation='vertical', padding=20, spacing=20, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        # Título de la pantalla
        title_label = Label(text="ESTADÍSTICAS", font_size='24sp', color=(0, 0, 0, 1), size_hint=(1, None), height=50)
        layout.add_widget(title_label)

        # Referencias arriba del gráfico de Servicios
        service_ref_label = Label(text="Datos obtenidos de los registros visibles de tipo de servicio.", font_size='16sp', color=(0, 0, 0, 1), size_hint=(1, None), height=30)
        layout.add_widget(service_ref_label)

        # Añadir gráfico de Servicios
        service_title = Label(text="Gráfico de Servicios", font_size='20sp', color=(0, 0, 0, 1), size_hint=(1, None), height=40)
        layout.add_widget(service_title)

        self.service_graph = PieGraph([], labels=[], title="Servicios", size_hint=(1, None), height=400)
        layout.add_widget(self.service_graph)

        # Referencias arriba del gráfico de Ganancias
        gain_ref_label = Label(text="Datos obtenidos de los registros visibles de costo de servicio.", font_size='16sp', color=(0, 0, 0, 1), size_hint=(1, None), height=30)
        layout.add_widget(gain_ref_label)

        # Añadir gráfico de Ganancias
        gain_title = Label(text="Gráfico de Ganancias", font_size='20sp', color=(0, 0, 0, 1), size_hint=(1, None), height=40)
        layout.add_widget(gain_title)

        self.gain_graph = PieGraph([], labels=[], title="Ganancias", size_hint=(1, None), height=400)
        layout.add_widget(self.gain_graph)

        # Botón para regresar a la pantalla principal
        back_button = Button(text="Volver a Home", size_hint=(1, None), height=50)
        back_button.bind(on_press=self.go_back_home)
        layout.add_widget(back_button)

        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)

    def on_enter(self):
        self.display_statistics()

    def display_statistics(self):
        service_counts = {}  # Almacenar el conteo de cada tipo de servicio
        gains = []
        x_labels_gains = []

        # Obtener datos desde los registros visibles
        view_records_screen = self.manager.get_screen('view_records')

        # Depurar si hay registros visibles
        if not view_records_screen.ids.client_list.children:
            print("No hay registros visibles para mostrar.")
            return  # No hay registros visibles, no intentamos dibujar

        print(f"Se encontraron {len(view_records_screen.ids.client_list.children)} registros visibles.")

        # Recorrer cada registro visible en client_list
        for widget in view_records_screen.ids.client_list.children:
            if hasattr(widget, 'client_id'):
                client_id = widget.client_id
                print(f"Procesando registro con ID de cliente: {client_id}")
                
                # Obtener datos del cliente desde Firestore
                client_ref = db.collection('clientes').document(client_id)
                client_doc = client_ref.get()

                if client_doc.exists:
                    client_data = client_doc.to_dict()
                    print(f"Datos del cliente {client_id}: {client_data}")

                    servicios = client_data.get('servicios', {})
                    financieros = client_data.get('financieros', {})

                    # Obtener tipo de servicio y su cantidad
                    tipo_servicio = servicios.get('tipo_servicio', 'Desconocido')
                    service_counts[tipo_servicio] = service_counts.get(tipo_servicio, 0) + 1

                    # Calcular las ganancias
                    costo_servicio = financieros.get('costo_servicio', 0)
                    gains.append(float(costo_servicio))
                    x_labels_gains.append(f"Cliente {client_id[:5]}")
                else:
                    print(f"No se encontró documento para el cliente ID: {client_id}")
            else:
                print("No se encontró atributo 'client_id' en el widget del cliente.")

        # Verificar si hay datos válidos para los gráficos
        if service_counts and sum(service_counts.values()) > 0:
            print(f"Datos de servicios: {service_counts}")
            self.service_graph.data = list(service_counts.values())
            self.service_graph.labels = list(service_counts.keys())
            self.service_graph.update_graph()
        else:
            print("No se encontraron datos para el gráfico de servicios.")

        if gains and sum(gains) > 0:
            print(f"Datos de ganancias: {gains}")
            self.gain_graph.data = gains
            self.gain_graph.labels = x_labels_gains
            self.gain_graph.update_graph()
        else:
            print("No se encontraron datos para el gráfico de ganancias.")

    def go_back_home(self, instance):
        self.manager.current = 'home_screen'
