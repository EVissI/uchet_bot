import random
from typing import Tuple

from app.db.dao import MaterialReminderDAO
from app.db.models import MaterialReminder
from app.db.schemas import MaterialReminderFilter


def generate_math_example() -> Tuple[str, int]:
    """
    Generates a simple math example with numbers from 1 to 20
    Returns tuple with example string and correct answer
    """
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    operation = '+'
    
    example = f"{a} {operation} {b}"
    
    answer = a + b
            
    return example, answer




