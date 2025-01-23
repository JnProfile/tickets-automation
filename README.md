# Playwright Test Automation

This project implements automated testing using **Playwright**, **pytest**, and the **Page Object Model (POM)** approach. Tests are written in Python and executed in headful mode to interact with the application's interface.

---

## 🔧 Installation and Setup

Before getting started, make sure you have the following installed:
- Python 3.12+
- Playwright
- pip (Python package manager)

### 1. Clone the repository

```bash
git clone <repository-url>
cd <project-folder>
```

### 2. Create a virtual environment

Create and activate a virtual environment:

```bash
python3 -m venv venv
. venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows
```

### 3. Install dependencies

Install all necessary dependencies from `requirements.txt`:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Install Playwright browsers

Install the browsers required for testing:

```bash
python -m playwright install
```

---

## 🚀 Running Tests

### 1. In only headful mode

To run all tests:

```bash
python -m pytest -m basic_search
```

## 🤝 CI/CD Integration

This project is configured to run tests on a self-hosted runner. See the `.github/workflows/playwright-tests.yml` file for configuration details. It requires to have python3.12+ on machine
