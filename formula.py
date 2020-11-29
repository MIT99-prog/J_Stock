#
import pandas as pd
import numpy as np
from errorhandler import Error, ErrorList
from widget_helper import Result


class FormulaMeta(type):
    def __instancecheck__(self, instance):
        return self.__subclasscheck__(type(instance))

    def __subclasscheck__(self, subclass):
        return (hasattr(subclass, 'check_parameters') and callable(subclass.check_parameters)
                and hasattr(subclass, 'pre_process_1') and callable(subclass.pre_process_1)
                and hasattr(subclass, 'pre_process_2') and callable(subclass.pre_process_2)
                and hasattr(subclass, 'calculation') and callable(subclass.calculation)
                and hasattr(subclass, 'post_process') and callable(subclass.post_process))


class Formula:
    def __init__(self):
        pass

    def check_parameters(self) -> bool:
        pass

    def pre_process_1(self) -> pd.Series:
        pass

    def pre_process_2(self) -> pd.Series:
        pass

    def calculation(self) -> pd.Series:
        pass

    def post_process(self) -> pd.Series:
        pass


class CalcProfitRatio(metaclass=FormulaMeta):
    def __init__(self, operand_1: pd.Series, operand_2: pd.Series):
        self.operand_1 = operand_1
        self.operand_2 = operand_2
        self.answer = object
        self.result = Result()
        self.result.action_name = self.__str__()

        if self.check_parameters():
            try:
                self.pre_process_1()
                self.pre_process_2()
                self.calculation()
                self.post_process()
            except ValueError:
                er = Error(ValueError, self.__str__(), 'ValueError occurred!')
                e_list = ErrorList().add_list(er)
                self.result.error_list.add_list(e_list)
                self.result.exec_continue = False

    def check_parameters(self) -> bool:
        if self.operand_1.index.equals(self.operand_2.index):
            return True
        else:
            return False

    def pre_process_1(self):
        pass

    def pre_process_2(self):
        # for avoiding zero divide
        # self.operand_2 = self.operand_2.where(self.operand_2.values > 0, 1)
        pass

    def calculation(self):
        self.answer = self.operand_1 / self.operand_2 * 100

    def post_process(self):
        self.answer = self.answer.where(self.answer.values != np.inf, 0)
        self.result.result_type = 'pd.Series'
        self.result.result_data = self.answer


class CalcProfitMean(metaclass=FormulaMeta):
    def __init__(self, operand_1: pd.DataFrame, operand_2: pd.DataFrame):
        self.operand_1 = operand_1
        self.operand_2 = operand_2
        self.answer = object
        self.result = Result()
        self.result.action_name = self.__str__()

        if self.check_parameters():
            try:
                self.pre_process_1()
                self.pre_process_2()
                self.calculation()
                self.post_process()
            except ValueError:
                er = Error(ValueError, self.__str__(), 'ValueError occurred!')
                e_list = ErrorList().add_list(er)
                self.result.error_list.add_list(e_list)
                self.result.exec_continue = False

    def check_parameters(self) -> bool:
        if self.operand_1.index.equals(self.operand_2.index) and self.operand_1.columns.equals(self.operand_2.columns):
            return True
        else:
            return False

    def pre_process_1(self):
        pass

    def pre_process_2(self):
        # for avoiding zero divide
        # self.operand_2 = self.operand_2.where(self.operand_2.values > 0, 1)
        pass

    def calculation(self):
        self.answer = self.operand_1 / self.operand_2 * 100
        self.answer = self.answer.where(self.answer.values != np.inf, 0)
        self.answer = self.answer.values.mean(axis=0)

    def post_process(self):
        self.result.result_type = 'pd.Series'
        self.result.result_data = pd.Series(self.answer, index=self.operand_1.columns)


if __name__ == '__main__':
    op1 = pd.DataFrame([[0, 1], [1.1, 2.5], [2, 2.3], [2.5, 3]], columns=['A', 'B'])
    op2 = pd.DataFrame([[1.2, 1], [0, 3.1], [5.2, 5.5], [6, 8.1]], columns=['A', 'B'])
    cp = CalcProfitMean(op1, op2)
    print('end')
