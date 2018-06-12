from orm.orm_smartphones import Smartphone, Brand
from orm.orm_engine import session

class Variant:
    def __init__(self, text, rate = None):
        self.text = text

        if rate is None:
            self.rate = text
        else:
            self.rate = rate


class Question:
    def __init__(self, text, criteria, variants):
        if len(variants) == 0 or len(variants) > 4:
            raise Exception("Number of the variants must be from 1 to 4")

        self.__check_rates(variants)

        self.text = text
        self.variants = variants
        self.criteria = criteria


    def __check_rates(self, variants):
        var_len = len(variants)
        for i in range(var_len):
            for j in range(var_len):
                if variants[i].rate == variants[j].rate and not i == j:
                    raise Exception("All rates must be different!")


class Questioning:
    def __init__(self, questions):
        self.questions = questions

        self.__position = -1

        self.__criterias_answers = {}

        self.__current_question = None

    def next_question(self):
        self.__position += 1

        if self.__position == len(self.questions):
            self.__position = -1
            return None

        self.__current_question = self.questions[self.__position]

        return self.__current_question


    def answer(self, variant):
        if self.__current_question is None:
            raise Exception("You didnt take any question by using Consultant.next_question")

        self.__criterias_answers[self.__current_question.criteria] = variant.rate

    def get_current(self):
        return self.__current_question


    def get_result(self):
        query = session.query(Smartphone).join(Brand)

        for item in self.__criterias_answers:
            query = query.filter(item == self.__criterias_answers[item])

        return query.all()

























