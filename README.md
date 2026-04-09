# Selenium Upskilling - Sauce Demo Tests

## Overview
This project contains Selenium automation tests for the Sauce Demo website.
- **Test Site**: https://www.saucedemo.com/
- **Language**: Python
- **Test Framework**: Pytest

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Tests

**Using Python directly:**
```bash
python test_sauce_demo.py
```

**Using Pytest (recommended):**
```bash
pytest test_sauce_demo.py -v
```

## Test Credentials
The Sauce Demo site provides test credentials:
- **Username**: `standard_user`
- **Password**: `secret_sauce`

(Other valid usernames include: `problem_user`, `performance_glitch_user`, `locked_out_user`)

## Tests Included

1. **test_login_successful** - Tests user login functionality
2. **test_add_to_cart** - Tests adding products to shopping cart
3. **test_logout** - Tests logout functionality

## Project Structure
```
├── requirements.txt          # Python dependencies
├── test_sauce_demo.py        # Main test file
└── README.md                 # This file
```

## Files Explained

- **requirements.txt**: Contains all necessary Python packages
  - `selenium`: Web automation framework
  - `webdriver-manager`: Automatic WebDriver management
  - `pytest`: Testing framework

- **test_sauce_demo.py**: Contains test cases with:
  - `setup_method()`: Initializes Chrome WebDriver
  - `teardown_method()`: Cleans up after tests
  - Individual test methods for different scenarios

## Next Steps
- Add more test cases as needed
- Explore the Orange CRM site (alternative testing target)
- Implement Page Object Model (POM) design pattern
- Add test data management
- Set up CI/CD integration

## Troubleshooting
- If WebDriver fails to download, ensure you have internet connection
- Chrome browser must be installed on your system
- Make sure Python 3.8+ is installed
