# Patrones de diseño en Python

Repositorio de referencia con ejemplos mínimos y ejecutables de los patrones
de diseño del catálogo GoF. Cada patrón tiene al menos una versión **antes**
(el problema, sin el patrón) y una versión **con el patrón** (la solución),
para que otros proyectos puedan reconocer el problema y copiar la solución.
Algunos patrones recorren varios pasos intermedios o comparan variantes del
mismo patrón.

- **¿Querés las reglas y plantillas para tu proyecto?** Leé
  [PATTERNS.md](PATTERNS.md).
- **¿Querés entender el razonamiento?** Abrí el README de la carpeta del
  patrón y recorré sus archivos en el orden de la tabla.

## Mapa del repositorio

### Creacionales

| Patrón | Carpeta | Archivo | Qué muestra |
| --- | --- | --- | --- |
| Abstract Factory | [abstract_factory/](creational/abstract_factory/README.md) | [cars_before_abstract_factory.py](creational/abstract_factory/cars_before_abstract_factory.py) | Antes |
|  |  | [cars_with_abstract_factory.py](creational/abstract_factory/cars_with_abstract_factory.py) | Con el patrón |
| Builder | [builder/](creational/builder/README.md) | [computer_long_constructor_before_builder.py](creational/builder/computer_long_constructor_before_builder.py) | Antes, paso 1: constructor largo |
|  |  | [computer_public_attributes_before_builder.py](creational/builder/computer_public_attributes_before_builder.py) | Antes, paso 2: atributos públicos |
|  |  | [computer_encapsulated_before_builder.py](creational/builder/computer_encapsulated_before_builder.py) | Antes, paso 3: configuración encapsulada |
|  |  | [computer_build_before_builder.py](creational/builder/computer_build_before_builder.py) | Antes, paso 4: pasos ordenados |
|  |  | [computer_with_builder.py](creational/builder/computer_with_builder.py) | Con el patrón, paso 5 |
| Factory | [factory/](creational/factory/README.md) | [cars_before_factory.py](creational/factory/cars_before_factory.py) | Antes, paso 1 |
|  |  | [cars_with_simple_factory.py](creational/factory/cars_with_simple_factory.py) | Con el patrón, paso 2: Simple Factory |
|  |  | [cars_with_factory_method.py](creational/factory/cars_with_factory_method.py) | Con el patrón, paso 3: Factory Method |
| Prototype | [prototype/](creational/prototype/README.md) | [computer_before_prototype.py](creational/prototype/computer_before_prototype.py) | Antes |
|  |  | [computer_with_shallow_copy_prototype.py](creational/prototype/computer_with_shallow_copy_prototype.py) | Con el patrón: copia superficial |
|  |  | [computer_with_deep_copy_prototype.py](creational/prototype/computer_with_deep_copy_prototype.py) | Con el patrón: copia profunda |
|  |  | [computer_with_registry_prototype.py](creational/prototype/computer_with_registry_prototype.py) | Con el patrón: registro de prototipos |
| Singleton | [singleton/](creational/singleton/README.md) | [logger_before_singleton.py](creational/singleton/logger_before_singleton.py) | Antes |
|  |  | [logger_with_classic_singleton.py](creational/singleton/logger_with_classic_singleton.py) | Con el patrón: clásico |
|  |  | [logger_with_base_class_singleton.py](creational/singleton/logger_with_base_class_singleton.py) | Con el patrón: clase base |
|  |  | [logger_with_metaclass_singleton.py](creational/singleton/logger_with_metaclass_singleton.py) | Con el patrón: metaclase |
|  |  | [logger_with_monostate_singleton.py](creational/singleton/logger_with_monostate_singleton.py) | Con el patrón: Monostate (Borg) |

### Estructurales

