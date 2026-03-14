FACTOR_TWO_MACHINES = 0.5
FACTOR_DOUBLE_EXERCIZE = 2.0
FACTOR_ROOM = -0.1
"""
room: 1 begin, 10 end
"""

EXERCISES = {
    "A5": {
        "factor": 10 * FACTOR_ROOM * FACTOR_DOUBLE_EXERCIZE,
        "short": "Leg Curls",
        "comment": "Technogym, Sitz 6, Fuss 6, ROM 2",
        "weight": 35.0,
    },
    "A2": {
        "factor": 10 * FACTOR_ROOM * FACTOR_DOUBLE_EXERCIZE,
        "short": "Leg Press",
        "comment": "Sitz 4, Fuss 1",
        "weight": 60.0,
    },
    "C3": {
        "factor": 7 * FACTOR_ROOM * FACTOR_DOUBLE_EXERCIZE,
        "short": "Torso Rotation sitting",
        "comment": "Nautilus ROM 80",
        "weight": 36.0,
    },
    "C1": {
        "factor": 7 * FACTOR_ROOM,
        "short": "Abdominal Crunch",
        "comment": "Nautilus, Sitz 6",
        "weight": 30.0,
    },
    "D1/D4": {
        "factor": 3 * FACTOR_ROOM * FACTOR_DOUBLE_EXERCIZE,
        "short": "Chest Press",
        "comment": "Nautilus, Sitz 7, Rücken 2",
        "weight": 30.0,
    },
    "B5": {
        "factor": 4 * FACTOR_ROOM,
        "short": "Lat Pull",
        "comment": "Technogym, Sitz 6",
        "weight": 40.0,
    },
    "B4": {
        "factor": 6 * FACTOR_ROOM,
        "short": "Cable Row Close",
        "comment": "Technogym",
        "weight": 20.0,
    },
    "B2/B7": {
        "factor": 3 * FACTOR_ROOM * FACTOR_DOUBLE_EXERCIZE,
        "short": "Butterfly",
        "comment": "Nautilus, Rücken 2",
        "weight": 23.0,
    },
    "B3": {
        "factor": 7 * FACTOR_ROOM * FACTOR_DOUBLE_EXERCIZE,
        "short": "Back Extension",
        "comment": "Technogym, Rücken 4, ROM 2",
        "weight": 35.0,
    },
    "F1": {
        "factor": 4 * FACTOR_ROOM,
        "short": "Shoulder Press",
        "comment": "Technogym, Sitz 6",
        "weight": 15.0,
    },
}
