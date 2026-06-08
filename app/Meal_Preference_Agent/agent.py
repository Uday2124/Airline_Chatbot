import re
import requests
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

API_BASE = "http://127.0.0.1:5000/api"

# --- CONCISE TOOLS ---
def get_booking_info(pnr: str):
    """Retrieves passenger list, flight numbers, and current meal status for a PNR."""
    try:
        res = requests.get(f"{API_BASE}/booking/{pnr}")
        return {"success": True, "data": res.json()} if res.status_code == 200 else {"success": False, "message": "PNR not found"}
    except Exception as e: return {"success": False, "message": str(e)}

# --- MEAL CATALOG TOOLS ---
def get_meal_catalog():
    """Fetches the list of available meal names from the airline catalog."""
    try:
        res = requests.get(f"{API_BASE}/meal/catalog")
        return {"success": True, "meals": res.json().get("meals", [])} if res.status_code == 200 else {"success": False, "message": "Catalog unavailable"}
    except Exception as e: return {"success": False, "message": str(e)}

# --- MEAL UPDATE TOOL ---
def update_passenger_meal(pnr: str, passenger_id: str, meal_name: str):
    """Updates a specific passenger's meal choice. Requires passenger_id and a valid meal_name."""
    try:
        res = requests.put(f"{API_BASE}/booking/{pnr}/meal", json={"passenger_id": passenger_id, "meal_name": meal_name})
        return {"success": True, "message": res.json()["message"]} if res.status_code == 200 else {"success": False, "message": res.text}
    except Exception as e: return {"success": False, "message": str(e)}
    
# --- LLM Model ---
llm = LiteLlm(model="openai/gpt-4o-mini",temperature=0.5)

# --- Meal Preference Agent ---
root_agent = Agent(
    name="Meal_Preference_Agent",
    model=llm,
    instruction="""
   ROLE: Meal Specialist
    * Handle meal-related requests (meal, food, diet). If passenger details are requested, provide exact details.
    * Ignore all non-meal messages silently — do not mention seats, travel, or other topics.
    * If non-meal messages are detected, then transfer to supervisor agent directly without any explanation.
    * Treat any message containing meal-related terms as a valid meal request.

    CONVERSATION FLOW:
    1.Strict Rule: If user asks for booking/passenger details, just call get_booking_info and provide exact passenger details. Do not call any other tools(as per the user request).
    2. PNR Detection & Memory
     - Automatically extract PNR from any user message (e.g., PNR002).
     - Store the last used PNR in memory.
    3. Passenger Selection
     - Use get_booking_info(PNR) to get passengers.
     - If multiple passengers exist, prompt the user to select one (show name and flight).
     - If only one passenger, auto-select.
    4. Meal Selection
     - Use get_meal_catalog() to show valid meal options only if the user has not specified a meal.
     - If the user specifies a valid meal from the catalog, update immediately.
    5. Meal Update
     - Show the current meal for the selected passenger and validate the new meal with the current meal to avoid unnecessary updates.
     - Call update_passenger_meal(PNR, passenger, meal) immediately after valid selection.
     - Confirm with:    
        “The meal for [Passenger Name] on flight [Flight No] has been updated to [Meal].”

    STRICT RULES: (follow these strictly)
     - Never invent meals; only use meals from get_meal_catalog().
     - Never ask for PNR unnecessarily if already provided. Only ask for PNR if none is in memory and none is in the current message.
     - Ignore all non-meal messages silently. Transfer to supervisor agent directly without any explanation.
     - Do not mention seats, travel, or transfer to other agents.
     - Continue until meal update or clarification is complete.

    OUTPUT & TONE:
    - Polite, precise, professional confirmations.
    - Invisible for non-meal topics.
    """,
    tools=[get_booking_info, get_meal_catalog, update_passenger_meal]
)