import argparse

def main():
    parser = argparse.ArgumentParser(description="Simple CLI Application")
    
    # Adding arguments
    parser.add_argument("number1", type=int, help="First number")
    parser.add_argument("number2", type=int, help="Second number")
    parser.add_argument("-a", "--add", action="store_true", help="Add the numbers")
    parser.add_argument("-s", "--subtract", action="store_true", help="Subtract the numbers")

    # Parsing arguments
    args = parser.parse_args()

    # Perform operations based on arguments
    if args.add:
        result = args.number1 + args.number2
        print(f"The sum is: {result}")
    elif args.subtract:
        result = args.number1 - args.number2
        print(f"The difference is: {result}")
    else:
        print("No operation specified. Please use --add or --subtract.")

if __name__ == "__main__":
    main()