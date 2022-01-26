""" Used to decode the number pattern into a description.
"""

def name(stroke: int) -> str:
    """ Turns a stroke number sequence into a name."""
    if stroke == 5:  # Dot
        return "Pan"
    if stroke == 159:  # Slash
        return "Zoom in"
    if stroke == 951:  # Reverse slash
        return "Full page view"
    if stroke == 357:  # Backslash
        return "Zoom in"
    if stroke == 753:  # Reverse backslash
        return "Zoom out"
    if stroke == 74123654:  # P
        return "Print"
    if stroke == 96321456:
        return "Backwards P"
    if stroke == 321456987:  # S
        return "Save"
    if stroke == 75357:
        return "Reverse backslash return"
    if stroke == 1475963:
        return "W"
    if stroke == 3214789:
        return "C"
    if stroke == 1235789:
        return "Z"
    if stroke == 3215987:
        return "Reverse Z"
    if stroke == 9874123:
        return "Reverse C"
    if stroke == 74159:
        return "Shark"
    if stroke == 96357:
        return "Reverse Shark"
    if stroke == 741236987:
        return "D"
    if stroke == 7412369:
        return "Upsidedown U"
    if stroke == 74123:
        return "Upsidedown L"
    if stroke == 1478963:
        return "U"
    if stroke == 32147:
        return "Reverse upside-down L"
    if stroke == 9632147:
        return "Reverse upside-down U"
    if stroke == 3698741:
        return "Reverse U"
    if stroke == 1474123:
        return "Small r"
    if stroke == 32159:
        return "Backwards 7"
    if stroke == 12357:
        return "7"
    if stroke == 95123:
        return "Reverse backwards 7"
    if stroke == 456:
        return "Dash"
    if stroke == 654:
        return "Reverse dash"
    if stroke == 258:
        return "Bar"
    if stroke == 852:
        return "Reverse bar"
    if stroke == 96321:
        return "Backwards upside-down L"
    if stroke == 7896321:
        return "Backwards reverse C"
    if stroke == 1236987:
        return "Backwards C"
    if stroke == 78963:
        return "Backwards reverse L"
    if stroke == 98741:
        return "Reverse L"
    if stroke == 14789:
        return "L"
    if stroke == 36987:
        return "Backwards L"
    if stroke == 12369:
        return "Backwards upside-down reverse L"
    if stroke == 123658:
        return "?"
    if stroke == 7415963:
        return "N"
    if stroke == 7415369:
        return "M"
    return "Unknown"

# Could add 3, E, B
