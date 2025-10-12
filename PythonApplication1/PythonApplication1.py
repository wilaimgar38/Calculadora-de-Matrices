import numpy as np
import customtkinter as ctk
import tkinter as tk

# ==============================================================================
# CLASE 1: LÓGICA DE MATRICES (Backend con NumPy)
# ==============================================================================
class MatrixLogic:
    """Clase para manejar las operaciones matemáticas de matrices usando NumPy."""

    @staticmethod
    def list_to_numpy(matrix_data: list) -> np.ndarray:
        """Convierte una lista de listas de strings/floats a un array de NumPy."""
        try:
            # np.array con dtype=float maneja la conversión y los números decimales
            return np.array(matrix_data, dtype=float)
        except ValueError:
            raise ValueError("Error: Asegúrate de que todos los valores sean números válidos (solo números y puntos).")

    @staticmethod
    def get_determinant(matrix_data: list) -> str:
        """Calcula el determinante de una matriz."""
        matrix = MatrixLogic.list_to_numpy(matrix_data)
        
        # 1. Verificar si es cuadrada
        if matrix.shape[0] != matrix.shape[1]:
            return "Error: La matriz debe ser cuadrada para calcular el determinante."
        
        # 2. Calcular y formatear el resultado
        det = np.linalg.det(matrix)
        return f"Determinante = {det:.4f}" # Formateado a 4 decimales

    @staticmethod
    def add(matrix_data_a: list, matrix_data_b: list) -> str:
        """Suma dos matrices (A + B)."""
        matrix_a = MatrixLogic.list_to_numpy(matrix_data_a)
        matrix_b = MatrixLogic.list_to_numpy(matrix_data_b)

        # 1. Verificar compatibilidad de dimensiones
        if matrix_a.shape != matrix_b.shape:
            return "Error: Las matrices deben tener el mismo tamaño para la suma."

        # 2. Realizar la suma
        result = matrix_a + matrix_b 
        return f"Suma:\n{result}"

    @staticmethod
    def subtract(matrix_data_a: list, matrix_data_b: list) -> str:
        """Resta dos matrices (A - B)."""
        matrix_a = MatrixLogic.list_to_numpy(matrix_data_a)
        matrix_b = MatrixLogic.list_to_numpy(matrix_data_b)

        # 1. Verificar compatibilidad de dimensiones
        if matrix_a.shape != matrix_b.shape:
            return "Error: Las matrices deben tener el mismo tamaño para la resta."

        # 2. Realizar la resta
        result = matrix_a - matrix_b 
        return f"Resta:\n{result}"
        
    @staticmethod
    def multiply(matrix_data_a: list, matrix_data_b: list) -> str:
        """Multiplica dos matrices (A * B)."""
        matrix_a = MatrixLogic.list_to_numpy(matrix_data_a)
        matrix_b = MatrixLogic.list_to_numpy(matrix_data_b)

        # 1. Verificar compatibilidad (Columnas de A = Filas de B)
        if matrix_a.shape[1] != matrix_b.shape[0]:
            return "Error: Las columnas de la primera matriz deben ser iguales a las filas de la segunda para multiplicar."

        # 2. Realizar la multiplicación matricial usando el operador @
        result = matrix_a @ matrix_b
        return f"Multiplicación:\n{result}"

    @staticmethod
    def gauss_jordan(matrix_data: list) -> str:
        """
        Intenta obtener la inversa usando np.linalg.inv() como proxy para una
        matriz cuadrada no singular. La implementación completa de Gauss-Jordan
        para reducción por filas requiere lógica manual más compleja.
        """
        matrix = MatrixLogic.list_to_numpy(matrix_data)
        
        if matrix.shape[0] != matrix.shape[1]:
            return "Error: La matriz debe ser cuadrada para aplicar la inversa (proxy de Gauss-Jordan)."
            
        try:
            # Si el determinante es cero, la inversa falla y no hay solución única.
            if np.linalg.det(matrix) == 0:
                return "Error: La matriz es singular (determinante cero). No se puede invertir ni tiene solución única."
                
            inv = np.linalg.inv(matrix)
            return f"Inversa (Método de Gauss-Jordan aplicado para inversa):\n{inv}"
            
        except np.linalg.LinAlgError:
            return "Error: La matriz no es invertible."
        
