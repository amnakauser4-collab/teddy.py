# Smart Electricity Usage Monitor - AI Agent Instructions

## Project Overview
This is a standalone Python script for personal electricity usage tracking and bill estimation. The application maintains daily usage data and calculates bills based on tiered tariff rates.

## Architecture
- **Single-file design**: All functionality in `# Smart Electricity Usage Monitor.py`
- **Global state**: `daily_usage` list stores float values, `TARIFF` tuple contains rates
- **Modular functions**: Separate functions for input, calculations, and output
- **CLI interface**: Menu-driven loop for user interaction

## Key Patterns
- **Configuration**: Use tuples for immutable data like `TARIFF = (10, 15)` (Rs per unit)
- **Data storage**: Lists for accumulating daily usage values
- **Bill calculation**: Tiered pricing - first 100 units × TARIFF[0], remainder × TARIFF[1]
- **Alerts**: Warn when total usage exceeds 200 units
- **Input handling**: Direct `float(input())` conversion (no validation)

## Development Workflow
- **Execution**: Run with `python "# Smart Electricity Usage Monitor.py"`
- **No dependencies**: Pure Python standard library
- **No build/test process**: Direct script execution
- **Debugging**: Print statements for output, no logging framework

## Code Conventions
- **Naming**: snake_case functions (`calculate_total_units`, `show_report`)
- **Data structures**: Tuples for fixed config, lists for dynamic data
- **Error handling**: Minimal - assumes valid numeric input
- **Output**: Simple print statements with formatted strings
- **Menu system**: String comparison for choices ('1', '2', '3')

## Examples
- Adding usage: `daily_usage.append(float(input("Enter today's electricity usage (units): ")))`
- Bill logic: `if total_units <= 100: bill = total_units * TARIFF[0] else: bill = 100 * TARIFF[0] + (total_units - 100) * TARIFF[1]`
- Report display: Print summary with conditional alerts

## Integration Points
- None - standalone script
- No external APIs, databases, or file I/O beyond console