from collections import namedtuple

default_income = 5000

Expense = namedtuple("Expense", ["name", "weight"])
Category = namedtuple("Category", ["name", "color", "expenses", "weight"])

default_categories = [
    Category(
        name="Housing & Utilities",
        color="#116530",  # Dark Green
        expenses=[
            Expense("Rent", 0.4),
            Expense("Mortgage", 0.4),
            Expense("Homeowners Insurance", 0.05),
            Expense("Renters Insurance", 0.05),
            Expense("Property Taxes", 0.1),
            Expense("Home Maintenance & Repairs", 0.1),
            Expense("Electricity", 0.1),
            Expense("Water & Sewer", 0.05),
            Expense("Internet", 0.05),
            Expense("Cell Phone", 0.05),
        ],
        weight=0.275,  # 25-30%
    ),
    Category(
        name="Transportation",
        color="#21B6A8",  # Teal
        expenses=[
            Expense("Car Payment", 0.4),
            Expense("Car Insurance", 0.2),
            Expense("Gas", 0.2),
            Expense("Public Transportation", 0.1),
            Expense("Vehicle Maintenance & Repairs", 0.1),
        ],
        weight=0.125,  # 10-15%
    ),
    Category(
        name="Food & Essentials",
        color="#A3EBB1",  # Light Green
        expenses=[
            Expense("Groceries", 0.6),
            Expense("Dining Out", 0.2),
            Expense("Coffee Shops", 0.1),
            Expense("Fast Food", 0.05),
            Expense("Meal Delivery", 0.05),
        ],
        weight=0.125,  # 10-15%
    ),
    Category(
        name="Health & Insurance",
        color="#18A558",  # Green
        expenses=[
            Expense("Health Insurance", 0.4),
            Expense("Dental Insurance", 0.15),
            Expense("Vision Insurance", 0.1),
            Expense("Doctor Visits", 0.2),
            Expense("Prescription Medications", 0.15),
        ],
        weight=0.15,  # 10-20%
    ),
    Category(
        name="Education & Personal Development",
        color="#145DA0",  # Deep Blue
        expenses=[
            Expense("Tuition", 0.3),
            Expense("Books & Supplies", 0.1),
            Expense("Online Courses", 0.1),
            Expense("Certifications", 0.1),
        ],
        weight=0.05,  # 5-10%
    ),
    Category(
        name="Family & Children",
        color="#2E8BC0",  # Medium Blue
        expenses=[
            Expense("Childcare", 0.4),
            Expense("Babysitting", 0.2),
            Expense("School Lunches", 0.15),
            Expense("College Savings", 0.15),
            Expense("Extracurricular Activities", 0.1),
        ],
        weight=0.05,  # 5-10%
    ),
    Category(
        name="Entertainment & Recreation",
        color="#B1D4E0",  # Light Blue
        expenses=[
            Expense("Hobbies", 0.3),
            Expense("Concerts", 0.2),
            Expense("Movies", 0.2),
            Expense("Gaming", 0.2),
            Expense("Theme Parks", 0.1),
        ],
        weight=0.075,  # 5-10%
    ),
    Category(
        name="Gifts & Donations",
        color="#189AB4",  # Teal Blue
        expenses=[
            Expense("Birthdays", 0.3),
            Expense("Holidays", 0.3),
            Expense("Weddings", 0.2),
            Expense("Charitable Donations", 0.1),
            Expense("Tithing", 0.1),
        ],
        weight=0.05,  # 5-10%
    ),
    Category(
        name="Travel & Vacations",
        color="#75E6DA",  # Light Cyan
        expenses=[
            Expense("Flights", 0.4),
            Expense("Hotels", 0.3),
            Expense("Rental Cars", 0.1),
            Expense("Travel Insurance", 0.1),
            Expense("Tours", 0.1),
        ],
        weight=0.075,  # 5-10%
    ),
    Category(
        name="Pets",
        color="#10564F",  # Dark Cyan
        expenses=[
            Expense("Pet Food", 0.5),
            Expense("Vet Visits", 0.3),
            Expense("Grooming", 0.1),
            Expense("Boarding", 0.1),
        ],
        weight=0.025,  # 2.5-5%
    ),
    Category(
        name="Savings & Investments",
        color="#4A90A2",
        expenses=[
            Expense("Emergency Fund", 0.4),
            Expense("Retirement Contributions", 0.3),
            Expense("Stock Market Investments", 0.2),
            Expense("Real Estate Investments", 0.1),
        ],
        weight=0.125,  # 10-15%
    ),
    Category(
        name="Shopping & Miscellaneous",
        color="#508AA8",  # Muted Blue-Green
        expenses=[
            Expense("Clothing", 0.4),
            Expense("Shoes", 0.2),
            Expense("Beauty & Cosmetics", 0.2),
            Expense("Tech & Gadgets", 0.2),
        ],
        weight=0.075,  # 5-10%
    ),
    Category(
        name="Debt & Financial Obligations",
        color="#88C0D0",  # Soft Cyan-Blue
        expenses=[
            Expense("Student Loan Payments", 0.2),
            Expense("Credit Card Payments", 0.2),
            Expense("Personal Loan Payments", 0.3),
            Expense("IRS Taxes", 0.2),
            Expense("Court Fees", 0.0),
        ],
        weight=0.05,  # 5-10%
    ),
]
