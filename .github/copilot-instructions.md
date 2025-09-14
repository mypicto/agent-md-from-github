# Instructions for the Agent

## Core Design Principles

* **Robert C. Martin's Single Responsibility Principle (SRP)**: A class or method should have responsibility toward only one actor.
* **Robert C. Martin's Open/Closed Principle (OCP)**: Software entities should be open for extension but closed for modification.
* **Andy Hunt and Dave Thomas' Don't Repeat Yourself (DRY)**: Eliminate duplication of knowledge or logic.
* **Jerry Weinberg's Principle of Least Astonishment**: Interfaces should behave in a predictable and intuitive way.
* **Ian Holland's Law of Demeter (LoD)**: Minimize dependencies by interacting only with closely related objects.
* **Kelly Johnson's KISS Principle (KISS)**: Keep the design simple and clear.

## Class Design

* As Martin Fowler suggests with the Humble Object Pattern, separate testable business logic from infrastructure.
* Prefer object composition over inheritance to encourage flexibility and reduce coupling.

## Method Design

* As Erich Gamma and the other GoF authors recommend, replace duplicated switch statements or conditional branches with the Strategy Pattern or Factory Pattern.
* Following Robert C. Martin's guidance, use exceptions for error handling instead of return codes.
* As advocated in Clean Code, prefer early returns to reduce nesting and improve readability.
* A method should perform only the single task implied by its name.
* When throwing exceptions, always set messages that are helpful for debugging and analysis.

## Naming Conventions

* As Robert C. Martin emphasizes in *Clean Code*, base names on purpose, not behavior.
* Avoid abbreviations and always use complete words.
* As Martin Fowler recommends, when multiple variations of an object or method exist, use contrasting and descriptive names to make the differences clear.

## Commenting

* As Kent Beck and Martin Fowler note, remove redundant comments that merely restate the code itself.
* As Martin Fowler advises in *Refactoring*, don't hide poor readability with comments—extract logic and give it meaningful names.

## Testing

* Test method names should be in Japanese and follow the format MethodName_StateUnderTest_ExpectedBehavior.

## Code Review

* Be mindful of whether readability can be improved through better naming.
* Infer the purpose and intent of logic to consider whether the methods or classes bearing that responsibility are truly correct.
* Warn about fields that may be referenced while uninitialized.
* Warn about potential memory leaks.
* When proposing improvements, allow interface and structural changes only for the objects under review and new objects.

## Project Architecture Overview

This project follows the **Clean Architecture** principles, inspired by Robert C. Martin's guidelines, to ensure separation of concerns, testability, and maintainability. The architecture is divided into four main layers, each with specific responsibilities. New team members should familiarize themselves with this structure to contribute effectively.

### Layer Structure

1. **Domain Layer** (`src/domain/`):
   - Contains the core business logic, entities, value objects, and interfaces.
   - Examples: `DateRange`, `PullRequestMetadata`, `RepositoryIdentifier`, and interfaces like `GitHubRepositoryInterface`.
   - This layer is independent of external frameworks and should not depend on other layers.
   - **Responsibilities**: Define business rules, data structures, and contracts (interfaces) for external dependencies.

2. **Application Layer** (`src/application/`):
   - Contains use cases and application services that orchestrate domain objects.
   - Examples: Services for PR review collection, exceptions handling.
   - **Responsibilities**: Implement business workflows, handle application-specific logic, and coordinate between domain and infrastructure layers.

3. **Infrastructure Layer** (`src/infrastructure/`):
   - Contains implementations of interfaces defined in the domain layer.
   - Examples: `FileSystemOutputWriter`, `JsonOutputFormatter`, repository implementations.
   - **Responsibilities**: Handle external concerns like file I/O, API calls, databases, and third-party services.

4. **Presentation Layer** (`src/presentation/`):
   - Contains controllers and UI-related code.
   - Examples: `AuthController`, `FetchController`.
   - **Responsibilities**: Handle user input, format output, and interact with the application layer.

### Dependency Direction

- Dependencies flow inward: Presentation → Application → Domain ← Infrastructure.
- The Domain layer defines interfaces that Infrastructure implements (Dependency Inversion Principle).
- No layer should depend on layers outward; use dependency injection for cross-layer communication.

### Testing Structure

- Tests are organized mirroring the source structure: `test/domain/`, `test/application/`, `test/infrastructure/`, `test/presentation/`.

### Guidelines for New Team Members

- **Start with Domain**: When adding new features, begin by defining domain entities and interfaces. This ensures the core logic is solid and testable.
- **Respect Layer Boundaries**: Do not introduce dependencies that violate the layer structure. For example, avoid importing infrastructure code directly into domain classes.
- **Use Interfaces**: Always define interfaces in the domain layer for external dependencies, and implement them in infrastructure.
- **Dependency Injection**: Use dependency injection (e.g., via `ServiceFactory`) to provide implementations to higher layers.
- **Keep It Simple**: Follow KISS and DRY principles; avoid over-engineering.
- **Test Early**: Write tests alongside code, especially for domain logic, to validate behavior.
- **Code Reviews**: Pay attention to whether new code adheres to the architecture and principles outlined here.

