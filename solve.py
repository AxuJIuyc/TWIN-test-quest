import io
import requests
import re

class CheckOperator:
    def __init__(self, num, oper):
        self.num = num
        self.oper = oper

    # поиск номера в базе
    def check_operator(self):
        req_num = requests.get(f'http://rosreestr.subnets.ru/?get=num&num={self.num}')
        
        text = req_num.text
        if req_num.status_code != 200 or re.findall(r'Возникла ошибка', text, re.I):
            return [2, 'нет']
        
        operator = re.findall(r'(operator: )(\S*(?:\s\S+)?\n)', text, re.I)[0][1].strip()
        if operator == self.oper:
            return [1, operator]
        else:
            return [0, operator]

class ReaderWriter:
    def __init__(self, rfile, wfile):
        self.reslst = [] # Итоговый список
        self.rfile = rfile
        self.wfile = wfile

    # Чтение данных из файла        
    def read_and_write_files(self):
        with io.open(self.rfile, 'r', encoding='utf-8') as f:
            T = 0
            F = 0
            N = 0
            while True:
                line = list(f.readline().strip().split())
                if line == []:
                    break
                check = CheckOperator(line[0], line[1])
                check = check.check_operator()
                line += [check[1], str(check[0])]
                self.reslst += [line]
                
                if check[0] == 1:
                    T += 1
                elif check[0] == 0:
                    F += 1
                else:
                    N += 1
    
        # запись в файл итогового списка
        with io.open(self.wfile, 'w', encoding='utf-8') as olf:
            olf.write(';'.join(['Номер', 'Оператор (изначальный)', 
                'Оператор (из росреестра)','Совпадение', '\n']))
            for i in self.reslst:
                olf.write(';'.join(i))
                olf.write('\n')
            olf.write(';'.join(['Совпадений', 'Несовпадений', 'Не найдено', '\n']))
            olf.write(';'.join([str(T), str(F), str(N)]))

def main():
    solve = ReaderWriter('clients.txt', 'operators_list.csv')
    solve.read_and_write_files()   
    
if __name__ == '__main__':
    main()