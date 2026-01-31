from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


try:
    from backend.analytics.report import load_session, summarize_session, interpret_profile
    from backend.game.engine import init_game, play_round
    from backend.core.schemas import ActionRequest, GameStateResponse
except ImportError:  
    from analytics.report import load_session, summarize_session, interpret_profile
    from game.engine import init_game, play_round
    from core.schemas import ActionRequest, GameStateResponse

app = FastAPI(title="LatentMind")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


GAME_SESSIONS = {}


@app.post("/start", response_model=GameStateResponse)
def start_game():
    game_id, state = init_game()
    GAME_SESSIONS[game_id] = state
    return state.public_view()


@app.post("/action", response_model=GameStateResponse)
def take_action(req: ActionRequest):
    state = GAME_SESSIONS.get(req.game_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Invalid game_id")

    new_state = play_round(state, req.action)
    GAME_SESSIONS[req.game_id] = new_state
    return new_state.public_view()


@app.get("/")
def root():
    return {
        "message": "LatentMind backend is running.",
        "endpoints": ["/start", "/action", "/docs"]
    }


@app.get("/report/{game_id}")
def get_report(game_id: str):
    rows = load_session(game_id)
    if not rows:
        return {"error": "Session not found"}

    summary = summarize_session(rows)
    interpretation = interpret_profile(summary["final_profile"])

    return {
        "game_id": game_id,
        "summary": summary,
        "interpretation": interpretation
    }
