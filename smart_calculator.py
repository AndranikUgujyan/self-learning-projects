"""
This is simple implementation of smart calculator
that can validate and evaluate input calculation request.
"""

operator_list = ['+', '-', '*', '/']
command_list = ["/exit", "/help"]


class Calculator:

    def var_def_dec(self):
        proc_string = input()
        proc_string = proc_string.strip()

        if proc_string == "/exit":
            return "Bye!"

        elif "^" in proc_string:
            proc_string = proc_string.replace("^", "**")

        elif "//" in proc_string:
            print("Invalid expression")
            return Calculator().var_def_dec()

        elif proc_string == "/help":
            print("The program calculates the sum of numbers")
            return Calculator().var_def_dec()

        elif "/" in proc_string \
                and proc_string.replace(" ", "").index("/") < 1:
            print("Unknown command")
            return Calculator().var_def_dec()

        elif "=" not in proc_string \
                and not proc_string.replace(" ", "")[0:3].isdigit() \
                and not proc_string.replace(" ", "")[0:3].isalpha() \
                and proc_string.replace(" ", "")[0:3].isalnum():
            print("Invalid identifier")
            return Calculator().var_def_dec()

        elif "=" in proc_string \
                and not proc_string.replace(" ", "")[:proc_string.replace(" ", "").index("=")].isalpha():
            print("Invalid identifier")
            return Calculator().var_def_dec()

        elif "=" in proc_string \
                and proc_string.replace(" ", "")[:proc_string.replace(" ", "").index("=")].isalpha() \
                and not proc_string.replace(" ", "")[proc_string.replace(" ", "").index("=") + 1:].isalpha() \
                and not proc_string.replace(" ", "")[proc_string.replace(" ", "").index("=") + 1:].isdigit():
            print("Invalid assignment")
            return Calculator().var_def_dec()

        elif not self.check_brackets(proc_string):
            print("Invalid expression")
            return Calculator().var_def_dec()

        try:
            if 1 < proc_string.replace(" ", "").count("="):
                print("Invalid assignment")
                return Calculator().var_def_dec()

            elif proc_string == " " \
                    or proc_string == "":
                return Calculator().var_def_dec()

            elif "=" in proc_string.replace(" ", ""):
                exec(proc_string, globals())
                return Calculator().var_def_dec()

            else:
                result = eval(proc_string)
                if isinstance(result, float) and result.is_integer() or result < 0:
                    print(int(result))
                else:
                    print(result)
                return Calculator().var_def_dec()

        except NameError:
            print("Unknown variable")
            return Calculator().var_def_dec()
        except SyntaxError:
            print("Invalid expression")
            return Calculator().var_def_dec()

    def check_brackets(self, expression):

        open_tup = tuple('(')
        close_tup = tuple(')')
        map_of_bracket = dict(zip(open_tup, close_tup))
        queue = []
        for i in expression:
            if i in open_tup:
                queue.append(map_of_bracket[i])
            elif i in close_tup:
                if not queue or i != queue.pop():
                    return False
        if not queue:
            return True

        else:
            return False


cal = Calculator()
print(cal.var_def_dec())
