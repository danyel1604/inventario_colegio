from django.db import models, transaction
from django.core.exceptions import ValidationError

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Articulo(models.Model):
    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='articulos')
    codigo_interno = models.CharField(max_length=50, unique=True)
    stock_actual = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=5)

    def __str__(self):
        return f"[{self.codigo_interno}] {self.nombre} - Stock: {self.stock_actual}"

class Movimiento(models.Model):
    TIPO_CHOICES = [
        ('ENTRADA', 'Ingreso de material'),
        ('SALIDA', 'Entrega a profesor/alumno'),
    ]
    
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.CharField(max_length=150, help_text="¿Quién lo entregó o retiró?")

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.cantidad} unidades de {self.articulo.nombre}"

    def clean(self):
        """
        Esta función habla directamente con la pantalla de Firefox.
        Si la regla no se cumple, frena el formulario y muestra el aviso en rojo.
        """
        super().clean()
        if self.pk is None and self.tipo == 'SALIDA':
            if self.articulo and self.articulo.stock_actual < self.cantidad:
                raise ValidationError(
                    f"¡Alerta de Stock! Solo quedan {self.articulo.stock_actual} unidades de "
                    f"'{self.articulo.nombre}'. No es posible retirar {self.cantidad}."
                )

    def save(self, *args, **kwargs):
        """
        Esta función procesa los números en la base de datos una vez que la alerta pasó.
        """
        with transaction.atomic():
            if self.pk is None:  # Solo para nuevos registros
                if self.tipo == 'ENTRADA':
                    self.articulo.stock_actual += self.cantidad
                elif self.tipo == 'SALIDA':
                    if self.articulo.stock_actual >= self.cantidad:
                        self.articulo.stock_actual -= self.cantidad
                self.articulo.save()
            super().save(*args, **kwargs)