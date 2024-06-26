import abc
from table_data_classes import Penalty


class CalculatorBase(abc.ABC):
    def __init__(self, penalty: Penalty):
        self.penalty = penalty

    @abc.abstractmethod
    def calculate(self, value: int) -> float:
        pass

    @property
    def  get_id(self):
        return self.penalty.id


class QuantityCalculator(CalculatorBase):
    def calculate(self, value: int) -> float:
        return value * self.penalty.penalty


class PenaltyCalculator:
    def __init__(self, penalties: list[Penalty]):
        self.list_of_calculators: dict[int, CalculatorBase] = {}

        for penalty in penalties:
            if not penalty.type_navigation.is_range:
                self.list_of_calculators[penalty.id] = QuantityCalculator(penalty)

    def calculate(self, values: dict) -> float:
        calculation_sum = 0.0

        for penalty_id, value in values:
            calculation_sum += self.list_of_calculators[penalty_id].calculate(value)

        return calculation_sum
