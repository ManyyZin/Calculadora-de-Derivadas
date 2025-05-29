import tkinter as tk
from tkinter import messagebox
from sympy import symbols, diff, integrate, sympify, lambdify, E
import numpy as np
import matplotlib.pyplot as plt

class CalculadoraMatematica:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Derivadas e Integrais")
        self.root.geometry("500x300")

        self.x = symbols('x')
        self.funcao = None

        self.criar_interface()

    def criar_interface(self):
        tk.Label(self.root, text="Digite a função f(x):", font=("Arial", 12)).pack(pady=5)
        self.entrada_funcao = tk.Entry(self.root, width=20, font=("Arial", 12))
        self.entrada_funcao.pack()

        tk.Label(self.root, text="Limite inferior (opcional):", font=("Arial", 10)).pack()
        self.entrada_limite_inferior = tk.Entry(self.root, width=20)
        self.entrada_limite_inferior.pack()

        tk.Label(self.root, text="Limite superior (opcional):", font=("Arial", 10)).pack()
        self.entrada_limite_superior = tk.Entry(self.root, width=20)
        self.entrada_limite_superior.pack()

        tk.Button(self.root, text="Calcular", command=self.calcular, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)

        self.resultado = tk.Label(self.root, text="", font=("Arial", 11), justify="left", wraplength=480)
        self.resultado.pack(pady=10)

        tk.Button(self.root, text="Visualizar Gráfico", command=self.mostrar_grafico, bg="#2196F3", fg="white", font=("Arial", 12)).pack(pady=5)

    def calcular(self):
        try:
            funcao_input = self.entrada_funcao.get()
            funcao_input = funcao_input.replace("^", "**").replace("e", "E")
            self.funcao = sympify(funcao_input)

            derivada1 = diff(self.funcao, self.x)
            derivada2 = diff(derivada1, self.x)
            integral_indef = integrate(self.funcao, self.x)

            limite_inferior = self.entrada_limite_inferior.get()
            limite_superior = self.entrada_limite_superior.get()

            integral_definida = "Não calculada"
            if limite_inferior and limite_superior:
                a = sympify(limite_inferior)
                b = sympify(limite_superior)
                integral_definida = integrate(self.funcao, (self.x, a, b))

            resultado_texto = f"""
Função: {funcao_input}

Derivada de 1ª ordem:
  {derivada1}

Derivada de 2ª ordem:
  {derivada2}

Integral indefinida:
  {integral_indef}

Integral definida:
  {integral_definida}
"""
            self.resultado.config(text=resultado_texto)

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    def mostrar_grafico(self):
        if self.funcao is None:
            messagebox.showinfo("Aviso", "Por favor, calcule uma função primeiro.")
            return

        try:
            f_lambd = lambdify(self.x, self.funcao, "numpy")
            x_vals = np.linspace(-10, 10, 400)
            y_vals = f_lambd(x_vals)

            plt.figure(figsize=(8, 5))
            plt.plot(x_vals, y_vals, label=f'f(x) = {self.funcao}')
            plt.axhline(0, color='black', linewidth=0.5)
            plt.axvline(0, color='red', linewidth=0.5)
            plt.title("Gráfico da Função")
            plt.xlabel("x")
            plt.ylabel("f(x)")
            plt.legend()
            plt.grid(True)
            plt.show()

        except Exception as e:
            messagebox.showerror("Erro no gráfico", f"Erro ao gerar gráfico: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraMatematica(root)
    root.mainloop()