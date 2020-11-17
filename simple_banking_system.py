"""
This is simple banking system implementation by Luhn algorithm and sqlite3.
"""

"""
Issuer Identification Number - Iin
Credit Card numbers - Ccn
Customer Account Number - can
"""
from random import randint
import sqlite3 as sl

Iin = 400000
Ccn_length = 16
Menu = "1. Create an account\n2. Log into account\n0. Exit"
Balance_menu = "1. Balance\n2. Add income\n3. Do transfer" \
               "\n4. Close account\n5. Log out\n0. Exit"

Card_db_name = "card.s3db"


class BankingSystem:
    def __init__(self):
        self.flag = True

    def ds_start(self):
        if self.create_db():
            return self.bank_system()
        else:
            return "DB already"

    def bank_system(self):
        print(Menu)
        user_input_1 = int(input())
        self.ds_start()
        if user_input_1 == 1:
            self.create_an_account()
            return self.bank_system()
        elif user_input_1 == 2:
            print("Enter your card number:")
            input_card_number = str(input())
            print("Enter your PIN:")
            input_pin = int(input())
            db_dat = self.take_val(input_card_number, input_pin)
            if db_dat:
                print("You have successfully logged in!\n")
                return self.account_menu(input_card_number, input_pin, db_dat[2])
            else:
                print("Wrong card number or PIN!\nTry again\n")
                return self.bank_system()
        elif user_input_1 == 0:
            return "Bye"
        else:
            print("Wrong input")
            return self.bank_system()

    def account_menu(self, card_number_imputed, pin_number_imputed, value_of_balance):

        print(Balance_menu)
        balance_input = int(input())
        if balance_input == 1:
            balance_value = self.take_val(card_number_imputed, pin_number_imputed)
            print(balance_value)
            return self.account_menu(card_number_imputed, pin_number_imputed, value_of_balance)
        elif balance_input == 2:
            print("Enter income:")
            add_income = int(input())
            result = self.change_val(card_number_imputed, pin_number_imputed, add_income)
            print(result)
            return self.account_menu(card_number_imputed, pin_number_imputed, value_of_balance)
        elif balance_input == 3:
            # print("Transfer\nEnter card number:")
            # number_for_transfer = int(input())
            result = self.transfer(card_number_imputed)
            print(result)
            return self.account_menu(card_number_imputed, pin_number_imputed, value_of_balance)
        elif balance_input == 4:
            result = self.delete_account(card_number_imputed, pin_number_imputed)
            print(result)
            return self.bank_system()
        elif balance_input == 5:
            return self.bank_system()
        elif balance_input == 0:
            return False
            # return "Bye"
        else:
            print("Wrong input")
            return self.account_menu(card_number_imputed, pin_number_imputed, value_of_balance)

    def create_an_account(self):
        gen_card_numb = self.generate_card_number()
        if self.luhn_algorithm(gen_card_numb):
            pin = randint(1000, 9999)
            self.fill_db(gen_card_numb, pin)
            result = "Your card has been created\nYour card number:" \
                     "\n{}\nYour card PIN:\n{}\n".format(gen_card_numb, pin)
            print(result)

            return result
        else:
            self.create_an_account()

    def generate_card_number(self):
        can_length = Ccn_length - len(str(Iin))
        iin_range_start = 10 ** (can_length - 1)
        iin_range_end = (10 ** can_length) - 1
        can = randint(iin_range_start, iin_range_end)
        ccn = str(Iin) + str(can)
        return int(ccn)

    def luhn_algorithm(self, identification_numbers):
        identification_numbers_in_list = list(map(int, str(identification_numbers)))
        last_digit_dropping = identification_numbers_in_list[:-1]
        numbers_of_last_digit = identification_numbers_in_list[-1]
        for number_index, number in enumerate(last_digit_dropping):
            if (number_index + 1) % 2 != 0:
                last_digit_dropping[number_index] = number * 2
        for each_number in last_digit_dropping:
            if 9 < each_number:
                needed_index = last_digit_dropping.index(each_number)
                last_digit_dropping[needed_index] = each_number - 9
        if (sum(last_digit_dropping) + numbers_of_last_digit) % 10 == 0:
            return True
        else:
            return False

    def create_db(self, db_name=Card_db_name):
        try:
            if self.flag:
                conn = sl.connect(db_name)
                cursor = conn.cursor()
                cursor.execute('''CREATE TABLE card
                         (id INTEGER,
                         number TEXT,
                         pin TEXT,
                         balance INTEGER DEFAULT 0);''')
                conn.commit()
                conn.close()
                self.flag = False
                return True
        except sl.OperationalError:
            return False

    def fill_db(self, card_number_value, card_pin_val):
        conn = sl.connect(Card_db_name)
        cursor = conn.cursor()
        sql = 'INSERT INTO card (number,pin) values(?, ?)'
        cursor.execute(sql, (str(card_number_value), str(card_pin_val)))
        conn.commit()
        conn.close()
        return "Done"

    def take_val(self, imputed_card_number, imputed_card_pin):
        conn = sl.connect(Card_db_name)
        cursor = conn.cursor()
        for row in cursor.execute(
                "SELECT number, pin, balance from card WHERE number={} AND pin={}".format(imputed_card_number,
                                                                                          imputed_card_pin)):
            conn.commit()
            conn.close()
            result = "Balance: {}\n".format(row[2])
            return result

    def change_val(self, imputed_card_number_for_income,
                   imputed_card_pin_for_income,
                   imputed_income):
        conn = sl.connect(Card_db_name)
        cursor = conn.cursor()
        cursor.execute("UPDATE card SET balance = balance + {} WHERE number={} AND pin={};".format(imputed_income,
                                                                                                   imputed_card_number_for_income,
                                                                                                   imputed_card_pin_for_income))
        conn.commit()
        conn.close()
        return "Income was added!"

    def transfer(self, current_card_number):
        print("Transfer\nEnter card number:")
        number_for_transfer = int(input())
        if self.luhn_algorithm(number_for_transfer):
            conn = sl.connect(Card_db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT pin, balance from card WHERE number={};".format(number_for_transfer))
            result = cursor.fetchone()
            if result:
                data_for_transfer = cursor.execute(
                    "SELECT balance from card WHERE number={};".format(current_card_number))
                for row in data_for_transfer:
                    balance = row[0]
                    print("Enter how much money you want to transfer:")
                    money_for_transfer = int(input())
                    if money_for_transfer <= balance:
                        cursor.execute("UPDATE card SET balance = balance + {} "
                                       "WHERE number={};".format(money_for_transfer, number_for_transfer))
                        cursor.execute("UPDATE card SET balance = balance - {} "
                                       "WHERE number={};".format(money_for_transfer, current_card_number))
                        conn.commit()
                        conn.close()
                        return "Success!"
                    else:
                        conn.commit()
                        conn.close()
                        return "Not enough money!"
            else:
                conn.commit()
                conn.close()
                return "Such a card does not exist."
        else:
            return "Probably you made mistake in card number. Please try again!"

    def delete_account(self, val_card_number, val_card_pin_val):
        conn = sl.connect(Card_db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM card WHERE number = {} AND pin = {};".format(val_card_number, val_card_pin_val))
        conn.commit()
        conn.close()
        return "The account has been closed!"


bs = BankingSystem()
print(bs.bank_system())
