"""import pymysql
from pymysql.cursors import DictCursor
from contextlib import closing
from config import *"""
from datetime import date
# from decimal import Decimal
import sqlite3
import logging
from typing import List


class DBWorker:

    @property
    def connection(self):
        return sqlite3.connect(self.db)

    def __init__(self):
        self.db = 'ambar_book.db'

    def get_product_id(self, name='') -> int:
        with self.connection as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute('select `id` from `products` where `name` = ?', (name, ))
            return dict(cur.fetchone())['id']

    def get_product_remainder(self, product_id) -> int:
        with self.connection as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(
                'select `remainder` from `products` where `id` = ?',
                (product_id, ))
            return dict(cur.fetchone())['remainder']

    def get_price(self, product_id: int,
                  decrement: float = 0.0) -> float:
        with self.connection as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(
                'select id, price, remainder from prices_of_inc where product_id = ? order by date',
                (product_id, )
            )
            remainders = [dict(row) for row in cur.fetchall()]
            index = 0
            sum_costs = 0
            sum_value = 0
            while index < len(remainders):
                val_difference = float(remainders[index]['remainder'])
                if float(remainders[index]['remainder']) > decrement:
                    remainders[index]['remainder'] = float(remainders[index]['remainder']) - decrement
                else:
                    remainders[index]['remainder'] = 0.0
                val_difference -= float(remainders[index]['remainder'])
                sum_costs += int(remainders[index]['price']) * val_difference
                decrement -= float(remainders[index]['remainder'])
                if decrement <= 0.0:
                    break
                sum_value += val_difference
                index += 1
            else:
                logging.error(f'Не хватало кол-ва для списания продукта: {product_id}')
            for remainder in remainders:
                q = f'update prices_of_inc set ' \
                    f'remainder = {remainder["remainder"]} ' \
                    f'where id = {remainder["id"]}'
                cur.execute(q)
            return sum_costs/sum_value

    def get_unit(self, product_id: int) -> str:
        with self.connection as conn:
            cur = conn.cursor()
            cur.execute(
                'select unit from products where id = ?',
                (product_id, )
            )
            return cur.fetchone()[0]

    def add_changing(self, product_id: int,
                     increment: float = 0.0, decrement: float = 0.0,
                     mdate: date = date.today(), price=None,
                     agreement_info: str = None,
                     invoice_info: str = None) -> None:
        if not increment:
            price: float = price or self.get_price(product_id, decrement)
        unit: str = self.get_unit(product_id)
        with self.connection as conn:
            cur = conn.cursor()
            cur.execute(
                'insert into changings (product_id, date, price, increment,'
                'decrement, unit, agreement_info, invoice_info) '
                'values (?, ?, ?, ?, ?, ?, ?, ?)',
                (product_id, mdate, price, increment, decrement, unit,
                 agreement_info, invoice_info)
            )

    def get_child_count(self) -> int:
        with self.connection as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(
                "SELECT `child_count` FROM `child_counts` WHERE `date` = ?",
                (date.today(), ))
            results = [dict(result) for result in cur.fetchall()]
            assert bool(len(results))
            return int(results[0]['child_count'])

    def save_child_count(self, value: int, mdate=date.today()) -> None:
        with self.connection as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(
                '''insert into `child_counts` (`child_count`, `date`)
                 values (?, ?)''', (int(value), mdate))

    def get_products(self) -> List[dict]:
        with self.connection as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(
                'select `id`, `name`, `remainder`, `show`, `unit` from `products`')
            results = [dict(result) for result in cur.fetchall()]
            return results

    def get_products_by_fields(self, fields: list) -> list:
        """For getting only necessary fields"""
        with self.connection as conn:
            cur = conn.cursor()
            cur.execute(
                'select ' + ', '.join(fields) + ' from products'
            )
            return cur.fetchall()

    def get_changings(self, product_filter: str = "1") -> List[dict]:
        with self.connection as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            query = 'select id, date, price, increment, decrement, remain' \
                    f'der, unit from changings where {product_filter}'
            cur.execute(query)
            results = [dict(result) for result in cur.fetchall()]
            return results

    def add_product(self, name, unit):
        with self.connection as conn:
            cur = conn.cursor()
            query = f"insert into products (name, unit) values ({name}, {unit})"
            cur.execute(query)
            conn.commit()

    def add_meal(self, name):
        with self.connection as conn:
            cur = conn.cursor()
            query = f"insert into meals (name) values ({name})"
            cur.execute(query)
            conn.commit()


"""
class DBWorker:
    
    def __init__(self):
        self.query = ''
        with self.connection as conn:
            pass

    @property
    def connection(self):
        return closing(pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            cursorclass=DictCursor
        ))

    def get_product_id(self, name=''):
        self.query = f''
        with self.connection as conn:
            with conn.cursor() as cur:
                cur.execute('select `id` from `products` where `name` = %s', name)
                return cur.fetchone()['id']

    def add_changing(self, product_name, value, mdate=date.today()):
        
        product_id = self.get_product_id(name=product_name)
        self.query = f'INSERT INTO `changes` (`product_id`, `value`, `date`) VALUES (%s, %s, %s)'
        with self.connection as conn:
            with conn.cursor() as cur:
                cur.execute(self.query, (product_id, value, mdate))
                conn.commit()
        with self.connection as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT `remainder` FROM `products` WHERE `id` = %s", product_id)
                remainder = cur.fetchone()['remainder']
                remainder += Decimal(value)
                cur.execute("UPDATE `products` SET `remainder` = %s WHERE `id` = %s", (remainder, product_id))
                conn.commit()

    def get_child_count(self):
        with self.connection as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT `child_count` FROM `child_counts` WHERE date = %s", date.today())
                results = cur.fetchall()
                if bool(len(results)):
                    return int(results[0]['child_count'])
                else:
                    raise AssertionError

    def save_child_count(self, value, mdate=date.today()):
        with self.connection as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO `child_counts` (`child_count`, `date`) VALUES (%s, %s)", (value, mdate))
                conn.commit()

    def get_products(self) -> list:
        with self.connection as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM `products` WHERE `show` = 1")
                return cur.fetchall()

"""