# DRY & SOLID Principles Review

Review the current project (or the files specified in $ARGUMENTS) for violations of **DRY** and **SOLID** principles.

## Instructions

1. If `$ARGUMENTS` is provided, review only those specific files or app directories.
2. If no arguments are given, scan all Python files across `core/`, `users/`, `inventory/`, `bookings/`, `payments/`.

For each file reviewed, check the following:

---

### DRY (Don't Repeat Yourself)
- Duplicated logic across views, serializers, or models that could be abstracted
- Copy-pasted validation or queryset filters
- Repeated URL patterns or config values that should be constants
- Similar serializers that could share a base class
- Utility code that exists in multiple places

---

### SOLID Principles

**S — Single Responsibility**
- Classes/functions doing more than one thing
- Views mixing business logic with HTTP handling
- Models containing too much logic (should be thin or delegated to services)

**O — Open/Closed**
- Code that must be modified rather than extended to add new behavior
- Hardcoded conditionals (`if type == 'X'`) instead of polymorphism or strategy patterns

**L — Liskov Substitution**
- Subclasses that override methods in ways that break parent contracts
- Signal handlers or mixins that produce unexpected side effects

**I — Interface Segregation**
- Serializers with too many fields forced on consumers that need only a subset
- ViewSets that expose all actions when only some are needed (missing `http_method_names` or action restrictions)

**D — Dependency Inversion**
- Views or models importing and directly using concrete implementations instead of abstractions
- Hardcoded service calls that can't be swapped or tested in isolation

---

## Output Format

For each violation found:
- **File** and **line number**
- **Principle violated** (e.g., DRY, SRP, OCP)
- **Description** of the issue
- **Suggested fix** with a code snippet where applicable

End with a summary scorecard:
```
DRY:   X issues
SRP:   X issues
OCP:   X issues
LSP:   X issues
ISP:   X issues
DIP:   X issues
```

If no violations are found for a principle, say "No issues found."

Be concise and actionable. Prioritize real issues over theoretical ones.