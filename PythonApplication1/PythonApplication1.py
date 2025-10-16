import numpy as np
import customtkinter as ctk
import tkinter as tk 
from tkinter import messagebox 
import random

#LÓGICA DE MATRICES (Backend con NumPy)

class MatrixLogic:
    #Clase para manejar las operaciones matemáticas de matrices usando NumPy.

    _FORMAT_OPTIONS = {
        'precision': 2, 
        'suppress_small': True,
        'separator': '  ',
    }

    @staticmethod
    def list_to_numpy(matrix_data: list) -> np.ndarray:
        """Convierte una lista de listas de strings/floats a un array de NumPy."""
        try:
            # np.array con dtype=float maneja la conversión y los números decimales
            return np.array(matrix_data, dtype=float) 
        except ValueError:
            raise ValueError("Asegúrate de que todos los valores sean números válidos (solo números y puntos).")

    @staticmethod
    def _format_matrix_string(np_array: np.ndarray) -> str:
        """Convierte la matriz de NumPy a un string limpio y bien espaciado."""
        formatted_str = np.array2string(np_array, **MatrixLogic._FORMAT_OPTIONS)
        cleaned_str = formatted_str.replace('[[', '').replace(']]', '')
        cleaned_str = cleaned_str.replace(' [', '\n').replace('[', '\n')
        cleaned_str = cleaned_str.replace(']', '')
        
        lines = [line.strip() for line in cleaned_str.split('\n') if line.strip()]
        return "\n".join(lines)

    @staticmethod
    def get_determinant_formatted(matrix_data: list) -> str:
        """Calcula y formatea el determinante para la interfaz."""
        try:
            matrix = MatrixLogic.list_to_numpy(matrix_data)
            if matrix.shape[0] != matrix.shape[1]:
                return "Error: La matriz debe ser cuadrada para calcular el determinante."
            
            det = np.linalg.det(matrix)
            return f"Determinante = {det:.2f}" 
        except ValueError as ve:
            return f"Error: {ve}"

    @staticmethod
    def add(matrix_data_a: list, matrix_data_b: list) -> str:
        """Suma dos matrices (A + B)."""
        try:
            matrix_a = MatrixLogic.list_to_numpy(matrix_data_a)
            matrix_b = MatrixLogic.list_to_numpy(matrix_data_b)
        except ValueError as ve:
            return f"Error: {ve}"

        if matrix_a.shape != matrix_b.shape:
            return "Error: Las matrices deben tener el mismo tamaño para la suma."

        result = matrix_a + matrix_b 
        formatted_result = MatrixLogic._format_matrix_string(result)
        return f"Suma:\n{formatted_result}"

    @staticmethod
    def subtract(matrix_data_a: list, matrix_data_b: list) -> str:
        """Resta dos matrices (A - B)."""
        try:
            matrix_a = MatrixLogic.list_to_numpy(matrix_data_a)
            matrix_b = MatrixLogic.list_to_numpy(matrix_data_b)
        except ValueError as ve:
            return f"Error: {ve}"

        if matrix_a.shape != matrix_b.shape:
            return "Error: Las matrices deben tener el mismo tamaño para la resta."

        result = matrix_a - matrix_b 
        formatted_result = MatrixLogic._format_matrix_string(result)
        return f"Resta:\n{formatted_result}"
        
    @staticmethod
    def multiply(matrix_data_a: list, matrix_data_b: list) -> str:
        """Multiplica dos matrices (A * B)."""
        try:
            matrix_a = MatrixLogic.list_to_numpy(matrix_data_a)
            matrix_b = MatrixLogic.list_to_numpy(matrix_data_b)
        except ValueError as ve:
            return f"Error: {ve}"

        if matrix_a.shape[1] != matrix_b.shape[0]:
            return "Error: Las columnas de la primera matriz deben ser iguales a las filas de la segunda para multiplicar."

        result = matrix_a @ matrix_b
        formatted_result = MatrixLogic._format_matrix_string(result)
        return f"Multiplicación:\n{formatted_result}"

        
