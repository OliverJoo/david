import sys
# import math
from PyQt6.QtWidgets import (QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QVBoxLayout)
from PyQt6.QtCore import Qt
# from PyQt6.QtGui import QFont


# 문제 1. 계산기 제작
# 아이폰 계산기와 최대한 유사하게 계산기 UI를 만든다. 출력 형태 및 버튼의 배치는 동일하게 해야한다. 색상이나 버튼의 모양까지 동일할 필요는 없다.
# 각각의 버튼을 누를 때 마다 숫자가 입력 될 수 있게 이벤트를 처리한다.
# 이번 과제에서는 실제로 계산 기능까지 구현된 필요는 없다.

# 문제 2. 계산기의 기능 제작
# Calculator 클래스만들고 사칙 연산을 담당할 메소드인 add(), subtract(), multiply(), divide() 를 추가하고 동작할 수 있게 기능을 구현한다.
# Calculator 클래스에 추가로 초기화 및 음수양수, 퍼센트 등을 담당할 reset(), negative-positive(), percent() 메소드를 추가하고 기능을 구현한다.
# 숫자키를 누를 때 마다 화면에 숫자가 누적된다.
# 소수점 키를 누르면 소수점이 입력된다. 단 이미 소수점이 입력되어 있는 상태에서는 추가로 입력되지 않는다.
# Calculator 클래스에 결과를 출력할 equal() 메소드를 추가하고 기능을 구현한다.
# UI의 각 버튼과 Calculator 클래스를 연결해서 완전한 동작을 구현한다.
# 완성된 코드는 calculator.py 로 저장한다.

# 제약 사항
# 수학에서 발생할 수 있는 예외들이 다 적용되어 있어야 한다.
# 0을 나누면 안된다.
# 처리 할 수 있는 숫자의 범위가 넘어가면 에러 처리를 해야한다.
# 계산 기능들을 완성하기 위해서 math 등 외부 라이브러리를 사용 할 수 있다.

class Calculator:

    def __init__(self):
        self.reset()

    def reset(self):
        """계산기 초기화"""
        self.current_value = 0.0
        self.pending_value = 0.0
        self.pending_operation = None
        self.display_value = '0'
        self.waiting_for_operand = True

    def add(self, x, y):
        return x + y

    def subtract(self, x, y):
        return x - y

    def multiply(self, x, y):
        return x * y

    def divide(self, x, y):
        if y == 0:
            raise ValueError('0으로 나눌 수 없습니다')
        return x / y

    def negative_positive(self, value):
        return -value

    def percent(self, value):
        return value / 100

    def equal(self):
        """계산 결과 반환"""
        if self.pending_operation is None:
            return self.current_value

        try:
            if self.pending_operation == '+':
                result = self.add(self.pending_value, self.current_value)
            elif self.pending_operation == '-':
                result = self.subtract(self.pending_value, self.current_value)
            elif self.pending_operation == '×':
                result = self.multiply(self.pending_value, self.current_value)
            elif self.pending_operation == '÷':
                result = self.divide(self.pending_value, self.current_value)
            else:
                result = self.current_value

            # 숫자 범위 검사
            if abs(result) > 1e15:
                raise OverflowError('결과가 너무 큽니다')

            return result

        except (ValueError, OverflowError, ZeroDivisionError) as e:
            raise e


