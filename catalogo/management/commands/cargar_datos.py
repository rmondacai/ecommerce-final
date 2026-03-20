"""
Carga datos de prueba: categorías, productos, y usuarios (admin + cliente).
Uso: python manage.py cargar_datos
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from catalogo.models import Categoria, Producto


class Command(BaseCommand):
    help = 'Carga categorías, productos y usuarios de prueba.'

    def handle(self, *args, **options):
        self.stdout.write('Cargando datos de prueba...\n')

        # --- Usuarios ---
        if not User.objects.filter(username='admin1').exists():
            User.objects.create_superuser('admin1', 'admin1@test.com', 'admin1234')
            self.stdout.write(self.style.SUCCESS('  Usuario ADMIN creado: admin1 / admin1234'))
        else:
            self.stdout.write('  Usuario admin1 ya existe.')

        if not User.objects.filter(username='cliente1').exists():
            User.objects.create_user('cliente1', 'cliente1@test.com', 'cliente1234',
                                     first_name='Juan', last_name='Pérez')
            self.stdout.write(self.style.SUCCESS('  Usuario CLIENTE creado: cliente1 / cliente1234'))
        else:
            self.stdout.write('  Usuario cliente1 ya existe.')

        # --- Categorías ---
        cats_data = [
            ('Electrónica', 'Dispositivos electrónicos y accesorios.'),
            ('Ropa', 'Prendas de vestir.'),
            ('Hogar', 'Artículos para el hogar.'),
            ('Deportes', 'Equipamiento deportivo.'),
            ('Libros', 'Libros físicos.'),
        ]
        cats = {}
        for nombre, desc in cats_data:
            cat, created = Categoria.objects.get_or_create(nombre=nombre, defaults={'descripcion': desc})
            cats[nombre] = cat
            self.stdout.write(f'  Categoría "{nombre}": {"creada" if created else "ya existía"}')

        # --- Productos ---
        prods_data = [
            ('Audífonos Bluetooth', 'Audífonos inalámbricos con cancelación de ruido y 30h de batería.', 45990, 25, 'Electrónica'),
            ('Teclado Mecánico RGB', 'Teclado mecánico con switches Cherry MX y retroiluminación.', 62990, 15, 'Electrónica'),
            ('Mouse Inalámbrico', 'Mouse ergonómico con sensor óptico de alta precisión.', 18990, 40, 'Electrónica'),
            ('Monitor 27"', 'Monitor IPS Full HD con marco delgado.', 189990, 8, 'Electrónica'),
            ('Webcam HD', 'Cámara web 1080p con micrófono integrado.', 29990, 20, 'Electrónica'),
            ('Polera Algodón', 'Polera de algodón orgánico, corte regular.', 12990, 50, 'Ropa'),
            ('Chaqueta Impermeable', 'Chaqueta ligera con capucha ajustable.', 39990, 20, 'Ropa'),
            ('Jeans Slim Fit', 'Jeans de mezclilla stretch con cinco bolsillos.', 24990, 35, 'Ropa'),
            ('Lámpara LED Escritorio', 'Lámpara LED con brazo articulado y puerto USB.', 22990, 18, 'Hogar'),
            ('Organizador de Bambú', 'Organizador con compartimentos para escritorio.', 9990, 45, 'Hogar'),
            ('Set de Toallas', 'Set de 4 toallas de algodón egipcio.', 15990, 30, 'Hogar'),
            ('Balón de Fútbol', 'Balón tamaño 5, cosido a máquina.', 14990, 22, 'Deportes'),
            ('Colchoneta Yoga', 'Colchoneta antideslizante 6mm con correa.', 11990, 28, 'Deportes'),
            ('Python Crash Course', 'Libro introductorio a Python con proyectos. Eric Matthes.', 28990, 12, 'Libros'),
            ('Clean Code', 'Guía de código limpio. Robert C. Martin.', 32990, 10, 'Libros'),
        ]
        for nombre, desc, precio, stock, cat_name in prods_data:
            prod, created = Producto.objects.get_or_create(
                nombre=nombre,
                defaults={'descripcion': desc, 'precio': precio, 'stock': stock, 'categoria': cats[cat_name]}
            )
            self.stdout.write(f'  Producto "{nombre}": {"creado" if created else "ya existía"}')

        self.stdout.write(self.style.SUCCESS('\nDatos cargados correctamente.'))
        self.stdout.write(self.style.SUCCESS('\n--- CREDENCIALES DE PRUEBA ---'))
        self.stdout.write(self.style.SUCCESS('  ADMIN:   admin1   / admin1234'))
        self.stdout.write(self.style.SUCCESS('  CLIENTE: cliente1 / cliente1234'))
