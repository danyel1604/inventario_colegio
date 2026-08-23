import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .models import Articulo, Movimiento

def lista_articulos(request):
    articulos = Articulo.objects.all()
    datos = []
    for articulo in articulos:
        datos.append({
            'id': articulo.id,
            'codigo_interno': articulo.codigo_interno,
            'nombre': articulo.nombre,
            'stock_actual': articulo.stock_actual,
            'categoria': articulo.categoria.nombre
        })
    return JsonResponse(datos, safe=False)

# ¡NUEVA FUNCIÓN! Esta recibe el movimiento desde Firefox
@csrf_exempt 
def registrar_movimiento(request):
    if request.method == 'POST':
        try:
            # Leemos los datos que nos envía JavaScript
            datos = json.loads(request.body)
            articulo_id = datos.get('articulo_id')
            tipo = datos.get('tipo')
            cantidad = int(datos.get('cantidad'))
            responsable = datos.get('responsable')

            # Buscamos el artículo en la base de datos
            articulo = Articulo.objects.get(id=articulo_id)

            # Creamos el registro del movimiento
            nuevo_movimiento = Movimiento(
                articulo=articulo,
                tipo=tipo,
                cantidad=cantidad,
                responsable=responsable
            )
            
            # Esto ejecuta tu validación (avisa si falta stock)
            nuevo_movimiento.clean() 
            # Esto guarda y actualiza el número automáticamente
            nuevo_movimiento.save()  

            return JsonResponse({'mensaje': '¡Movimiento guardado con éxito!'})

        except ValidationError as e:
            # Si models.py frena la operación, le mandamos el error al navegador
            return JsonResponse({'error': list(e)[0]}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Error: ' + str(e)}, status=500)