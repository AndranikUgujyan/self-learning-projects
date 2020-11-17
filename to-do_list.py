"""
This is simple implementation of To-Do list
base of SQLAlchemy to manage SQLite database on python.
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime, timedelta

Menu = "1) Today's tasks\n" \
       "2) Week's tasks\n" \
       "3) All tasks\n" \
       "4) Missed tasks\n" \
       "5) Add task\n" \
       "6) Delete task\n" \
       "0) Exit"

Engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(Engine)
Session = sessionmaker(bind=Engine)
session = Session()


class ToDo:

    def to_do_menu(self):
        print(Menu)
        choice = int(input())
        if choice == 1:
            print(self.today_task())
            return self.to_do_menu()
        elif choice == 2:
            print(self.week_tasks())
            return self.to_do_menu()
        elif choice == 3:
            print(self.all_tasks())
            return self.to_do_menu()
        elif choice == 4:
            print(self.missed_tasks())
            return self.to_do_menu()
        elif choice == 5:
            print(self.add_task())
            return self.to_do_menu()
        elif choice == 6:
            print(self.delete_task())
            return self.to_do_menu()
        elif choice == 0:
            return "Bye!"
        else:
            print("Wrong input, try again")
            return self.to_do_menu()

    def today_task():
        today = datetime.today()
        rows = session.query(Table).filter(Table.deadline == today.date()).all()
        if rows:
            today_info = "Today {}:".format(rows[0].deadline.strftime("%d %b"))
            result = "{}\n{}".format(today_info, rows[0].task)
            return result + "\n"
        else:
            today_info = "Today {}:".format(datetime.today().strftime("%d %b"))
            result = "{}\nNothing to do!".format(today_info)
            return result + "\n"

    def week_tasks():
        result = ""
        today = datetime.today()
        for week_days in range(7):
            day_after_tomorrow = today + timedelta(days=week_days)
            rows = session.query(Table).filter(Table.deadline == day_after_tomorrow.date()).all()
            if rows:
                day_info = "{}\n{}".format(rows[0].deadline.strftime("%A %d %b"), rows[0].task)
                result += "\n{}\n".format(day_info)
            else:
                result += "\n{}\nNothing to do!\n".format(day_after_tomorrow.strftime("%A %d %b"))
        return result + "\n"

    def all_tasks():
        result = "All tasks:"
        rows = session.query(Table).order_by(Table.deadline).all()
        count = 1
        for each_task_info in rows:
            result += "\n {}. {}. {}".format(str(count),
                                             each_task_info.task,
                                             each_task_info.deadline.strftime("%d %b"))
            count += 1
        return result + "\n"

    def missed_tasks():
        result = "Missed tasks:"
        missing_task_count = 1
        rows = session.query(Table).order_by(Table.deadline <= datetime.today().date()).all()
        if rows:
            for each_task_info in rows:
                result += "\n {}. {}. {}".format(str(missing_task_count),
                                                 each_task_info.task,
                                                 each_task_info.deadline.strftime("%d %b"))
                missing_task_count += 1
            return result + "\n"
        else:
            result += "Nothing is missed!"
            return result + "\n"

    def add_task():
        print("Enter task")
        entered_task = input()
        print("Enter deadline")
        enter_deadline = input()
        new_row = Table(task=entered_task,
                        deadline=datetime.strptime(enter_deadline, '%Y-%m-%d').date())
        session.add(new_row)
        session.commit()
        return "The task has been added!" + "\n"

    def delete_task():
        result = ""
        task_dict = {}
        task_count_for_delete = 1
        print("Choose the number of the task you want to delete:")
        rows = session.query(Table).order_by(Table.deadline).all()
        if rows:
            for each_task_info in rows:
                result += "\n {}. {}. {}".format(str(task_count_for_delete),
                                                 each_task_info.task,
                                                 each_task_info.deadline.strftime("%d %b"))
                task_dict[task_count_for_delete] = each_task_info.task
                task_count_for_delete += 1
            print(result + "\n")
            delete_chose = input()
            if int(delete_chose) in range(1, task_count_for_delete):
                rows = session.query(Table).filter(Table.task == task_dict[int(delete_chose)]).all()
                specific_row = rows[0]
                session.delete(specific_row)
                session.commit()
                return "The task has been deleted!\n"
            else:
                return "Wrong input, try again!"
        else:
            result = "Nothing to delete"
            return result + "\n"


td = ToDo()
print(td.to_do_menu())
