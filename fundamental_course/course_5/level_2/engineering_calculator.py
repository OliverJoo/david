import sys
import math
from PyQt6.QtWidgets import (
    QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QVBoxLayout, QLabel
)
from PyQt6.QtCore import Qt


# 문제 3. 공학용 계산기 제작
# Python으로 UI를 만들 수 있는 PyQT 라이브러리를 설치한다.
# 아이폰을 가로로 했을 때 나타나는 공학용 계산기와 최대한 유사하게 계산기 UI를 만든다. 출력 형태 및 버튼의 배치는 동일하게 해야한다. 색상이나 버튼의 모양까지 동일할 필요는 없다.
# 각각의 버튼을 누를 때 마다 숫자가 입력 될 수 있게 이벤트를 처리한다.
# 이번 과제에서는 실제로 계산 기능까지 구현된 필요는 없다.
# 완성된 코드는 engineering_calculator.py 로 저장한다.


# 문제 4. 공학용 계산기의 기능 제작
# Calculator 클래스를 상속받아서 EngineeringCalculator 클래스를 만든다.
# 공학용 계산기에서 추가된 30가지 기능을 정리하고 이 중에서 삼각함수 관련 기능인 sin, cos, tan, sinh, cosh, tanh와 원주율 과 x의 제곱 그리고 x의 세제곱 등을 담당할 메소드의 이름을 짓고 그 내용을 구현한다.
# 계산 기능들을 완성하기 위해서 math 등 외부 라이브러리를 사용 할 수 있다.
# 완성된 클래스의 기능들과 UI의 버튼들을 매칭 시킨다.
# 완성된 코드는 engineering_calculator.py 로 저장한다.

# 제약 사항
# 수학에서 발생할 수 있는 예외들이 다 적용되어 있어야 한다.
# 0을 나누면 안된다.
# 처리 할 수 있는 숫자의 범위가 넘어가면 에러 처리를 해야한다.
# 계산 기능들을 완성하기 위해서 math 등 외부 라이브러리를 사용 할 수 있다.

class Calculator:
    def __init__(self):
        self.reset()
    def reset(self):
        self.current_value = 0.0
        self.pending_value = 0.0
        self.pending_operation = None
        self.display_value = '0'
        self.waiting_for_operand = True
        self.just_evaluated = False  # = 직후 플래그
    def add(self, x, y): return x + y
    def subtract(self, x, y): return x - y
    def multiply(self, x, y): return x * y
    def divide(self, x, y):
        if y == 0:
            raise ValueError('0으로 나눌 수 없습니다')
        return x / y
    def negative_positive(self, value): return -value
    def percent(self, value): return value / 100
    def equal(self):
        if self.pending_operation is None:
            self.just_evaluated = True
            return self.current_value
        try:
            op = self.pending_operation
            if op == '+':
                result = self.add(self.pending_value, self.current_value)
            elif op == '-':
                result = self.subtract(self.pending_value, self.current_value)
            elif op == '×':
                result = self.multiply(self.pending_value, self.current_value)
            elif op == '÷':
                result = self.divide(self.pending_value, self.current_value)
            else:
                result = self.current_value
            if abs(result) > 1e15:
                raise OverflowError('결과가 너무 큽니다')
            self.just_evaluated = True
            return result
        except (ValueError, OverflowError, ZeroDivisionError) as e:
            self.just_evaluated = True
            raise e

class EngineeringCalculator(Calculator):
    def sin_function(self, x): return math.sin(x)
    def cos_function(self, x): return math.cos(x)
    def tan_function(self, x): return math.tan(x)
    def sinh_function(self, x): return math.sinh(x)
    def cosh_function(self, x): return math.cosh(x)
    def tanh_function(self, x): return math.tanh(x)
    def pi_constant(self): return math.pi
    def square_function(self, x): return x * x
    def cube_function(self, x): return x * x * x

class EngineeringCalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.calculator = EngineeringCalculator()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('공학용 계산기 (연속 연산 지원)')
        self.setFixedSize(410, 600)
        self.setStyleSheet('background-color: black;')
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        mode_label = QLabel('Rad', self)
        mode_label.setStyleSheet('color: white; font-size: 13px; margin: 0 0 3px 3px')
        main_layout.addWidget(mode_label, alignment=Qt.AlignmentFlag.AlignLeft)

        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setText('0')
        self.display.setStyleSheet(
            'background-color: black; color: white; font-size: 36px; border: none; padding: 20px;')
        main_layout.addWidget(self.display)

        # 공학용 버튼
        eng_layout = QGridLayout()
        eng_layout.setSpacing(5)
        eng_btns = [
            ('x²', 0, 0), ('x³', 0, 1), ('sin', 0, 2), ('cos', 0, 3),
            ('tan', 1, 0), ('sinh',1,1), ('cosh',1,2), ('tanh',1,3),
            ('π', 2, 0)
        ]
        for text, r, c in eng_btns:
            btn = QPushButton(text)
            btn.setFixedSize(82, 40)
            btn.setStyleSheet(
                'background-color: #007AFF; color: white; font-size: 16px; border-radius: 22px; border: none;'
            )
            btn.clicked.connect(lambda checked, t=text: self.eng_button_clicked(t))
            eng_layout.addWidget(btn, r, c)
        main_layout.addLayout(eng_layout)

        # 기본 계산기
        base_layout = QGridLayout()
        base_layout.setSpacing(5)
        base_btns = [
            ('AC',   0, 0, 'gray'),   ('+/-', 0, 1, 'gray'), ('%',   0, 2, 'gray'), ('÷',   0, 3, 'orange'),
            ('7',    1, 0, 'dark'),   ('8',   1, 1, 'dark'), ('9',   1, 2, 'dark'), ('×',   1, 3, 'orange'),
            ('4',    2, 0, 'dark'),   ('5',   2, 1, 'dark'), ('6',   2, 2, 'dark'), ('-',   2, 3, 'orange'),
            ('1',    3, 0, 'dark'),   ('2',   3, 1, 'dark'), ('3',   3, 2, 'dark'), ('+',   3, 3, 'orange'),
        ]
        for text, r, c, color in base_btns:
            btn = QPushButton(text)
            btn.setFixedSize(82, 56)
            if color == 'gray':
                btn.setStyleSheet(
                    'background-color: #A6A6A6; color: black; font-size: 20px; border-radius: 28px; border: none;'
                )
            elif color == 'dark':
                btn.setStyleSheet(
                    'background-color: #333333; color: white; font-size: 20px; border-radius: 28px; border: none;'
                )
            elif color == 'orange':
                btn.setStyleSheet(
                    'background-color: #FF9500; color: white; font-size: 20px; border-radius: 28px; border: none;'
                )
            btn.clicked.connect(lambda checked, t=text: self.base_button_clicked(t))
            base_layout.addWidget(btn, r, c)
        # 하단 구분: 0(좌, 2칸), .(중간), =(우측)
        zero_btn = QPushButton('0')
        zero_btn.setFixedSize(170, 56)
        zero_btn.setStyleSheet(
            'background-color: #333333; color: white; font-size: 20px; border-radius: 28px; border: none;'
        )
        zero_btn.clicked.connect(lambda checked, t='0': self.base_button_clicked(t))
        base_layout.addWidget(zero_btn, 4, 0, 1, 2)

        dot_btn = QPushButton('.')
        dot_btn.setFixedSize(82, 56)
        dot_btn.setStyleSheet(
            'background-color: #333333; color: white; font-size: 20px; border-radius: 28px; border: none;'
        )
        dot_btn.clicked.connect(lambda checked, t='.': self.base_button_clicked(t))
        base_layout.addWidget(dot_btn, 4, 2, 1, 1)

        eq_btn = QPushButton('=')
        eq_btn.setFixedSize(82, 56)
        eq_btn.setStyleSheet(
            'background-color: #FF9500; color: white; font-size: 20px; border-radius: 28px; border: none;'
        )
        eq_btn.clicked.connect(lambda checked, t='=': self.base_button_clicked(t))
        base_layout.addWidget(eq_btn, 4, 3, 1, 1)

        main_layout.addLayout(base_layout)
        self.setLayout(main_layout)

    # ---------- 이벤트: 공학용 연산(등호 후에도 new operand 방지) ------------
    def eng_button_clicked(self, button_text):
        try:
            value = float(self.calculator.display_value)
            if button_text == 'sin':
                result = self.calculator.sin_function(value)
            elif button_text == 'cos':
                result = self.calculator.cos_function(value)
            elif button_text == 'tan':
                result = self.calculator.tan_function(value)
            elif button_text == 'sinh':
                result = self.calculator.sinh_function(value)
            elif button_text == 'cosh':
                result = self.calculator.cosh_function(value)
            elif button_text == 'tanh':
                result = self.calculator.tanh_function(value)
            elif button_text == 'π':
                result = self.calculator.pi_constant()
            elif button_text == 'x²':
                result = self.calculator.square_function(value)
            elif button_text == 'x³':
                result = self.calculator.cube_function(value)
            else:
                return
            self.calculator.current_value = result
            self.calculator.display_value = self.format_number(result)
            self.calculator.waiting_for_operand = True
            self.calculator.just_evaluated = True  # <-- 등호와 동일하게 처리!
            self.update_display()
        except Exception:
            self.display.setText('오류')
            self.calculator.reset()

    # ---------- 이벤트: 기본 계산기 ------------
    def base_button_clicked(self, button_text):
        try:
            # 등호 직후 연산자/피연산자 구분
            if button_text in '0123456789':
                if self.calculator.just_evaluated:
                    # 등호 직후에 숫자 입력: 새로 입력 시작
                    self.calculator.display_value = button_text
                    self.calculator.current_value = float(button_text)
                    self.calculator.waiting_for_operand = False
                    self.calculator.pending_operation = None
                    self.calculator.just_evaluated = False
                else:
                    self.digit_clicked(button_text)
            elif button_text == '.':
                if self.calculator.just_evaluated:
                    self.calculator.display_value = '0.'
                    self.calculator.current_value = 0.0
                    self.calculator.waiting_for_operand = False
                    self.calculator.pending_operation = None
                    self.calculator.just_evaluated = False
                else:
                    self.decimal_clicked()
            elif button_text in '+-×÷':
                if self.calculator.just_evaluated:
                    self.calculator.pending_value = self.calculator.current_value
                    self.calculator.pending_operation = button_text
                    self.calculator.waiting_for_operand = True
                    self.calculator.just_evaluated = False
                else:
                    self.operation_clicked(button_text)
            elif button_text == '=':
                self.equals_clicked()
            elif button_text == 'AC':
                self.all_clear_clicked()
            elif button_text == '+/-':
                self.sign_clicked()
            elif button_text == '%':
                self.percent_clicked()
        except Exception:
            self.display.setText('오류')
            self.calculator.reset()

    def digit_clicked(self, digit):
        if self.calculator.waiting_for_operand:
            self.calculator.display_value = digit
            self.calculator.waiting_for_operand = False
        else:
            if len(self.calculator.display_value) < 15:
                self.calculator.display_value += digit
        self.calculator.current_value = float(self.calculator.display_value)
        self.update_display()

    def decimal_clicked(self):
        if self.calculator.waiting_for_operand:
            self.calculator.display_value = '0.'
            self.calculator.waiting_for_operand = False
        elif '.' not in self.calculator.display_value:
            self.calculator.display_value += '.'
        self.update_display()

    def operation_clicked(self, operation):
        if not self.calculator.waiting_for_operand:
            if self.calculator.pending_operation:
                result = self.calculator.equal()
                self.calculator.current_value = result
                self.calculator.display_value = self.format_number(result)
            self.calculator.pending_value = self.calculator.current_value
            self.calculator.pending_operation = operation
            self.calculator.waiting_for_operand = True
        self.update_display()

    def equals_clicked(self):
        if self.calculator.pending_operation:
            result = self.calculator.equal()
            self.calculator.current_value = result
            self.calculator.display_value = self.format_number(result)
            self.calculator.pending_operation = None
            self.calculator.waiting_for_operand = True
        else:
            self.calculator.just_evaluated = True
        self.update_display()

    def all_clear_clicked(self):
        self.calculator.reset()
        self.update_display()

    def sign_clicked(self):
        value = self.calculator.negative_positive(self.calculator.current_value)
        self.calculator.current_value = value
        self.calculator.display_value = self.format_number(value)
        self.calculator.just_evaluated = False
        self.update_display()

    def percent_clicked(self):
        value = self.calculator.percent(self.calculator.current_value)
        self.calculator.current_value = value
        self.calculator.display_value = self.format_number(value)
        self.calculator.just_evaluated = False
        self.update_display()

    def format_number(self, number):
        if number == int(number):
            return str(int(number))
        else:
            return f'{number:.10g}'

    def update_display(self):
        self.display.setText(self.calculator.display_value)

def main():
    app = QApplication(sys.argv)
    calculator = EngineeringCalculatorUI()
    calculator.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
