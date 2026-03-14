FACTOR_TWO_MACHINES = 0.5
FACTOR_DOUBLE_EXERCIZE = 2.0
FACTOR_ROOM = -0.1
"""
room: 1 begin, 10 end
"""

EXERCISES = {
    "factor": 3 * FACTOR_ROOM,
    "E1": {
        "short": "ROM 1",
        "comment": "Abduktor",
        "weight": 54.5,
        "set1": 16,
        "set2": 16,
    },
    "E2": {
        "factor": 3 * FACTOR_ROOM,
        "short": "ROM 5",
        "comment": "Adduktor",
        "weight": 38.3,
        "set1": 16,
        "set2": 16,
    },
    "A5": {
        "factor": 10 * FACTOR_ROOM * FACTOR_DOUBLE_EXERCIZE,
        "short": "Beinbeuger",
        "comment": "Technogym, Sitz 2, Fuss 1, ROM 2",
        "weight": 17.5,
        "set1": 17,
        "set2": 17,
    },
    "A2": {
        "factor": 10 * FACTOR_ROOM * FACTOR_DOUBLE_EXERCIZE,
        "short": "Beinpresse",
        "comment": "Sitz 1, Fuss 2",
        "weight": 40.0,
        "set1": 18,
        "set2": 18,
    },
    "C1": {
        "factor": 7 * FACTOR_ROOM,
        "short": "Bauch Crunch",
        "comment": "Nautilus, Sitz 3",
        "weight": 30.0,
        "set1": 18,
        "set2": 18,
    },
    "Mitte1": {
        "factor": 5 * FACTOR_ROOM * FACTOR_DOUBLE_EXERCIZE,
        "short": "Kurzhantel 45 Bank Seitenneigen",
        "comment": "Höhe 4",
        "weight": 3.0,
        "set1": 17,
        "set2": 17,
    },
    "Mitte2": {
        "factor": 5 * FACTOR_ROOM * FACTOR_DOUBLE_EXERCIZE,
        "short": "45 Bank Rückenstrecken mit Gewicht",
        "comment": "Höhe 2",
        "weight": 3.0,
        "set1": 16,
        "set2": 16,
    },
    "B5": {
        "factor": 4 * FACTOR_ROOM,
        "short": "Lat Zug",
        "comment": "Technogym, Sitz 4",
        "weight": 27.5,
        "set1": 18,
        "set2": 18,
    },
    "D2": {
        "factor": 1 * FACTOR_ROOM,
        "short": "Butterfly gebeugte Arme",
        "comment": "Technogym, Sitz 4",
        "weight": 12.5,
        "set1": 16,
        "set2": 16,
    },
    "F1": {
        "factor": 1 * FACTOR_ROOM,
        "short": "Schulterdrücken",
        "comment": "Technogym, Sitz 4",
        "weight": 7.5,
        "set1": 15,
        "set2": 15,
    },
    "H2": {
        "factor": 4 * FACTOR_ROOM,
        "short": "Trizepsstrecken",
        "comment": "Sitz 4, Rücken 4",
        "weight": 9.0,
        "set1": 18,
        "set2": 18,
    },
}
