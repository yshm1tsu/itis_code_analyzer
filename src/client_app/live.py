from rich.console import Console
from rich.table import Table


class TableProcessor:
    def __init__(self):
        self.table = Table(title="Результаты", show_lines=True)
        self.console = Console()

    def initialize_table(self):
        self.table = Table(title="Результаты", show_lines=True)
        self.table.add_column("Файл", style="cyan", no_wrap=True)
        self.table.add_column("Результаты проверки", style="magenta")

    def create_table(self, values: dict):
        for key in values.keys():
            value = values[key] if values[key] != "" else "\u2713"
            self.table.add_row(key, value)

    def update_table(self, values):
        self.console.clear()
        self.initialize_table()
        self.create_table(values)

    def print_table(self):
        self.console.print(self.table, justify="center")


#
# table_processor = TableProcessor()
# table_processor.initialize_table()
# table_processor.update_table({
#     "a": "b",
#     "c": "d"
# })
# table_processor.print_table()