| Patrón | Carpeta | Archivo | Qué muestra |
| --- | --- | --- | --- |
| Adapter | [adapter/](structural/adapter/README.md) | [customers_before_adapter.py](structural/adapter/customers_before_adapter.py) | Antes, paso 1: solo clientes |
|  |  | [customers_vendors_before_adapter.py](structural/adapter/customers_vendors_before_adapter.py) | Antes, paso 2: condicionales por tipo |
|  |  | [customers_vendors_with_class_adapter.py](structural/adapter/customers_vendors_with_class_adapter.py) | Con el patrón, paso 3: por herencia |
|  |  | [customers_vendors_with_object_adapter.py](structural/adapter/customers_vendors_with_object_adapter.py) | Con el patrón, paso 4: por composición |
| Bridge | [bridge/](structural/bridge/README.md) | [subscription_before_bridge.py](structural/bridge/subscription_before_bridge.py) | Antes, paso 1: una jerarquía |
|  |  | [subscription_discount_before_bridge.py](structural/bridge/subscription_discount_before_bridge.py) | Antes, paso 2: explosión de subclases |
|  |  | [subscription_discount_with_bridge.py](structural/bridge/subscription_discount_with_bridge.py) | Con el patrón, paso 3 |
| Composite | [composite/](structural/composite/README.md) | [family_before_composite.py](structural/composite/family_before_composite.py) | Antes |
|  |  | [family_with_composite.py](structural/composite/family_with_composite.py) | Con el patrón |
| Decorator | [decorator/](structural/decorator/README.md) | [cars_before_decorator.py](structural/decorator/cars_before_decorator.py) | Antes: autos |
|  |  | [cars_with_decorator.py](structural/decorator/cars_with_decorator.py) | Con el patrón: autos |
|  |  | [pizza_before_decorator.py](structural/decorator/pizza_before_decorator.py) | Antes: pizzas |
|  |  | [pizza_with_decorator.py](structural/decorator/pizza_with_decorator.py) | Con el patrón: pizzas |
| Facade | [facade/](structural/facade/README.md) | [schedule_server_before_facade.py](structural/facade/schedule_server_before_facade.py) | Antes |
|  |  | [schedule_server_with_facade.py](structural/facade/schedule_server_with_facade.py) | Con el patrón |
| Flyweight | [flyweight/](structural/flyweight/README.md) | [collider_events_before_flyweight.py](structural/flyweight/collider_events_before_flyweight.py) | Antes |
|  |  | [collider_events_with_flyweight.py](structural/flyweight/collider_events_with_flyweight.py) | Con el patrón |
| Proxy | [proxy/](structural/proxy/README.md) | [employee_access_before_proxy.py](structural/proxy/employee_access_before_proxy.py) | Antes |
|  |  | [employee_access_with_proxy.py](structural/proxy/employee_access_with_proxy.py) | Con el patrón |

### De comportamiento

| Patrón | Carpeta | Archivo | Qué muestra |
| --- | --- | --- | --- |
| Observer | [observer/](behavioral/observer/README.md) | [kpi_dashboard_before_observer.py](behavioral/observer/kpi_dashboard_before_observer.py) | Antes |
|  |  | [kpi_dashboard_with_observer.py](behavioral/observer/kpi_dashboard_with_observer.py) | Con el patrón |
| State | [state/](behavioral/state/README.md) | [state_power_before_state.py](behavioral/state/state_power_before_state.py) | Antes |
|  |  | [state_power_with_state.py](behavioral/state/state_power_with_state.py) | Con el patrón |
| Strategy | [strategy/](behavioral/strategy/README.md) | [shipping_cost_before_strategy.py](behavioral/strategy/shipping_cost_before_strategy.py) | Antes |
|  |  | [shipping_cost_with_strategy.py](behavioral/strategy/shipping_cost_with_strategy.py) | Con el patrón |
| Template Method | [template_method/](behavioral/template_method/README.md) | [compiler_before_template_method.py](behavioral/template_method/compiler_before_template_method.py) | Antes: compiladores |
|  |  | [compiler_with_template_method.py](behavioral/template_method/compiler_with_template_method.py) | Con el patrón: compiladores |
|  |  | [travel_agency_before_template_method.py](behavioral/template_method/travel_agency_before_template_method.py) | Antes: agencia de viajes |
|  |  | [travel_agency_with_template_method.py](behavioral/template_method/travel_agency_with_template_method.py) | Con el patrón: agencia de viajes |


