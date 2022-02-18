# Consigna
## Objetivo
El objetivo de la prueba es crear una aplicación web sencilla en Django 3.0. La pantalla
principal será un listado de reservas.
## Explicación
Una reserva consiste de:
- fecha entrada
- fecha salida
- tipo de habitación
- nº huéspedes
- datos de contacto (nombre, email, teléfono)
- precio total de la reserva
- localizador
- nº de habitación (opcional)


Habrá un botón para crear una reserva nueva. Este botón llevará a una pantalla que debe
permitir introducir 2 fechas (entrada y salida), el número de huéspedes. 

Al buscar entre 2
fechas le mostrará como mínimo la siguiente información:
- Tipo de habitación
- Nº de habitaciones disponibles para este rango de fechas
- Precio total de la estancia
- Un botón para seleccionar esa habitación


Tras seleccionar la habitación deseada, le llevará a un formulario donde tendrá que introducir
los datos de contacto para la reserva (nombre, email, teléfono). 

Al finalizar el formulario se
creará la reserva (con un localizador alfanumérico único) y le llevará a la pantalla con el listado
de reservas.


Algunos detalles a tener en cuenta:
- Habrá 4 tipos de habitaciones: 
  - 10 individuales, 
  - 5 dobles, 
  - 4 triples, 
  - 6 cuádruples.
- El precio diario de cada tipo de habitación es: 
  - individual=20€/día, 
  - doble=30€/día,
  - triple=40€/día, 
  - cuádruple=50€/día
- En una habitación 
  - individual sólo cabe 1 persona (huésped)
  - doble caben 1 o 2 personas
  - triple caben 1, 2, o 3 personas
  - cuádruple caben 1, 2, 3 o 4
personas. 
- Si el usuario hace una búsqueda para 3 personas, solo deberá
mostrar habitaciones triples y cuádruples (siempre y cuando estén disponibles para
esas fechas) .
- A medida que se vayan creando reservas, debe descontarse del número de
habitaciones disponibles de ese tipo para ese rango de fechas. 
- Solo se podrán crear
reservas desde la fecha actual hasta el 31/12/~2020~2022.
- Cualquier cambio o añadido sobre lo aquí explicado que suponga una mejora en la aplicación
será bienvenida y tenida en cuenta. Queremos ver cómo eres capaz de pensar por ti mismo/a
añadiendo mejoras sobre lo requerido. También queremos ver que tu código es limpio y
eficiente.
## Condiciones de entrega
Para entregar la prueba se debe subir a una cuenta de github y facilitarnos el enlace. La prueba
se entregará con 2 reservas ya creadas. Se usará una base de datos SQLite que estará
incluida en el repositorio git.
Es necesario facilitar una url a la prueba funcionando. Antes de revisar el código
comprobaremos la funcionalidad de la prueba en esa url. Puedes utilizar cualquier servicio
gratuito como pythonanywhere, heroku, etc

# Desarrollo
## Requerimientos
- Python 3.9.5
- Django 3.0.14

# Release
**Última versión**: v0.1.0
**Instancia de prueba**: https://mggp.pythonanywhere.com/
