# Librarymu/calculator_class.py
import ast

class Calculator:
    def evaluate(self, expression):
        try:
            # Gunakan pustaka ast untuk evaluasi ekspresi secara aman
            parsed_expression = ast.parse(expression, mode='eval')
            result = eval(compile(parsed_expression, filename='<string>', mode='eval'))
            return result
        except Exception as e:
            # Tangkap kesalahan dan kembalikan None jika terjadi kesalahan evaluasi
            return None
