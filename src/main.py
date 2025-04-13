from src.structs.name import Name
from src.person import Person
from src.calculator import CoffeePaymentCalculator

def main():
    # Initialize the calculator
    calculator = CoffeePaymentCalculator()
    
    # Example usage
    # Create some people
    person1 = Person(Name("John", "Doe"), 5)
    person2 = Person(Name("Jane", "Smith"), 3)
    
    # Add people to calculator
    calculator.add_person(person1)
    calculator.add_person(person2)
    
    # Add a purchase
    calculator.add_purchase(
        date="2024-04-13",
        amount=500,  # in CZK
        location="Coffee Shop",
        items=["Coffee beans", "Filters"]
    )
    
    # Calculate and display results
    summary = calculator.generate_payment_summary()
    print(summary)

if __name__ == "__main__":
    main() 