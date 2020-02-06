from time import ctime


def save_data(client_name, data):
    DATA.append(
        {
            'customer_name': client_name,
            'product': data,
            'time': ctime()
        }
    )


def end_program(client_name=None, data=None):
    if data is not None:
        save_data(client_name, data)

    print(DATA)
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

            product_qty = get_number_input(f'How many {product_name} purchased?: ')
            if product_qty == -1:
                save_data(client_name, product_information)
                break

            elif product_qty != 0:
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
    DATA = []

    # the main code
    main()

    # close file
    ERROR_FILE.close()
