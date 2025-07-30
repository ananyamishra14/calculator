import tkinter as tk
from tkinter import font as tkfont
import math
import re

class ScientificCalculator:

    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator By Ananya")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#2a2d36")

        # Calculator state
        self.expression = ""
        self.just_evaluated = False

        # Fonts and colors
        self.display_font = tkfont.Font(family="Arial", size=32)
        self.button_font = tkfont.Font(family="Arial", size=12)
        self.colors = {
            "bg": "#2a2d36",
            "display_bg": "#2a2d36",
            "text": "#ffffff",
            "num_bg": "#3b3e47",
            "op_bg": "#ff9f0a",
            "func_bg": "#2c2f38",
            "eq_bg": "#28a745",
            "del_bg": "#dc3545",
        }

        # Display
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        display_frame = tk.Frame(self.root, bg=self.colors["bg"])
        display_frame.pack(expand=True, fill="both")

        self.display = tk.Entry(
            display_frame, 
            textvariable=self.display_var, 
            font=self.display_font, 
            bg=self.colors["display_bg"],
            fg=self.colors["text"],
            bd=0, 
            justify="right",
            insertbackground=self.colors['text']
        )
        self.display.pack(expand=True, fill="both", padx=10, pady=20)
        
        # Buttons
        button_frame = tk.Frame(self.root, bg=self.colors["bg"])
        button_frame.pack(expand=True, fill="both")
        self.create_buttons(button_frame)

    def create_buttons(self, parent):
        buttons = [
            ('sin', 0, 0, 1, 'func'), ('cos', 0, 1, 1, 'func'), ('tan', 0, 2, 1, 'func'), ('log', 0, 3, 1, 'func'), ('ln', 0, 4, 1, 'func'),
            ('√', 1, 0, 1, 'func'), ('^', 1, 1, 1, 'op'), ('(', 1, 2, 1, 'func'), (')', 1, 3, 1, 'func'), ('C', 1, 4, 1, 'del'),
            ('7', 2, 0, 1, 'num'), ('8', 2, 1, 1, 'num'), ('9', 2, 2, 1, 'num'), ('/', 2, 3, 1, 'op'), ('DEL', 2, 4, 1, 'del'),
            ('4', 3, 0, 1, 'num'), ('5', 3, 1, 1, 'num'), ('6', 3, 2, 1, 'num'), ('*', 3, 3, 1, 'op'), ('x!', 3, 4, 1, 'op'),
            ('1', 4, 0, 1, 'num'), ('2', 4, 1, 1, 'num'), ('3', 4, 2, 1, 'num'), ('-', 4, 3, 1, 'op'), ('+', 4, 4, 1, 'op'),
            ('0', 5, 0, 2, 'num'), ('.', 5, 2, 1, 'num'), ('π', 5, 3, 1, 'num'), ('=', 5, 4, 1, 'eq')
        ]
        
        for i in range(6):
            parent.grid_rowconfigure(i, weight=1)
        for i in range(5):
            parent.grid_columnconfigure(i, weight=1)

        for (text, row, col, span, type) in buttons:
            bg_color = self.colors.get(f"{type}_bg", self.colors["num_bg"])
            button = tk.Button(
                parent, 
                text=text, 
                font=self.button_font,
                bg=bg_color,
                fg=self.colors["text"],
                relief="flat",
                command=lambda t=text: self.on_button_click(t)
            )
            button.grid(row=row, column=col, columnspan=span, sticky="nsew", padx=2, pady=2)

    def on_button_click(self, btn_text):
        if self.just_evaluated:
            if btn_text in ['+', '-', '*', '/', '^']:
                pass
            else:
                self.expression = ""
            self.just_evaluated = False

        if btn_text == 'C':
            self.expression = ""
        elif btn_text == 'DEL':
            self.expression = self.expression[:-1]
        elif btn_text == '=':
            self.evaluate_expression()
            return
        elif btn_text == 'x!':
            self.expression += '!'
        elif btn_text in ['sin', 'cos', 'tan', 'log', 'ln', '√']:
            self.expression += btn_text + '('
        else:
            if self.expression == "" and btn_text in '0123456789.π(':
                self.expression = btn_text
            elif self.expression == "0" and btn_text in '0123456789.π(':
                self.expression = btn_text
            else:
                self.expression += btn_text

        self.update_display()

    def update_display(self):
        self.display_var.set(self.expression if self.expression else "0")

    def evaluate_expression(self):
        eval_expr = self.expression
        try:
            def sin_deg(x): return math.sin(math.radians(x))
            def cos_deg(x): return math.cos(math.radians(x))
            def tan_deg(x): return math.tan(math.radians(x))

            safe_dict = {
                "sin": sin_deg, "cos": cos_deg, "tan": tan_deg,
                "log": math.log10, "ln": math.log, "sqrt": math.sqrt,
                "pi": math.pi, "e": math.e, "factorial": math.factorial
            }

            replacements = {
                '^': '**',
                '√': 'sqrt',
                'π': 'pi'
            }

            for old, new in replacements.items():
                eval_expr = eval_expr.replace(old, new)

            eval_expr = re.sub(r'(\d+\.?\d*)!', r'factorial(\1)', eval_expr)

            result = eval(eval_expr, {"__builtins__": None}, safe_dict)

            if isinstance(result, float) and result.is_integer():
                result = int(result)

            self.display_var.set(str(result))
            self.expression = str(result)
            self.just_evaluated = True

        except Exception:
            self.display_var.set("Error")
            self.expression = ""
            self.just_evaluated = True


if __name__ == "__main__":
    root = tk.Tk()
    calculator = ScientificCalculator(root)
    root.mainloop()
