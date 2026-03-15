import dataclasses


@dataclasses.dataclass
class WorkoutExercise:
    machine: str
    weight: float
    set1: int
    set2: int
    done: bool = False


class Workout(list[WorkoutExercise]):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({super().__repr__()})"


class Workouts(dict[str, Workout]):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({super().__repr__()})"
        return super().__repr__()


workouts = Workouts(
    {
        "2026-03-12": Workout(
            [
                WorkoutExercise("B3", 35.0, 15, 15),
                WorkoutExercise("A5", 35.0, 15, 15),
                WorkoutExercise("A2", 60.0, 18, 18),
            ]
        ),
        "2026-03-13": Workout(
            [
                WorkoutExercise("B3", 35.0, 15, 15),
                WorkoutExercise("A5", 35.0, 15, 15),
                WorkoutExercise("A2", 60.0, 18, 18),
            ]
        ),
    }
)

print("workouts")
print(repr(workouts))

# workouts2_text = "{'2026-03-12': [WorkoutExercise(machine='B3', weight=35.0, set1=15, set2=15, done=False), WorkoutExercise(machine='A5', weight=35.0, set1=15, set2=15, done=False), WorkoutExercise(machine='A2', weight=60.0, set1=18, set2=18, done=False)], '2026-03-13': [WorkoutExercise(machine='B3', weight=35.0, set1=15, set2=15, done=False), WorkoutExercise(machine='A5', weight=35.0, set1=15, set2=15, done=False), WorkoutExercise(machine='A2', weight=60.0, set1=18, set2=18, done=False)]}"
workouts2_text = "Workouts({'2026-03-12': Workout([WorkoutExercise(machine='B3', weight=35.0, set1=15, set2=15, done=False), WorkoutExercise(machine='A5', weight=35.0, set1=15, set2=15, done=False), WorkoutExercise(machine='A2', weight=60.0, set1=18, set2=18, done=False)]), '2026-03-13': Workout([WorkoutExercise(machine='B3', weight=35.0, set1=15, set2=15, done=False), WorkoutExercise(machine='A5', weight=35.0, set1=15, set2=15, done=False), WorkoutExercise(machine='A2', weight=60.0, set1=18, set2=18, done=False)])})"
workouts2 = eval(workouts2_text)
print("workouts2")
print(repr(workouts2))
pass
