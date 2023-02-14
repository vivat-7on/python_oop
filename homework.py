"""Fitness tracker module."""


class InfoMessage:
    """Informational message about the training."""

    def __init__(
            self, training_type: str,
            duration, distance,
            speed, calories) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        message = (
            'Тип тренировки: {}; '
            'Длительность: {:.3f} ч.; '
            'Дистанция: {:.3f} км; '
            'Ср. скорость: {:.3f} км/ч; '
            'Потрачено ккал: {:.3f}.'
        )
        return message.format(
            self.training_type, self.duration,
            self.distance, self.speed,
            self.calories
        )


class Training:
    """Basic training class."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    HOURSES_IN_MIN: int = 60
    SM_IN_M = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Get the distance in km."""
        return (
            self.action * self.LEN_STEP
            / self.M_IN_KM
        )  # Distance in kilometers per hour.

    def get_mean_speed(self) -> float:
        """Get the average speed of movement."""
        return (
            self.get_distance() / self.duration
        )  # Average speed in kilometers per hours.

    def get_spent_calories(self) -> float:
        """Get the number of calories consumed."""
        raise NotImplementedError

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

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Count the number of calories consumed while running."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * super().get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight
                / self.M_IN_KM
                * self.duration
                * self.HOURSES_IN_MIN)


class SportsWalking(Training):
    """Training: sports walking."""

    def __init__(
        self, action: int, duration: float, weight: float, height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    HOURSES_IN_MIN = 60
    CALORIES_MEAN_SPEED_MULTIPLIER = 0.035
    CALORIES_MEAN_SPEED_SHIFT = 0.029
    KM_H_IN_M_S = 0.278
    SM_IN_M = 100

    def get_spent_calories(self) -> float:
        """Count the number of calories consumed while sport walking."""

        mean_speed = super().get_mean_speed() * self.KM_H_IN_M_S

        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.weight
                 + (mean_speed ** 2
                    / (self.height
                       / self.SM_IN_M))
                 * self.CALORIES_MEAN_SPEED_SHIFT
                 * self.weight)
                * (self.duration
                   * self.HOURSES_IN_MIN))


class Swimming(Training):
    """Training: swimming."""

    LEN_STEP: float = 1.38
    SPEED_SHAFFLE: float = 1.1
    SPEED_MULTIPLIER = 2

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

    def get_mean_speed(self):
        """Get the average swimming speed."""
        return (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self) -> float:

        """Count the number of calories consumed while swimming."""
        return ((self.get_mean_speed()
                + self.SPEED_SHAFFLE)
                * self.SPEED_MULTIPLIER
                * self.weight
                * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Read the data received from the sensors."""
    training_code: dict = {'SWM': Swimming,
                           'RUN': Running,
                           'WLK': SportsWalking, }

    return training_code[workout_type](*data)


def main(training: Training) -> None:
    """The main function."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
