import sys
import math
from PyQt6.QtWidgets import (
    QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QVBoxLayout, QLabel, QSizePolicy
)
# from PyQt6.QtCore import Qt
from calculator import Calculator, CalculatorUI

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

class EngineeringCalculatorUI(CalculatorUI):
    def __init__(self):
        super().__init__()
        self.calculator = EngineeringCalculator()
        self.setWindowTitle('공학용 계산기')
        self.setFixedSize(470, 720)  # 넓고 높게
        self._init_engineering_ui()

    def _init_engineering_ui(self):
        eng_layout = QGridLayout()
        eng_layout.setSpacing(14)
        eng_layout.setContentsMargins(10, 10, 10, 10)
        eng_btns = [
            ('x²', 0, 0), ('x³', 0, 1), ('sin', 0, 2), ('cos', 0, 3),
            ('tan', 1, 0), ('sinh',1,1), ('cosh',1,2), ('tanh',1,3),
            ('π', 2, 0)
        ]
        for text, r, c in eng_btns:
            btn = QPushButton(text)
            btn.setFixedSize(110, 52)
            btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            btn.setStyleSheet(
                'background-color: #007AFF; color: white; font-size: 19px; border-radius: 26px; border: none;'
            )
            btn.clicked.connect(lambda checked, t=text: self.eng_button_clicked(t))
            eng_layout.addWidget(btn, r, c)
        self.layout().insertLayout(1, eng_layout)

        self.layout().insertSpacing(2, 18)

        if isinstance(self.layout().itemAt(2), QGridLayout):
            self.layout().itemAt(2).setSpacing(12)

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
            self.calculator.just_evaluated = True
            self.update_display()
        except Exception:
            self.display.setText('오류')
            self.calculator.reset()

def main():
    app = QApplication(sys.argv)
    calculator = EngineeringCalculatorUI()
    calculator.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

# 출력: 공학 버튼/숫자 버튼 사이 공간 넓게, 각 버튼 크기도 실제 아이폰 공학용 계산기처럼 시원하게 분리됨
