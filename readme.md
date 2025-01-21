# Expense Tracker CLI Application

The Expense Tracker is a command-line application designed to help users manage their personal finances efficiently. This application allows users to add, update, delete, and view expenses, as well as generate summaries and export data. Built with Python, it adheres to clean code, clean architecture principles and test driven development.

## Features
1. **Add Expense**: Add a new expense with a description, amount, and optional category.
2. **Update Expense**: Modify an existing expense.
3. **Delete Expense**: Remove an expense by its unique ID.
4. **View Expenses**: List all expenses in a tabular format.
5. **Summary**:
   - View the total expenses.
   - View monthly expense summaries for the current year.
6. **Category Management**: Filter expenses by category.
7. **Export to CSV**: Export all expenses to a CSV file for external use.

## Inspiration
The requirements for this projects are inspired from here: https://roadmap.sh/projects/expense-tracker

## Commands and Usage

### Adding an Expense
```bash
$ expense-tracker add --description "Lunch" --amount 20 --category "Food"
```

### Deleting an Expense
```bash
$ expense-tracker delete --id 1
```

### Viewing All Expenses
```bash
$ expense-tracker list
```

### Viewing Expense Summary
```bash
$ expense-tracker summary


$ expense-tracker summary --month 1
```

### Exporting to CSV
```bash
$ expense-tracker export --file expenses.csv
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/gunjanmodi/expense-tracker.git
   cd expense-tracker
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application
Run the main script from the terminal:
```bash
python cli.py <command> [options]
```

If you want to run with the binary named "expense-tracker", perform following command
```bash
ln -s <absolute path to the project expense-tracker>/cli.py /usr/local/bin/expense-tracker
```

## Testing
Run the test suite to ensure all components are functioning as expected:
```bash
pytest
```

## License
This project is licensed under the MIT License. See `LICENSE` for details.
