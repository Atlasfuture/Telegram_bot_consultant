from orm.orm_smartphones import Smartphone, User, Order
from orm.orm_engine import session

from bot.corpusgenerator import CorpusGenerator

from googletrans import Translator




class Conversation:
    """
    Class contains methods which handles requests and build
    response depending on current conversation state.

    Conversation has 5 modes:
    - conversation
    - questioning
    - quest_request
    - refresh
    - order
    """
    def __init__(self, questioning):
        self.__mode = "conversation"
        self.__questioning = questioning

        self.__current_lang = ''

        self.__order_string = ""

        self.__corpus_gen = CorpusGenerator()

        self.__translator = Translator()



    def __translate(self, message):
        return self.__translator.translate(message, dest=self.__current_lang).text


    def ask(self, str):
        """Handles request depending on
           current conversation state
        """


        if self.__mode == "quest_request":
            if str.lower() in "yes" or "yes" in str.lower():
                self.__mode = "questioning"
            else:
                self.__mode = "conversation"
        elif self.__mode == "questioning":
            quest = self.__questioning.get_current()

            for i in range(len(quest.variants)):
                if str in quest.variants[i].text:
                    self.__questioning.answer(quest.variants[i])
                    return
            self.__mode = "refresh"
        elif self.__mode == "conversation":
            self.__current_lang = self.__translator.detect(str).lang

            if not self.__current_lang == 'en':
                str = self.__translator.translate(str).text

            if str.lower() in "smartphone" or "smartphone" in str.lower():
                self.__mode = "quest_request"

            self.__corpus_gen.process(str)
            self.__corpus_gen.save()


    def response(self):
        """
        Generates response depending on
        current conversation state

        :return:
        current mode: questioning => list(<class 'orm.orm_smartphones.Smartphone'>) ||
                                      <class 'str'>
                                      dict('Text':<class 'str'>,
                                      'Variants':list(<class 'Variant'>))

        current mode: conversation => <class 'str'>

        current mode: quest_request => dict('Text':<class 'str'>,
                                      'Variants':list(<class 'Variant'>))

        current mode: refresh => dict('Text':<class 'str'>,
                                      'Variants':list(<class 'Variant'>))

        current mode: order => <class 'str'>
        """
        if self.__mode == "questioning":
            question = {}

            quest = self.__questioning.next_question()

            if quest is None:
                self.__mode = "conversation"
                result = self.__questioning.get_result()

                if not len(result) == 0:
                    return self.__questioning.get_result()
                else:
                    return [self.__translate("There is no results for your criterias")]
            else:
                question["Text"] = self.__translate(quest.text)
                question["Variants"] = []
                for item in quest.variants:
                    question["Variants"].append(item.text)
                return question
        elif self.__mode == "conversation":
            return self.__translate(self.__corpus_gen.generate())
        elif self.__mode == "quest_request":
            question = {}
            question["Text"] = self.__translate("Do you wanna choose smartphone?")
            question["Variants"] = ["Yes", "No"]
            return question
        elif self.__mode == "refresh":
            self.__mode = "questioning"
            quest = self.__questioning.get_current()

            question = {}

            question["Text"] = "{}. {}".format(self.__translate("Sorry I dont "
                        "understand. Please try again"), self.__translate(quest.text))
            question["Variants"] = []
            for item in quest.variants:
                question["Variants"].append(item.text)
            return question
        elif self.__mode == "order":
            self.__mode = "conversation"
            return self.__order_string



    def current_state(self):
        """
        Returns current conversation state
        :return:
        <class 'str'>
        """
        return self.__mode


    def order(self, call_query):
        """
        Creates order record based on request
        :param call_query: <class 'telebot.types.CallbackQuery'>
        """


        self.__mode = "order"
        user_tuple = call_query.from_user



        query = session.query(User).filter_by(tele_id = user_tuple.id)
        users = query.all()

        if not len(users):
            user = users[0]
        else:
            user = User(tele_id = user_tuple.id)
            session.add(user)
            session.commit()

        query = session.query(Smartphone).filter_by(name = call_query.data)

        smartphone = query.first()


        order = Order(user_id = user.id, smartphone_id = smartphone.id)
        session.add(order)
        session.commit()

        self.__order_string = self.__translate("Your order is accepted. Your order`s id: {}").format(order.id)







