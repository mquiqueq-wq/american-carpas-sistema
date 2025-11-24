from django.apps import AppConfig


class InventarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventario'
    verbose_name = 'Gestión de Inventarios'
    
    def ready(self):
        """
        Método que se ejecuta cuando la aplicación está lista.
        Aquí se pueden importar signals si se necesitan.
        """
        pass