# ==============================================================================
# CLASE 2: INTERFAZ GRÁFICA (Frontend con CustomTkinter)
# ==============================================================================
class MatrixApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de Matrices 🧮")
        self.geometry("1200x700")
        
        # Variables para almacenar los widgets de entrada de matrices
        self.matrix_A_entries = []
        self.matrix_B_entries = []

        # --- Configuración del Layout Principal ---
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure(2, weight=1) 

        # --- 1. Definición de Dimensiones (Fila 0) ---
        self.create_dimension_frame(row=0, col=0, label_text="Matriz A:", is_A=True)
        self.create_dimension_frame(row=0, col=1, label_text="Matriz B:", is_A=False)

        # --- 2. Contenedores de Matrices (Fila 1) ---
        self.matrix_A_container = self.create_matrix_container("MATRIZ A", row=1, col=0)
        self.matrix_B_container = self.create_matrix_container("MATRIZ B", row=1, col=1)

        # --- 3. Marco de Entrada de Comandos (Fila 1, Columna 2) ---
        self.create_command_frame(row=1, col=2)
        
        # --- 4. Área de Resultado (Fila 0, Columna 3) ---
        self.create_result_frame(row=0, col=3, rowspan=2)

        # Inicializar matrices 3x3 por defecto
        self.update_matrix_grid(self.matrix_A_container, 3, 3, is_A=True)
        self.update_matrix_grid(self.matrix_B_container, 3, 3, is_A=False)

    # --- MÉTODOS DE CREACIÓN DE WIDGETS ---

    def create_dimension_frame(self, row, col, label_text, is_A):
        """Crea el frame para que el usuario elija el tamaño de la matriz."""
        frame = ctk.CTkFrame(self)
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkLabel(frame, text=label_text).grid(row=0, column=0, padx=5, pady=5)

        rows_var = tk.IntVar(value=3)
        cols_var = tk.IntVar(value=3)

        ctk.CTkLabel(frame, text="Filas:").grid(row=0, column=1)
        rows_entry = ctk.CTkEntry(frame, width=50, textvariable=rows_var)
        rows_entry.grid(row=0, column=2, padx=5)

        ctk.CTkLabel(frame, text="Cols:").grid(row=1, column=1)
        cols_entry = ctk.CTkEntry(frame, width=50, textvariable=cols_var)
        cols_entry.grid(row=1, column=2, padx=5)

        update_command = lambda: self.handle_update_grid(
            rows_entry, cols_entry, self.matrix_A_container if is_A else self.matrix_B_container, is_A
        )
        ctk.CTkButton(frame, text="Establecer", command=update_command).grid(row=0, column=3, rowspan=2, padx=10)

    def create_matrix_container(self, title, row, col):
        """Crea el frame que contendrá las casillas de entrada (Entrys) de la matriz."""
        frame = ctk.CTkFrame(self)
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(frame, text=title, font=("Arial", 14, "bold")).pack(pady=5)
        
        matrix_grid_frame = ctk.CTkFrame(frame)
        matrix_grid_frame.pack(padx=10, pady=10, fill="both", expand=True)
        return matrix_grid_frame

    def create_command_frame(self, row, col):
        """Crea el marco para la entrada de comandos del usuario."""
        frame = ctk.CTkFrame(self)
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="ns")

        ctk.CTkLabel(frame, text="COMANDO", font=("Arial", 14, "bold")).pack(pady=10, padx=10)
        
        # Campo de entrada para la expresión (Ej: A + B)
        self.command_entry = ctk.CTkEntry(frame, width=200, placeholder_text="Ej: A + B, Det(B), A * B")
        self.command_entry.pack(pady=10, padx=10)
        
        # Botón de Cálculo
        ctk.CTkButton(frame, text="CALCULAR", command=self.process_command, width=200).pack(pady=10, padx=10)
        
        # Guía de uso
        guide_text = (
            "VARIABLES:\nA = Matriz A, B = Matriz B\n\n"
            "OPERACIONES:\n"
            "A + B (Suma)\n"
            "A - B (Resta)\n"
            "A * B (Multiplicación)\n"
            "Det(A) o Det(B) (Determinante)\n"
            "Gauss(A) o Gauss(B) (Inversa/Gauss)"
        )
        ctk.CTkLabel(frame, text=guide_text, justify=tk.LEFT).pack(pady=20, padx=10)


    def create_result_frame(self, row, col, rowspan):
        """Crea el frame y el widget de texto para mostrar el resultado."""
        frame = ctk.CTkFrame(self)
        frame.grid(row=row, column=col, rowspan=rowspan, padx=10, pady=10, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(frame, text="RESULTADO 📝", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10)
        self.result_text = ctk.CTkTextbox(frame, wrap="word")
        self.result_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    
    # --- MÉTODOS DE MANEJO DE MATRICES Y COMANDOS ---

    def handle_update_grid(self, rows_entry, cols_entry, container_frame, is_A):
        """Obtiene dimensiones, valida y actualiza la cuadrícula de entradas."""
        try:
            rows = int(rows_entry.get())
            cols = int(cols_entry.get())
            
            if rows <= 0 or cols <= 0:
                self.update_result("Error: Las dimensiones deben ser mayores a 0.")
                return
                
            self.update_matrix_grid(container_frame, rows, cols, is_A)
            self.update_result(f"Matriz {'A' if is_A else 'B'} redibujada a {rows}x{cols}.")
            
        except ValueError:
            self.update_result("Error: Por favor, ingrese números enteros para filas y columnas.")

    def update_matrix_grid(self, container_frame, rows, cols, is_A):
        """Crea una nueva cuadrícula de entradas Entry en el frame."""
        for widget in container_frame.winfo_children():
            widget.destroy()

        entry_list = []
        if is_A:
            self.matrix_A_entries = entry_list
        else:
            self.matrix_B_entries = entry_list
            
        for r in range(rows):
            row_entries = []
            for c in range(cols):
                entry = ctk.CTkEntry(container_frame, width=50, justify="center")
                entry.insert(0, "0") 
                entry.grid(row=r, column=c, padx=3, pady=3)
                row_entries.append(entry)
            entry_list.append(row_entries)
            
        for i in range(cols):
            container_frame.grid_columnconfigure(i, weight=1)

    def get_matrix_data(self, is_A: bool) -> list:
        """Extrae los valores de los Entry widgets como lista de listas de strings."""
        entries = self.matrix_A_entries if is_A else self.matrix_B_entries
        
        matrix_data = []
        for row_entries in entries:
            row_data = [entry.get() for entry in row_entries]
            matrix_data.append(row_data)
        return matrix_data

    def update_result(self, text: str):
        """Limpia el área de resultado y escribe el nuevo texto."""
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", str(text))

    def process_command(self):
        """Analiza el comando ingresado por el usuario y realiza la operación."""
        command = self.command_entry.get().strip().upper().replace(" ", "") # Limpieza y mayúsculas
        
        # 1. Obtener los datos de las matrices A y B
        try:
            matrix_a_data = self.get_matrix_data(is_A=True)
            matrix_b_data = self.get_matrix_data(is_A=False)
        except Exception as e:
            self.update_result(f"Error al leer matrices: {e}")
            return

        result = ""
        
        try:
            if "+" in command: # SUMA (Ej: A+B, B+A)
                parts = command.split('+')
                if parts == ['A', 'B'] or parts == ['B', 'A']:
                    result = MatrixLogic.add(matrix_a_data, matrix_b_data)
                else:
                    raise ValueError("Formato de suma inválido. Use A+B o B+A.")

            elif "-" in command: # RESTA (Ej: A-B, B-A)
                parts = command.split('-')
                if parts == ['A', 'B']:
                    result = MatrixLogic.subtract(matrix_a_data, matrix_b_data)
                elif parts == ['B', 'A']:
                    result = MatrixLogic.subtract(matrix_b_data, matrix_a_data)
                else:
                    raise ValueError("Formato de resta inválido. Use A-B o B-A.")
                    
            elif "X" in command or "*" in command: # MULTIPLICACIÓN (Ej: A*B, BXA)
                op = '*' if '*' in command else 'X'
                parts = command.split(op)

                if parts == ['A', 'B']:
                    result = MatrixLogic.multiply(matrix_a_data, matrix_b_data)
                elif parts == ['B', 'A']:
                    result = MatrixLogic.multiply(matrix_b_data, matrix_a_data) 
                else:
                    raise ValueError("Formato de multiplicación inválido. Use A*B o B*A.")

            elif command.startswith("DET(") and command.endswith(")"): # DETERMINANTE (Ej: DET(A))
                matrix_var = command[4:-1]
                if matrix_var == 'A':
                    result = MatrixLogic.get_determinant(matrix_a_data)
                elif matrix_var == 'B':
                    result = MatrixLogic.get_determinant(matrix_b_data)
                else:
                    raise ValueError("Variable de determinante inválida (solo A o B).")

            elif command.startswith("GAUSS(") and command.endswith(")"): # GAUSS-JORDAN (Ej: GAUSS(A))
                matrix_var = command[6:-1]
                if matrix_var == 'A':
                    result = MatrixLogic.gauss_jordan(matrix_a_data)
                elif matrix_var == 'B':
                    result = MatrixLogic.gauss_jordan(matrix_b_data)
                else:
                    raise ValueError("Variable de Gauss-Jordan inválida (solo A o B).")
            
            else:
                result = "Error: Comando no reconocido. Consulte la guía de operaciones."

            self.update_result(result)
            
        except ValueError as ve:
            self.update_result(f"Error de sintaxis: {ve}")
        except Exception as e:
            self.update_result(f"Error inesperado: {e}")


# ==============================================================================
# EJECUCIÓN PRINCIPAL
# ==============================================================================
if __name__ == "__main__":
    # Configuración de apariencia de CustomTkinter
    ctk.set_appearance_mode("System")  # Tema por defecto del sistema
    ctk.set_default_color_theme("blue") 
    
    app = MatrixApp()
    app.mainloop()

