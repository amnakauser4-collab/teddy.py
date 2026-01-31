# Smart Electricity Usage Monitor

# Tuple for tariff slabs (fixed data)
TARIFF = (10, 15)   # Rs per unit

# List to store daily usage
daily_usage = []

# Function to add daily usage
def add_daily_usage():
    units = float(input("Enter today's electricity usage (units): "))
    daily_usage.append(units)
    print("Usage added successfully.\n")

# Function to calculate total units
def calculate_total_units():
    return sum(daily_usage)

# Function to calculate bill
def calculate_bill(total_units):
    if total_units <= 100:
        bill = total_units * TARIFF[0]
    else:
        bill = (100 * TARIFF[0]) + ((total_units - 100) * TARIFF[1])
    return bill

# Function to show report
def show_report():
    if len(daily_usage) == 0:
        print("No data available.\n")
        return

    total_units = calculate_total_units()
    bill = calculate_bill(total_units)

    print("\n--- Electricity Usage Report ---")
    print("Days Recorded:", len(daily_usage))
    print("Total Units Used:", total_units)
    print("Estimated Bill: Rs", bill)

    if total_units > 200:
        print("⚠️ ALERT: High electricity consumption!")
    else:
        print("✅ Usage is under control.")
    print()

# Main menu
while True:
    print("1. Add Daily Usage")
    print("2. View Report")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_daily_usage()
    elif choice == "2":
        show_report()
    elif choice == "3":
        print("Thank you for using the system.")
        break
    else:
        print("Invalid choice. Try again.\n")