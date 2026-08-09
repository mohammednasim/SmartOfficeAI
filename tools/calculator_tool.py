import math


def calculator(expression):
    """
    Simple calculator tool.
    Example:
        10+20
        100/5
        25*8
        (20+5)*3
        math.sqrt(81)
    """

    try:
        
        result = eval(
            expression,
            {
                "__builtins__": {},
                "math": math
            },
            {}
        )

        return f"Answer: {result}"

    except Exception as e:

        return f"Calculation Error: {e}"