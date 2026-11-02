"""Print employee details with the access check mixed into the lookup.

Pattern: Proxy (structural), problem side.
Counterpart: ``employee_access_with_proxy.py``.

Notes
-----
Scenario:
    An HR system lists employees. Anyone may see an employee's id and
    name, but only requesters with the ``can_see_personal`` permission
    may see birthdates and salaries. A requester without that
    permission does not see personal data at all, not even their own.

What goes wrong here:
    - ``employee_details`` both fetches records and enforces the
      privacy rule, so two responsibilities share one function.
    - Every other piece of code that reads employees must remember to
      repeat the same check; forgetting it leaks salaries.
    - The rule cannot be changed, logged or tested on its own, and the
      data source cannot be swapped without touching the access code.

Roles::

    client ---> employee_details(employees, access, ids, requester)
                  lookup record
                  if requester may see personal data -> add salary
"""

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Employee:
    """Employee record as stored in the database; salary in US cents."""

    empid: int
    name: str
    birthdate: date
    salary: int


@dataclass(frozen=True)
class AccessControl:
    """Permission record for one requester."""

    empid: int
    can_see_personal: bool


def employee_details(
    employees: Mapping[int, Employee],
    access: Mapping[int, AccessControl],
    empids: Iterable[int],
    requester_id: int,
) -> list[str]:
    """Return one description line per known employee.

    Unknown ids are skipped. Personal data is included only when the
    requester has an access record with ``can_see_personal`` set.

    Parameters
    ----------
    employees : Mapping of int to Employee
        All employee records, keyed by id.
    access : Mapping of int to AccessControl
        Permission records, keyed by requester id.
    empids : Iterable of int
        Ids of the employees to describe.
    requester_id : int
        Id of the employee asking for the data.

    Returns
    -------
    list of str
        Human-readable details, one line per employee.
    """
    control = access.get(requester_id)
    can_see_personal = control is not None and control.can_see_personal
    lines: list[str] = []
    for empid in empids:
        if empid not in employees:
            continue
        employee = employees[empid]
        details = f"Employee Id: {employee.empid}, Name: {employee.name}"
        if can_see_personal:
            details += (
                f", Birthdate: {employee.birthdate.isoformat()}"
                f", Salary: {format_cents(employee.salary)}"
            )
        lines.append(details)
    return lines


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


def sample_access() -> dict[int, AccessControl]:
    """Return the demo permission records: only the manager has access."""
    return {101: AccessControl(101, can_see_personal=True)}


def client() -> None:
    """List employees for an ordinary employee and for the manager."""
    employees = sample_employees()
    access = sample_access()

    print("Requester 3 is an ordinary employee:")
    for line in employee_details(employees, access, [3, 4], 3):
        print(line)

    print("Requester 101 may see personal data:")
    for line in employee_details(employees, access, [1, 2, 5], 101):
        print(line)


if __name__ == "__main__":
    client()
