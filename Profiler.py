import datetime

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


class Operation:
    def __init__(self, name: str, max_number: int):
        self.name = name
        self.operation_count = 0
        self.max_number = max_number

    def count(self, value: int = 1):
        if value < 1:
            raise Exception('''Value can't be non-positive.''')
        self.operation_count += value

    def to_string(self):
        return f'{self.name}, {self.max_number}, {self.operation_count}'


class Profiler:
    def __init__(self, name: str = 'Profiler'):
        self.name = name
        self.operations = {}
        self.joint_operations = {}

    def create_operation(self, name: str, max_number: int) -> Operation:
        op = Operation(name, max_number)

        try:
            self.operations[name].append(op)
        except:
            self.operations[name] = [op]

        return op

    def join_operations(self, name: str, *names):

        for opName in names:
            if opName not in self.operations.keys():
                raise Exception(f'''Operation {opName} not existent.''')

        joint_operation = [self.operations[opName] for opName in names]

        self.joint_operations[name] = joint_operation

        for opName in names:
            del self.operations[opName]

    def show_report(self):
        with PdfPages(self.name + '.pdf') as pdf:

            for key, value in self.operations.items():
                figure = plt.figure(key)

                plt.plot([k.max_number for k in value], [k.operation_count for k in value])

                plt.title(key)

                plt.ylabel('Operation count')
                plt.xlabel('Size')

                plt.show()

                pdf.savefig(figure)

                plt.close()

            for key, value in self.joint_operations.items():
                figure = plt.figure(key)

                plt.title(key)

                for operation in value:
                    plt.plot([k.max_number for k in operation], [k.operation_count for k in operation])

                    plt.ylabel('Operation count')
                    plt.xlabel('Size')

                plt.legend([x[0].name for x in value])
                plt.show()
                pdf.savefig(figure)
                plt.close()

            d = pdf.infodict()
            d['Title'] = self.name
            try:
                import getpass
                d['Author'] = getpass.getuser()
            except:
                pass

            d['CreationDate'] = datetime.datetime.today()
            d['ModDate'] = datetime.datetime.today()


if __name__ == '__main__':
    profiler = Profiler('Test for profiler')

    for i in range(1, 10):
        op1 = profiler.create_operation('aia a fost', i)
        op2 = profiler.create_operation('asta nu chiar', i)
        op3 = profiler.create_operation('asta poate', i)

        op1.count(i ** 3)
        op2.count(i * i)
        op3.count(i * 20)

    profiler.join_operations('idk', 'aia a fost', 'asta nu chiar')

    profiler.show_report()
