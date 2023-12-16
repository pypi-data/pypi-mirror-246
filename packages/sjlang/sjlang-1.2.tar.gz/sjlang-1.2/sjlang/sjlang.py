import inspect

class MyInterpreter:
    def __init__(self):
        self.variables = {}

    def run(self, code):
        lines = code.split('\n')
        for line in lines:
            self.execute(line)

    def execute(self, line):
        if line.startswith("말해라"):
            self.print_output(line)
        elif line.startswith("기억해라"):
            self.store_variable(line)
        elif line.startswith("세찐찐이가"):
            pass
        elif line.startswith("뭔소리냐ㅋㅋ"):
            exit()
        elif line.startswith("반복해라"):
            self.repeat(line)
        elif line.startswith("더해라"):
            self.add(line)
        elif line.startswith("빼라"):
            self.subtract(line)
        elif line.startswith("정해라"):
            self.set_value(line)
        elif "맞냐" in line and "?" in line:
            self.check_condition(line)
        else:
            print(f"뭔 코드냐 ㅋㅋ - {line}")

    def check_condition(self, line):
        _, rest = line.split("맞냐", 1)
        condition, code = rest.split("말해라", 1)
        condition = condition.strip()
        code = code.strip()
        try:
            if eval(condition, globals(), self.variables):
                self.run(code)
        except Exception as e:
            print(f"에러 발생: {e}")

    def print_output(self, line):
        _, output = line.split("말해라 ")
        variable_name = output.strip('()')
        if variable_name in self.variables:
            print(self.variables[variable_name])
        else:
            print(f"뭔 변수냐 ㅋㅋ - {variable_name}")

    def store_variable(self, line):
        _, assignment = line.split("기억해라 ")
        variable, value = assignment.split(" = ")
        self.variables[variable] = value

    def repeat(self, line):
        _, rest = line.split("반복해라 ")
        count, code_to_repeat = rest.split(" ", 1)
        count = int(count)
        for _ in range(count):
            self.run(code_to_repeat)

    def add(self, line):
        _, rest = line.split("더해라 ")
        variable, value = rest.split(" ", 1)

        if variable in self.variables:
            current_value = self.variables[variable]
            try:
                current_value = int(current_value)
                value = int(value)
                result = current_value + value
            except ValueError:
                result = current_value + value

            self.variables[variable] = result
        else:
            print(f"{variable}이 뭐냐ㅋㅋ")

    def subtract(self, line):
        _, rest = line.split("빼라 ")
        variable, value = rest.split(" ", 1)

        if variable in self.variables:
            current_value = self.variables[variable]
            try:
                current_value = int(current_value)
                value = int(value)
                result = current_value - value
                self.variables[variable] = result
            except ValueError:
                print(f"그게 되겠냐 ㅋㅋ")
        else:
            print(f"{variable}이 뭐냐ㅋㅋ.")

    def set_value(self, line):
        _, rest = line.split("정하기 ")
        variable, value = rest.split(" ", 1)

        if variable in self.variables:
            self.variables[variable] = value
        else:
            print(f"{variable}이 뭐냐ㅋㅋ")

def run_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()
        interpreter = MyInterpreter()

        if "세찐찐이가" not in code:
            print("이게 무슨 세찐찐이랭이냐")
            return

        if "뭔소리냐ㅋㅋ" not in code:
            print("이게 무슨 세찐찐이랭이냐")
            return

        interpreter.run(code)

file_path = input("불러올 파일 경로를 입력하세요: ")

run_from_file(file_path)
