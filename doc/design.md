# AlgoBench — Diseño del sistema

## 0. Convenciones de formato de código

- **Clases**: PascalCase
- **Funciones y variables**: snake\_case

## 1. Recursos de la API y relaciones

La API se organiza en torno a los siguientes recursos:

- **Algorithms**: catálogo de algoritmos disponibles, con su descripción, complejidad teórica e implementaciones existentes.
- **Implementations**: implementaciones concretas de un algoritmo en un lenguaje determinado (Python o C++).
- **Executions**: ejecuciones individuales de una implementación sobre unos datos de entrada.
- **Benchmarks**: pruebas que agrupan varias ejecuciones para comparar el rendimiento de distintas implementaciones.

Relaciones principales:

- Un `Algorithm` puede tener varias `Implementations`. Cada implementación pertenece a un único algoritmo.
- Una `Implementation` puede tener muchas `Executions`. Cada ejecución utiliza una única implementación.
- Un `Benchmark` agrupa varias `Executions`. Una ejecución puede pertenecer a un benchmark o existir independientemente.
- Las ejecuciones de un mismo benchmark utilizan el mismo algoritmo y los mismos datos de entrada, pero pueden utilizar implementaciones diferentes y repetirse varias veces.

El sistema también contempla usuarios y autenticación como funcionalidades futuras, pero no forman parte del alcance inicial del MVP.

## 2. Endpoints

Se utilizarán nombres de recursos en plural y se emplearán los métodos HTTP según la operación realizada.

| Método | Ruta | Descripción | Códigos esperados |
|---|---|---|---|
| GET | `/algorithms` | Consultar el catálogo de algoritmos. | 200 |
| GET | `/algorithms/{algorithm_id}` | Consultar la información de un algoritmo. | 200, 404 |
| GET | `/algorithms/{algorithm_id}/implementations` | Consultar las implementaciones de un algoritmo. | 200, 404 |
| GET | `/implementations/{implementation_id}` | Consultar una implementación. | 200, 404 |
| POST | `/executions` | Solicitar una ejecución individual. | 201, 404, 422 |
| GET | `/executions/{execution_id}` | Consultar el resultado de una ejecución. | 200, 404 |
| GET | `/executions` | Consultar el historial de ejecuciones. | 200 |
| POST | `/benchmarks` | Crear un benchmark. | 201, 404, 422 |
| GET | `/benchmarks/{benchmark_id}` | Consultar los resultados de un benchmark. | 200, 404 |
| GET | `/benchmarks` | Consultar el historial de benchmarks. | 200 |

Los códigos indican:

- `200 OK`: consulta realizada correctamente.
- `201 Created`: recurso creado correctamente.
- `404 Not Found`: el recurso solicitado no existe.
- `422 Unprocessable Entity`: los datos de entrada no cumplen las validaciones.
- `500 Internal Server Error`: error interno no previsto.

Los endpoints de historial permitirán incorporar filtros y paginación.

## 3. Modelo de datos

Se utilizará una base de datos relacional SQLite, accedida mediante SQLAlchemy.

### Algorithm

- `alg_id`: clave primaria.
- `name`: nombre del algoritmo.
- `description`: descripción.
- `time_complexity`: complejidad temporal teórica.
- `space_complexity`: complejidad espacial teórica.

### Implementation

- `impl_id`: clave primaria.
- `alg_id`: clave foránea hacia Algorithm.
- `identifier`: identificador único de la implementación.
- `language`: lenguaje de programación (`PYTHON` o `CPP`).

### Execution

- `ex_id`: clave primaria.
- `impl_id`: clave foránea hacia Implementation.
- `benchmark_id`: clave foránea opcional hacia Benchmark.
- `input`: datos de entrada en formato JSON.
- `output`: resultado en formato JSON, si existe.
- `execution_time_ns`: tiempo de ejecución en nanosegundos.
- `status`: estado de la ejecución.
- `error`: información del error, si se produce.

### Benchmark

- `bm_id`: clave primaria.
- `algorithm_id`: clave foránea hacia Algorithm.
- `input`: datos utilizados en la comparación, en formato JSON.
- `repetitions`: número de repeticiones por implementación.
- `statistics`: resultados estadísticos de la comparación, en formato JSON.
- `status`: estado del benchmark.

Las claves foráneas permiten mantener la relación entre las entidades. El campo `benchmark_id` de Execution será nullable para permitir ejecuciones independientes.

Los datos de entrada y salida se almacenarán como JSON porque los distintos algoritmos pueden necesitar estructuras diferentes. Por ejemplo, un algoritmo de ordenación recibe una colección de números, mientras que Binary Search necesita también un elemento que buscar.

## 4. Contrato JSON entre Python y C++

La comunicación inicial se realizará mediante procesos independientes. Python enviará una petición JSON al programa C++ y recibirá una respuesta JSON.

### Petición

```json
{
  "algorithm": "quick_sort",
  "input": {
    "values": [8, 3, 5, 1, 9]
  }
}
```

El campo `algorithm` identifica el algoritmo que debe ejecutarse. `input` contiene los datos necesarios para ese algoritmo.

### Respuesta correcta

```json
{
  "success": true,
  "result": {
    "values": [1, 3, 5, 8, 9]
  },
  "execution_time_ns": 12500
}
```

### Respuesta de error

```json
{
  "success": false,
  "error": {
    "code": "INVALID_INPUT",
    "message": "The input data is invalid"
  }
}
```

El campo `success` indica si la operación ha terminado correctamente. Si falla, `error` contiene un código identificativo y un mensaje descriptivo.

Cada petición y respuesta utilizará un único objeto JSON. El programa C++ escribirá la respuesta JSON en la salida estándar, reservando la salida de error para mensajes de diagnóstico.

El tiempo se medirá dentro de cada implementación, sin incluir el tiempo necesario para iniciar el proceso C++. Así se evita que el coste de comunicación distorsione la comparación del tiempo de ejecución del algoritmo.

## 5. Estructura de carpetas

```text
AlgoBench/
│
├── src/
│   └── algobench/
│       ├── api/
│       ├── services/
│       ├── repositories/
│       ├── models/
│       ├── schemas/
│       ├── algorithms/
│       ├── cpp_engine/
│       └── core/
│
├── cpp/
│   ├── src/
│   └── include/
│
├── tests/
├── docs/
│   ├── design.md
│   └── decisions.md
│
├── requirements.txt
└── README.md
```

Responsabilidades:

- `api/`: endpoints y configuración de las rutas de FastAPI.
- `services/`: lógica de negocio y coordinación de operaciones.
- `repositories/`: acceso y consultas a la base de datos.
- `models/`: modelos de persistencia de SQLAlchemy.
- `schemas/`: esquemas Pydantic para validar peticiones y respuestas.
- `algorithms/`: implementaciones de los algoritmos en Python.
- `cpp_engine/`: comunicación y gestión de los procesos C++ desde Python.
- `core/`: configuración general de la aplicación.
- `cpp/`: código fuente y cabeceras del motor C++.
- `tests/`: pruebas automatizadas.
- `docs/`: documentación y registro de decisiones técnicas.

Esta separación permite mantener la API, la lógica de negocio, el acceso a datos y los motores de ejecución independientes, facilitando su modificación y prueba.


