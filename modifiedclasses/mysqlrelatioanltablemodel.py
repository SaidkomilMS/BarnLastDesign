from PyQt5.QtSql import QSqlRelationalTableModel, QSqlRecord


class SRTM(QSqlRelationalTableModel):
    def primeInsert(self, row: int, record: QSqlRecord) -> None:
        print(f"Record - {record} is added to {row}-row")
        print("1")

    def beforeUpdate(self, row: int, record: QSqlRecord) -> None:
        print(f"Record at {row}-row will be changed to: {record}")
        print("2")

    def beforeInsert(self, record: QSqlRecord) -> None:
        print(f"Record - {record} will be added")
        print("3")

    def beforeDelete(self, row: int) -> None:
        print(f"Record at {row}-row will be deleted")
        print("4")

    def dataChanged(self, begin, end, roles: list = None):
        if not roles:
            roles = []
        print(f"Data changed. Begin: {begin}; End: {end}; Roles: {roles}")
        print("5")
