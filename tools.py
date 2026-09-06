def calculate(expression):
    try:
        result = eval(expression, {"_builtins_": {}}, {})
        return f"Calculator result: {result}"
    except Exception:
        return "Sorry, I could not calculate that."


def create_study_plan(subject, hours):
    return (
        f"Study Plan for {subject}:\n"
        f"1. Read the topic - {hours // 2} hours\n"
        f"2. Practice questions - 1 hour\n"
        f"3. Quick revision - 1 hour"
    )