# ==============================================================================
# CLASE 2: INTERFAZ GRÁFICA (Frontend con CustomTkinter)
# ==============================================================================
class MatrixApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de Matrices 🧮")
        self.geometry("1200x700")
        
        self.matrix_A_entries = []
        self.matrix_B_entries = []

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure(2, weight=1) 

        self.create_dimension_frame(row=0, col=0, label_text="Matriz A:", is_A=True)
        self.create_dimension_frame(row=0, col=1, label_text="Matriz B:", is_A=False)

        self.matrix_A_container = self.create_matrix_container("MATRIZ A", row=1, col=0)
        self.matrix_B_container = self.create_matrix_container("MATRIZ B", row=1, col=1)

        self.create_command_frame(row=1, col=2)
        
        self.create_result_frame(row=0, col=3, rowspan=2)

        self.update_matrix_grid(self.matrix_A_container, 3, 3, is_A=True)
        self.update_matrix_grid(self.matrix_B_container, 3, 3, is_A=False)


    def create_dimension_frame(self, row, col, label_text, is_A):
        frame = ctk.CTkFrame(self)
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1) # Aumentar columnas

        ctk.CTkLabel(frame, text=label_text).grid(row=0, column=0, padx=5, pady=5)

        rows_var = tk.IntVar(value=3)
        cols_var = tk.IntVar(value=3)

        ctk.CTkLabel(frame, text="Filas:").grid(row=0, column=1)
        rows_entry = ctk.CTkEntry(frame, width=50, textvariable=rows_var)
        rows_entry.grid(row=0, column=2, padx=5)

        ctk.CTkLabel(frame, text="Cols:").grid(row=1, column=1)
        cols_entry = ctk.CTkEntry(frame, width=50, textvariable=cols_var)
        cols_entry.grid(row=1, column=2, padx=5)

        # Botón para ESTABLECER dimensiones
        update_command = lambda: self.handle_update_grid(
            rows_entry, cols_entry, self.matrix_A_container if is_A else self.matrix_B_container, is_A
        )
        ctk.CTkButton(frame, text="Establecer", command=update_command).grid(row=0, column=3, rowspan=2, padx=5)
        
        # Botón para LLENAR CON ALEATORIOS
        random_command = lambda: self.fill_random_data(is_A=is_A)
        ctk.CTkButton(frame, text="Aleatorio", command=random_command).grid(row=0, column=4, rowspan=2, padx=5)


    def create_matrix_container(self, title, row, col):
        frame = ctk.CTkFrame(self)
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(frame, text=title, font=("Arial", 14, "bold")).pack(pady=5)
        
        matrix_grid_frame = ctk.CTkFrame(frame)
        matrix_grid_frame.pack(padx=10, pady=10, fill="both", expand=True)
        return matrix_grid_frame

    def create_command_frame(self, row, col):
        """Crea el marco para la SELECCIÓN de comandos del usuario (ComboBox)."""
        frame = ctk.CTkFrame(self)
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="ns")

        ctk.CTkLabel(frame, text="OPERACIÓN", font=("Arial", 14, "bold")).pack(pady=10, padx=10)
        
        command_options = [
            "A + B", "A - B", "B - A", 
            "A * B", "B * A", 
            "Det(A)", "Det(B)",
            "Gauss(A)", "Gauss(B)"
        ]

        # Campo de SELECCIÓN para la expresión (SIN el parámetro 'command')
        self.command_combobox = ctk.CTkComboBox(
            frame, 
            values=command_options, 
            width=200, 
        )
        self.command_combobox.set("Seleccionar Operación")
        self.command_combobox.pack(pady=10, padx=10)
        
        # El botón es el ÚNICO que llama a self.process_command
        ctk.CTkButton(frame, text="CALCULAR", command=self.process_command, width=200).pack(pady=10, padx=10)
        
        guide_text = (
            "Seleccione una operación del menú superior:\n\n"
            "A, B = Matrices de entrada\n"
            "+, -, * = Suma, Resta, Multiplicación\n"
            "Det() = Determinante\n"
            "Gauss() = Inversa (Gauss-Jordan)"
        )
        ctk.CTkLabel(frame, text=guide_text, justify="left").pack(pady=20, padx=10)


    def create_result_frame(self, row, col, rowspan):
        frame = ctk.CTkFrame(self)
        frame.grid(row=row, column=col, rowspan=rowspan, padx=10, pady=10, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(frame, text="RESULTADO 📝", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10)
        self.result_text = ctk.CTkTextbox(frame, wrap="word")
        self.result_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    
    def handle_update_grid(self, rows_entry, cols_entry, container_frame, is_A):
        try:
            rows = int(rows_entry.get())
            cols = int(cols_entry.get())
            
            if rows <= 0 or cols <= 0:
                self.update_result("Error: Las dimensiones deben ser mayores a 0.")
                messagebox.showerror("Error de Dimensión", "Error: Las dimensiones deben ser mayores a 0.")
                return
                
            self.update_matrix_grid(container_frame, rows, cols, is_A)
            self.update_result(f"Matriz {'A' if is_A else 'B'} redibujada a {rows}x{cols}.")
            
        except ValueError:
            self.update_result("Error: Por favor, ingrese números enteros para filas y columnas.")
            messagebox.showerror("Error de Entrada", "Error: Por favor, ingrese números enteros para filas y columnas.")

    def update_matrix_grid(self, container_frame, rows, cols, is_A):
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

    # ======================================================================
    # NUEVO MÉTODO: LLENAR CON DATOS ALEATORIOS
    # ======================================================================
    def fill_random_data(self, is_A: bool):
        """Llena la matriz con números enteros aleatorios entre 0 y 9."""
        entries = self.matrix_A_entries if is_A else self.matrix_B_entries
        matrix_name = "A" if is_A else "B"
        
        if not entries:
            self.update_result(f"Error: La Matriz {matrix_name} no está inicializada o tiene dimensiones 0x0.")
            messagebox.showwarning("Error de Llenado", f"Error: La Matriz {matrix_name} no está inicializada o tiene dimensiones 0x0.")
            return

        for row_entries in entries:
            for entry in row_entries:
                # 1. Limpiar el contenido actual
                entry.delete(0, tk.END) 
                # 2. Insertar un nuevo número aleatorio (entero entre 0 y 9)
                random_number = random.randint(0, 9)
                entry.insert(0, str(random_number))

        self.update_result(f"Matriz {matrix_name} llenada con números aleatorios.")

    def get_matrix_data(self, is_A: bool) -> list:
        entries = self.matrix_A_entries if is_A else self.matrix_B_entries
        
        matrix_data = []
        for row_entries in entries:
            row_data = [entry.get() for entry in row_entries]
            matrix_data.append(row_data)
        return matrix_data

    def update_result(self, text: str):
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", str(text))

    def _process_gauss_jordan(self, matrix_data: list):
        """Maneja el proceso de Gauss-Jordan, incluyendo la confirmación con pop-up."""
        try:
            matrix = MatrixLogic.list_to_numpy(matrix_data)
        except ValueError as ve:
            self.update_result(f"Error: {ve}")
            messagebox.showerror("Error de Datos", f"Error: {ve}")
            return
            
        if matrix.shape[0] != matrix.shape[1]:
            msg = "Error: La matriz debe ser cuadrada para aplicar Gauss-Jordan/Inversa."
            self.update_result(msg)
            messagebox.showerror("Error de Forma", msg)
            return

        try:
            det = np.linalg.det(matrix)
            
            if np.isclose(det, 0.0):
                msg = "¡ADVERTENCIA! El determinante es cero. La matriz es singular y NO tiene inversa."
                self.update_result(msg)
                messagebox.showwarning("Advertencia (Matriz Singular)", msg)
                return
            else:
                msg_confirm = (
                    f"La matriz es invertible (Determinante = {det:.2f}).\n\n"
                    "¿Desea proceder con el cálculo del Método de Gauss-Jordan (Inversa)?"
                )
                
                if messagebox.askyesno("Confirmar Operación", msg_confirm):
                    inv = np.linalg.inv(matrix)
                    formatted_inv = MatrixLogic._format_matrix_string(inv)
                    self.update_result(f"RESULTADO DE LA INVERSA (Gauss-Jordan):\n{formatted_inv}")
                else:
                    self.update_result("Proceso de Gauss-Jordan cancelado por el usuario.")
            
        except np.linalg.LinAlgError:
            msg = "Error: Falló el cálculo del determinante o la inversa."
            self.update_result(msg)
            messagebox.showerror("Error de Cálculo", msg)
    
    def process_command(self, selection=None):
        """Analiza el comando seleccionado por el usuario y realiza la operación."""
        command = self.command_combobox.get().strip().upper() 
        
        if command == "SELECCIONAR OPERACIÓN":
            self.update_result("Por favor, seleccione una operación del menú y presione CALCULAR.")
            return

        try:
            matrix_a_data = self.get_matrix_data(is_A=True)
            matrix_b_data = self.get_matrix_data(is_A=False)
        except Exception as e:
            error_msg = f"Error al leer matrices: {e}"
            self.update_result(error_msg)
            messagebox.showerror("Error de Lectura", error_msg)
            return

        result = ""
        
        try:
            if command == "A + B":
                result = MatrixLogic.add(matrix_a_data, matrix_b_data)
            elif command == "A - B":
                result = MatrixLogic.subtract(matrix_a_data, matrix_b_data)
            elif command == "B - A":
                result = MatrixLogic.subtract(matrix_b_data, matrix_a_data) 
            elif command == "A * B":
                result = MatrixLogic.multiply(matrix_a_data, matrix_b_data)
            elif command == "B * A":
                result = MatrixLogic.multiply(matrix_b_data, matrix_a_data) 
            elif command == "DET(A)":
                result = MatrixLogic.get_determinant_formatted(matrix_a_data)
            elif command == "DET(B)":
                result = MatrixLogic.get_determinant_formatted(matrix_b_data)
            
            elif command == "GAUSS(A)":
                self._process_gauss_jordan(matrix_a_data)
                return 
            elif command == "GAUSS(B)":
                self._process_gauss_jordan(matrix_b_data)
                return 
            
            else:
                result = "Error: Operación no reconocida."

            self.update_result(result) 
            if isinstance(result, str):
                if result.startswith("Error:"):
                    messagebox.showerror("Error de Operación", result)
                elif result.startswith("¡ADVERTENCIA!"):
                    messagebox.showwarning("Advertencia", result)
            
        except ValueError as ve:
            error_msg = f"Error de datos: {ve}"
            self.update_result(error_msg)
            messagebox.showerror("Error de Datos", error_msg)
        except Exception as e:
            error_msg = f"Error inesperado en la operación: {e}"
            self.update_result(error_msg)
            messagebox.showerror("Error Inesperado", error_msg)

# EJECUCIÓN PRINCIPAL

if __name__ == "__main__":
    # Cambia el modo de apariencia a "Dark" (Oscuro)
    ctk.set_appearance_mode("Dark") 
    # Puedes mantener el tema de color para los botones y elementos interactivos
    ctk.set_default_color_theme("blue") 
    
    app = MatrixApp()
    app.mainloop()
