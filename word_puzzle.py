import random
import re

WORD_PUZZLES = {
    1: ["HOUSE", "BRICK", "PLATE", "ROOF", "WALL"],
    2: ["CEMENT", "MIXER", "TILE", "GLASS", "DOOR"],
    3: ["STRUCTURE", "FOUNDATION", "SCHEDULE", "MEASUREMENT", "RENOVATION"],
}


def puzzle_for_level(level, seed=None):
    rng = random.Random(seed) if seed is not None else random
    options = WORD_PUZZLES.get(level, WORD_PUZZLES[1])
    return rng.choice(options)


def check_guess(level, guess, seed=None):
    answer = puzzle_for_level(level, seed)
    return str(guess or "").strip().upper() == str(answer).upper()


def check_math_answer(expected, guess):
    try:
        return float(guess) == float(expected)
    except (TypeError, ValueError):
        return False


def math_problem(level, seed=None):
    rng = random.Random(seed) if seed is not None else random
    base = max(2, int(level))
    a = rng.randint(2, 10 * base)
    b = rng.randint(2, 10 * base)
    operator = rng.choice(["+", "-", "*"])
    if operator == "+":
        answer = a + b
        question = f"{a} + {b}"
    elif operator == "-":
        answer = a - b if a >= b else b - a
        question = f"{max(a, b)} - {min(a, b)}"
    else:
        answer = a * b
        question = f"{a} x {b}"
    return question, answer
