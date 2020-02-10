from time import strftime, ctime
import json


def show_logs():
    print("{:^12s} | {:^12s} | {:^4s} | {:^9s} | {:^15s} | {:^16s}"
          .format("Client", "Product", "Qty", "Price", "Total", "Time"))
    print("\n{:^12s} | {:^12s} | {:^4s} | {:^9s} | {:^15s} | {:^16s}"
          .format("Client", "Product", "Qty", "Price", "Total", "Time"), file=SHOW_LOGS_FILE)
    print("-" * 90)
    print("-" * 90, file=SHOW_LOGS_FILE)

    for transaction in DATA:
        client_name = transaction['customer_name']
        products = transaction['product']
        time = transaction['time']

        overall_total = 0
        for product in products:
            product_name = product['product_name']
            product_quantity = product['product_quantity']
            product_price = product['product_price']

            total = product_price * product_quantity
            overall_total += total

            total = f'{total:,.2f}'
            product_price = f'{product_price:,.2f}'
            print(
                f"{client_name:<12s} | {product_name:<12s} | {product_quantity:^4.0f} | {product_price:>9s} | {total:>15s} | {time:>16s}")
            print(f"{client_name:<12s} | {product_name:<12s} | {product_quantity:^4.0f} | {product_price:>9s} | {total:>15s} | {time:>16s}", file=SHOW_LOGS_FILE)
            client_name = ''

        overall_total = f'{overall_total:,.2f}'
        print("{:^12s} | {:^12s} | {:^4s} | {:^9s} | {:>15s} | {:>16s}"
              .format("", "", "", "", overall_total, time))
        print("{:^12s} | {:^12s} | {:^4s} | {:^9s} | {:>15s} | {:>16s}"
              .format("", "", "", "", overall_total, time), file=SHOW_LOGS_FILE)
        print("-" * 90)
        print("-" * 90, file=SHOW_LOGS_FILE)


def save_data(client_name, product_information):
    DATA.append(
        {
            'customer_name': client_name,
            'product': product_information,
            'time': strftime("%d/%m/%Y %H:%M")
        }
    )


def end_program():
    # backup data and exit program

    with open("cash_register_backup.json", "w") as backup:
        json.dump(DATA, backup)
        
    show_logs()
    exit()


def get_number_input(prompt):
    """
    use prompt to collects input and return float
    """

    # initialize value
    value = None

    # if collected value is not float
    while type(value) != float:
        try:
            value = float(input(prompt))
            return value

        except KeyboardInterrupt:
            end_program()

        except ValueError as e:
            print("Invalid Input!")
            print(ctime(), e, file=ERROR_FILE)


def main():
    while True:
        client_name = input('What is the customer\'s name?: ')
        if not client_name:
            print('Name must be provided!')
            continue

        elif client_name == '-1':
            end_program()

        # store all product details
        product_information = []

        while True:
            product_name = input('what is the product name?: ')

            if not product_name:
                print('Product name must be provided!')
                continue

            elif product_name == '-1':
                # end_program(client_name, product_information)
                save_data(client_name, product_information)
                break

            product_qty = get_number_input(
                f'How many {product_name} purchased?: ')
            if product_qty == -1:
                save_data(client_name, product_information)
                break

            product_price = get_number_input(f"How much is {product_name}?: ")
            if product_price == -1:
                # end_program(client_name, product_information)
                save_data(client_name, product_information)
                break

            product_information.append(
                {
                    'product_name': product_name,
                    'product_quantity': product_qty,
                    'product_price': product_price
                }
            )


if __name__ == '__main__':
    # super globals
    ERROR_FILE = open('error_log.txt', 'a')
    SHOW_LOGS_FILE = open('show_logs.txt', 'a')
    DATA = []

    # the main code
    main()

    # close file
    SHOW_LOGS_FILE.close()
    ERROR_FILE.close()
