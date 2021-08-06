import datetime, csv
from models import Base, session, Product, engine


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
                new_entry = True
                for item in query:
                    if item.product_quantity == quantity:
                        if item.product_price == price:
                            new_entry = False

            if new_entry:
                product = Product(product_name=name, product_price=price,
                product_quantity=quantity, date_updated=date)
                session.add(product)
        session.commit()

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv('inventory.csv')