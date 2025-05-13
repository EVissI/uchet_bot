import random
from typing import Tuple

def generate_math_example() -> Tuple[str, int]:
    """
    Generates a simple math example with numbers from 1 to 20
    Returns tuple with example string and correct answer
    """
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    operations = ['+','*']
    operation = random.choice(operations)
    
    example = f"{a} {operation} {b}"
    
    match operation:
        case '+':
            answer = a + b
        case '*':
            answer = a * b
            
    return example, answer

def escape_markdown(text: str) -> str:
    """Escape special characters for MarkdownV2"""
    if not isinstance(text, str):
        text = str(text)
    chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in chars:
        text = text.replace(char, f'\{char}')
    return text