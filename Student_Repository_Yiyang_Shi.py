"""Author:Yiyang Shi
   Program content:HW09: Creating a data repository of courses, students, and instructors
   Creating a data repository of courses, students, and instructors
"""
from typing import Tuple, Iterator, Dict, IO, Any
from prettytable import PrettyTable


def file_reader(path: str, fields: int, sep: str = ',', header: bool = False) -> Iterator[Tuple[str]]:
    """ Reading text files with a fixed number of fields, separated by a specific character"""
    with open(path, "r") as file:
        try:
            fp: IO = open(path, 'r')    # open the file
        except FileNotFoundError:
            raise FileNotFoundError("Warning! Cannot open the file!")     # file cannot find
        else:
            with fp:
                count: int = 0      # set the count
                for n, line in enumerate(fp, 0):
                    count += 1
                    num_fields: Any = line.rstrip('/n').split(sep)      # get the number of fields
                    if len(num_fields) != fields:
                        raise ValueError(f'{path} has {len(num_fields)} fields on line {count} '
                                         f'but expected {fields} fields!')  # when fields is not equal to num_fields
                    elif n == 1 and header:
                        continue
                    else:
                        yield tuple([f.strip() for f in num_fields])        # yield the tuple


class Student:
    """read the files for students"""
    def __init__(self) -> None:
        """ set the directory"""
        self.stu_dic: Dict = dict()
        self.gra_dic: Dict = dict()

    def stu(self) -> dict:
        """ read the student file"""
        for id, name, school in file_reader('students.txt', 3, sep='\t', header=False):
            x: dict = {id: [name]}
            self.stu_dic.update(x)
        return self.stu_dic

    def stu_grade(self) -> dict:
        """ read the grade file"""
        for id, course, grade, ins in file_reader('grades.txt', 4, sep='\t', header=False):
            y: dict = {id: [course]}
            if id not in self.gra_dic.keys():
                self.gra_dic.update(y)
            else:
                self.gra_dic[id].append([course])
        return self.gra_dic


class Instructor:
    """read the files for instructors"""
    def __init__(self) -> None:
        """ set the directory"""
        self.ins_dic: Dict = dict()
        self.grade_dic: Dict = dict()
        self.stugre_dic: Dict = dict()

    def stu_in(self) -> dict:
        """ read the instructors file"""
        for ins, name, school in file_reader('instructors.txt', 3, sep='\t', header=False):
            x: dict = {ins: [name, school]}
            self.ins_dic.update(x)
        return self.ins_dic

    def ins_grade(self) -> dict:
        """ read the grade file"""
        for id, course, grade, ins in file_reader('grades.txt', 4, sep='\t', header=False):
            y: dict = {course: [ins]}
            if ins not in self.grade_dic.keys():
                self.grade_dic.update(y)
            else:
                self.grade_dic[course].append([ins])
        return self.grade_dic

    def ins_stgre(self) -> dict:
        """ read the grade file"""
        for id, course, grade, ins in file_reader('grades.txt', 4, sep='\t', header=False):
            z: dict = {course: [id]}
            if course not in self.stugre_dic.keys():
                self.stugre_dic.update(z)
            else:
                self.stugre_dic[course].append([id])
        return self.stugre_dic


class Repository:
    """print the prettytable and do with files"""
    def student(self) -> None:
        """print the prettytable for students"""
        t: Student = Student()
        student_file: dict = t.stu()
        student_course: dict = t.stu_grade()
        course_id: dict = {}        # set all the dicts
        for key, value in student_course.items():
            if str(value) not in course_id:
                course_id[key] = value
            else:
                course_id[key].append(value)        # get the dicts together
        for keys, value in student_file.items():
            for key, values in course_id.items():
                if keys == key:
                    student_file[key].append(values)        # make the dict to print table
        pt: PrettyTable = PrettyTable(field_names=['CWID', "Name", "Completed Courses"])
        for key, value in student_file.items():
            pt.add_row([key, value[0], value[-1]])
        print("Student Summary")
        print(pt)   # print prettytable

    def instructor(self) -> None:
        """print the prettytable for instructors"""
        inst: Instructor = Instructor()
        ins_course: dict = inst.stu_in()
        ins_grade: dict = inst.ins_grade()
        student_count: dict = inst.ins_stgre()
        ins_id: dict = {}       # set all the dicts
        for key, value in ins_grade.items():
            if str(value) not in ins_id:
                ins_id[key] = value
            else:
                ins_id[key].append(value)
        for keys, value in ins_course.items():
            for key, values in ins_id.items():
                if keys == (values[0]):
                    ins_id[key].append(value)       # make the dict to print table
        count_lis: list = list()
        for key, value in student_count.items():
            count_lis.append(len(value))
        for key, values in student_count.items():
            ins_id[key].append(len(values))         # get all the dict, prepare for printing table
        pt: PrettyTable = PrettyTable(field_names=['CWID', "Name", "Dept", "Course", "Students"])
        for key, value in ins_id.items():
            pt.add_row([value[0], (value[-2])[0], (value[-2])[-1], key, value[-1]])
        print("Instructor Summary")
        print(pt)  # print prettytable


def main():
    """the main function"""
    s: Repository = Repository()
    s.student()
    s.instructor()


main()  # run the program



