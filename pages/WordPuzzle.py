import random
import streamlit as st

from word_puzzle import check_guess, check_math_answer, math_problem, puzzle_for_level


def _scramble_word(word: str) -> str:
    letters = list(word)
    if len(letters) < 2:
        return word
    shuffled = letters[:]
    while True:
        random.shuffle(shuffled)
        if ''.join(shuffled) != word:
            return ''.join(shuffled)


def _init_state():
    if 'puzzle_level' not in st.session_state:
        st.session_state.puzzle_level = 1
    if 'puzzle_score' not in st.session_state:
        st.session_state.puzzle_score = 0
    if 'puzzle_streak' not in st.session_state:
        st.session_state.puzzle_streak = 0
    if 'puzzle_seed' not in st.session_state:
        st.session_state.puzzle_seed = random.SystemRandom().randrange(1, 1_000_000)

    if 'math_level' not in st.session_state:
        st.session_state.math_level = 1
    if 'math_score' not in st.session_state:
        st.session_state.math_score = 0
    if 'math_streak' not in st.session_state:
        st.session_state.math_streak = 0
    if 'math_seed' not in st.session_state:
        st.session_state.math_seed = random.SystemRandom().randrange(1, 1_000_000)


def render():
    _init_state()

    st.subheader('🧩 AILYN WORD PUZZLE')
    st.caption('Randomized construction words and arithmetic challenges from easy to hardest.')

    game_mode = st.radio('Challenge', ['Words', 'Math'], horizontal=True, key='puzzle_game_mode')

    if game_mode == 'Words':
        current_level = int(st.session_state.puzzle_level)
        puzzle = puzzle_for_level(current_level, st.session_state.puzzle_seed)
        score = st.session_state.puzzle_score
        streak = st.session_state.puzzle_streak
        level = current_level
        prompt = 'Type the correct word...'
        hint = {
            'HOUSE': 'A home for people and families.',
            'BRICK': 'A building block used in masonry.',
            'PLATE': 'A flat structural or metal sheet.',
            'ROOF': 'The top covering of a structure.',
            'WALL': 'A vertical structure that divides space.',
            'CEMENT': 'A binding material used in construction.',
            'MIXER': 'A machine used to blend materials.',
            'TILE': 'A flat piece used for flooring or roofing.',
            'GLASS': 'A transparent material for windows.',
            'DOOR': 'An entry or exit panel in a wall.',
            'STRUCTURE': 'A built form made from parts and materials.',
            'FOUNDATION': 'The base that supports the whole building.',
            'SCHEDULE': 'A planned timeline for work progress.',
            'MEASUREMENT': 'The act of determining size and dimensions.',
            'RENOVATION': 'Updating or improving an existing property.',
        }.get(puzzle, 'Think about building and project work.')
        scramble = _scramble_word(puzzle)
        panel_text = f"<div class='puzzle-card'><div class='puzzle-level'>WORD LEVEL {level}</div><div class='puzzle-scramble'>{scramble}</div><div class='puzzle-hint'>Hint: {hint}</div></div>"
    else:
        current_level = int(st.session_state.math_level)
        math_question, math_answer = math_problem(current_level, st.session_state.math_seed)
        score = st.session_state.math_score
        streak = st.session_state.math_streak
        level = current_level
        prompt = 'Enter the numeric answer...'
        panel_text = (
            f"<div class='puzzle-card'><div class='puzzle-level'>MATH LEVEL {level}</div>"
            f"<div class='puzzle-scramble'>{math_question}</div>"
            "<div class='puzzle-hint'>Solve without a calculator. Difficulty increases each level.</div></div>"
        )

    score_col, streak_col, level_col = st.columns(3)
    with score_col:
        st.metric('Score', score)
    with streak_col:
        st.metric('Streak', streak)
    with level_col:
        st.metric('Level', level)

    st.markdown(panel_text, unsafe_allow_html=True)

    with st.form('word_puzzle_form', clear_on_submit=True):
        if game_mode == 'Words':
            answer = st.text_input('Your answer', placeholder=prompt)
        else:
            answer = st.number_input('Your answer', value=0, placeholder=prompt, step=1)
        submitted = st.form_submit_button('CHECK ANSWER', use_container_width=True)

    if submitted:
        if game_mode == 'Words':
            correct = check_guess(level, answer, st.session_state.puzzle_seed)
            if correct:
                st.session_state.puzzle_score += level * 10
                st.session_state.puzzle_streak += 1
                st.session_state.puzzle_level = level + 1
                st.session_state.puzzle_seed = random.SystemRandom().randrange(1, 1_000_000)
                st.success('Correct. Level unlocked!')
                st.rerun()
            else:
                st.session_state.puzzle_streak = 0
                st.error('Not quite. Try again.')
        else:
            correct = check_math_answer(math_answer, answer)
            if correct:
                st.session_state.math_score += level * 10
                st.session_state.math_streak += 1
                st.session_state.math_level = level + 1
                st.session_state.math_seed = random.SystemRandom().randrange(1, 1_000_000)
                st.success('Correct. Level unlocked!')
                st.rerun()
            else:
                st.session_state.math_streak = 0
                st.error('Not quite. Try again.')

    if st.button('RESET PUZZLE PROGRESS', key='reset_puzzle'):
        st.session_state.puzzle_level = 1
        st.session_state.puzzle_score = 0
        st.session_state.puzzle_streak = 0
        st.session_state.puzzle_seed = random.SystemRandom().randrange(1, 1_000_000)
        st.session_state.math_level = 1
        st.session_state.math_score = 0
        st.session_state.math_streak = 0
        st.session_state.math_seed = random.SystemRandom().randrange(1, 1_000_000)
        st.rerun()

    st.divider()
    if st.button('🏠 RETURN TO DASHBOARD', use_container_width=True, key='puzzle_home'):
        st.session_state.page = 'Dashboard'
        st.query_params['page'] = 'Dashboard'
        st.rerun()
