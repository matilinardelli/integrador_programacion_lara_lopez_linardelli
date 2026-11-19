# integrador_programacion_lara_lopez_linardelli
INTEGRANTES: 
Matias Linardelli 
Thiago Lopez
Ignacio Lara

DESCRIPCION:
Este sistema permite gestionar una base de datos de países almacenada en un archivo de formato CSV (paises.csv). Está diseñado con un enfoque modular y robusto, incorporando validaciones exhaustivas para evitar errores de ejecución ante entradas incorrectas del usuario o anomalías en el archivo de datos.

CARACTERÍSTICAS:
Persistencia de datos: Lee automáticamente los registros al iniciar y guarda los cambios (altas, modificaciones, eliminaciones) de forma persistente.
Manejo de errores y validaciones: Cuenta con funciones especializadas para controlar que los campos de texto no estén vacíos, que los continentes pertenezcan a una lista predefinida y que los valores numéricos (población y superficie) sean estrictamente positivos y válidos.
Búsqueda flexible: Implementa un buscador por coincidencias parciales de palabras sin necesidad de librerías externas.
Herramientas de análisis: Permite filtrar por continente, rangos numéricos, ordenar la información bajo distintos criterios y generar estadísticas generales (promedios, extremos y conteos por continente).

INSTRUCCIONES DE USO:
1) Asegúrarse de tener un archivo llamado paises.csv en el mismo directorio que el script. El archivo debe contener las siguientes columnas de encabezado exactas: nombre, continente, poblacion, superficie.
2) El programa desplegará un menú interactivo con 10 opciones numeradas. Ingresa el número correspondiente a la acción que desees realizar y sigue las indicaciones en pantalla.

EJEMPLOS DE ENTRADA Y SALIDA:
1) Consultar pais por nombre:
Entrada:
Seleccione una opción (1-10): 3
--- Consultar país ---
Nombre del país a buscar: argentina

Salida:
Se encontraron 1 resultado(s).

- Argentina | Continente: América | Población: 45,800,000 | Superficie: 2,780,400.0 km²

2) Filtrar por rango de poblacion:
Entrada:
Seleccione una opción (1-10): 5
--- Filtrar por población ---
Población mínima: 10000000
Población máxima: 50000000

Salida:
Se encontraron 2 resultado(s).
Países con población entre 10,000,000 y 50,000,000:
- Argentina | Población: 45,800,000
- Peru | Población: 33,000,000

3) Manejo de errores de validacion:
Entrada:
--- Agregar país ---
Nombre: Chile
Continente:
  1. América
  ...
Elija una opción (1-6): 1
Población: -500

salida:
Error: El campo 'Población' debe ser mayor a 0.








