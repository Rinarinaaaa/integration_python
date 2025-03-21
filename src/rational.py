import re

class RationalFunction:
    def __init__(self, rational_function):
        self.rational_function = rational_function
        self.type = {}
        self.variable = None

    def parse_fractionally_rational_function(self):
        rational_function_str = self.rational_function.replace(" ", "")

        type1_pattern = r"^([+-]?\d+)/\(([+-]?\d*)?([a-zA-Z])[+-]?(\d+)\)$"  # A / (kx - a)
        type2_pattern = r"^([+-]?\d+)/\(\(([+-]?\d*)?([a-zA-Z])[+-]?(\d+)\)\^(\d+)\)$"  # A / ((kx - a)^n)
        type3_pattern = r"^\(([+-]?\d*)?([a-zA-Z])([+-]\d+)\)/\(([a-zA-Z])\^2([+-]\d+[a-zA-Z][+-]\d+)\)$"  # (Mx + N) / (x^2 + px + q)
        type4_pattern = r"^\(([+-]?\d*)?([a-zA-Z])([+-]\d+)\)/\(\(([a-zA-Z])\^2([+-]\d+[a-zA-Z][+-]\d+)\)\^(\d+)\)$"  # (Mx + N) / ((x^2 + px + q)^n)
        type5_pattern = r"([+-]?\d*\.?\d*)([a-zA-Z])\^?(\d*)|([+-]?\d+\.?\d*)"  # Полином

        if '/' in rational_function_str:
            match = re.match(type1_pattern, rational_function_str)
            if match:
                A = int(match.group(1))
                k_str = match.group(2)
                k = int(k_str) if k_str and k_str not in ('+', '-') else (1 if not k_str else -1 if k_str == '-' else 1)
                variable = match.group(3)
                a = int(match.group(4))
                self.type = {"type": "I", "A": A, "k": k, "a": a, "variable": variable}
                return

            match = re.match(type2_pattern, rational_function_str)
            if match:
                A = int(match.group(1))
                k_str = match.group(2)
                k = int(k_str) if k_str and k_str not in ('+', '-') else (1 if not k_str else -1 if k_str == '-' else 1)
                variable = match.group(3)
                a = int(match.group(4))
                n = int(match.group(5))
                self.type = {"type": "II", "A": A, "k": k, "a": a, "n": n, "variable": variable}
                return

            match = re.match(type3_pattern, rational_function_str)
            if match:
                M = int(match.group(1)) if match.group(1) and match.group(1) not in ('+', '-') else 1
                variable = match.group(2)
                N = int(match.group(3))
                p_q = match.group(5)
                p, q = map(int, re.findall(r"[+-]?\d+", p_q))
                self.type = {"type": "III", "M": M, "N": N, "p": p, "q": q, "variable": variable}
                return

            match = re.match(type4_pattern, rational_function_str)
            if match:
                M = int(match.group(1)) if match.group(1) and match.group(1) not in ('+', '-') else 1
                variable = match.group(2)
                N = int(match.group(3))
                p_q = match.group(5)
                p, q = map(int, re.findall(r"[+-]?\d+", p_q))
                n = int(match.group(6))
                self.type = {"type": "IV", "M": M, "N": N, "p": p, "q": q, "n": n, "variable": variable}
                return

        else:
            matches = re.findall(type5_pattern, rational_function_str)
            if matches:
                coefficients = {}
                for match in matches:
                    coef_str, variable, power_str, const = match
                    if variable:
                        self.variable = variable
                        coef = float(coef_str) if coef_str and coef_str not in ("+", "-") else 1.0
                        if coef_str == "-":
                            coef = -1.0
                        power = int(power_str) if power_str else 1
                        coefficients[power] = coefficients.get(power, 0) + coef
                    elif const:
                        coef = float(const)
                        coefficients[0] = coefficients.get(0, 0) + coef
                self.type = {"type": "polynomial", "coefficients": coefficients, "variable": self.variable}
                return

        raise ValueError(f"Error: The expression `{rational_function_str}` does not match any known type.")

if __name__ == "__main__":
    test_cases = [
        # Полиномы
        ("4x^3 - 2x^2 + x - 7", "полином"),
        ("-x^2 + 3x - 5", "полином"),
        ("2x + 5", "полином"),
        ("7", "полином"),
        # Дробно-рациональные функции типа I
        ("7/(-x-2)", "I"),
        ("-5/(y+4)", "I"),
        ("100/(z-50)", "I"),
        # Дробно-рациональные функции типа II
        ("8/((-x+3)^4)", "II"),
        ("-9/((x-7)^2)", "II"),
        ("12/((z+1)^3)", "II"),
        # Дробно-рациональные функции типа III
        ("(5x+1)/(x^2-4x+4)", "III"),
        ("(-2x+7)/(x^2+3x+2)", "III"),
        ("(10y+5)/(y^2-6y+9)", "III"),
        ("(y+5)/(y^2-6y+9)", "III"),
        # Дробно-рациональные функции типа IV
        ("(3x-4)/((x^2+2x+1)^3)", "IV"),
        ("(x+5)/((x^2-5x+6)^2)", "IV"),
        ("(2y+8)/((y^2-3y+1)^5)", "IV"),
        # Ошибочные случаи
        ("(x+1)/(x^3+2x+1)", "Ошибка"),
        ("7/x^3", "Ошибка"),
        ("(x^2+3x+5)/(2x+1)", "Ошибка"),
    ]

    for expression, expected_type in test_cases:
        try:
            func = RationalFunction(expression)
            func.parse_fractionally_rational_function()
            print(f"✅ {expression} → {func.type}")
        except ValueError as e:
            print(f"❌ {expression} → {e}")