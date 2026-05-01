import random

SESSION_KEY = 'captcha_answer'

_QUESTIONS = [
    ('+', lambda a, b: a + b),
    ('-', lambda a, b: a - b),
]


def generate(request):
    """Store a new math question in the session and return the question string."""
    op_symbol, op_fn = random.choice(_QUESTIONS)
    if op_symbol == '+':
        a, b = random.randint(2, 15), random.randint(2, 15)
    else:
        a = random.randint(6, 20)
        b = random.randint(1, a - 1)
    request.session[SESSION_KEY] = str(op_fn(a, b))
    return f"What is {a} {op_symbol} {b}?"


def verify(request, user_answer):
    """Return True if user_answer matches the stored answer, then clear it."""
    correct = request.session.pop(SESSION_KEY, None)
    if not correct:
        return False
    return user_answer.strip() == correct
