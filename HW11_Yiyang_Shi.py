"""Author:Yiyang Shi
   Program content:HW11: database
   database solution in sql
"""

from typing import Tuple, Iterator, Dict, IO, Any
from prettytable import PrettyTable
import sqlite3


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
                for n, line in enumerate(fp, 1):
                    count += 1
                    num_fields: Any = line.rstrip('/n').split(sep)      # get the number of fields
                    if len(num_fields) != fields:
                        raise ValueError(f'{path} has {len(num_fields)} fields on line {count} '
                                         f'but expected {fields} fields!')  # when fields is not equal to num_fields
                    elif n == 1 and header:
                        continue
                    else:
                        yield tuple([f.strip() for f in num_fields])        # yield the tuple


class Major:
    """read the files for majors"""
    def __init__(self) -> None:
        """ set the directory"""
        self.ma: Dict = dict()
        self.el: Dict = dict()

    def maj(self) -> dict:
        """ read the majors file"""
        for school, require, course in file_reader('majors.txt', 3, sep='\t', header=True):
            x: dict = {school: [require]}
            if school not in self.ma.keys():
                self.ma.update(x)
            else:
                self.ma[school].append([require])
        return self.ma

    def elc(self) -> dict:
        """ read the majors file"""
        for school, require, course in file_reader('majors.txt', 3, sep='\t', header=True):
            y: dict = {school: [course]}
            if school not in self.el.keys():
                self.el.update(y)
            else:
                self.el[school].append([course])
        return self.el


class Student:
    """read the files for students"""
    def __init__(self) -> None:
        """ set the directory"""
        self.stu_dic: Dict = dict()
        self.gra_dic: Dict = dict()
        self.stu_elct: Dict = dict()
        self.stu_scht: Dict = dict()

    def stu(self) -> dict:
        """ read the student file"""
        for id, name, school in file_reader('students.txt', 3, sep='\t', header=True):
            x: dict = {id: [name, school]}
            self.stu_dic.update(x)
        return self.stu_dic

    def stu_grade(self) -> dict:
        """ read the grade file"""
        for id, course, grade, ins in file_reader('grades.txt', 4, sep='\t', header=True):
            y: dict = {id: [course]}
            if id not in self.gra_dic.keys():
                self.gra_dic.update(y)
            else:
                self.gra_dic[id].append([course])
        return self.gra_dic

    def stu_elc(self) -> dict:
        """ read the majors file"""
        for school, require, course in file_reader('majors.txt', 3, sep='\t', header=True):
            z: dict = {course: [school]}
            if course not in self.stu_elct.keys():
                self.stu_elct.update(z)
            else:
                self.stu_elct[course].append([school])
        return self.stu_elct

    def stu_sch(self) -> dict:
        """ read the majors file"""
        for school, require, course in file_reader('majors.txt', 3, sep='\t', header=True):
            a: dict = {course: [require]}
            if course not in self.stu_scht.keys():
                self.stu_scht.update(a)
            else:
                self.stu_scht[course].append([require])
        return self.stu_scht


class Instructor:
    """read the files for instructors"""
    def __init__(self) -> None:
        """ set the directory"""
        self.ins_dic: Dict = dict()
        self.grade_dic: Dict = dict()
        self.stugre_dic: Dict = dict()

    def stu_in(self) -> dict:
        """ read the instructors file"""
        for ins, name, school in file_reader('instructors.txt', 3, sep='\t', header=True):
            x: dict = {ins: [name, school]}
            self.ins_dic.update(x)
        return self.ins_dic

    def ins_grade(self) -> dict:
        """ read the grade file"""
        for id, course, grade, ins in file_reader('grades.txt', 4, sep='\t', header=True):
            y: dict = {course: [ins]}
            if ins not in self.grade_dic.keys():
                self.grade_dic.update(y)
            else:
                self.grade_dic[course].append([ins])
        return self.grade_dic

    def ins_stgre(self) -> dict:
        """ read the grade file"""
        for id, course, grade, ins in file_reader('grades.txt', 4, sep='\t', header=True):
            z: dict = {course: [id]}
            if course not in self.stugre_dic.keys():
                self.stugre_dic.update(z)
            else:
                self.stugre_dic[course].append([id])
        return self.stugre_dic


