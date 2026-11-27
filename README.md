# Software FJ

## Fase 4 - Componente práctico - Prácticas simuladas

### Información académica

- Universidad: Universidad Nacional Abierta y a Distancia (UNAD).
- Escuela: Ciencias Básicas, Tecnología e Ingeniería (ECBTI).
- Programa: Ingeniería de Sistemas.
- Curso: Programación.
- Código del curso: 213023.
- Año: 2026.

## 1. Descripción del proyecto

Software FJ es un sistema integral de gestión de clientes, servicios y reservas desarrollado en Python, aplicando los principios de la programación orientada a objetos y el manejo avanzado de excepciones.

El sistema permite administrar reservas de salas, alquiler de equipos y asesorías especializadas, garantizando la estabilidad del programa frente a los errores contemplados en las simulaciones.

## 2. Objetivo general

Desarrollar una aplicación orientada a objetos que permita gestionar clientes, servicios y reservas mediante mecanismos de validación y manejo de excepciones, buscando la estabilidad y robustez del sistema.

## 3. Funcionalidades

- Registro y validación de clientes.
- Gestión de servicios.
- Reserva de salas.
- Alquiler de equipos.
- Asesorías especializadas.
- Confirmación, cancelación y procesamiento de reservas.
- Cálculo de costos, impuestos y descuentos.
- Validación de disponibilidad.
- Manejo de errores y excepciones.
- Registro de eventos mediante logging.

## 4. Conceptos de programación implementados

- Abstracción.
- Encapsulamiento.
- Herencia.
- Polimorfismo.
- Clases abstractas.
- Sobrescritura de métodos.
- Sobrecarga mediante parámetros opcionales.
- Excepciones personalizadas.
- Bloques try, except, else y finally.
- Encadenamiento de excepciones.
- Gestión de objetos mediante listas.

## 5. Arquitectura del sistema

| Clase | Responsabilidad |
|---|---|
| Entidad | Clase abstracta general. |
| Cliente | Administración y validación de clientes. |
| Servicio | Clase abstracta de servicios. |
| ReservaSala | Gestión de reservas de salas. |
| AlquilerEquipo | Gestión de alquileres de equipos. |
| Asesoria | Gestión de asesorías especializadas. |
| Reserva | Administración de las reservas. |
| Sistema | Coordinación de las operaciones. |

## 6. Estructura del repositorio

| Archivo | Descripción |
|---|---|
| software_fj.py | Código fuente del sistema y simulaciones. |
| software_fj.ipynb | Cuaderno ejecutable de Python. |
| software_fj.log | Registro de eventos y errores. |
| README.md | Documentación del proyecto. |
| .gitignore | Configuración de archivos ignorados por Git. |

## 7. Requisitos de ejecución

- Python 3.
- Jupyter Notebook o Google Colab para ejecutar el archivo IPYNB.
- No requiere bases de datos.
- No requiere instalar bibliotecas externas.

## 8. Instrucciones de ejecución

### Mediante Python

Descargar el archivo software_fj.py, abrir una terminal en la carpeta correspondiente y ejecutar:

```bash
python software_fj.py
```

### Mediante Google Colab

1. Descargar el archivo software_fj.ipynb.
2. Ingresar a Google Colab.
3. Cargar el cuaderno.
4. Ejecutar todas las celdas.
5. Revisar los resultados de las simulaciones.

El archivo software_fj.log se genera automáticamente durante la ejecución y se reemplaza en cada nueva simulación.

## 9. Resultados de las simulaciones

| Indicador | Resultado |
|---|---:|
| Operaciones simuladas | 20 |
| Operaciones válidas | 11 |
| Operaciones inválidas controladas | 9 |
| Resultados conformes con lo esperado | 20 |
| Porcentaje de conformidad | 100 % |

Se verificó que el sistema continúa funcionando después de detectar los errores previstos, registrando los eventos y excepciones en el archivo de logs.

## 10. Consideraciones

El sistema utiliza datos ficticios y tarifas de ejemplo con fines académicos. La información se administra en memoria mediante objetos y listas, sin utilizar motores de bases de datos.

La disponibilidad de los servicios se controla mediante su estado y las reservas activas.

## 11. Conclusiones

La implementación de la programación orientada a objetos permite desarrollar una solución modular, organizada y extensible.

El manejo de excepciones personalizadas facilita la identificación y el control de errores, evitando interrupciones durante las operaciones simuladas.

El uso de GitHub permite gestionar el historial de cambios, documentar el proyecto y facilitar el desarrollo colaborativo.

## 12. Referencias bibliográficas

- Van Rossum, G., & Drake Jr., F. L. (2024). El tutorial de Python. Python Software Foundation. https://docs.python.org/es/3.12/tutorial/errors.html

- Cuevas Álvarez, A. (2016). Python 3: curso práctico. RA-MA Editorial.

- Mishra, P. (2024). Ultimate Git and GitHub for Modern Software Development. Orange Education Pvt Ltd.

- Silva, F. D. (2025). Basics of using GitHub. Repositorio Institucional UNAD. https://repository.unad.edu.co/handle/10596/75882

- Zambrano, J. P. (2025). Introducción al uso de GitHub. Repositorio Institucional UNAD. https://repository.unad.edu.co/handle/10596/75876

---

Proyecto académico - UNAD - 2026.
