"""Fitness tracker module."""
from dataclasses import dataclass, asdict
from typing import Type, Dict, List, ClassVar


@dataclass
class InfoMessage:
    """Informational message about the training."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        message: str = (
            'Тип тренировки: {training_type}; '
            'Длительность: {duration:.3f} ч.; '
            'Дистанция: {distance:.3f} км; '
            'Ср. скорость: {speed:.3f} км/ч; '
            'Потрачено ккал: {calories:.3f}.'
        ).format(**(asdict(self)))

        return message


@dataclass
class Training:
    """Basic training class."""
    action: int
    duration: float
    weight: float

    M_IN_KM: ClassVar[float] = 1000.0
    LEN_STEP: ClassVar[float] = 0.65
    HOURS_IN_MIN: ClassVar[int] = 60

    def get_distance(self) -> float:
        """Get the distance in km."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get the average speed of movement in km per hour."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Get the number of calories consumed."""
        raise NotImplementedError("Undefined function.")

    def show_training_info(self) -> InfoMessage:
        """Return an informational message about the completed workout."""
        return InfoMessage(
            type(self).__name__,
            self.duration, self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Training: running."""

    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[int] = 18
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 1.79

    def get_spent_calories(self) -> float:
        """Count the number of calories consumed while running."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * super().get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight
                / self.M_IN_KM
                * self.duration
                * self.HOURS_IN_MIN)


class SportsWalking(Training):
    """Training: sports walking."""

    SM_IN_M: ClassVar[int] = 100
    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[float] = 0.035
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 0.029
    KM_H_IN_M_S: ClassVar[float] = 0.278

    def __init__(
            self, action: int, duration: float, weight: float, height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Count the number of calories consumed while sport walking."""
        mean_speed: float = super().get_mean_speed() * self.KM_H_IN_M_S

        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.weight
                 + (mean_speed ** 2
                    / (self.height
                       / self.SM_IN_M))
                 * self.CALORIES_MEAN_SPEED_SHIFT
                 * self.weight)
                * (self.duration
                   * self.HOURS_IN_MIN))


class Swimming(Training):
    """Training: swimming."""

    LEN_STEP: ClassVar[float] = 1.38
    SPEED_SHAFFLE: ClassVar[float] = 1.1
    SPEED_MULTIPLIER: ClassVar[int] = 2


    def __init__(
            self, action: int,
            duration: float,
            weight: float,
            length_pool: int,
            count_pool: int
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Get the distance in km."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self):
        """Get the average swimming speed."""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Count the number of calories consumed while swimming."""
        return ((self.get_mean_speed()
                 + self.SPEED_SHAFFLE)
                * self.SPEED_MULTIPLIER
                * self.weight
                * self.duration)


def read_package(training_type: str, training_results: List[int]) -> Training:
    """Read the data received from the sensors."""

    training_code: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking}
    if training_type not in training_code:
        raise NotImplementedError("Undefined training type.")
    return training_code[training_type](*training_results)


def main(workout: Training) -> None:
    """The main function."""

    info: InfoMessage = workout.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: List[tuple] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)

