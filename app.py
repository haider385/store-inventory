import datetime, csv
from models import Base, session, Product, engine
from time import sleep

def view_entry(id):
    product = session.query(Product).filter(Product.product_id==id).first()
    print(f'\n{product.__repr__()}')


def backup(filename):
    """Creates a csv backup of the db with the specified filename"""
    all_products = session.query(Product)
    header = ['ID', 'Product Name', 'Price', 'Quantity', 'Date Updated']
    with open(f'{filename}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for product in all_products:
            data = [
                product.product_id,
                product.product_name,
                f'${product.product_price/100}',
                product.product_quantity,
                product.date_updated
            ]
            writer.writerow(data)
        csvfile.close()


def add_entry(name, quantity, price):
    """takes name str, quantity int and cleaned price. Updates if already
       exists. Creates new entry if no entry exists with same name"""

    exists = False
    today = datetime.datetime.today()
    date = clean_date(today.strftime('%m/%d/%Y'))

    for product in session.query(Product):
        if product.product_name == name:
            exists = True
    
    if exists == True:
        product = session.query(Product).filter(Product.product_name==name).first()
        product.product_quantity = quantity
        product.product_price = price
        product.date_updated = date
        session.add(product)
    else:
        product = Product(
            product_name = name,
            product_quantity = quantity,
            product_price = price,
            date_updated = date
        )
        session.add(product)
    
    session.commit()


def clean_price(price):
    #expected format is a number to 2d.p. as a string starting with '$'
    if '.' in price:
        try:
            split_price = price[1:].split('.')
            if len(split_price[1]) == 2:
                price_in_cents = int(''.join(split_price))
        except:
            pass
        else:
            return price_in_cents
    print(f"'{price}' is not a valid price.")
    print("""You must enter the price in dollars and cents without the dollar sign. 
             \rE.g. if the price is $7.54, you should enter '7.54'""")
    return False


def clean_date(date):
    #expected format is MM/DD/YYYY
    split_date = date.split('/')
    try:
        cleaned = datetime.date(year=int(split_date[2]), 
                                month=int(split_date[0]),
                                day=int(split_date[1]))
    except:
        pass
    else:
        return cleaned
    print(f"'{date}' is not a valid date.")
    print("""You must enter the date in the format MM/DD/YYYY.
             \rE.g. for the 3rd of June 2021, you should enter 06/03/2021""")


def add_csv(filename):
    """Adds entries from csv file to the db. If multiple products
       with the same name exist in the csv file, only the one that has
       been updated most recently is added."""
    with open(f'{filename}') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            new_entry = False
            name = row['product_name']
            price = clean_price(row['product_price'])
            quantity = int(row['product_quantity'])
            date = clean_date(row['date_updated'])
            query = session.query(Product).filter_by(product_name=row['product_name'])

            if query.count() == 0:
                new_entry = True
            else:
                for item in query:
                    if date > item.date_updated:
                        item.product_price = price
                        item.product_quantity = quantity
                        item.date_updated = date
                        session.add(item)

            if new_entry:
                product = Product(product_name=name, product_price=price,
                product_quantity=quantity, date_updated=date)
                session.add(product)
        session.commit()

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv('inventory.csv')
    choices = ['v', 'a', 'b', 'q']
    quitting = False
    while not quitting:
        print("""Please enter the letter corresponding to the option of your choice.
                 \r'v': View a single product's inventory
                 \r'a': Add a new product to the database
                 \r'b': Make a backup of the entire inventory
                 \r'q': Quit the program""")
        choice = input(': ').strip().lower()
        if choice not in choices:
            print("That is not a valid option, please try again.\n")
            continue
        elif choice == 'q':
            quitting = True
        elif choice == 'v':
            count = session.query(Product).count()
            print("\nEnter the ID of the product you would like to view.")
            id_choice = input(f'Enter a number 1 - {count}: ').strip()
            try:
                int(id_choice)
            except:
                print(f"\n{id_choice} is not a valid ID.\n")
            else:
                if int(id_choice) <= count and int(id_choice) > 0:
                    view_entry(int(id_choice))
                    input("Press Enter to continue.\n")
                else:
                    print(f"\n{id_choice} is not a valid ID.\n")
        elif choice == 'a':
            print("\nYou are now adding a new product to the database.")
            name = input("\nProduct Name: ")

            price_correct = False
            while not price_correct:
                price = input("\nPrice: ")
                price_correct = clean_price(f'${price}')

            quantity_correct = False
            while not quantity_correct:
                quantity = input("\nQuantity: ")
                try:
                    int(quantity)
                except:
                    print(f"{quantity} is not a valid quantity, Enter an integer.")
                else:
                    quantity = int(quantity)
                    quantity_correct = True
            
            add_entry(name, quantity, price_correct)
            print(f"{name} has been successfully added to the database.")
            input("Press Enter to continue.\n")
        elif choice == 'b':
            filename = 'backup'
            backup(filename)
            print(f"The database backup has been successful. See {filename}.csv.")
            input("Press Enter to continue.\n")
            