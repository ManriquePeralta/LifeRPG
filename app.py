from flask import Flask, jsonify, request, render_template
from datetime import date
from models import Stats, Calendar
from models import Player
from actions import ALL_ACTIONS




player = Player()
app = Flask(__name__)




def relationship_multiplier(player):
    if player.stats.get("relacion") >= 80:
        return 1.1
    return 1.0




@app.route("/stats", methods=["GET"])
def get_stats():
    return jsonify(player.stats.values)


@app.route("/actions", methods=["GET"])
def list_actions():
    return jsonify([
{
"name": a.name,
"type": a.action_type,
"requirements": a.requirements
}
for a in ALL_ACTIONS
])




@app.route("/do_action", methods=["POST"])
def do_action():
    data = request.json
    action_name = data.get("action")

    action = next((a for a in ALL_ACTIONS if a.name == action_name), None)
    if not action:
        return jsonify({"error": "Acción no encontrada"}), 404

    if action.is_allowed(player):
        if action.action_type == "positive":
            mult = relationship_multiplier(player)
            action.apply_effects(player, multiplier=mult)
            result = "OK"
        else:
             # special permitida → COSTO
            action.apply_effects(player)
            result = "SPECIAL_COST"
    else:
         # no permitida → CASTIGO
        action.apply_penalty(player)
        result = "RULE_BROKEN"

    # Registrar en el calendario
    today = str(date.today())
    happiness_value = player.stats.get("felicidad")
    notes = data.get("notes", "")
    player.calendar.update_entry(today, happiness_value, notes)

    return jsonify({
    "result": result,
    "action": action.name,
    "type": action.action_type,
    "allowed": action.is_allowed(player),
    "stats": player.stats.values
})


@app.route("/calendar", methods=["GET"])
def get_calendar():
    return jsonify(player.calendar.get_all())


@app.route("/calendar/<day>", methods=["GET"])
def get_day(day):
    entry = player.calendar.get_entry(day)
    if entry:
        return jsonify(entry)
    return jsonify({"error": "Día no encontrado"}), 404


@app.route("/calendar/<day>", methods=["POST"])
def update_day(day):
    data = request.json
    notes = data.get("notes", "")
    happiness = data.get("happiness", 50)
    player.calendar.update_entry(day, happiness, notes)
    return jsonify({"success": True, "data": player.calendar.get_entry(day)})


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)