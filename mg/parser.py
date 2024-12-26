import ply.lex as lex
import ply.yacc as yacc

tokens = ("DATE", "EXERCISE", "NUMBER", "COMMA")

t_COMMA = r","
t_ignore = " \t"


def t_DATE(t):
    r"\d{4}-\d{2}-\d{2}"
    return t


def t_EXERCISE(t):
    r"[A-Za-z]+"
    return t


def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


lexer = lex.lex()


def p_workout(p):
    """workout : DATE exercises"""
    p[0] = (p[1], p[2])


def p_exercises_multiple(p):
    """exercises : exercise exercises"""
    p[0] = [p[1]] + p[2]


def p_exercises_single(p):
    """exercises : exercise"""
    p[0] = [p[1]]


def p_exercise(p):
    """exercise : EXERCISE sets"""
    p[0] = (p[1], p[2])


def p_sets_multiple(p):
    """sets : set COMMA sets"""
    p[0] = [p[1]] + p[3]


def p_sets_single(p):
    """sets : set"""
    p[0] = [p[1]]


def p_set_weight_reps(p):
    """set : NUMBER NUMBER"""
    p[0] = (p[1], p[2])


def p_set_reps(p):
    """set : NUMBER"""
    p[0] = (None, p[1])


def p_error(p):
    print(f"Syntax error at '{p.value}'")


parser = yacc.yacc()


def fill_none_with_previous(weights):
    if all(weight is None for weight, _ in weights):
        return [(0, reps) for _, reps in weights]
    last_weight = 0
    result = []
    for weight, reps in weights:
        if weight is not None:
            last_weight = weight
        result.append((last_weight, reps))
    return result


def create_exercise_dict(exercises):
    exercise_dict = {}
    for exercise, sets in exercises:
        sets = fill_none_with_previous(sets)
        reps = [reps for _, reps in sets]
        intensity = [weight for weight, _ in sets]
        exercise_dict[exercise] = {"reps": reps, "intensity": intensity}
    return exercise_dict
