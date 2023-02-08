from typing import Tuple, Optional, get_type_hints
from dataclasses import dataclass, astuple
from datetime import date


@dataclass
class RequestParams:
    year: int
    grade: int
    roll_number: int
    school_number: Optional[int] = None
    centre_number: Optional[int] = None
    student_initial: Optional[str] = None
    mother_initial: Optional[str] = None

    # if this parameter is required for a given year-grade pair,
    # then bruteforce is probably infeasible for that year-grade pair.
    dob: Optional[date] = None

    def __check_types(self):
        for attr, expected_type in get_type_hints(self).items():
            attr_value = getattr(self, attr)
            actual_type = type(attr_value)
            try:
                assert isinstance(attr_value, expected_type)
            except AssertionError:
                raise ValueError(f"{attr} must be of type '{expected_type.__name__}' not '{actual_type.__name__}'.")

    def __post_init__(self):
        self.__check_types()

        if not (2004 <= self.year <= (max_year := 2022)):  # probably the first year results were published online
            raise Exception(f"Year must be between 2004 and {max_year} (both inclusive)")

        if self.grade not in (10, 12):
            raise Exception(f"Grade must be either 10 or 12, not {self.grade}")

        if self.mother_initial or self.student_initial:
            # because if one initial is present then the other must be present too
            if not (isinstance(self.mother_initial, str) and isinstance(self.student_initial, str)):
                raise Exception("Both initials must be present.")
            if not (len(self.mother_initial) == len(self.student_initial) == 1):
                raise Exception("Initials must be only character long.")

    @property
    def admit_card_id(self):
        return f"{self.student_initial}{self.mother_initial}" \
               f"{str(self.roll_number)[-3:-1]}{str(self.centre_number)[:4]}".upper()

    def copy(self):
        return RequestParams(*astuple(self))


class ParamIterator:
    def __init__(self, initial_params: RequestParams):
        """
        This is an infinite generator, it is upon the callee to stop the iterator. It will keep generating next
        parameters depending on the initial params and the current direction. It is also upon the callee to switch
        direction of search to lower once the upper limit is reached.
        """
        if initial_params.dob is not None:
            raise Exception("Can not bruteforce DOB.")
        self.initial_params = initial_params
        self.current = initial_params.copy()
        self.admit_card_required = self.current.student_initial is not None
        self.step, self.__direction_switched = -1, False
        self.exit = False

    def switch_direction(self):
        if self.__direction_switched:
            raise Exception("Can't switch search direction more than once.")
        self.__direction_switched = True
        self.step = 1
        self.current = self.initial_params.copy()

    def match_found(self):
        """
        Called when a certain admit card ID combination is correct, so that it steps to the next roll number.
        """
        self.current.roll_number += self.step
        self.current.mother_initial = "A" if self.step < 0 else "Z"
        self.current.student_initial, _ = self.iter_char(self.current.student_initial, -self.step)

    def iter_char(self, char: str, step: int = None) -> Tuple[str, bool]:
        """
        Steps character in given direction and also returns boolean about whether loop was completed.
        """
        if step is None:
            step = self.step
        ordinal = ord(char) + step
        loop_completed = not (65 <= ordinal <= 90)
        if loop_completed:
            return "Z" if ordinal < 65 else "A", True
        else:
            return chr(ordinal), False

    def iter(self) -> None:
        if not self.admit_card_required:
            self.current.roll_number += self.step
            return

        self.current.mother_initial, loop_completed = self.iter_char(self.current.mother_initial)
        if loop_completed:
            self.current.student_initial, _ = self.iter_char(self.current.student_initial)

    def __iter__(self) -> RequestParams:
        while not self.exit:
            self.iter()
            yield self.current.copy()
