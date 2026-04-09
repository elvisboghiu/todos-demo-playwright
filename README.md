# TodoMVC Automated Tests

Automated test suite for the [TodoMVC application](https://demo.playwright.dev/todomvc/#/) using Playwright with Python. This project validates core todo management functionality including item creation, completion, deletion, and filtering capabilities.

## Project Overview

This test suite provides comprehensive automated testing for the TodoMVC application with support for:

- **Todo Creation**: Adding todo items with English text, non-English characters (Chinese, Arabic, Emoji), and numeric content
- **Todo Completion**: Marking items as complete and verifying completion status
- **Todo Deletion**: Removing items from the list
- **Filtering**: Active and Completed filter views
- **Character Preservation**: Ensuring special characters and non-English text are handled correctly

The tests are built using:
- **Playwright**: Browser automation framework for reliable end-to-end testing
- **Pytest**: Test framework for organizing and running tests
- **Hypothesis**: Property-based testing library for generating test cases across input domains

## Requirements

### System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Browser**: Chromium (installed automatically by Playwright)

### Python Dependencies

All dependencies are listed in `requirements.txt`:

```
playwright>=1.40.0
pytest>=8.0.0
hypothesis>=6.80.0
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/todomvc-playwright-tests.git
cd todomvc-playwright-tests
```

### 2. Create a Virtual Environment

It's recommended to use a Python virtual environment to isolate project dependencies:

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers

Playwright requires browser binaries to be installed. Run the following command:

```bash
playwright install
```

This will download and install Chromium, Firefox, and WebKit browsers. You can also install specific browsers:

```bash
# Install only Chromium
playwright install chromium

# Install only Firefox
playwright install firefox

# Install only WebKit
playwright install webkit
```

### 5. Verify Installation

To verify that everything is set up correctly, run a quick test:

```bash
pytest tests/test_todo_creation.py::test_add_english_todo -v
```

You should see the test execute and pass.

## Project Structure

```
todomvc-playwright-tests/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── pytest.ini                         # Pytest configuration
├── .gitignore                         # Git ignore rules
├── pages/
│   ├── __init__.py
│   └── todo_page.py                   # Page Object Model for TodoMVC UI
├── tests/
│   ├── test_todo_creation.py          # Tests for adding todos
│   ├── test_todo_completion.py        # Tests for marking todos complete
│   ├── test_todo_deletion.py          # Tests for deleting todos
│   ├── test_todo_filters.py           # Tests for filter functionality
│   ├── test_non_english_characters.py # Tests for non-English character support
│   └── test_numeric_text.py           # Tests for numeric text support
├── utils/
│   ├── __init__.py
│   └── test_data.py                   # Test data generators
└── conftest.py                        # Pytest fixtures and configuration
```

## Test Execution

### Run All Tests

```bash
pytest
```

### Run Tests with Verbose Output

```bash
pytest -v
```

### Run Specific Test File

```bash
pytest tests/test_todo_creation.py
```

### Run Specific Test Function

```bash
pytest tests/test_todo_creation.py::test_add_english_todo
```

### Run Tests by Marker

```bash
# Run only unit tests
pytest -m unit

# Run only property-based tests
pytest -m property

# Run only integration tests
pytest -m integration
```

### Run Tests with Coverage Report

```bash
pytest --cov=pages --cov=utils --cov-report=html
```

This generates an HTML coverage report in the `htmlcov/` directory.

### Run Tests in Parallel

For faster test execution, install pytest-xdist and run:

```bash
pip install pytest-xdist
pytest -n auto
```

## Test Organization

### Unit Tests

Unit tests verify specific examples and edge cases:

- **test_todo_creation.py**: Tests for adding todos with various text types
- **test_todo_completion.py**: Tests for marking todos as complete
- **test_todo_deletion.py**: Tests for deleting todos
- **test_todo_filters.py**: Tests for filter functionality
- **test_non_english_characters.py**: Tests for non-English character support
- **test_numeric_text.py**: Tests for numeric text support

### Property-Based Tests

Property-based tests verify universal properties across many generated inputs using Hypothesis:

- **Property 1**: Todo Creation Adds Item to List
- **Property 2**: Input Field Clears After Addition
- **Property 3**: Completed Items Appear in Completed View
- **Property 4**: Active Filter Shows Only Incomplete Items
- **Property 5**: Completed Filter Shows Only Completed Items
- **Property 6**: Deleted Items Disappear from All Views
- **Property 7**: Character Preservation in Display

Each property test runs a minimum of 100 iterations with randomly generated inputs.

## Page Object Model

The `TodoPage` class in `pages/todo_page.py` encapsulates all interactions with the TodoMVC UI:

### Key Methods

- `add_todo(text)` - Add a new todo item
- `get_todo_items()` - Get all visible todo items
- `mark_todo_complete(index)` - Mark a todo as complete
- `delete_todo(index)` - Delete a todo item
- `click_active_filter()` - Click the Active filter
- `click_completed_filter()` - Click the Completed filter
- `click_all_filter()` - Click the All filter
- `get_active_todos()` - Get active (incomplete) todos
- `get_completed_todos()` - Get completed todos
- `is_todo_completed(index)` - Check if a todo is marked complete

## Configuration

### Pytest Configuration

The `pytest.ini` file contains the following configuration:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
markers =
    unit: Unit tests
    property: Property-based tests
    integration: Integration tests
```

### Playwright Configuration

Playwright can be configured via environment variables or through the page fixture in `conftest.py`. Common configurations include:

- **Headless Mode**: Set `PLAYWRIGHT_HEADLESS=0` to run tests with visible browser
- **Slow Motion**: Set `PLAYWRIGHT_SLOW_MO=1000` to slow down actions by 1000ms
- **Browser Type**: Set `PLAYWRIGHT_BROWSER=firefox` to use Firefox instead of Chromium

## Troubleshooting

### Playwright Installation Issues

If you encounter issues installing Playwright browsers, try:

```bash
# Clear Playwright cache
rm -rf ~/.cache/ms-playwright

# Reinstall browsers
playwright install
```

### Tests Timing Out

If tests are timing out, you can increase the timeout in `conftest.py`:

```python
page.set_default_timeout(30000)  # 30 seconds
```

### Element Not Found Errors

Ensure the TodoMVC application is accessible at `https://demo.playwright.dev/todomvc/#/`. If the URL has changed, update the `BASE_URL` in `pages/todo_page.py`.

### Non-English Character Issues

If non-English characters are not displaying correctly, ensure your terminal and IDE are configured to use UTF-8 encoding.

## GitHub Repository Setup

### Initial Repository Setup

1. Create a new repository on GitHub
2. Clone this repository locally
3. Add your GitHub repository as a remote:

```bash
git remote add origin https://github.com/yourusername/todomvc-playwright-tests.git
```

4. Push the code to GitHub:

```bash
git branch -M main
git push -u origin main
```

### Continuous Integration

To set up automated testing on GitHub, create a `.github/workflows/tests.yml` file:

```yaml
name: Run Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Install Playwright browsers
      run: playwright install
    
    - name: Run tests
      run: pytest -v
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and commit: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Submit a pull request

## Development

### Running Tests During Development

For development, you can run tests in watch mode using pytest-watch:

```bash
pip install pytest-watch
ptw
```

### Debugging Tests

To debug a failing test, run it with the `--pdb` flag:

```bash
pytest tests/test_todo_creation.py::test_add_english_todo --pdb
```

This will drop into the Python debugger when the test fails.

### Viewing Browser During Test Execution

To see the browser window during test execution, set the `PLAYWRIGHT_HEADLESS` environment variable:

```bash
# On macOS/Linux
PLAYWRIGHT_HEADLESS=0 pytest tests/test_todo_creation.py

# On Windows
set PLAYWRIGHT_HEADLESS=0
pytest tests/test_todo_creation.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or contributions, please open an issue on GitHub or contact the project maintainers.

## References

- [Playwright Documentation](https://playwright.dev/python/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Hypothesis Documentation](https://hypothesis.readthedocs.io/)
- [TodoMVC Application](https://demo.playwright.dev/todomvc/#/)
