from dbworker import DBWorker
from art import *
import art


if __name__ == '__main__':
    worker = DBWorker()
    print(worker.get_changings('product_id=1'))