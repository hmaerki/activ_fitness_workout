# from __future__ import annotations

from pyscript import document, when
import configuration
import json
import js

try:
    import micropython

    IS_MICROPYTHON = True
except ImportError:
    IS_MICROPYTHON = False

STORAGE_KEY = "activ_fitness_workouts"
STORAGE_WHO = "activ_fitness_who"


class CurrentExercise:
    def __init__(
        self,
        workout_date: str,
        exercise: configuration.Exercise,
        workout_exercise: dict[str, float | int | bool],
    ) -> None:
        assert isinstance(workout_date, str)
        assert isinstance(exercise, configuration.Exercise)
        assert isinstance(workout_exercise, dict)
        configuration.who.validate_workout_exercise(workout_exercise=workout_exercise)

        self.workout_date = workout_date
        self.exercise = exercise
        self.workout_exercise = workout_exercise

    def get_value(
        self,
        persistence: "Persistence",
        key: str,
    ) -> float | int | bool:
        return persistence.get_exercise_value(
            workout_date=self.workout_date,
            machine=self.exercise.machine,
            key=key,
        )

    def set_value(
        self,
        persistence: "Persistence",
        key: str,
        value: float | int | bool,
    ) -> None:
        persistence.set_exercise_value(
            workout_date=self.workout_date,
            machine=self.exercise.machine,
            key=key,
            value=value,
        )


class Persistence:
    def __init__(self) -> None:
        self.dict_workouts: dict[str, dict] = {}  # type: ignore
        workouts_text = js.localStorage.getItem(STORAGE_KEY)
        if workouts_text:
            self.dict_workouts = json.loads(workouts_text)
        _who_key = js.localStorage.getItem(STORAGE_WHO)
        if _who_key:
            who_key = str(_who_key)
        else:
            who_key = configuration.WHO_HANS.key
        self.who = configuration.DICT_WHO[who_key]

    @property
    def has_workouts(self) -> bool:
        return len(self.dict_workouts) > 0

    @property
    def workout_dates(self) -> list[str]:
        return sorted(self.dict_workouts.keys(), reverse=True)

    def get_progress(self, workout_date: str) -> str:
        dict_workout = self.dict_workouts[workout_date]
        done_count = sum(1 for v in dict_workout.values() if v.get("done"))
        total_count = len(dict_workout)
        return f"{done_count}/{total_count} done"

    def get_workout(
        self,
        workout_date: str,
        remove_done: bool = False,
    ) -> dict[str, dict[str, float | int | bool]]:
        dict_workout_exercise = self.dict_workouts[workout_date]
        if remove_done:
            for _machine, dict_workout in dict_workout_exercise.items():
                if "done" in dict_workout:
                    del dict_workout["done"]
        return dict_workout_exercise

    def _get_exercise(
        self,
        workout_date: str,
        machine: str,
    ) -> dict[str, float | int | bool]:
        return self.get_workout(workout_date=workout_date).get(machine, {})

    def get_exercise_value(
        self,
        workout_date: str,
        machine: str,
        key: str,
    ) -> float | bool:
        assert key in configuration.Who.WORKOUT_KEYS
        default_value = self.who.get_default_value(machine=machine, key=key)
        return self._get_exercise(workout_date=workout_date, machine=machine).get(
            key, default_value
        )

    def set_exercise_value(
        self, workout_date: str, machine: str, key: str, value: float | int | bool
    ) -> None:
        assert key in configuration.Who.WORKOUT_KEYS
        self._get_exercise(workout_date=workout_date, machine=machine)[key] = value

    def get_done(self, workout_date: str, machine: str) -> bool:
        done = self.get_exercise_value(
            workout_date=workout_date, machine=machine, key="done"
        )
        assert isinstance(done, bool)
        return done

    def get_current_exercise(self, workout_date: str, machine: str) -> CurrentExercise:
        return CurrentExercise(
            workout_date=workout_date,
            exercise=self.who.get_exercise(machine=machine),
            workout_exercise=self._get_exercise(
                workout_date=workout_date, machine=machine
            ),
        )

    def set_workout(
        self,
        workout_date: str,
        dict_workout: dict[str, dict[str, float | int | bool]],
    ) -> None:
        configuration.Who.validate_workout(dict_workout=dict_workout)
        self.dict_workouts[workout_date] = dict_workout

    def new_workout(self, workout_str: str) -> None:
        self.dict_workouts[workout_str] = self.who.workout_template.copy()

    def save(self) -> None:
        js.localStorage.setItem(STORAGE_KEY, json.dumps(self.dict_workouts))

    def delete_workout(self, workout_date: str) -> None:
        if workout_date in self.dict_workouts:
            del self.dict_workouts[workout_date]
            self.save()

    def delete_storage(self) -> None:
        js.localStorage.removeItem(STORAGE_KEY)
        self.dict_workouts = {}

    def toggle_who(self) -> None:
        self.who = configuration.WHO_OTHER[self.who.key]
        js.localStorage.setItem(STORAGE_WHO, self.who.key)


