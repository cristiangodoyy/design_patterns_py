# Graph Report - design_patterns_py  (2026-10-22)

## Corpus Check
- 85 files · ~53,464 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: .graphify-bak 1, (none) 1, .lock 1)

## Summary
- 1909 nodes · 2547 edges · 124 communities (59 shown, 65 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 44 edges (avg confidence: 0.83)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Subscription Bridge Solution
- Car Factory Method
- Subscription Discount Problem
- Pizza Decorator Problem
- Car Simple Factory
- Composite Family Tree
- Schedule Server Facade Solution
- Employee Access Proxy
- Car Abstract Factory Problem
- Computer State Problem
- AST Module Structure
- Computer Registry Prototype
- Schedule Server Facade Problem
- Compiler Template Method
- Subscription Bridge Problem
- Customer Object Adapter
- Shipping Strategy Solution
- Computer State Machine
- Car Factory Problem
- Shallow Copy Prototype
- Car Decorator Problem
- Deep Copy Prototype
- Shipping Cost Problem
- Computer Builder Problem
- Customer Class Adapter
- Monostate Logger Singleton
- Metaclass Singleton Logger
- Base Class Singleton
- Pattern Guide Catalogue
- Car Abstract Factory Solution
- Encapsulated Builder Problem
- Family Composite Problem
- Logger Singleton Problem
- Employee Access Problem
- Project Docs and Rules
- KPI Dashboard Observer Problem
- Classic Lazy Singleton
- Singleton Concepts
- Pizza Decorator Solution
- Car Trim Classes
- Collider Flyweight Problem
- Flyweight Factory
- KPI Dashboard Observer Solution
- Computer Power State
- Venice Trip Template
- Computer Builder Solution
- Car Decorator Solution
- Computer State Classes
- Compiler Template Problem
- Venice Trip Package
- Car Abstract Factory Base
- Computer Factory Method
- Pizza Decorator Toppings
- CodeSight Context Docs
- Computer Prototype Problem
- Customer Adapter Entities
- KPI Display Observers
- KPI Observer Subjects
- Computer Long Constructor
- Computer Public Attributes
- Computer Builder Director
- HP Builder
- Car Decorator Base
- Pizza Decorator Wrappers
- Collider Event Physics
- KPI Source Metrics
- Travel Template Problem
- Customer Adapter Problem
- Lenovo Builder
- KPI Observer Base
- KPI Classes
- Power State Problem
- Off State
- Hibernated State
- Sleeping State
- Testing Rules
- Cadillac Factory
- Chevy Spark Factory
- Ford Fiesta Factory
- Lincoln Factory
- Ford Mustang Factory
- Prototype Clone Notes
- Logger Records
- Black Pizza Decorator
- Vegan Pizza Base
- Event Kinematics
- Employee Adapter Solution
- Option Categories
- Non-Vegan Pizza
- Facade Pattern Notes
- Collider Flyweight Solution
- Forecast KPIs
- Powered On State
- Trip Template Notes
- Docs Sync Hook
- Car Factory Registry
- Repository Guidelines
- Economy Trim
- Inline Four Engine
- Leather Upholstery
- Luxury Trim
- Sport Trim
- Ferrari Red Paint
- V6 Engine
- Vinyl Upholstery
- Shipping Strategy Classes
- Computer Builder Classes
- Car Factory Method Classes
- Person Composite Classes
- Employee Proxy Classes
- Extra Cheese Decorator
- KPI Enum Names
- Subscription Bridge Classes
- Car Decorator Components
- Null Object Notes
- Pizza Decorator Classes
- Repository Root

## God Nodes (most connected - your core abstractions)
1. `AbsCar` - 22 edges
2. `ComputerState` - 21 edges
3. `PATTERNS.md (prescriptive pattern guide)` - 21 edges
4. `AbsAuto` - 15 edges
5. `Trip` - 14 edges
6. `AbsDecorator` - 14 edges
7. `AbsBuilder` - 13 edges
8. `Subscription` - 13 edges
9. `AbsCar` - 13 edges
10. `make_car()` - 12 edges

## Surprising Connections (you probably didn't know these)
- `codesight middleware section` --conceptually_related_to--> `Strategy`  [INFERRED]
  .codesight/middleware.md → PATTERNS.md
- `FlyweightFactory (cache by key)` --semantically_similar_to--> `Singleton pattern`  [INFERRED] [semantically similar]
  structural/flyweight/README.md → creational/singleton/README.md
- `Design-pattern example rules` --shares_data_with--> `General conventions (ABC roles, dataclasses, int cents)`  [INFERRED]
  .claude/python.md → PATTERNS.md
- `Repository assumptions` --conceptually_related_to--> `Design-pattern example rules`  [INFERRED]
  CLAUDE.md → .claude/python.md
- `codesight libraries inventory` --shares_data_with--> `Repository map tables`  [INFERRED]
  .codesight/libs.md → README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **GoF pattern catalogue** — patterns_abstract_factory, patterns_builder, patterns_factory_method, patterns_prototype, patterns_singleton, patterns_adapter, patterns_bridge, patterns_composite, patterns_decorator, patterns_facade, patterns_flyweight, patterns_proxy, patterns_observer, patterns_state, patterns_strategy, patterns_template_method [EXTRACTED 1.00]
- **Docs-in-sync feedback loop** — claude, claude_test_docs_sync_hook, tests_unit_test_docs_in_sync, readme, patterns [EXTRACTED 1.00]
- **Validation command set** — claude_validation_commands, claude_testing_validation_ladder, readme_tests_section, claude_python_runtime_tooling [INFERRED 0.75]
- **Observer dashboard participants** — behavioral_observer_readme_subject, behavioral_observer_readme_observer, behavioral_observer_readme_kpiobserver, behavioral_observer_readme_kpis, behavioral_observer_readme_kpisource, behavioral_observer_readme_currentkpis, behavioral_observer_readme_forecastkpis [EXTRACTED 1.00]
- **Computer power state machine** — behavioral_state_readme_computer_context, behavioral_state_readme_computerstate, behavioral_state_readme_off, behavioral_state_readme_on, behavioral_state_readme_suspended, behavioral_state_readme_hibernated [EXTRACTED 1.00]

## Communities (124 total, 65 thin omitted)

### Community 0 - "Subscription Bridge Solution"
Cohesion: 0.05
Nodes (11): add_months(), Annual, client(), CorporateDiscount, describe(), Discount, format_cents(), Monthly (+3 more)

### Community 1 - "Car Factory Method"
Cohesion: 0.06
Nodes (10): AbsAuto, AbsFactory, ChevyFactory, ChevyVolt, client(), FordFactory, FordFusion, JeepFactory (+2 more)

### Community 2 - "Subscription Discount Problem"
Cohesion: 0.06
Nodes (11): add_months(), Annual, AnnualCorporate, AnnualStudent, client(), describe(), format_cents(), Monthly (+3 more)

### Community 3 - "Pizza Decorator Problem"
Cohesion: 0.06
Nodes (10): AbsPizza, client(), describe(), format_cents(), NonVeganPizza, NonVeganPizzaWithChicken, NonVeganPizzaWithChickenAndTomatoes, NonVeganPizzaWithTomatoes (+2 more)

### Community 4 - "Car Simple Factory"
Cohesion: 0.05
Nodes (8): AbsAuto, AutoFactory, ChevyVolt, client(), default_auto_factory(), FordFusion, JeepSahara, NullCar

### Community 5 - "Composite Family Tree"
Cohesion: 0.06
Nodes (7): age_on(), client(), Component, Individual, NullPerson, Person, Tree

### Community 6 - "Schedule Server Facade Solution"
Cohesion: 0.06
Nodes (7): Bootloader, client(), ExecutionContext, ListenerRegistry, ProcessManager, ScheduleServerFacade, SystemObjects

### Community 7 - "Employee Access Proxy"
Cohesion: 0.06
Nodes (13): AbsEmployees, AccessControl, AccessControlList, AccessPolicy, client(), Employee, EmployeeInfo, Employees (+5 more)

### Community 8 - "Car Abstract Factory Problem"
Cohesion: 0.05
Nodes (10): CadillacCTS, ChevyCamaro, ChevySpark, client(), Edition, FordFiesta, FordMustang, LincolnMKS (+2 more)

### Community 9 - "Computer State Problem"
Cohesion: 0.06
Nodes (9): client(), Computer, InvalidTransitionError, PowerStatus, client(), MaldivesTrip, TravelAgency, TripKind (+1 more)

### Community 10 - "AST Module Structure"
Cohesion: 0.11
Nodes (22): Tests and validation section, _member_names(), _module_definitions(), _module_docstring(), _patterns_sections(), _public_classes(), _python_blocks(), _read() (+14 more)

### Community 11 - "Computer Registry Prototype"
Cohesion: 0.07
Nodes (8): AbsComputer, AbsPrototype, client(), Laptop, MainBoard, PrototypeManager, _spec_sheet(), Tower

### Community 12 - "Schedule Server Facade Problem"
Cohesion: 0.06
Nodes (6): Bootloader, client(), ExecutionContext, ListenerRegistry, ProcessManager, SystemObjects

### Community 13 - "Compiler Template Method"
Cohesion: 0.07
Nodes (4): AndroidCompiler, client(), Compiler, IOSCompiler

### Community 14 - "Subscription Bridge Problem"
Cohesion: 0.08
Nodes (7): add_months(), Annual, client(), describe(), format_cents(), Monthly, Subscription

### Community 15 - "Customer Object Adapter"
Cohesion: 0.06
Nodes (8): Addressable, client(), Customer, describe(), Employee, EmployeeAdapter, Vendor, VendorAdapter

### Community 16 - "Shipping Strategy Solution"
Cohesion: 0.09
Nodes (8): AbsStrategy, client(), FedExStrategy, format_cents(), Order, PostalStrategy, ShippingCost, UPSStrategy

### Community 17 - "Computer State Machine"
Cohesion: 0.07
Nodes (16): Computer (context), ComputerState (abstract state), Hibernated state, InvalidTransitionError, Off state, On state, Suspended state, Shipper enum if-chain (before version) (+8 more)

### Community 18 - "Car Factory Problem"
Cohesion: 0.07
Nodes (6): ChevyVolt, client(), FordFusion, get_car(), JeepSahara, NullCar

### Community 19 - "Shallow Copy Prototype"
Cohesion: 0.09
Nodes (7): AbsComputer, AbsPrototype, client(), Laptop, MainBoard, _spec_sheet(), Tower

### Community 20 - "Car Decorator Problem"
Cohesion: 0.09
Nodes (7): AbsCar, client(), describe(), Economy, format_cents(), Luxury, Sport

### Community 21 - "Deep Copy Prototype"
Cohesion: 0.09
Nodes (7): AbsComputer, AbsPrototype, client(), Laptop, MainBoard, _spec_sheet(), Tower

### Community 22 - "Shipping Cost Problem"
Cohesion: 0.11
Nodes (5): client(), format_cents(), Order, Shipper, ShippingCost

### Community 23 - "Computer Builder Problem"
Cohesion: 0.10
Nodes (3): client(), Computer, MyComputerBuilder

### Community 24 - "Customer Class Adapter"
Cohesion: 0.11
Nodes (6): Addressable, client(), Customer, describe(), Vendor, VendorAdapter

### Community 25 - "Monostate Logger Singleton"
Cohesion: 0.11
Nodes (4): AuditLogger, Borg, client(), Logger

### Community 26 - "Metaclass Singleton Logger"
Cohesion: 0.11
Nodes (3): client(), Logger, SingletonMeta

### Community 27 - "Base Class Singleton"
Cohesion: 0.13
Nodes (4): AuditLogger, client(), Logger, Singleton

### Community 29 - "Car Abstract Factory Solution"
Cohesion: 0.16
Nodes (7): AbsFactory, client(), drive_lineup(), factory_for(), FordFactory, GeneralMotorsFactory, Maker

### Community 30 - "Encapsulated Builder Problem"
Cohesion: 0.14
Nodes (3): client(), Computer, MyComputerBuilder

### Community 31 - "Family Composite Problem"
Cohesion: 0.16
Nodes (5): age_on(), client(), Family, find_oldest(), Person

### Community 32 - "Logger Singleton Problem"
Cohesion: 0.17
Nodes (4): charge_card(), client(), create_order(), Logger

### Community 33 - "Employee Access Problem"
Cohesion: 0.19
Nodes (7): AccessControl, client(), Employee, employee_details(), format_cents(), sample_access(), sample_employees()

### Community 34 - "Project Docs and Rules"
Cohesion: 0.16
Nodes (12): AGENTS.md (project context and graphify rules), graphify usage rules, CLAUDE.md (project instructions), Project context section, Python rules (.claude/python.md), NumPyDoc docstring conventions, StrEnum conventions, Pydantic v2 rules (overridden for examples) (+4 more)

### Community 35 - "KPI Dashboard Observer Problem"
Cohesion: 0.20
Nodes (3): client(), Dashboard, KPI

### Community 37 - "Singleton Concepts"
Cohesion: 0.13
Nodes (8): Singleton base class (one instance per subclass), Borg monostate (shared __dict__), Classic __new__ singleton (Logger), LazyLogger instance() singleton, SingletonMeta metaclass, Event (extrinsic state with __slots__), FlyweightFactory (cache by key), ParticleType (frozen intrinsic state)

### Community 38 - "Pizza Decorator Solution"
Cohesion: 0.16
Nodes (3): AbsPizza, describe(), format_cents()

### Community 40 - "Collider Flyweight Problem"
Cohesion: 0.20
Nodes (5): client(), generate_events(), parse_event(), raw_record(), total_size()

### Community 41 - "Flyweight Factory"
Cohesion: 0.20
Nodes (4): client(), FlyweightFactory, generate_events(), parse_event()

### Community 46 - "Car Decorator Solution"
Cohesion: 0.19
Nodes (3): AbsCar, describe(), format_cents()

### Community 48 - "Compiler Template Problem"
Cohesion: 0.20
Nodes (3): AndroidCompiler, client(), IOSCompiler

### Community 54 - "CodeSight Context Docs"
Cohesion: 0.22
Nodes (11): CODESIGHT AI context map, codesight config section, codesight test coverage section, codesight libraries inventory, codesight middleware section, codesight wiki index, codesight wiki libraries article, codesight wiki scan log (+3 more)

### Community 55 - "Computer Prototype Problem"
Cohesion: 0.22
Nodes (3): client(), MainBoard, Tower

### Community 56 - "Customer Adapter Entities"
Cohesion: 0.20
Nodes (4): client(), Customer, describe(), Vendor

### Community 58 - "KPI Observer Subjects"
Cohesion: 0.24
Nodes (7): CurrentKPIs, ForecastKPIs, KPIObserver base, KPIs (concrete subject), KPISource protocol, Observer, Subject

### Community 70 - "Customer Adapter Problem"
Cohesion: 0.28
Nodes (3): client(), Customer, describe()

### Community 78 - "Testing Rules"
Cohesion: 0.29
Nodes (7): Testing and validation rules (.claude/testing.md), Test failure reporting format, LLM and agent test separation, Pytest markers policy, Test impact policy, Given-when-then test naming, Arrange-Act-Assert test structure

### Community 84 - "Prototype Clone Notes"
Cohesion: 0.29
Nodes (3): clone() returning Self, PrototypeManager registry, Tower (concrete prototype)

### Community 89 - "Employee Adapter Solution"
Cohesion: 0.38
Nodes (7): Addressable (target protocol), describe() single loop over Addressable, Employee (adaptee), EmployeeAdapter, Vendor (adaptee), VendorAdapter (class adapter via inheritance), VendorAdapter (object adapter via composition)

### Community 92 - "Facade Pattern Notes"
Cohesion: 0.29
Nodes (3): Client repeats boot and shutdown sequence (before version), ScheduleServerFacade, Server subsystem classes (Bootloader, ExecutionContext, ListenerRegistry, SystemObjects, ProcessManager)

### Community 98 - "Car Factory Registry"
Cohesion: 0.33
Nodes (6): AbsCar (product interface), AbsFactory, drive_lineup client, factory_for runtime registry, FordFactory, GeneralMotorsFactory

### Community 99 - "Repository Guidelines"
Cohesion: 0.33
Nodes (5): Code review checklist, README.md (repository map), Before/with file naming scheme, Running the examples as modules, Three pattern families

### Community 109 - "Shipping Strategy Classes"
Cohesion: 0.40
Nodes (5): AbsStrategy, FedExStrategy, PostalStrategy, ShippingCost (context), UPSStrategy

### Community 110 - "Computer Builder Classes"
Cohesion: 0.50
Nodes (5): AbsBuilder, Computer (product), Director, HPBuilder, LenovoBuilder

### Community 111 - "Car Factory Method Classes"
Cohesion: 0.50
Nodes (5): AbsAuto product interface, AbsFactory (factory method creator), AutoFactory, ChevyFactory, FordFactory and JeepFactory, NullCar (Null Object)

### Community 112 - "Person Composite Classes"
Cohesion: 0.40
Nodes (5): Component (common interface), Individual (leaf contract with birthdate), NullPerson (null object for empty tree), Person (leaf), Tree (composite)

### Community 113 - "Employee Proxy Classes"
Cohesion: 0.40
Nodes (5): AbsEmployees (subject interface), AccessControlList, AccessPolicy protocol, EmployeesProxy, Employees (real subject)

### Community 118 - "Subscription Bridge Classes"
Cohesion: 0.67
Nodes (3): NoDiscount, StudentDiscount and CorporateDiscount, Discount (implementor), Subscription (abstraction)

### Community 119 - "Car Decorator Components"
Cohesion: 0.67
Nodes (3): AbsCar (component), AbsDecorator base, OptionCategory (one option per category)

## Knowledge Gaps
- **59 isolated node(s):** `design-patterns-py`, `codesight test coverage section`, `codesight wiki scan log`, `pyproject.toml`, `StrEnum conventions` (+54 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 932 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **65 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CLAUDE.md (project instructions)` connect `Project Docs and Rules` to `AST Module Structure`, `Repository Guidelines`, `Pattern Guide Catalogue`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **What connects `design-patterns-py`, `codesight test coverage section`, `codesight wiki scan log` to the rest of the system?**
  _59 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Subscription Bridge Solution` be split into smaller, more focused modules?**
  _Cohesion score 0.05194805194805195 - nodes in this community are weakly interconnected._
- **Why does `Tests and validation section` connect `AST Module Structure` to `Repository Guidelines`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Should `Car Factory Method` be split into smaller, more focused modules?**
  _Cohesion score 0.05587808417997097 - nodes in this community are weakly interconnected._
- **Why does `README.md (repository map)` connect `Repository Guidelines` to `Project Docs and Rules`, `AST Module Structure`, `Pattern Guide Catalogue`, `CodeSight Context Docs`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Should `Subscription Discount Problem` be split into smaller, more focused modules?**
  _Cohesion score 0.05580693815987934 - nodes in this community are weakly interconnected._