"""Protect employee personal data with a proxy in front of the directory.

Pattern: Proxy (structural).
Counterpart: ``employee_access_before_proxy.py``.

Notes
-----
Why:
    - ``Employees`` only fetches records; ``EmployeesProxy`` only
      enforces the privacy rule. Each has a single responsibility.
    - The proxy implements the same ``AbsEmployees`` interface as the
      real subject, so clients cannot tell them apart and cannot
      bypass the check by accident.
    - The rule is identical to the counterpart file: only requesters
      with ``can_see_personal`` see birthdates and salaries; anyone
      else sees ids and names only, including for their own record.

When to use:
    - Protection proxy: control access to an object based on who asks.
    - Virtual proxy: delay creating an expensive object until needed.
    - Remote proxy: represent an object that lives elsewhere.
    - Smart reference: add logging, caching or reference counting
      around an object without changing it.

Trade-offs:
    - One more level of indirection for every call.
    - The proxy must track the subject's interface; every new method
      has to be forwarded.

Related:
    - Decorator has the same structure but adds behavior; a proxy
      controls access to the subject.
    - Adapter changes the interface; a proxy keeps it identical.

Roles::

    client ---> AbsEmployees (Subject)
                  ^                 ^
                  |                 |
        EmployeesProxy (Proxy) --> Employees (RealSubject)
              |
              v
        AccessControlList (permissions consulted by the proxy)
"""

from abc import ABC, abstractmethod
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, replace
from datetime import date
from typing import Protocol


@dataclass(frozen=True)
class Employee:
    """Employee record as stored in the database; salary in US cents.

    Role in the pattern: data owned by the RealSubject.
    """

    empid: int
    name: str
    birthdate: date
    salary: int


@dataclass(frozen=True)
class EmployeeInfo:
    """Employee data returned to clients.

    Personal fields are ``None`` when the requester may not see them.

    Role in the pattern: result type shared by Subject implementations.
    """

    empid: int
    name: str
    birthdate: date | None = None
    salary: int | None = None


@dataclass(frozen=True)
class AccessControl:
    """Permission record for one requester.

    Role in the pattern: data consulted by the Proxy.
    """

    empid: int
    can_see_personal: bool


class AccessPolicy(Protocol):
    """Question the proxy asks about a requester's permissions.

    The proxy depends on this question, not on how the answer is stored,
    so any policy (a list, a database, a role check) can be plugged in.

    Role in the pattern: collaborator interface of the Proxy.
    """

    def can_see_personal(self, requester_id: int) -> bool:
        """Return whether ``requester_id`` may see personal data."""
        ...


class AccessControlList:
    """Answer permission questions from a set of access records.

    Role in the pattern: collaborator of the Proxy; keeps the policy
    lookup out of both the proxy and the real subject.
    """

    def __init__(self, controls: Mapping[int, AccessControl]) -> None:
        """Copy the access records, keyed by requester id.

        Parameters
        ----------
        controls : Mapping of int to AccessControl
            Permission record of each requester.
        """
        self._controls = dict(controls)

    def can_see_personal(self, requester_id: int) -> bool:
        """Return whether ``requester_id`` may see personal data."""
        control = self._controls.get(requester_id)
        return control is not None and control.can_see_personal


class AbsEmployees(ABC):
    """Interface shared by the real directory and its proxy.

    Contract: ``empid`` and ``name`` are always set; ``birthdate`` and
    ``salary`` may be ``None`` when the requester is not allowed to see
    them. Callers must handle that case.

    Role in the pattern: Subject.
    """

    @abstractmethod
    def get_employee_info(self, empids: Iterable[int]) -> list[EmployeeInfo]:
        """Return information for the known employees in ``empids``.

        Parameters
        ----------
        empids : Iterable of int
            Ids to look up; unknown ids are skipped.

        Returns
        -------
        list of EmployeeInfo
            One entry per known employee, in request order. Personal
            fields may be ``None``; see the class contract.
        """


class Employees(AbsEmployees):
    """Directory that returns full employee records.

    Role in the pattern: RealSubject.
    """

    def __init__(self, records: Mapping[int, Employee]) -> None:
        """Copy the employee records, keyed by employee id.

        Parameters
        ----------
        records : Mapping of int to Employee
            Every employee record.
        """
        self._records = dict(records)

    def get_employee_info(self, empids: Iterable[int]) -> list[EmployeeInfo]:
        """Return each known employee's full record, personal data included."""
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
    """Directory wrapper that hides personal data from unauthorised users.

    Role in the pattern: Proxy (protection proxy).
    """

    def __init__(
        self,
        employees: AbsEmployees,
        access: AccessPolicy,
        requester_id: int,
    ) -> None:
        """Put the access check in front of ``employees`` for one requester.

        Parameters
        ----------
        employees : AbsEmployees
            Real subject (or another proxy) to delegate to.
        access : AccessPolicy
            Permissions consulted on every request.
        requester_id : int
            Employee on whose behalf the data is requested.
        """
        self._employees = employees
        self._access = access
        self._requester_id = requester_id

    def get_employee_info(self, empids: Iterable[int]) -> list[EmployeeInfo]:
        """Return the records, hiding personal data unless allowed."""
        infos = self._employees.get_employee_info(empids)
        if self._access.can_see_personal(self._requester_id):
            return infos
        return [replace(info, birthdate=None, salary=None) for info in infos]


def format_employee(info: EmployeeInfo) -> str:
    """Return one description line, showing only the visible fields."""
    details = f"Employee Id: {info.empid}, Name: {info.name}"
    if info.birthdate is not None and info.salary is not None:
        details += (
            f", Birthdate: {info.birthdate.isoformat()}"
            f", Salary: {format_cents(info.salary)}"
        )
    return details


def format_cents(cents: int) -> str:
    """Return ``cents`` formatted as dollars, for example ``$5.20``."""
    return f"${cents // 100}.{cents % 100:02d}"


def sample_employees() -> dict[int, Employee]:
    """Return the demo employee records, keyed by id."""
    records = (
        Employee(1, "Bob", date(1994, 7, 4), 8_000_000),
        Employee(2, "Carol", date(1992, 5, 28), 8_500_000),
        Employee(3, "Ted", date(1988, 2, 18), 5_500_000),
        Employee(4, "Alice", date(1987, 11, 25), 4_000_000),
        Employee(101, "Morgan the Manager", date(1975, 3, 14), 10_000_000),
    )
    return {record.empid: record for record in records}


def sample_access() -> AccessControlList:
    """Return the demo permissions: only the manager has access."""
    return AccessControlList({101: AccessControl(101, can_see_personal=True)})


def client() -> None:
    """List employees for an ordinary employee and for the manager."""
    directory = Employees(sample_employees())
    access = sample_access()

    print("Requester 3 is an ordinary employee:")
    ordinary = EmployeesProxy(directory, access, requester_id=3)
    for info in ordinary.get_employee_info([3, 4]):
        print(format_employee(info))

    print("Requester 101 may see personal data:")
    manager = EmployeesProxy(directory, access, requester_id=101)
    for info in manager.get_employee_info([1, 2, 5]):
        print(format_employee(info))


if __name__ == "__main__":
    client()
