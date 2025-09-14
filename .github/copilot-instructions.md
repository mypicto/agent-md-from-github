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