class CalculatorUI(QWidget):
    """계산기 UI 클래스"""

    def __init__(self):
        super().__init__()
        self.calculator = Calculator()
        self.init_ui()

    def init_ui(self):
        """UI 초기화 - 아이폰 계산기 스타일"""
        self.setWindowTitle('계산기')
        self.setFixedSize(320, 460)
        self.setStyleSheet('background-color: black;')

        # 메인 레이아웃
        main_layout = QVBoxLayout()
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # 디스플레이
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setText('0')
        self.display.setStyleSheet('''
            QLineEdit {
                background-color: black;
                color: white;
                font-size: 36px;
                font-weight: 300;
                border: none;
                padding: 20px;
            }
        ''')
        main_layout.addWidget(self.display)

        # 버튼 그리드
        button_layout = QGridLayout()
        button_layout.setSpacing(5)

        # 버튼 정의 (텍스트, 행, 열, 행스팬, 열스팬, 스타일)
        buttons = [
            ('AC', 0, 0, 1, 1, 'gray'),
            ('+/-', 0, 1, 1, 1, 'gray'),
            ('%', 0, 2, 1, 1, 'gray'),
            ('÷', 0, 3, 1, 1, 'orange'),
            ('7', 1, 0, 1, 1, 'dark_gray'),
            ('8', 1, 1, 1, 1, 'dark_gray'),
            ('9', 1, 2, 1, 1, 'dark_gray'),
            ('×', 1, 3, 1, 1, 'orange'),
            ('4', 2, 0, 1, 1, 'dark_gray'),
            ('5', 2, 1, 1, 1, 'dark_gray'),
            ('6', 2, 2, 1, 1, 'dark_gray'),
            ('-', 2, 3, 1, 1, 'orange'),
            ('1', 3, 0, 1, 1, 'dark_gray'),
            ('2', 3, 1, 1, 1, 'dark_gray'),
            ('3', 3, 2, 1, 1, 'dark_gray'),
            ('+', 3, 3, 1, 1, 'orange'),
            ('0', 4, 0, 1, 2, 'dark_gray'),  # 0 버튼은 2칸
            ('.', 4, 2, 1, 1, 'dark_gray'),
            ('=', 4, 3, 1, 1, 'orange'),
        ]

        # 버튼 스타일 정의
        button_styles = {
            'gray': '''
                QPushButton {
                    background-color: #A6A6A6;
                    color: black;
                    font-size: 20px;
                    font-weight: 500;
                    border-radius: 35px;
                    border: none;
                }
                QPushButton:pressed {
                    background-color: #8A8A8A;
                }
            ''',
            'dark_gray': '''
                QPushButton {
                    background-color: #333333;
                    color: white;
                    font-size: 20px;
                    font-weight: 500;
                    border-radius: 35px;
                    border: none;
                }
                QPushButton:pressed {
                    background-color: #1A1A1A;
                }
            ''',
            'orange': '''
                QPushButton {
                    background-color: #FF9500;
                    color: white;
                    font-size: 20px;
                    font-weight: 500;
                    border-radius: 35px;
                    border: none;
                }
                QPushButton:pressed {
                    background-color: #CC7700;
                }
            '''
        }

        # 버튼 생성 및 배치
        for button_text, row, col, rowspan, colspan, style in buttons:
            button = QPushButton(button_text)
            button.setFixedSize(70 if colspan == 1 else 145, 70)
            button.setStyleSheet(button_styles[style])
            button.clicked.connect(lambda checked, text=button_text: self.button_clicked(text))
            button_layout.addWidget(button, row, col, rowspan, colspan)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def button_clicked(self, button_text):
        try:
            if button_text in '0123456789':
                self.digit_clicked(button_text)
            elif button_text == '.':
                self.decimal_clicked()
            elif button_text in '+-×÷':
                self.operation_clicked(button_text)
            elif button_text == '=':
                self.equals_clicked()
            elif button_text == 'AC':
                self.all_clear_clicked()
            elif button_text == '+/-':
                self.sign_clicked()
            elif button_text == '%':
                self.percent_clicked()
        except Exception as e:
            self.display.setText('Undefined')
            self.calculator.reset()

    def digit_clicked(self, digit):
        """숫자 버튼 클릭 처리"""
        if self.calculator.waiting_for_operand:
            self.calculator.display_value = digit
            self.calculator.waiting_for_operand = False
        else:
            if len(self.calculator.display_value) < 15:  # 최대 자릿수 제한
                self.calculator.display_value += digit

        self.calculator.current_value = float(self.calculator.display_value)
        self.update_display()

    def decimal_clicked(self):
        """소수점 버튼 클릭 처리"""
        if self.calculator.waiting_for_operand:
            self.calculator.display_value = '0.'
            self.calculator.waiting_for_operand = False
        elif '.' not in self.calculator.display_value:
            self.calculator.display_value += '.'

        self.update_display()

    def operation_clicked(self, operation):
        """연산자 버튼 클릭 처리"""
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
        """등호 버튼 클릭 처리"""
        if self.calculator.pending_operation:
            result = self.calculator.equal()
            self.calculator.current_value = result
            self.calculator.display_value = self.format_number(result)
            self.calculator.pending_operation = None
            self.calculator.waiting_for_operand = True

        self.update_display()

    def all_clear_clicked(self):
        self.calculator.reset()
        self.update_display()

    def sign_clicked(self):
        value = self.calculator.negative_positive(self.calculator.current_value)
        self.calculator.current_value = value
        self.calculator.display_value = self.format_number(value)
        self.update_display()

    def percent_clicked(self):
        """퍼센트 버튼 클릭 처리"""
        value = self.calculator.percent(self.calculator.current_value)
        self.calculator.current_value = value
        self.calculator.display_value = self.format_number(value)
        self.update_display()

    def format_number(self, number):
        if number == int(number):
            return str(int(number))
        else:
            return f'{number:.10g}'  # 불필요한 소수점 제거

    def update_display(self):
        """디스플레이 업데이트"""
        self.display.setText(self.calculator.display_value)


def main():
    """메인 함수"""
    app = QApplication(sys.argv)
    calculator = CalculatorUI()
    calculator.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