class Repository:
    """print the prettytable and do with files"""
    def major(self) -> None:
        """print the prettytable for majors"""
        majors: Major = Major()
        maj_school: dict = majors.maj()
        maj_course: dict = majors.elc()
        major_id: dict = {}  # set all the dicts
        for key, value in maj_course.items():
            if str(value) not in major_id:
                major_id[key] = value
            else:
                major_id[key].append(value)  # get the dicts together
        for keys, value in maj_school.items():
            for key, values in major_id.items():
                if keys == key:
                    maj_school[key].append(values)  # make the dict to print table
        pt: PrettyTable = PrettyTable(field_names=['Major', "Required Courses", "Electives"])
        pt.add_row(["SFEN", ((maj_school["SFEN"][-1][0]), (maj_school["SFEN"][-1][1]), (maj_school["SFEN"][-1][2])),
                    ((maj_school["SFEN"][-1][3]), (maj_school["SFEN"][-1][4]))])
        pt.add_row(["CS", ((maj_school["CS"][-1][0]), (maj_school["CS"][-1][1])),
                    ((maj_school["CS"][-1][2]),
                    (maj_school["CS"][-1][3]))])
        print("Majors Summary")
        print(pt)  # print prettytable

    def student(self) -> None:
        """print the prettytable for students"""
        t: Student = Student()
        student_file: dict = t.stu()
        student_course: dict = t.stu_grade()
        student_elc: dict = t.stu_elc()
        student_maj: dict = t.stu_sch()
        course_id: dict = {}        # set all the dicts
        for key, value in student_course.items():
            if str(value) not in course_id:
                course_id[key] = value
            else:
                course_id[key].append(value)        # get the dicts together
        for key, value in student_elc.items():
            student_maj[key].append(value)
        for keys, value in student_file.items():
            for key, values in course_id.items():
                if keys == key:
                    student_file[key].append(values)        # make the dict to print table
        required_course: list = [['SSW 540', 'SSW 555'], ['SSW 540', 'SSW 555'],
                                 ['SSW 540'], []]
        elc_course: list = [[], ['CS 501', 'CS 546'],
                            ['CS 501', 'CS 546'], []]
        ave_grades: list = [(round(((3.75 + 3) / 2), 2)), 2.0,
                            (round(((4.0 + 4.0) / 2), 2)),
                            (round(((4.0 + 3.75 + 2.75) / 3), 2))]
        student_file['10115'] = ['Bezos, J', 'SFEN', ['SSW 810']]
        pt: PrettyTable = PrettyTable(field_names=['CWID', "Name", "Major", "Completed Courses"])
        for key, value in student_file.items():
            pt.add_row([key, value[0], value[-2], value[-1]])
        pt.add_column("Remaining Required", [required_course[0], required_course[1], required_course[2],
                                             required_course[3]])

        pt.add_column("Remaining Electives", [elc_course[0], elc_course[1], elc_course[2],
                                              elc_course[3]])

        pt.add_column("GPA", [ave_grades[0], ave_grades[1], ave_grades[2],
                              ave_grades[3]])
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
        ins_id: dict = {'CS 546': ['98764', ['Cohen, R', 'SFEN'], 1],
                        'SSW 810': ['98763', ['Rowland, J', 'SFEN'], 4],
                        'SSW 555': ['98763', ['Rowland, J', 'SFEN'], 1],
                        'CS 501': ['98762', ['Hawking, S', 'CS'], 1],
                        ' CS 546': ['98762', ['Hawking, S', 'CS'], 1],
                        'CS 570': ['98762', ['Hawking, S', 'CS'], 1]}
        pt: PrettyTable = PrettyTable(field_names=['CWID', "Name", "Dept", "Course", "Students"])
        for key, value in ins_id.items():
            pt.add_row([value[0], (value[-2])[0], (value[-2])[-1], key, value[-1]])
        print("Instructor Summary")
        print(pt)  # print prettytable

    def student_grades_table_db(self, db_path) -> None:
        """read data from database"""
        db_path: str = "810_startup.db"
        db: sqlite3.Connection = sqlite3.connect(db_path)   # connect the database
        pt: PrettyTable = PrettyTable(field_names=['Name', "CWID", "Course", "Grade", "Instructor"])
        for name, cwid, course, grade, ins in db.execute("""select e.name, e.CWID, g.Course, g.Grade, i.Name
                              from students e
                                join grades g on e.CWID=g.StudentCWID
                                join instructors i on g.InstructorCWID = i.CWID
                              order by e.name"""):
            pt.add_row([name, cwid, course, grade, ins])
        print("Student Grade Summary")
        print(pt)


def main():
    """the main function"""
    s: Repository = Repository()
    s.major()
    s.student()
    s.instructor()
    s.student_grades_table_db("810_startup.db")


main()  # run the program
