from fastapi import FastAPI
from pydantic import BaseModel
from intent import parse_intent
from actions import handle_action
from utils import short_response, log_event

app = FastAPI()


class CommandRequest(BaseModel):
    text: str


@app.post("/command")
async def command(req: CommandRequest):
    user_input = req.text.strip()

    log_event("INPUT", {"text": user_input})

    intent = parse_intent(user_input)
    log_event("INTENT", intent)

    try:
        result = handle_action(intent)
    except Exception as e:
        result = f"Error: {str(e)}"

    log_event("RESULT", result)

    response = short_response(result, user_input)
    log_event("RESPONSE", response)

    return {
        "intent": intent,
        "response": response
    }