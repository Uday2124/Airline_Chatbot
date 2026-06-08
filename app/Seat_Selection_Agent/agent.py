import requests
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

API_BASE = "http://127.0.0.1:5000/api"

# --- CONCISE TOOLS ---
def get_booking_info(pnr: str):
    """Retrieves passenger list, flight numbers, and current seat status for a PNR."""
    try:
        res = requests.get(f"{API_BASE}/booking/{pnr}")
        return {"success": True, "data": res.json()} if res.status_code == 200 else {"success": False, "message": "PNR not found"}
    except Exception as e: return {"success": False, "message": str(e)}

# --- SEAT TOOLS ---
def get_seat_layout(flight_number: str):
    """Fetches the full seat layout (numbers, types, legroom, status) for a specific flight."""
    try:
        res = requests.get(f"{API_BASE}/aircraft/{flight_number}/layout")
        return {"success": True, "seats": res.json().get("seats", [])} if res.status_code == 200 else {"success": False, "message": "Layout not found"}
    except Exception as e: return {"success": False, "message": str(e)}

# --- SEAT UPDATE TOOL ---
def update_passenger_seat(pnr: str, passenger_id: str, seat_number: str, flight_number: str, confirmed: bool = False):
    """Assigns a seat. Handles extra legroom automatically."""
    try:
        # Get seat layout
        layout = get_seat_layout(flight_number)

        if not layout["success"]:
            return {"success": False, "message": "Unable to fetch seat layout"}

        # Find selected seat
        seat = next((s for s in layout["seats"] if s["seat_number"] == seat_number), None)

        if not seat:
            return {"success": False, "message": "Seat not found"}

        # Check extra legroom
        if seat.get("extra_legroom") == 1 and not confirmed:
            return {
                "success": False,
                "requires_confirmation": True,
                "message": f"Seat {seat_number} has extra legroom ($25 fee). Proceed?"
            }

        #Call API
        res = requests.put(
            f"{API_BASE}/booking/{pnr}/seat",
            json={
                "passenger_id": passenger_id,
                "seat_number": seat_number,
                "flight_number": flight_number
            }
        )

        return {
            "success": res.status_code == 200,
            "message": res.json().get("message", res.text)
        }

    except Exception as e:
        return {"success": False, "message": str(e)}


# --- LLM Model ---
llm = LiteLlm(model="openai/gpt-4o-mini",temperature=0.5)

root_agent = Agent(
    name="Seat_Selection_Agent",
    model=llm,
    instruction="""
    ROLE: Seat Specialist
    You are an expert in seat assignments and cabin preferences (Window, Aisle, Legroom). Only handle seat-related tasks.

    OPERATIONAL PROTOCOLS:
    1.Strict Rule: If user asks for booking/passenger details, just call get_booking_info and provide exact passenger details. Do not call any other tools(as per the user request).
    2.PNR Extraction: Identify the PNR (ex: PNR001) from the conversation; do not ask if already provided.
    3.Verification: Call get_booking_info to retrieve current seat and passenger details.
    4.Passenger Selection: If multiple passengers exist, prompt the user to specify which passenger.
    5.Seat Layout: Call get_seat_layout(flight_number). List available seats clearly; separately list booked/blocked seats.
    6.Premium Seats: If user selects seats with extra_legroom, Inform the user of the $25 fee and await explicit confirmation before calling update_passenger_seat(confirmed=True).

    SCOPE & BOUNDARIES:
    1.Handle only seats.
    2.If user mentions meals, visas, or other topics, do not respond; silently return control to Supervisor_Agent.
    3.Never explain, Never give extra responses, or mention other agents.

    OUTPUT & TONE:
        Confirmation Message:   Confirmation Message: Give a polite and professional confirmation message with the passenger's name, flight number, and new seat number.
        Tone: Helpful, precise, technical, and invisible for non-seat topics.
    """,
    tools=[get_booking_info, get_seat_layout, update_passenger_seat]
)