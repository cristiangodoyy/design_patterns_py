# Guía de patrones de diseño para otros proyectos

Esta guía es la **referencia prescriptiva** del repositorio: dice cuándo usar
cada patrón, qué señales indican que hace falta y trae plantillas listas para
copiar. Los ejemplos de cada carpeta muestran el razonamiento paso a paso
(versión "antes" y "con el patrón"); este documento resume las reglas que
otros proyectos deben seguir.

> Si solo vas a leer un archivo, leé este.

Cada plantilla es una **versión reducida del módulo "con" de su carpeta**:
usa las mismas clases, los mismos métodos y los mismos mensajes, y solo deja
afuera las piezas repetidas (por ejemplo, la tercera edición de autos o el
segundo builder). Las señales describen el problema que muestra el módulo
"antes" de la misma carpeta.

## Cómo usar esta guía en tu proyecto

1. Copiá este archivo (o enlazalo) en la documentación de tu proyecto.
2. Referencialo desde las instrucciones para agentes de IA (`CLAUDE.md`,
   `AGENTS.md`, `.cursorrules`), por ejemplo:
   `Seguir los patrones de diseño de PATTERNS.md al crear o modificar clases.`
3. Usá la [lista de revisión](#lista-de-revisión-para-code-review) en los
   code reviews.
4. Ante la duda, abrí el ejemplo "antes/con" de la carpeta del patrón para
   ver el razonamiento completo.

[`test_patterns_snippets.py`](tests/unit/test_patterns_snippets.py) ejecuta
cada plantilla de este documento, cada una por separado, y
[`test_docs_in_sync.py`](tests/unit/test_docs_in_sync.py) comprueba que cada
clase y cada método de una plantilla existan en los módulos de su carpeta.
Si cambiás una plantilla o un ejemplo, corré `uv run --group tests pytest -q`.

## Convenciones generales

Las plantillas siguen estas convenciones (Python ≥ 3.12):

| Tema | Convención |
| --- | --- |
| Roles del patrón | `abc.ABC` + `@abstractmethod` para Product, Component, Strategy, State, etc.: Python impide instanciar una implementación incompleta. `typing.Protocol` cuando el tipado estructural es parte de la idea (el adapter de objeto). |
| Datos | `@dataclass` (`frozen=True` si el objeto no debe cambiar). |
| Dependencias | Se reciben por el constructor, tipadas con la **abstracción**. |
| Creación de objetos | En un único lugar (`client()`, una fábrica, un registro). El cliente no hace `Concreto()`. |
| Dinero | `int` en centavos, nunca `float`. |
| Errores | Excepciones específicas con mensajes accionables (por ejemplo, listar las claves válidas). |
| Nombres | Nada de `id` ni `type` como nombre de parámetro o atributo: ocultan funciones built-in. |

Cada patrón trae una **precaución**: aplicalo cuando la señal aparece de
verdad, no por si acaso.

---

## Creacionales

### Abstract Factory

**Regla:** si tenés **familias de productos** que deben usarse juntos, creá
una fábrica por familia y hacé que el cliente reciba la fábrica.

**Señales:**

- `if/elif` anidados sobre dos dimensiones, como `make_car(maker, edition)`
  en `cars_before_abstract_factory.py`.
- El único tipo común es la unión de todas las clases concretas
  (`type Car = FordFiesta | FordMustang | ...`).
- Nada impide mezclar un Ford económico con un GM de lujo.

**Plantilla:**

Dos ediciones por fabricante (el módulo tiene tres: también `create_luxury`).

```python
from abc import ABC, abstractmethod
from enum import StrEnum, auto


class Maker(StrEnum):
    GM = auto()
    FORD = auto()


class AbsCar(ABC):
    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def start(self) -> None: ...

    @abstractmethod
    def stop(self) -> None: ...


class FordFiesta(AbsCar):
    def __init__(self) -> None:
        super().__init__("Ford Fiesta")

    def start(self) -> None:
        print(f"{self.name} running cheaply.")

    def stop(self) -> None:
        print(f"{self.name} shutting down.")


class FordMustang(AbsCar):
    def __init__(self) -> None:
        super().__init__("Ford Mustang")

    def start(self) -> None:
        print(f"{self.name} roaring and ready to go!")

    def stop(self) -> None:
        print(f"{self.name} shutting down.")


class ChevySpark(AbsCar):
    def __init__(self) -> None:
        super().__init__("Chevy Spark")

    def start(self) -> None:
        print(f"{self.name} running efficiently.")

    def stop(self) -> None:
        print(f"{self.name} shutting down.")


class ChevyCamaro(AbsCar):
    def __init__(self) -> None:
        super().__init__("Chevy Camaro")

    def start(self) -> None:
        print(f"{self.name} V8 sounding awesome!")

    def stop(self) -> None:
        print(f"{self.name} shutting down.")


class AbsFactory(ABC):
    """Una fábrica por familia: el cliente elige la familia con ella."""

    @abstractmethod
    def create_economy(self) -> AbsCar: ...

    @abstractmethod
    def create_sport(self) -> AbsCar: ...


class FordFactory(AbsFactory):
    def create_economy(self) -> AbsCar:
        return FordFiesta()

    def create_sport(self) -> AbsCar:
        return FordMustang()


class GeneralMotorsFactory(AbsFactory):
    def create_economy(self) -> AbsCar:
        return ChevySpark()

    def create_sport(self) -> AbsCar:
        return ChevyCamaro()


FACTORIES: dict[Maker, AbsFactory] = {
    Maker.FORD: FordFactory(),
    Maker.GM: GeneralMotorsFactory(),
}


def factory_for(maker: Maker | str) -> AbsFactory:
    try:
        return FACTORIES[Maker(maker)]
    except ValueError as exc:
        known = ", ".join(sorted(FACTORIES))
        raise ValueError(
            f"Unknown maker {maker!r}; expected one of: {known}"
        ) from exc


def drive_lineup(factory: AbsFactory) -> None:
    """Cliente: solo conoce AbsFactory y AbsCar."""
    for car in (factory.create_economy(), factory.create_sport()):
        car.start()
        car.stop()


def test_each_factory_builds_its_own_family() -> None:
    assert isinstance(factory_for("gm").create_sport(), ChevyCamaro)
    assert isinstance(factory_for(Maker.FORD).create_economy(), FordFiesta)
    drive_lineup(factory_for(Maker.FORD))
```

**Precaución:** agregar un **tipo de producto** (por ejemplo, una edición
pickup) obliga a cambiar `AbsFactory` y todas las fábricas.

Ejemplo completo: [creational/abstract_factory/](creational/abstract_factory/README.md)

### Builder

**Regla:** si un objeto se arma en **pasos ordenados** y hay varias
configuraciones, separá la secuencia (director) de las piezas (builders).

**Señales:**

- Un constructor con un argumento por componente
  (`computer_long_constructor_before_builder.py`).
- El cliente asigna atributos públicos uno por uno y puede olvidar alguno
  (`computer_public_attributes_before_builder.py`).
- La secuencia de pasos y las piezas viven en la misma clase, que hay que
  copiar para cada configuración (`computer_build_before_builder.py`).

**Plantilla:**

Un solo builder, como en `computer_with_builder.py` (el módulo también tiene
`HPBuilder`).

```python
from abc import ABC, abstractmethod


class Computer:
    def __init__(self) -> None:
        self.case: str = ""
        self.mainboard: str = ""
        self.cpu: str = ""
        self.memory: str = ""
        self.hard_drive: str = ""
        self.video_card: str = ""


class AbsBuilder(ABC):
    def __init__(self) -> None:
        self._computer = Computer()

    def new_computer(self) -> None:
        self._computer = Computer()

    def get_computer(self) -> Computer:
        return self._computer

    @abstractmethod
    def install_case(self) -> None: ...

    @abstractmethod
    def build_mainboard(self) -> None: ...

    @abstractmethod
    def install_hard_drive(self) -> None: ...

    @abstractmethod
    def install_video_card(self) -> None: ...


class LenovoBuilder(AbsBuilder):
    def install_case(self) -> None:
        self._computer.case = "Coolermaster"

    def build_mainboard(self) -> None:
        self._computer.mainboard = "MSI"
        self._computer.cpu = "Intel Core i9"
        self._computer.memory = "2 x 16GB"

    def install_hard_drive(self) -> None:
        self._computer.hard_drive = "SSD 2TB"

    def install_video_card(self) -> None:
        self._computer.video_card = "GeForce GTX"


class Director:
    """Conoce el orden de los pasos, no las piezas."""

    def __init__(self, builder: AbsBuilder) -> None:
        self._builder = builder

    def build_computer(self) -> None:
        self._builder.new_computer()
        self._builder.install_case()
        self._builder.build_mainboard()
        self._builder.install_hard_drive()
        self._builder.install_video_card()

    def get_computer(self) -> Computer:
        return self._builder.get_computer()


def test_director_runs_every_step() -> None:
    director = Director(LenovoBuilder())
    director.build_computer()
    computer = director.get_computer()
    assert computer.cpu == "Intel Core i9"
    assert computer.video_card == "GeForce GTX"
```

**Precaución:** si solo hay campos opcionales y ningún orden que respetar,
un `dataclass` con argumentos por nombre alcanza.

Ejemplo completo: [creational/builder/](creational/builder/README.md)

### Factory Method

**Regla:** sacá la instanciación del cliente. Si todos los productos se
crean igual, alcanza un registro (Simple Factory); si cada uno necesita su
propia lógica, usá un método fábrica que decidan las subclases.

**Señales:**

- Un `if/elif` sobre el nombre del producto, como `get_car(car_name)` en
  `cars_before_factory.py`.
- Agregar un modelo obliga a abrir el módulo y editar esa función.

**Plantilla:**

Simple Factory, como en `cars_with_simple_factory.py` (con un solo auto
registrado):

```python
from abc import ABC, abstractmethod


class AbsAuto(ABC):
    @abstractmethod
    def start(self) -> None: ...

    @abstractmethod
    def stop(self) -> None: ...


class ChevyVolt(AbsAuto):
    def start(self) -> None:
        print("Chevy Volt running with shocking power!")

    def stop(self) -> None:
        print("Chevy Volt shutting down.")


class NullCar(AbsAuto):
    """Null Object: lo que se devuelve para un nombre desconocido."""

    def __init__(self, car_name: str) -> None:
        self._car_name = car_name

    def start(self) -> None:
        print(f'Cannot start unknown car "{self._car_name}".')

    def stop(self) -> None:
        print(f'Cannot stop unknown car "{self._car_name}".')


class AutoFactory:
    def __init__(self) -> None:
        self._autos: dict[str, type[AbsAuto]] = {}

    def register(self, car_name: str, auto_class: type[AbsAuto]) -> None:
        self._autos[car_name] = auto_class

    def create_instance(self, car_name: str) -> AbsAuto:
        auto_class = self._autos.get(car_name)
        if auto_class is None:
            return NullCar(car_name)
        return auto_class()


def default_auto_factory() -> AutoFactory:
    factory = AutoFactory()
    factory.register("chevy", ChevyVolt)
    return factory


def test_simple_factory() -> None:
    factory = default_auto_factory()
    assert isinstance(factory.create_instance("chevy"), ChevyVolt)
    assert isinstance(factory.create_instance("tesla"), NullCar)
```

Factory Method, como en `cars_with_factory_method.py` (con dos fábricas de
las tres):

```python
from abc import ABC, abstractmethod


class AbsAuto(ABC):
    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def start(self) -> None: ...

    @abstractmethod
    def stop(self) -> None: ...


class ChevyVolt(AbsAuto):
    def start(self) -> None:
        print(f"{self.name} running with shocking power!")

    def stop(self) -> None:
        print(f"{self.name} shutting down.")


class FordFusion(AbsAuto):
    def start(self) -> None:
        print(f"{self.name} running smoothly.")

    def stop(self) -> None:
        print(f"{self.name} shutting down.")


class AbsFactory(ABC):
    @abstractmethod
    def create_auto(self) -> AbsAuto:
        """Factory method: cada fábrica concreta decide qué auto crear."""

    def drive_new_car(self) -> AbsAuto:
        car = self.create_auto()
        car.start()
        car.stop()
        return car


class ChevyFactory(AbsFactory):
    def create_auto(self) -> AbsAuto:
        return ChevyVolt("Chevy Volt")


class FordFactory(AbsFactory):
    def create_auto(self) -> AbsAuto:
        return FordFusion("Ford Fusion")


FACTORIES: dict[str, type[AbsFactory]] = {
    "chevy": ChevyFactory,
    "ford": FordFactory,
}


def load_factory(factory_name: str) -> AbsFactory:
    factory_class = FACTORIES.get(factory_name)
    if factory_class is None:
        known = ", ".join(sorted(FACTORIES))
        raise ValueError(
            f"Unknown factory {factory_name!r}; expected one of: {known}"
        )
    return factory_class()


def test_factory_method() -> None:
    assert load_factory("ford").drive_new_car().name == "Ford Fusion"
    try:
        load_factory("tesla")
    except ValueError as error:
        assert "chevy, ford" in str(error)
    else:
        raise AssertionError("expected ValueError")
```

**Precaución:** con dos productos que no van a crecer, un `if` es más claro.

Ejemplo completo: [creational/factory/](creational/factory/README.md)

### Prototype

**Regla:** si los objetos nuevos son **variaciones de uno ya configurado**,
copialo con `clone()` en lugar de repetir el constructor.

**Señales:**

- Cada variante repite todos los argumentos del constructor, como las tres
  `Tower` de `computer_before_prototype.py`.
- Copiar campo por campo y reusar `original.mainboard` hace que dos objetos
  compartan una parte mutable sin querer.

**Plantilla:**

Copia profunda más el registro de prototipos, como en
`computer_with_registry_prototype.py` (sin `Laptop` ni `describe`):

```python
import copy

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self


class AbsPrototype(ABC):
    @abstractmethod
    def clone(self) -> Self: ...


class AbsComputer(AbsPrototype):
    model: str


@dataclass
class MainBoard:
    manufacturer: str
    model: str


@dataclass
class Tower(AbsComputer):
    model: str
    mainboard: MainBoard
    processor: str

    def clone(self) -> Self:
        # deepcopy: el clon tiene su propio MainBoard.
        return copy.deepcopy(self)


class PrototypeManager[P: AbsPrototype]:
    def __init__(self, kind: type[P]) -> None:
        self._kind = kind
        self._prototypes: dict[str, P] = {}

    def register(self, name: str, prototype: object) -> None:
        if not isinstance(prototype, self._kind):
            raise TypeError(
                f"Cannot register {name!r}: expected an instance of "
                f"{self._kind.__name__}, got {type(prototype).__name__}."
            )
        self._prototypes[name] = prototype

    def clone(self, name: str) -> P:
        try:
            prototype = self._prototypes[name]
        except KeyError:
            known = ", ".join(self.names()) or "none"
            raise KeyError(
                f"No prototype named {name!r}. Registered names: {known}."
            ) from None
        return prototype.clone()

    def names(self) -> list[str]:
        return sorted(self._prototypes)


def test_clones_do_not_touch_the_preset() -> None:
    manager = PrototypeManager(AbsComputer)
    manager.register(
        "gaming-tower",
        Tower("T1", MainBoard(manufacturer="ASUS", model="Game"), "AMD"),
    )
    tower = manager.clone("gaming-tower")
    assert isinstance(tower, Tower)
    tower.mainboard.model = "Business"
    preset = manager.clone("gaming-tower")
    assert isinstance(preset, Tower)
    assert preset.mainboard.model == "Game"
```

**Precaución:** `copy.copy` comparte las partes mutables (la "sorpresa" de
`computer_with_shallow_copy_prototype.py`); `copy.deepcopy` copia todo,
incluso lo que debería compartirse. Definí `__deepcopy__` si necesitás
controlarlo.

**Variantes del repositorio:** la plantilla combina la copia profunda de
`computer_with_deep_copy_prototype.py` con el registro de
`computer_with_registry_prototype.py`. Usá la copia superficial
(`computer_with_shallow_copy_prototype.py`) solo si todos los campos son
inmutables, como el `Laptop` de ese módulo; en `Tower` el clon comparte el
`MainBoard` con el original.

Ejemplo completo: [creational/prototype/](creational/prototype/README.md)

### Singleton

**Regla:** usalo solo si **debe existir una única instancia** y muchos
módulos no relacionados necesitan alcanzarla. Si varias clases lo necesitan
o hay hilos, usá la variante de metaclase con lock.

**Señales:**

- Cada módulo crea su propio `Logger()` y el log de un checkout queda
  partido en dos buffers (`logger_before_singleton.py`).

**Plantilla:**

La variante de `logger_with_metaclass_singleton.py`:

```python
import threading

from typing import ClassVar


class SingletonMeta(type):
    _instances: ClassVar[dict[type, object]] = {}
    _lock: ClassVar[threading.Lock] = threading.Lock()

    def __call__[T](cls: type[T], *args: object, **kwargs: object) -> T:
        instance = SingletonMeta._instances.get(cls)
        if isinstance(instance, cls):  # fast path: no lock once built
            return instance
        with SingletonMeta._lock:
            instance = SingletonMeta._instances.get(cls)
            if not isinstance(instance, cls):
                instance = type.__call__(cls, *args, **kwargs)
                SingletonMeta._instances[cls] = instance
        return instance


class Logger(metaclass=SingletonMeta):
    def __init__(self, name: str = "app") -> None:  # se ejecuta una vez
        self.name = name
        self._records: list[str] = []
        self._records_lock = threading.Lock()

    def log(self, message: str) -> None:
        with self._records_lock:
            self._records.append(f"[{self.name}] {message}")

    @property
    def records(self) -> list[str]:
        with self._records_lock:
            return list(self._records)


def test_one_logger_for_everyone() -> None:
    first = Logger()
    first.log("order 42: created")
    later = Logger("ignored")
    later.log("order 42: card charged")
    assert later is first
    assert later.name == "app"
    assert first.records == [
        "[app] order 42: created",
        "[app] order 42: card charged",
    ]
```

**Precaución:** un singleton es estado global disfrazado: oculta
dependencias y filtra estado entre tests. Preferí crear la instancia una vez
en la composition root e inyectarla. En Python, un módulo ya es un singleton
natural.

**Otras variantes del repositorio** (la plantilla usa la de metaclase porque
es la única thread-safe y deja el `__init__` limpio):

- `logger_with_classic_singleton.py`: `__new__` sobrescrito, o un
  `instance()` perezoso al estilo GoF. Sirve para una única clase final y no
  es thread-safe.
- `logger_with_base_class_singleton.py`: una clase base `Singleton` con una
  instancia por subclase. Hay que proteger el `__init__`, porque Python lo
  ejecuta en cada llamada, y tampoco es thread-safe.
- `logger_with_monostate_singleton.py`: Monostate (Borg). Los objetos son
  distintos pero comparten el `__dict__`; sirve si solo importa el estado
  compartido y nada depende de `is`.

Ejemplo completo: [creational/singleton/](creational/singleton/README.md)

---

## Estructurales

### Adapter

**Regla:** si una clase existente no tiene la interfaz que tu código
espera, envolvela en un adapter. **No modifiques ninguna de las dos.**

**Señales:**

- El cliente ramifica según el tipo de entidad y conoce cómo guarda la
  dirección cada una, como `describe(kind)` en
  `customers_vendors_before_adapter.py`.

**Plantilla:**

El adapter de objeto de `customers_vendors_with_object_adapter.py` (sin
`Employee` ni `EmployeeAdapter`):

```python
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol


class Addressable(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def address(self) -> str: ...


@dataclass(frozen=True)
class Customer:
    name: str
    address: str


@dataclass(frozen=True)
class Vendor:  # adaptado: no se toca
    name: str
    number: int
    street: str


class VendorAdapter:
    def __init__(self, vendor: Vendor) -> None:
        self._vendor = vendor

    @property
    def name(self) -> str:
        return self._vendor.name

    @property
    def address(self) -> str:
        return f"{self._vendor.number} {self._vendor.street}"


def describe(entities: Iterable[Addressable]) -> list[str]:
    return [
        f"Name: {entity.name}; Address: {entity.address}"
        for entity in entities
    ]


def test_customers_and_vendors_share_one_client() -> None:
    entities: tuple[Addressable, ...] = (
        Customer("Pizza Love", "33 Pepperoni Lane"),
        VendorAdapter(Vendor("Dough Factory", 1, "Semolina Court")),
    )
    assert describe(entities) == [
        "Name: Pizza Love; Address: 33 Pepperoni Lane",
        "Name: Dough Factory; Address: 1 Semolina Court",
    ]
```

**Precaución:** preferí el adapter de objeto (composición) al de clase
(herencia múltiple, `customers_vendors_with_class_adapter.py`): sirve para
cualquier instancia y no te ata a los detalles internos del adaptado.

Ejemplo completo: [structural/adapter/](structural/adapter/README.md)

### Bridge

**Regla:** si una jerarquía crece en **dos dimensiones independientes**,
separala en dos jerarquías y conectalas con una referencia.

**Señales:**

- Nombres de clase que combinan dos ejes, como `AnnualStudent` y
  `MonthlyCorporate` en `subscription_discount_before_bridge.py`.
- La misma regla (el 10 % de estudiantes) duplicada en varias subclases.

**Plantilla:**

Sin la fecha de vencimiento (el módulo también calcula `expiration`):

```python
from abc import ABC, abstractmethod
from datetime import date


class Discount(ABC):  # implementor
    @abstractmethod
    def apply(self, price: int) -> int: ...


class NoDiscount(Discount):
    def apply(self, price: int) -> int:
        return price


class StudentDiscount(Discount):
    def apply(self, price: int) -> int:
        return price * 90 // 100


class CorporateDiscount(Discount):
    def apply(self, price: int) -> int:
        return price * 80 // 100


class Subscription(ABC):  # abstracción
    def __init__(
        self, subscriber: str, enrolled: date, discount: Discount
    ) -> None:
        self._subscriber = subscriber
        self._enrolled = enrolled
        self._discount = discount

    @property
    def subscriber(self) -> str:
        return self._subscriber

    @property
    @abstractmethod
    def base_price(self) -> int: ...

    @property
    def price(self) -> int:
        return self._discount.apply(self.base_price)


class Annual(Subscription):
    @property
    def base_price(self) -> int:
        return 25_000


class Monthly(Subscription):
    @property
    def base_price(self) -> int:
        return 5_000


ENROLLED = date(2024, 1, 31)


def test_any_period_with_any_discount() -> None:
    assert Monthly("Ted", ENROLLED, StudentDiscount()).price == 4_500
    assert Annual("Alice", ENROLLED, CorporateDiscount()).price == 20_000
    assert Annual("Wilma", ENROLLED, NoDiscount()).price == 25_000
```

**Precaución:** con una sola dimensión real, el puente es indirección sin
beneficio.

Ejemplo completo: [structural/bridge/](structural/bridge/README.md)

### Composite

**Regla:** si tenés **jerarquías parte-todo**, hacé que las hojas y los
grupos compartan una interfaz y que los grupos deleguen en sus hijos.

**Señales:**

- El mismo bucle repetido para el grupo y para los objetos sueltos, como en
  `find_oldest(family, singles)` de `family_before_composite.py`.
- Un grupo no puede contener otro grupo.

**Plantilla:**

```python
from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator
from datetime import date


class Component(ABC):
    @abstractmethod
    def get_oldest(self) -> "Individual": ...


class Individual(Component):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def birthdate(self) -> date: ...

    def get_oldest(self) -> "Individual":
        return self


class Person(Individual):
    def __init__(self, name: str, birthdate: date) -> None:
        self._name = name
        self._birthdate = birthdate

    @property
    def name(self) -> str:
        return self._name

    @property
    def birthdate(self) -> date:
        return self._birthdate


class NullPerson(Individual):
    @property
    def name(self) -> str:
        return "nobody"

    @property
    def birthdate(self) -> date:
        return date.max


class Tree(Component, Iterable[Component]):
    def __init__(self, members: Iterable[Component]) -> None:
        self._members = list(members)

    def __iter__(self) -> Iterator[Component]:
        return iter(self._members)

    def get_oldest(self) -> Individual:
        return min(
            (member.get_oldest() for member in self),
            key=lambda individual: individual.birthdate,
            default=NullPerson(),
        )


def test_trees_nest_to_any_depth() -> None:
    hitchhikers = Tree(
        [
            Person("Trillian", date(1970, 3, 14)),
            Person("Arthur", date(1965, 7, 4)),
        ]
    )
    tree = Tree([hitchhikers, Person("Dirk", date(1990, 6, 6))])
    assert tree.get_oldest().name == "Arthur"
    assert Tree([]).get_oldest().name == "nobody"
```

**Precaución:** no subas a la interfaz común operaciones que solo tienen
sentido en las hojas (`birthdate`); ponelas en un contrato aparte
(`Individual`).

Ejemplo completo: [structural/composite/](structural/composite/README.md)

### Decorator

**Regla:** si necesitás **sumar responsabilidades a un objeto concreto en
tiempo de ejecución**, envolvelo en decoradores con su misma interfaz.

**Señales:**

- Una subclase por cada combinación, como `NonVeganPizzaWithChickenAndTomatoes`
  en `pizza_before_decorator.py`.
- La lógica de un ingrediente repetida en cada clase que lo incluye.

**Plantilla:**

La versión de pizzas de `pizza_with_decorator.py` (sin `ExtraCheese`; la de
autos, `cars_with_decorator.py`, sigue la misma forma):

```python
from abc import ABC, abstractmethod


class AbsPizza(ABC):
    @abstractmethod
    def get_description(self) -> str: ...

    @abstractmethod
    def get_price(self) -> int: ...

    @abstractmethod
    def is_vegan(self) -> bool: ...


class VeganPizza(AbsPizza):
    def get_description(self) -> str:
        return "Vegan pizza"

    def get_price(self) -> int:
        return 23000

    def is_vegan(self) -> bool:
        return True


class NonVeganPizza(AbsPizza):
    def get_description(self) -> str:
        return "Non-vegan pizza"

    def get_price(self) -> int:
        return 35000

    def is_vegan(self) -> bool:
        return False


class PizzaDecorator(AbsPizza):
    """Reenvía todo por defecto; cada ingrediente solo extiende lo suyo."""

    def __init__(self, pizza: AbsPizza) -> None:
        self._pizza = pizza

    def get_description(self) -> str:
        return self._pizza.get_description()

    def get_price(self) -> int:
        return self._pizza.get_price()

    def is_vegan(self) -> bool:
        return self._pizza.is_vegan()


class Tomatoes(PizzaDecorator):
    def get_description(self) -> str:
        return f"{super().get_description()}, tomatoes"

    def get_price(self) -> int:
        return super().get_price() + 520


class Chicken(PizzaDecorator):
    def __init__(self, pizza: AbsPizza) -> None:
        if pizza.is_vegan():
            raise ValueError(
                f"Cannot add chicken to {pizza.get_description()!r}"
            )
        super().__init__(pizza)

    def get_description(self) -> str:
        return f"{super().get_description()}, chicken"

    def get_price(self) -> int:
        return super().get_price() + 2072


def test_toppings_stack_and_rules_hold() -> None:
    pizza = Tomatoes(Chicken(Chicken(NonVeganPizza())))
    assert pizza.get_description() == (
        "Non-vegan pizza, chicken, chicken, tomatoes"
    )
    assert pizza.get_price() == 39664
    try:
        Chicken(VeganPizza())
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
```

**Precaución:** las combinaciones que la jerarquía prohibía por
construcción (pollo en una pizza vegana, dos motores en un auto) ahora hay
que validarlas en el constructor del decorador, y `isinstance` deja de
reconocer al objeto envuelto.

Ejemplo completo: [structural/decorator/](structural/decorator/README.md)

### Facade

**Regla:** si los clientes repiten la misma coreografía sobre varias clases
de un subsistema, ofreceles **un método por caso de uso**.

**Señales:**

- Doce llamadas ordenadas sobre cinco clases, copiadas en cada cliente,
  como en `schedule_server_before_facade.py`.

**Plantilla:**

Con tres de los cinco subsistemas (el módulo también tiene
`ListenerRegistry` y `SystemObjects`):

```python
import io

from contextlib import redirect_stdout


class Bootloader:
    def start_booting(self) -> None:
        print("Starting to boot")

    def read_system_config_file(self) -> None:
        print("Reading system config files")

    def init(self) -> None:
        print("Initializing")

    def destroy(self) -> None:
        print("Destroying")

    def shutdown(self) -> None:
        print("Shutting down")


class ExecutionContext:
    def initialize_context(self) -> None:
        print("Initializing context")

    def destroy_context(self) -> None:
        print("Destroying context")


class ProcessManager:
    def release_processes(self) -> None:
        print("Releasing processes")


class ScheduleServerFacade:
    def __init__(
        self,
        bootloader: Bootloader,
        context: ExecutionContext,
        processes: ProcessManager,
    ) -> None:
        self._bootloader = bootloader
        self._context = context
        self._processes = processes

    def start_server(self) -> None:
        self._bootloader.start_booting()
        self._bootloader.read_system_config_file()
        self._bootloader.init()
        self._context.initialize_context()

    def stop_server(self) -> None:
        self._processes.release_processes()
        self._bootloader.destroy()
        self._context.destroy_context()
        self._bootloader.shutdown()


def test_facade_runs_the_steps_in_order() -> None:
    facade = ScheduleServerFacade(
        Bootloader(), ExecutionContext(), ProcessManager()
    )
    output = io.StringIO()
    with redirect_stdout(output):
        facade.start_server()
        facade.stop_server()
    lines = output.getvalue().splitlines()
    assert lines[0] == "Starting to boot"
    assert lines[-1] == "Shutting down"
```

**Precaución:** la fachada simplifica el acceso, no lo prohíbe; y si
absorbe responsabilidades ajenas se vuelve una god class.

Ejemplo completo: [structural/facade/](structural/facade/README.md)

### Flyweight

**Regla:** si creás **muchísimos objetos con datos repetidos**, compartí la
parte inmutable desde una fábrica con caché.

**Señales:**

- Miles de `Event` que guardan cada uno su propia copia del nombre, la masa
  y la carga de la partícula (`collider_events_before_flyweight.py`).
- La memoria es un problema medido, no supuesto.

**Plantilla:**

```python
from dataclasses import dataclass
from types import MappingProxyType
from typing import Final


@dataclass(frozen=True, slots=True)
class ParticleType:  # estado intrínseco, compartido
    name: str
    mass_mev: float
    charge: int


class FlyweightFactory:
    CATALOG: Final = MappingProxyType(
        {
            "electron": (0.511, -1),
            "muon": (105.66, -1),
            "proton": (938.27, 1),
        }
    )

    def __init__(self) -> None:
        self._flyweights: dict[str, ParticleType] = {}

    def get_flyweight(self, name: str) -> ParticleType:
        if name not in self._flyweights:
            if name not in self.CATALOG:
                raise ValueError(f"Unknown particle {name!r}")
            mass_mev, charge = self.CATALOG[name]
            self._flyweights[name] = ParticleType(name, mass_mev, charge)
        return self._flyweights[name]

    @property
    def count(self) -> int:
        return len(self._flyweights)


class Event:  # estado extrínseco, propio de cada evento
    __slots__ = ("particle", "x_m", "y_m", "t_ns", "energy_mev")

    def __init__(
        self,
        particle: ParticleType,
        x_m: float,
        y_m: float,
        t_ns: float,
        energy_mev: float,
    ) -> None:
        self.particle = particle
        self.x_m = x_m
        self.y_m = y_m
        self.t_ns = t_ns
        self.energy_mev = energy_mev

    def lorentz_factor(self) -> float:
        return 1.0 + self.energy_mev / self.particle.mass_mev


def test_events_share_one_particle_type() -> None:
    factory = FlyweightFactory()
    first = Event(factory.get_flyweight("muon"), 0.5, 0.1, 4.5, 75.0)
    second = Event(factory.get_flyweight("muon"), 0.7, 0.2, 5.0, 100.0)
    assert first.particle is second.particle
    assert factory.count == 1
```

**Precaución:** el flyweight tiene que ser inmutable, y medí antes y
después para comprobar que el ahorro existe (el ejemplo lo mide con
`total_size()`).

Ejemplo completo: [structural/flyweight/](structural/flyweight/README.md)

### Proxy

**Regla:** si necesitás **controlar el acceso a un objeto** (permisos, carga
diferida, caché, registro), poné delante un objeto con su misma interfaz.

**Señales:**

- La regla de privacidad mezclada con la búsqueda de los registros, como en
  `employee_details` de `employee_access_before_proxy.py`.
- Cada cliente tiene que acordarse de repetir el mismo chequeo.

**Plantilla:**

```python
from abc import ABC, abstractmethod
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, replace
from datetime import date


@dataclass(frozen=True)
class Employee:
    empid: int
    name: str
    birthdate: date
    salary: int


@dataclass(frozen=True)
class EmployeeInfo:
    empid: int
    name: str
    birthdate: date | None = None
    salary: int | None = None


@dataclass(frozen=True)
class AccessControl:
    empid: int
    can_see_personal: bool


class AccessControlList:
    def __init__(self, controls: Mapping[int, AccessControl]) -> None:
        self._controls = dict(controls)

    def can_see_personal(self, requester_id: int) -> bool:
        control = self._controls.get(requester_id)
        return control is not None and control.can_see_personal


class AbsEmployees(ABC):
    @abstractmethod
    def get_employee_info(
        self, empids: Iterable[int]
    ) -> list[EmployeeInfo]: ...


class Employees(AbsEmployees):
    def __init__(self, records: Mapping[int, Employee]) -> None:
        self._records = dict(records)

    def get_employee_info(self, empids: Iterable[int]) -> list[EmployeeInfo]:
        return [
            EmployeeInfo(
                empid=record.empid,
                name=record.name,
                birthdate=record.birthdate,
                salary=record.salary,
            )
            for record in (
                self._records[empid]
                for empid in empids
                if empid in self._records
            )
        ]


class EmployeesProxy(AbsEmployees):
    def __init__(
        self,
        employees: AbsEmployees,
        access: AccessControlList,
        requester_id: int,
    ) -> None:
        self._employees = employees
        self._access = access
        self._requester_id = requester_id

    def get_employee_info(self, empids: Iterable[int]) -> list[EmployeeInfo]:
        infos = self._employees.get_employee_info(empids)
        if self._access.can_see_personal(self._requester_id):
            return infos
        return [replace(info, birthdate=None, salary=None) for info in infos]


def test_proxy_hides_personal_data() -> None:
    directory = Employees({1: Employee(1, "Bob", date(1994, 7, 4), 8_000_000)})
    access = AccessControlList({101: AccessControl(101, True)})
    ordinary = EmployeesProxy(directory, access, requester_id=3)
    manager = EmployeesProxy(directory, access, requester_id=101)
    assert ordinary.get_employee_info([1])[0].salary is None
    assert manager.get_employee_info([1])[0].salary == 8_000_000
```

**Precaución:** el proxy tiene que seguir la interfaz del objeto real, y los
clientes deben recibir el proxy, no el objeto real.

Ejemplo completo: [structural/proxy/](structural/proxy/README.md)

---

## De comportamiento

### Observer

**Regla:** si un cambio en un objeto debe reflejarse en **otros que no
conocés de antemano**, dejá que se suscriban.

**Señales:**

- Una clase que llama a mano a cada consumidor cuando cambian sus datos,
  como `Dashboard.publish` en `kpi_dashboard_before_observer.py`.
- Consumidores que se quieren agregar o quitar en tiempo de ejecución.

**Plantilla:**

Con una sola pantalla (el módulo también tiene `CurrentKPIs`):

```python
import io

from abc import ABC, abstractmethod
from contextlib import redirect_stdout


class Observer(ABC):
    @abstractmethod
    def update(self) -> None: ...


class Subject:
    def __init__(self) -> None:
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        if observer not in self._observers:
            raise ValueError(f"{type(observer).__name__} is not attached")
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in list(self._observers):  # copia: permite detach
            observer.update()


class KPIs(Subject):
    def __init__(self) -> None:
        super().__init__()
        self._open_tickets = 0
        self._closed_tickets = 0
        self._new_tickets = 0

    @property
    def open_tickets(self) -> int:
        return self._open_tickets

    @property
    def closed_tickets(self) -> int:
        return self._closed_tickets

    @property
    def new_tickets(self) -> int:
        return self._new_tickets

    def set_kpis(
        self, open_tickets: int, closed_tickets: int, new_tickets: int
    ) -> None:
        self._open_tickets = open_tickets
        self._closed_tickets = closed_tickets
        self._new_tickets = new_tickets
        self.notify()


class KPIObserver(Observer):
    """Modelo pull: lee los valores del subject al recibir el aviso."""

    def __init__(self, kpis: KPIs) -> None:
        self._kpis = kpis
        self._open_tickets = 0
        self._closed_tickets = 0
        self._new_tickets = 0

    def update(self) -> None:
        self._open_tickets = self._kpis.open_tickets
        self._closed_tickets = self._kpis.closed_tickets
        self._new_tickets = self._kpis.new_tickets
        self.display()

    @abstractmethod
    def display(self) -> None: ...


class ForecastKPIs(KPIObserver):
    def expected_open_tickets(self) -> int:
        return max(
            0, self._open_tickets + self._new_tickets - self._closed_tickets
        )

    def display(self) -> None:
        print(
            "Forecast open tickets in next hour: "
            f"{self.expected_open_tickets()}"
        )


def test_observer_is_notified_until_detached() -> None:
    kpis = KPIs()
    forecast = ForecastKPIs(kpis)
    kpis.attach(forecast)
    output = io.StringIO()
    with redirect_stdout(output):
        kpis.set_kpis(open_tickets=25, closed_tickets=10, new_tickets=5)
        kpis.detach(forecast)
        kpis.set_kpis(open_tickets=50, closed_tickets=10, new_tickets=20)
    assert output.getvalue() == "Forecast open tickets in next hour: 20\n"
```

**Precaución:** desconectá los observers que ya no se usan (*lapsed
listener*), y recordá que uno lento o que falla afecta a los siguientes.

Ejemplo completo: [behavioral/observer/](behavioral/observer/README.md)

### State

**Regla:** si **cada método ramifica sobre el mismo código de estado**,
poné cada estado en su clase y dejá que el contexto delegue.

**Señales:**

- `if self._status == PowerStatus...` repetido en `power_button`,
  `suspend` y `hibernate` (`state_power_before_state.py`).
- Reglas de transición implícitas en las ramas.

**Plantilla:**

```python
from abc import ABC, abstractmethod


class InvalidTransitionError(ValueError):
    """Raised when an action is not allowed in the current state."""


class ComputerState(ABC):
    @property
    def name(self) -> str:
        return type(self).__name__

    @property
    @abstractmethod
    def on_enter(self) -> str: ...

    @abstractmethod
    def power_button(self) -> "ComputerState": ...

    def suspend(self) -> "ComputerState":
        raise InvalidTransitionError(f"Cannot suspend while {self.name}")

    def hibernate(self) -> "ComputerState":
        raise InvalidTransitionError(f"Cannot hibernate while {self.name}")

    def __str__(self) -> str:
        return self.name


class Off(ComputerState):
    @property
    def on_enter(self) -> str:
        return "Powered off"

    def power_button(self) -> ComputerState:
        return On()


class On(ComputerState):
    @property
    def on_enter(self) -> str:
        return "Up and running"

    def power_button(self) -> ComputerState:
        return Off()

    def suspend(self) -> ComputerState:
        return Suspended()

    def hibernate(self) -> ComputerState:
        return Hibernated()


class Suspended(ComputerState):
    @property
    def on_enter(self) -> str:
        return "Sleeping, memory kept powered"

    def power_button(self) -> ComputerState:
        return On()


class Hibernated(ComputerState):
    @property
    def on_enter(self) -> str:
        return "Memory saved to disk"

    def power_button(self) -> ComputerState:
        return On()


class Computer:
    def __init__(self, model: str = "HP") -> None:
        self.model = model
        self._state: ComputerState = Off()

    @property
    def state(self) -> ComputerState:
        return self._state

    def power_button(self) -> None:
        self._change(self._state.power_button())

    def suspend(self) -> None:
        self._change(self._state.suspend())

    def hibernate(self) -> None:
        self._change(self._state.hibernate())

    def _change(self, state: ComputerState) -> None:
        print(f"{self._state} -> {state}: {state.on_enter}")
        self._state = state


def test_states_decide_the_transitions() -> None:
    computer = Computer()
    computer.power_button()
    computer.suspend()
    try:
        computer.hibernate()
    except InvalidTransitionError:
        pass
    else:
        raise AssertionError("expected InvalidTransitionError")
    assert str(computer.state) == "Suspended"
```

**Precaución:** con dos estados triviales, un `if` es más claro.

Ejemplo completo: [behavioral/state/](behavioral/state/README.md)

### Strategy

**Regla:** si **varios algoritmos resuelven la misma tarea** y hay que
elegir uno en tiempo de ejecución, encapsulá cada uno y pasalo al contexto.

**Señales:**

- `if/elif` que elige un cálculo según un código de tipo, como
  `ShippingCost.shipping_cost` sobre `Shipper` en
  `shipping_cost_before_strategy.py`.
- El dato (`Order`) guarda cómo se procesa (`shipper`).

**Plantilla:**

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Order:
    customer: str


class AbsStrategy(ABC):
    @abstractmethod
    def calculate(self, order: Order) -> int: ...


class FedExStrategy(AbsStrategy):
    def calculate(self, order: Order) -> int:
        return 300


class UPSStrategy(AbsStrategy):
    def calculate(self, order: Order) -> int:
        return 400


class PostalStrategy(AbsStrategy):
    def calculate(self, order: Order) -> int:
        return 500


class ShippingCost:
    def __init__(self, strategy: AbsStrategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> AbsStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: AbsStrategy) -> None:
        self._strategy = strategy

    def shipping_cost(self, order: Order) -> int:
        return self._strategy.calculate(order)


def test_strategy_is_swapped_at_runtime() -> None:
    order = Order("Ada")
    calculator = ShippingCost(FedExStrategy())
    assert calculator.shipping_cost(order) == 300
    calculator.strategy = PostalStrategy()
    assert calculator.shipping_cost(order) == 500
    calculator.strategy = UPSStrategy()
    assert calculator.shipping_cost(order) == 400
```

**Precaución:** si las estrategias no tienen estado, en Python alcanza con
pasar una función (`Callable[[Order], int]`).

Ejemplo completo: [behavioral/strategy/](behavioral/strategy/README.md)

### Template Method

**Regla:** si **varias clases repiten la misma secuencia de pasos**, escribí
la secuencia una vez en la base y dejá que las subclases completen los
pasos.

**Señales:**

- Métodos hermanos con el mismo esqueleto y nombres distintos, como
  `IOSCompiler.build()` y `AndroidCompiler.compile_and_run()` en
  `compiler_before_template_method.py`.
- Nada impide saltear un paso o cambiar el orden.

**Plantilla:**

La versión de compiladores de `compiler_with_template_method.py` (la de
viajes, `travel_agency_with_template_method.py`, sigue la misma forma):

```python
import io

from abc import ABC, abstractmethod
from contextlib import redirect_stdout
from typing import final


class Compiler(ABC):
    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        if "compile_and_run" in vars(cls):  # @final solo lo revisa mypy
            raise TypeError(
                f"{cls.__name__} must not override Compiler.compile_and_run()"
            )

    @final
    def compile_and_run(self) -> None:
        self.collect_source()
        self.compile_to_object()
        self.optimize()
        self.run()

    @abstractmethod
    def collect_source(self) -> None: ...

    @abstractmethod
    def compile_to_object(self) -> None: ...

    def optimize(self) -> None:  # hook: vacío por defecto
        return

    @abstractmethod
    def run(self) -> None: ...


class IOSCompiler(Compiler):
    def collect_source(self) -> None:
        print("Collecting Swift source code")

    def compile_to_object(self) -> None:
        print("Compiling Swift code to LLVM bitcode")

    def run(self) -> None:
        print("Program running on the iOS runtime")


class AndroidCompiler(Compiler):
    def collect_source(self) -> None:
        print("Collecting Kotlin source code")

    def compile_to_object(self) -> None:
        print("Compiling Kotlin code to DEX bytecode")

    def optimize(self) -> None:
        print("Shrinking DEX bytecode")

    def run(self) -> None:
        print("Program running on the Android runtime")


def test_only_android_overrides_the_hook() -> None:
    output = io.StringIO()
    with redirect_stdout(output):
        IOSCompiler().compile_and_run()
        AndroidCompiler().compile_and_run()
    assert output.getvalue().count("Shrinking DEX bytecode") == 1
```

**Precaución:** el esqueleto queda fijo por herencia. Si lo que varía es el
algoritmo entero, usá Strategy.

Ejemplo completo: [behavioral/template_method/](behavioral/template_method/README.md)

---

## Lista de revisión para code review

- [ ] **Necesidad**: ¿la señal del patrón aparece de verdad en el código, o
      es una variación hipotética?
- [ ] **Creación**: ¿el cliente evita instanciar clases concretas? ¿Las
      claves desconocidas dan un error claro o un Null Object?
- [ ] **Abstracciones**: ¿los roles del patrón son `ABC` con
      `@abstractmethod` (o `Protocol` cuando corresponde), y las
      dependencias llegan tipadas con ellas?
- [ ] **Estado compartido**: ¿los objetos compartidos (flyweights,
      singletons, prototipos superficiales) son inmutables o se copian bien?
- [ ] **Reglas perdidas**: ¿las combinaciones que antes garantizaba la
      jerarquía (Decorator) se validan ahora en tiempo de ejecución?
- [ ] **Invariantes**: ¿los template methods y las secuencias de un
      director están protegidos contra cambios de orden?
- [ ] **Equilibrio**: ¿cada clase nueva resuelve algo, o es complejidad
      especulativa?

## Glosario

| Término | Definición |
| --- | --- |
| Creacional / estructural / de comportamiento | Las tres familias del catálogo GoF: cómo se crean los objetos, cómo se componen y cómo reparten responsabilidades. |
| Rol | La función que cumple una clase dentro de un patrón (Product, Component, Strategy...). Cada clase de un ejemplo "con" la declara en su docstring. |
| Null Object | Un objeto que cumple la interfaz sin hacer nada, para no tener que preguntar por `None` (`NullCar`, `NullPerson`). |
| Estado intrínseco / extrínseco | En Flyweight: la parte compartible e inmutable (`ParticleType`) / la parte propia de cada uso (`Event`). |
| Hook | Paso opcional de un template method con una implementación vacía por defecto (`optimize`, `optional_excursion`). |
| Modelo pull / push | En Observer: el observer consulta los datos / el subject se los envía. Los ejemplos usan pull. |
| Composition root | El único punto de la aplicación donde se crean y conectan los objetos concretos (`client()` en cada ejemplo). |
