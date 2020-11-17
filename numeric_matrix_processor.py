"""
This is simple implementation of operations on matrices addition,
multiplication, finding the determinant, and dealing with inverse matrices.
"""

import sys

import numpy as np

Menu = "1. Add matrices\n" \
       "2. Multiply matrix by a constant\n" \
       "3. Multiply matrices\n" \
       "4. Transpose matrix\n" \
       "5. Calculate a determinant\n" \
       "6. Inverse matrix\n" \
       "0. Exit"

Transpose_menu = "1. Main diagonal\n" \
                 "2. Side diagonal\n" \
                 "3. Vertical line\n" \
                 "4. Horizontal line"


class MatrixProcessor:

    def matrix_menu(self):
        print(Menu)
        print("Your choice:")
        choice = input()
        if int(choice) == 1:
            print(self.matrix_addition())
            return self.matrix_menu()
        elif int(choice) == 2:
            print(self.mult_matrices_constant())
            return self.matrix_menu()
        elif int(choice) == 3:
            print(self.multiply_matrices())
            return self.matrix_menu()
        elif int(choice) == 4:
            print(self.transpose_matrices())
            return self.matrix_menu()
        elif int(choice) == 5:
            print(self.determinant_calculation())
            return self.matrix_menu()
        elif int(choice) == 6:
            print(self.inverse_matrix())
            return self.matrix_menu()
        elif int(choice) == 0:
            sys.exit()
        else:
            print("Wrong choice, try again")
            return self.matrix_menu

    def inverse_matrix(self):
        print("Enter size of matrix:")
        inverse_matrix_size = input()
        matrix_for_inversing = self.matrix_creation(inverse_matrix_size)
        inversed_matrix = np.linalg.inv(matrix_for_inversing)
        result = self.matrix_2_sting(inversed_matrix)
        return result

    def determinant_calculation(self):
        print("Enter matrix size:")
        dc_matrix_size = input()
        matrix_for_det_cal = self.matrix_creation(dc_matrix_size)
        result = np.linalg.det(matrix_for_det_cal)
        print("The result is:")
        return result

    def transpose_matrices(self):
        print(Transpose_menu)
        print("Your choice:")
        transpose_choice = input()
        if int(transpose_choice) == 1:
            return self.main_diagonal_transpose()
        elif int(transpose_choice) == 2:
            return self.side_diagonal_transpose()
        elif int(transpose_choice) == 3:
            return self.vertical_line_transpose()
        elif int(transpose_choice) == 4:
            return self.horizontal_line_transpose()
        else:
            print("Wrong choice, try again")
            return self.transpose_matrices

    def main_diagonal_transpose(self):
        print("Enter size of matrix:")
        mdt_matrix_size = input()
        matrix_for_mdt = self.matrix_creation(mdt_matrix_size)
        mdt_matrix = [[matrix_for_mdt[element_index][vector_index] for element_index in
                       range(len(matrix_for_mdt[vector_index]))] for vector_index in
                      range(len(matrix_for_mdt))]
        result = self.matrix_2_sting(mdt_matrix)
        return result

    def side_diagonal_transpose(self):
        print("Enter size of matrix:")
        sdt_matrix_size = input()
        matrix_for_sdt = self.matrix_creation(sdt_matrix_size)
        sdt_matrix = [[matrix_for_sdt[::-1][element_index][vector_index] for element_index in
                       range(len(matrix_for_sdt[vector_index]))] for vector_index in
                      range(len(matrix_for_sdt))][::-1]
        result = self.matrix_2_sting(sdt_matrix)
        return result

    def vertical_line_transpose(self):
        print("Enter size of matrix:")
        vlt_matrix_size = input()
        matrix_for_vlt = self.matrix_creation(vlt_matrix_size)
        vlt_matrix = [vector[::-1] for vector in matrix_for_vlt]
        result = self.matrix_2_sting(vlt_matrix)
        return result

    def horizontal_line_transpose(self):
        print("Enter size of matrix:")
        hlt_matrix_size = input()
        matrix_for_hlt = self.matrix_creation(hlt_matrix_size)
        hlt_matrix = matrix_for_hlt[::-1]
        result = self.matrix_2_sting(hlt_matrix)
        return result

    def multiply_matrices(self):
        print("Enter size of first matrix:")
        first_matrix_size = input()
        first_matrix = self.matrix_creation(first_matrix_size)
        print("Enter size of second matrix:")
        second_matrix_size = input()
        second_matrix = self.matrix_creation(second_matrix_size)
        if first_matrix_size.split()[1] == second_matrix_size.split()[0]:

            final_matrix = [[sum(a * b for a, b in zip(X_row, Y_col)) for
                             Y_col in zip(*second_matrix)] for X_row in first_matrix]

            result = self.matrix_2_sting(final_matrix)
            return result
        else:
            return "ERROR"

    def matrix_addition(self):
        output_result = ""
        final_matrix = []
        print("Enter size of first matrix:")
        first_matrix_size = input()
        first_matrix = self.matrix_creation(first_matrix_size)
        print("Enter size of second matrix:")
        second_matrix_size = input()
        second_matrix = self.matrix_creation(second_matrix_size)
        if first_matrix_size.split() == second_matrix_size.split():
            for row_number in range(int(first_matrix_size[0])):
                added_list = [str((value + second_matrix[row_number][index]))
                              for index, value in enumerate(first_matrix[row_number])]
                added_list[-1] = added_list[-1] + "\n"
                output_result += " ".join(added_list)
                final_matrix.append(added_list)
            output_result.replace("", "\n")
            print("The result is:")
            return output_result
        else:
            return "ERROR"

    def mult_matrices_constant(self):
        output_result = ""
        final_matrix = []
        print("Enter size of matrix:")
        entered_matrix_size = input()
        entered_matrix = self.matrix_creation(entered_matrix_size)
        print("Enter constant:")
        entered_constant = input()
        if "." in entered_constant:
            entered_constant = float(entered_constant)
        else:
            entered_constant = int(entered_constant)
        for row_number in range(int(entered_matrix_size[0])):
            added_list = [str((value * entered_constant)) for value in entered_matrix[row_number]]
            added_list[-1] = added_list[-1] + "\n"
            output_result += " ".join(added_list)
            final_matrix.append(added_list)
            output_result.replace("", "\n")
        print("The result is:")
        return output_result

    @staticmethod
    def matrix_creation(input_first):
        matrix = []
        shape = [int(shape) for shape in input_first.split()]
        print("Enter constant:")
        for row in range(shape[0]):
            row_value = input()
            row_list = row_value.split()
            if len(row_list) == shape[1]:
                row_list_int = [float(row) if "." in row else int(row) for row in row_list]
                matrix.append(row_list_int)
            else:
                return False
        return matrix

    @staticmethod
    def matrix_2_sting(matrix_for_print):
        matrix_in_string_format = ""
        for vector in matrix_for_print:
            str_vector = [str(element) for element in vector]
            str_vector[-1] = str_vector[-1] + "\n"
            matrix_in_string_format += " ".join(str_vector)
        print("The result is:")
        return matrix_in_string_format


mp = MatrixProcessor()
print(mp.matrix_menu())
