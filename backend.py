from flask import Flask, request, jsonify
from flask_cors import CORS
import psutil
import os
from google import genai
from commands import processcommand
from logger import log_command
from weather import get_weather
from dotenv import load_dotenv

from memory import list_memories
import requests

from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pythoncom

load_dotenv()

app = Flask(__name__)
CORS(app)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

@app.route("/api/health")
def health():

    return jsonify({
        "status": "online"
    })

# ─────────────────────────────────────────────
# SYSTEM API
# ─────────────────────────────────────────────

@app.route("/api/system")
def system():

    battery = psutil.sensors_battery()

    # Disk
    disk = psutil.disk_usage("C:\\")

    # Temperature
    temperature = None

    # Volume
    try:

        pythoncom.CoInitialize()

        devices = AudioUtilities.GetSpeakers()

        interface = devices.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL,
            None
        )

        volume = cast(
            interface,
            POINTER(IAudioEndpointVolume)
        )

        current = volume.GetMasterVolumeLevelScalar()

        volume_percent = round(current * 100)

    except Exception as e:

        print(
            "VOLUME ERROR:",
            e
        )

        volume_percent = 0
    return jsonify({

        "cpu": psutil.cpu_percent(
            interval=0.1
        ),

        "ram": {
            "used": round(
                psutil.virtual_memory().used
                / (1024 ** 3),
                1
            ),
            "total": round(
                psutil.virtual_memory().total
                / (1024 ** 3),
                1
            ),
            "percentage": psutil.virtual_memory().percent
        },

        "battery": {
            "level": (
                battery.percent
                if battery else 100
            ),
            "isCharging": (
                battery.power_plugged
                if battery else False
            )
        },

        "disk": {
            "used": round(
                disk.used / (1024 ** 3),
                1
            ),
            "total": round(
                disk.total / (1024 ** 3),
                1
            ),
            "percentage": disk.percent
        },

        "temperature": temperature,

        "volume": volume_percent
    })

# ─────────────────────────────────────────────
# CHAT API
# ─────────────────────────────────────────────

@app.route("/api/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "response": "No data received."
            }), 400

        messages = data.get(
            "messages",
            []
        )

        if not messages:

            return jsonify({
                "response": "No message provided."
            }), 400

        user_input = messages[-1].get(
            "content",
            ""
        ).strip()

        if not user_input:

            return jsonify({
                "response": "Empty message."
            }), 400

        print(
            f"\nUSER: {user_input}"
        )

        # -----------------------------
        # Command Processing
        # -----------------------------

        result = processcommand(
            user_input
        )

        if result:

            log_command(
                user_input,
                result
            )

            return jsonify({
                "response": str(result)
            })

        # -----------------------------
        # Gemini Fallback
        # -----------------------------

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_input
        )

        ai_response = (
            response.text.strip()
            if response.text
            else "No response generated."
        )

        log_command(
            user_input,
            ai_response
        )

        return jsonify({
            "response": ai_response
        })

    except Exception as e:

        print(
            "Backend Error:",
            e
        )

        return jsonify({
            "response": f"Error: {str(e)}"
        }), 500
        
@app.route("/api/weather")
def weather():

    data = get_weather("Tiruchirappalli")

    if not data:
        return jsonify({
            "error": "Weather unavailable"
        }), 500

    return jsonify(data)

@app.route("/api/history")
def history():

    try:

        with open(
            "logs/commands.log",
            "r",
            encoding="utf-8"
        ) as file:

            logs = file.readlines()

        return jsonify({
            "history": logs[::-1][:100]
        })

    except Exception:

        return jsonify({
            "history": []
        })
    


@app.route("/api/memories")
def memories():

    return jsonify({
        "memories": list_memories()
    })

@app.route("/api/screenshots")
def screenshots():

    try:

        files = []

        if os.path.exists("Screenshots"):

            for file in os.listdir("Screenshots"):

                if file.lower().endswith(".png"):

                    files.append(file)

        files.sort(
    key=lambda x: os.path.getmtime(
        os.path.join(
            "Screenshots",
            x
        )
    ),
    reverse=True
)

        return jsonify({
            "screenshots": files
        })

    except Exception:

        return jsonify({
            "screenshots": []
        })
    

# ─────────────────────────────────────────────
# START SERVER
# ─────────────────────────────────────────────

if __name__ == "__main__":

    print(
        "\nVEERA Backend Started"
    )

    print(
        "API Running: http://localhost:8000"
    )

    app.run(
        host="0.0.0.0",
        port=8000,
        debug=False
    )
