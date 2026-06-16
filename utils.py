import time


def log_event(stage: str, data: dict):
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] {stage}: {data}")


def short_response(result, user_input: str) -> str:
    if isinstance(result, list):
        if not result:
            return "No files found"
        
        names = [r.split("/")[-1] for r in result[:3]]
        return ", ".join(names)

    if isinstance(result, str):
        return result[:60]

    return "Done"