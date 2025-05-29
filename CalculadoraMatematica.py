# Importa as bibliotecas necessárias
import tkinter as tk  # Interface gráfica
from tkinter import messagebox  # Para exibir mensagens de erro
from sympy import symbols, diff, integrate, sympify, lambdify, E  # Biblioteca de cálculo simbólico
import numpy as np  # Biblioteca para cálculo numérico
import matplotlib.pyplot as plt  # Biblioteca para gráficos

# Classe principal da Calculadora
class CalculadoraMatematica:
    def __init__(self, root):
        self.root = root  # Janela principal
        self.root.title("Calculadora de Derivadas e Integrais")  # Título da janela
        self.root.geometry("500x300")  # Tamanho da janela

        self.x = symbols('x')  # Define a variável simbólica x
        self.funcao = None  # Armazena a função inserida pelo usuário

        self.criar_interface()  # Chama o método para criar a interface gráfica

    # Método para criar a interface gráfica
    def criar_interface(self):
        # Label para instrução de entrada da função
        tk.Label(self.root, text="Digite a função f(x):", font=("Arial", 12)).pack(pady=5)
        # Campo de entrada para a função
        self.entrada_funcao = tk.Entry(self.root, width=20, font=("Arial", 12))
        self.entrada_funcao.pack()

        # Label e entrada para o limite inferior da integral (opcional)
        tk.Label(self.root, text="Limite inferior (opcional):", font=("Arial", 10)).pack()
        self.entrada_limite_inferior = tk.Entry(self.root, width=20)
        self.entrada_limite_inferior.pack()

        # Label e entrada para o limite superior da integral (opcional)
        tk.Label(self.root, text="Limite superior (opcional):", font=("Arial", 10)).pack()
        self.entrada_limite_superior = tk.Entry(self.root, width=20)
        self.entrada_limite_superior.pack()

        # Botão que chama o método 'calcular'
        tk.Button(self.root, text="Calcular", command=self.calcular, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)

        # Label para exibir o resultado
        self.resultado = tk.Label(self.root, text="", font=("Arial", 11), justify="left", wraplength=480)
        self.resultado.pack(pady=10)

        # Botão para visualizar o gráfico
        tk.Button(self.root, text="Visualizar Gráfico", command=self.mostrar_grafico, bg="#2196F3", fg="white", font=("Arial", 12)).pack(pady=5)

    # Método que realiza os cálculos
    def calcular(self):
        try:
            # Pega o texto da entrada e substitui "^" por "**" para potenciação e "e" por "E" para o número de Euler
            funcao_input = self.entrada_funcao.get()
            funcao_input = funcao_input.replace("^", "**").replace("e", "E")
            # Converte o texto para uma expressão simbólica
            self.funcao = sympify(funcao_input)

            # Calcula derivadas de primeira e segunda ordem
            derivada1 = diff(self.funcao, self.x)
            derivada2 = diff(derivada1, self.x)
            # Calcula a integral indefinida
            integral_indef = integrate(self.funcao, self.x)

            # Pega os limites de integração, se fornecidos
            limite_inferior = self.entrada_limite_inferior.get()
            limite_superior = self.entrada_limite_superior.get()

            integral_definida = "Não calculada"
            # Se os limites forem fornecidos, calcula a integral definida
            if limite_inferior and limite_superior:
                a = sympify(limite_inferior)
                b = sympify(limite_superior)
                integral_definida = integrate(self.funcao, (self.x, a, b))

            # Monta o texto do resultado
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
            # Exibe o resultado no Label
            self.resultado.config(text=resultado_texto)

        except Exception as e:
            # Exibe mensagem de erro caso algo dê errado
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    # Método para gerar e exibir o gráfico da função
    def mostrar_grafico(self):
        if self.funcao is None:
            # Se nenhuma função foi calculada, avisa o usuário
            messagebox.showinfo("Aviso", "Por favor, calcule uma função primeiro.")
            return

        try:
            # Converte a função simbólica para função numérica para usar no gráfico
            f_lambd = lambdify(self.x, self.funcao, "numpy")
            # Cria valores de x de -10 a 10 com 400 pontos
            x_vals = np.linspace(-10, 10, 400)
            # Calcula os valores de y correspondentes
            y_vals = f_lambd(x_vals)

            # Configura o gráfico
            plt.figure(figsize=(8, 5))
            plt.plot(x_vals, y_vals, label=f'f(x) = {self.funcao}')
            plt.axhline(0, color='black', linewidth=0.5)  # Linha horizontal y=0
            plt.axvline(0, color='red', linewidth=0.5)  # Linha vertical x=0
            plt.title("Gráfico da Função")
            plt.xlabel("x")
            plt.ylabel("f(x)")
            plt.legend()
            plt.grid(True)
            plt.show()  # Exibe o gráfico

        except Exception as e:
            # Exibe erro se não conseguir gerar o gráfico
            messagebox.showerror("Erro no gráfico", f"Erro ao gerar gráfico: {e}")

# Bloco principal que inicia o programa
if __name__ == "__main__":
    root = tk.Tk()  # Cria a janela principal
    app = CalculadoraMatematica(root)  # Instancia a calculadora
    root.mainloop()  # Mantém a janela aberta