Cada carpeta tiene un `README.md` con: la idea del patrón, sus archivos, el
problema, la solución, un diagrama de clases Mermaid por archivo (herencia,
composición y dependencias), el patrón para reutilizar (con un link a su
plantilla en `PATTERNS.md`) y las simplificaciones del ejemplo. Además, el docstring de
cada módulo explica el escenario, qué falla o por qué funciona, cuándo usar
el patrón, sus trade-offs, los patrones relacionados y un diagrama de roles.

> **Nombres de archivo.** Todos siguen el esquema
> `<ejemplo>_before_<patrón>.py` / `<ejemplo>_with_<variante>_<patrón>.py`.

## Cómo ejecutar los ejemplos

Requisitos: Python ≥ 3.12 y [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run python -m creational.factory.cars_with_factory_method
uv run python -m structural.decorator.pizza_with_decorator
uv run python -m behavioral.state.state_power_with_state
```

Todos los módulos se ejecutan como
`uv run python -m <categoría>.<patrón>.<archivo>` (sin `.py`) y muestran su
resultado por consola. Los ejemplos no tienen dependencias externas.

## Tests y validación

Los tests de [tests/unit/](tests/unit/) validan los ejemplos y su
documentación:

- [test_examples_run.py](tests/unit/test_examples_run.py) ejecuta todos los
  ejemplos como scripts.
- [test_patterns_snippets.py](tests/unit/test_patterns_snippets.py) ejecuta
  las plantillas de `PATTERNS.md`, para que la guía no quede desactualizada.
- [test_docs_in_sync.py](tests/unit/test_docs_in_sync.py) verifica que cada
  ejemplo y cada clase estén documentados en el README de su carpeta y en
  este mapa, que los docstrings de módulo tengan sus secciones y declaren el
  rol de cada clase, que los archivos que mencionan existan, y que las
  plantillas de `PATTERNS.md` no usen nombres como `id` o `type`.

### Documentación sincronizada automáticamente

Si el cambio lo hace Claude Code, el hook de
[.claude/settings.json](.claude/settings.json) corre `test_docs_in_sync.py`
después de cada edición de un ejemplo o de un `.md`. Si falla, Claude recibe
el error y actualiza la documentación en ese mismo turno. Podés revisarlo o
desactivarlo con `/hooks`.

```bash
uv run --group tests pytest -q             # tests
uv run --group linters ruff check .        # lint
uv run --group linters ruff format --check .  # formato
uv run --group linters mypy .              # tipos (modo strict)
```

## Cómo usar este repositorio desde otro proyecto

1. Copiá o enlazá [PATTERNS.md](PATTERNS.md) en tu proyecto.
2. Referencialo en las instrucciones para agentes (`CLAUDE.md`, `AGENTS.md`,
   `.cursorrules`) para que el código generado siga estos patrones.
3. Usá la lista de revisión de `PATTERNS.md` en los code reviews.

## Conceptos generales

### Las tres familias

- **Creacionales:** cómo se crean los objetos sin que el cliente dependa de
  las clases concretas (Abstract Factory, Builder, Factory Method,
  Prototype, Singleton).
- **Estructurales:** cómo se componen clases y objetos en estructuras más
  grandes (Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy).
- **De comportamiento:** cómo se reparten las responsabilidades y se
  comunican los objetos (Observer, State, Strategy, Template Method).

### Precaución

- No apliques un patrón porque sí: cada uno agrega clases e indirección.
- Aplicalo cuando la señal que describe `PATTERNS.md` aparece de verdad en
  el código, no por una variación hipotética.
- Varios patrones tienen la misma forma (Strategy, State y Bridge; Adapter,
  Decorator y Proxy). Lo que los distingue es la **intención**: el
  docstring de cada ejemplo "con" explica la diferencia en su sección
  `Related`.

### Composición sobre herencia

La mayoría de los patrones de este repo reemplazan una jerarquía que crece
(una subclase por combinación) por objetos que se combinan en tiempo de
ejecución. La herencia queda para fijar contratos (`ABC`) y esqueletos
(Template Method).