class FitnessApp:
    def __init__(self) -> None:
        print("FitnessApp()")
        self.persistence = Persistence()
        self.current_exercise: CurrentExercise | None = None
        self.current_workout_date: str = ""

        self._dom_update_who()

        def _add(id, fn):
            if IS_MICROPYTHON:
                document.getElementById(id).addEventListener("click", fn)
            else:
                # from pyscript.ffi import create_proxy
                # document.getElementById(id).addEventListener("click", create_proxy(fn))
                when("click", "#" + id)(fn)

        _add("btn-new-workout", self.on_new_workout)
        _add("hans-im-glueck", self.on_toggle_who)
        _add("btn-back-to-workouts", self.on_show_workouts)
        _add("btn-done", self.on_done_exercise)
        _add("btn-cancel", self.on_cancel_exercise)
        _add("btn-delete-workout", self.on_delete_workout)
        _add("btn-show-json", self.on_show_json)
        _add("btn-back-from-json", self.on_back_from_json)
        _add("btn-save-json", self.on_save_json)
        _add("btn-delete-storage", self.on_delete_storage)
        _add("workouts-list", self.on_workout_click)
        _add("exercises-list", self.on_exercise_click)

        self.on_show_workouts()

    def _dom_update_who(self) -> None:
        document.getElementById(
            "hans-im-glueck"
        ).src = f"./assets/{self.persistence.who.image}"
        document.getElementById("who-name").textContent = self.persistence.who.name

    def on_toggle_who(self, event=None) -> None:
        self.persistence.toggle_who()
        self._dom_update_who()

    def _dom_show_view(self, view_id: str) -> None:
        for vid in ("view-workouts", "view-workout", "view-exercise", "view-json"):
            el = document.getElementById(vid)
            if vid == view_id:
                el.removeAttribute("hidden")
            else:
                el.setAttribute("hidden", "hidden")

    def on_show_workouts(self, event=None) -> None:
        self._dom_show_view("view-workouts")
        container = document.getElementById("workouts-list")
        container.innerHTML = ""

        if not self.persistence.has_workouts:
            li = document.createElement("li")
            li.textContent = "No workouts yet. Click 'New workout' to start!"
            li.className = "empty-hint"
            container.appendChild(li)
            return

        for workout_date in self.persistence.workout_dates:
            li = document.createElement("li")
            li.className = "workout-item"
            li.setAttribute("workout-date", workout_date)

            span_date = document.createElement("span")
            span_date.className = "workout-date"
            span_date.textContent = workout_date

            span_progress = document.createElement("span")
            span_progress.className = "workout-progress"
            span_progress.textContent = self.persistence.get_progress(workout_date)

            li.appendChild(span_date)
            li.appendChild(span_progress)
            container.appendChild(li)

    def on_new_workout(self, event=None) -> None:
        d = js.Date.new()
        self.current_workout_date = "{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            d.getFullYear(),
            d.getMonth() + 1,
            d.getDate(),
            d.getHours(),
            d.getMinutes(),
            d.getSeconds(),
        )
        self.persistence.new_workout(workout_str=self.current_workout_date)
        self.persistence.save()
        self._dom_show_workout()

    def on_workout_click(self, event) -> None:
        target = event.target.closest(".workout-item")
        if target:
            self.current_workout_date = str(target.getAttribute("workout-date"))
            self._dom_show_workout()

    def _dom_show_workout(self) -> None:
        assert self.current_workout_date != ""

        self._dom_show_view("view-workout")
        document.getElementById("workout-date").textContent = self.current_workout_date

        container = document.getElementById("exercises-list")
        container.innerHTML = ""

        for exercise in self.persistence.who.exercises:
            done = self.persistence.get_done(
                machine=exercise.machine, workout_date=self.current_workout_date
            )
            li = document.createElement("li")
            li.className = "exercise-item" + (" done" if done else "")
            li.setAttribute("data-key", exercise.machine)

            span_key = document.createElement("span")
            span_key.className = "exercise-key"
            span_key.textContent = exercise.machine

            span_name = document.createElement("span")
            span_name.className = "exercise-name"
            span_name.textContent = exercise.short

            li.appendChild(span_key)
            li.appendChild(span_name)
            if exercise.priority != "":
                img = document.createElement("img")
                img.src = f"./assets/{exercise.priority}"
                img.className = "priority-icon"
                img.alt = exercise.priority
                li.appendChild(img)
            container.appendChild(li)

    def on_exercise_click(self, event) -> None:
        target = event.target.closest(".exercise-item")
        if target:
            machine = str(target.getAttribute("data-key"))
            self.current_exercise = self.persistence.get_current_exercise(
                workout_date=self.current_workout_date,
                machine=machine,
            )
            self._dom_show_exercise()

    def _dom_show_exercise(self) -> None:
        self._dom_show_view("view-exercise")

        assert self.current_exercise is not None
        exercise = self.current_exercise.exercise

        document.getElementById("exercise-key").textContent = exercise.machine
        document.getElementById("exercise-short").textContent = exercise.short
        document.getElementById("exercise-comment").textContent = exercise.comment
        document.getElementById("exercise-weight").value = str(
            self.current_exercise.get_value(persistence=self.persistence, key="weight")
        )
        document.getElementById("exercise-set1").value = str(
            self.current_exercise.get_value(persistence=self.persistence, key="set1")
        )
        document.getElementById("exercise-set2").value = str(
            self.current_exercise.get_value(persistence=self.persistence, key="set2")
        )

        card = document.getElementById("exercise-detail-card")
        done = self.current_exercise.get_value(persistence=self.persistence, key="done")
        if done:
            card.classList.add("done")
        else:
            card.classList.remove("done")

        btn_done = document.getElementById("btn-done")
        SVG_LEFT = '<svg><use href="#arrow-left"/></svg>'
        SVG_RIGHT = '<svg><use href="#arrow-right"/></svg>'
        if done:
            btn_done.innerHTML = f"{SVG_LEFT} Undo Done"
        else:
            btn_done.innerHTML = f"Done {SVG_RIGHT}"

    def on_done_exercise(self, event=None) -> None:
        assert self.current_exercise is not None

        weight_val = str(document.getElementById("exercise-weight").value)
        if weight_val:
            self.current_exercise.set_value(
                self.persistence,
                key="weight",
                value=float(weight_val),
            )

        set1 = str(document.getElementById("exercise-set1").value)
        if set1:
            self.current_exercise.set_value(
                self.persistence,
                key="set1",
                value=int(set1),
            )
        set2 = str(document.getElementById("exercise-set2").value)
        if set1:
            self.current_exercise.set_value(
                self.persistence,
                key="set2",
                value=int(set2),
            )

        done = self.current_exercise.get_value(
            self.persistence,
            key="done",
        )
        self.current_exercise.set_value(
            self.persistence,
            key="done",
            value=not done,
        )

        self.persistence.save()
        self._dom_show_workout()

    def on_show_json(self, event=None) -> None:
        assert self.current_workout_date != ""
        self._dom_show_view("view-json")
        kwargs = {} if IS_MICROPYTHON else {"indent": 2}
        document.getElementById("json-content").value = json.dumps(
            self.persistence.get_workout(
                workout_date=self.current_workout_date,
                remove_done=True,
            ),
            **kwargs,  # type: ignore
        )
        document.getElementById("json-error").textContent = ""

    def on_save_json(self, event=None) -> None:
        workout_text = str(document.getElementById("json-content").value)
        error_el = document.getElementById("json-error")
        try:
            dict_workout = json.loads(workout_text)
        except ValueError as e:
            error_el.textContent = f"Invalid JSON: {e}"
            return
        self.persistence.set_workout(
            workout_date=self.current_workout_date,
            dict_workout=dict_workout,
        )
        self.persistence.save()
        error_el.textContent = ""
        self._dom_show_workout()

    def on_back_from_json(self, event=None) -> None:
        self._dom_show_workout()

    def on_cancel_exercise(self, event=None) -> None:
        self._dom_show_workout()

    def on_delete_storage(self, event=None) -> None:
        self.current_workout_date = ""
        self.persistence.delete_storage()
        self.on_show_workouts()

    def on_delete_workout(self, event=None) -> None:
        self.persistence.delete_workout(workout_date=self.current_workout_date)
        self.on_show_workouts()


APP = FitnessApp()
