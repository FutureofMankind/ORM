import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from Tables import create_tables, Publisher, Book, Sale, Shop, Stock

DSN = '...'
engine = sq.create_engine(DSN)

create_tables(engine)

p1 = Publisher(name='Роберт', books = [
    Book(title="Дверь в лето"),
    Book(title="Чужак в чужой стране"),
    Book(title="Звёздный десант")])
p2 = Publisher(name='Говард', books = [
    Book(title="Хребты безумия"),
    Book(title="Сомнамбулический поиск неведомого Кадата"),
    Book(title="Тень над Иннсмутом")])
p3 = Publisher(name="Филип", books = [
    Book(title="Мечтают ли андроиды об электроовцах?")
    Book(title="Симулякры")])
b1 = Book(title="Гражданин Галактики", publisher=p1)
b2 = Book(title="Зов Ктулху", publisher=p2)
b3 = Book(title="Красная планета", publisher=p1)
b4 = Book(title="Безымянный город", publisher=p2)

shop1 = Shop(name="Книжный червь")
stock1 = Stock(book=b1, shop=shop1, count=36)
sale1 = Sale(price=1000, stock=stock1, count=19)
stock2 = Stock(book=b3, shop=shop1, count=42)
sale2 = Sale(price=650, stock=stock2, count=20)

shop2 = Shop(name="Читалец")
stock3 = Stock(book=b2, shop=shop2, count=13)
sale3 = Sale(price=1000, stock=stock3, count=616)
stock4 = Stock(book=b3, shop=shop2, count=69)
sale4 = Sale(price=1500, stock=stock4, count=125)

Session = sessionmaker(bind=engine)
s = Session()
s.add_all([p1, p2, p3, b1, b2, b3, b4, shop1, shop2, stock1, stock2, stock3, stock4, sale1, sale2, sale3, sale4])
s.commit()

x = input()
print(s.query(Publisher).filter(sq.or_(Publisher.id==x, Publisher.name==x)).all()[0])

p = s.query(Publisher).filter(sq.or_(Publisher.id==x, Publisher.name==x)).all()[0]
sales = s.query(Sale).join(Stock).join(Shop).join(Book).filter(Book.publisher==p).subquery('t')
shops = s.query(Shop).join(Stock).join(Sale).filter(Sale.id==sales.c.id)
for i in shops:
    print(i)

s.close()