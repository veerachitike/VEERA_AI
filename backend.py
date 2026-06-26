from flask import (Flask,jsonify,request)
from werkzeug.utils import secure_filename
from flask_cors import CORS
import psutil
import os
from google import genai
from commands import processcommand
from logger import log_command
from weather import get_weather
from dotenv import load_dotenv
from flask import send_from_directory
from memory import (list_memories,save_memory,delete_memory,get_memory)
from memory_extractor import extract_memory
from chat_history import (save_chat,get_history)
import requests
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pythoncom
from rapidfuzz import fuzz
import json
from notifications import notify
from pypdf import PdfReader
from docx import Document
from ai import analyze_document
from speech import speak

DOCUMENTS = {}
load_dotenv()
def get_model():

    try:

        with open(
            "settings.json",
            "r",
            encoding="utf-8"
        ) as f:

            settings = json.load(f)

        return settings.get(
            "model",
            "gemini-2.5-flash"
        )

    except Exception as e:

        print(
            "Settings Read Error:",
            e
        )

        return "gemini-2.5-flash"
def similar(text, phrases, threshold=80):

    for phrase in phrases:

        score = fuzz.partial_ratio(
            text.lower(),
            phrase.lower()
        )

        if score >= threshold:

            return True

    return False
def memory_enabled():

    try:

        with open(
            "settings.json",
            "r",
            encoding="utf-8"
        ) as f:

            settings = json.load(f)

        return settings.get(
            "memoryEnabled",
            True
        )

    except Exception as e:

        print(
            "Settings Read Error:",
            e
        )

        return True
    
UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)
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

        conversation_id = data.get(
            "conversationId",
            "default"
        )

        print("=" * 60)
        print("CONVERSATION:", conversation_id)
        print("HAS DOCUMENT:", data.get("hasDocument"))
        print("DOCUMENT NAME:", data.get("documentName"))
        print("=" * 60)

        has_document = data.get(
            "hasDocument",
            False
        )

        document_name = data.get(
            "documentName",
            ""
        )

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

        # -----------------------------------
        # AUTO MEMORY EXTRACTION
        # -----------------------------------

        try:

            extracted = extract_memory(
                user_input
            )

            if extracted and memory_enabled():

                key, value = extracted

                save_memory(
                    key,
                    value
                )
                notify(
                    "VEERA Memory",
                    f"Saved: {key}"
                )
                print(
                    f"MEMORY SAVED: {key} = {value}"
                )

        except Exception as e:

            print(
                "Memory Extraction Error:",
                e
            )
        if not user_input and not has_document:

            return jsonify({
                "response": "Empty message."
            }), 400

        if not user_input and has_document:

            user_input = (
                f"Analyze the uploaded document "
                f"'{document_name}'."
            )
        print(
            f"\nUSER: {user_input}"
        )
        # ===================================
        # MEMORY COMMANDS
        # ===================================

        text = user_input.lower()
        # -----------------------------------
        # WHAT DO YOU KNOW ABOUT ME
        # -----------------------------------

        if similar(
                text,
                [
                    "what do you know about me",
                    "tell me about me",
                    "what do you remember about me",
                    "who am i"
                ]
            ):

            memories = list_memories()

            if not memories:

                return jsonify({
                    "response":
                    "I don't know anything about you yet."
                })

            response = "\n".join(
                [
                    f"{k}: {v}"
                    for k, v in memories
                ]
            )

            return jsonify({
                "response": response
            })

        # -----------------------------------
        # SHOW ALL MEMORIES
        # -----------------------------------

        if similar(
            text,
            [
                "show all memories",
                "show my memories",
                "list memories",
                "list my memories"
            ]
        ):
            memories = list_memories()

            if not memories:

                return jsonify({
                    "response":
                    "No memories stored."
                })

            response = "\n".join(
                [
                    f"{k}: {v}"
                    for k, v in memories
                ]
            )

            return jsonify({
                "response": response
            })

        # -----------------------------------
        # REMEMBER
        # -----------------------------------

        if (
            text.startswith("remember")
            or text.startswith("save this")
            or text.startswith("store this")
        ):

            memory_text = (
                user_input
                .replace("remember", "")
                .replace("save this", "")
                .replace("store this", "")
                .strip()
            )

            if " is " in memory_text:

                key, value = memory_text.split(
                    " is ",
                    1
                )

                key = (
                    key.strip()
                    .lower()
                    .replace("my ", "")
                    .replace(" ", "_")
                )

                if not memory_enabled():

                    return jsonify({
                        "response":
                        "Memory system is disabled."
                    })

                save_memory(
                    key,
                    value.strip()
                )

                return jsonify({
                    "response":
                    f"I've remembered that {key} is {value}."
                })

        # -----------------------------------
        # FORGET
        # -----------------------------------

        if (
            text.startswith("forget")
            or text.startswith("delete memory")
            or text.startswith("remove memory")
        ):

            memory_key = (
                user_input
                .replace("forget", "")
                .replace("delete memory", "")
                .replace("remove memory", "")
                .strip()
            )

            memory_key = (
                memory_key
                .lower()
                .replace("my ", "")
                .replace("the ", "")
                .replace(" ", "_")
            )

            success = delete_memory(
                memory_key
            )

            if success:

                return jsonify({
                    "response":
                    f"I've forgotten {memory_key}."
                })

            return jsonify({
                "response":
                f"I couldn't find {memory_key}."
            })
        # -----------------------------
        # Command Processing
        # -----------------------------
        desktop_commands = [
            "open",
            "close",
            "launch",
            "start",
            "shutdown",
            "restart",
            "mute",
            "volume",
            "screenshot",
            "clipboard",
        ]

        if any(user_input.lower().startswith(cmd)for cmd in desktop_commands):

            result = processcommand(user_input)

            if result:

                log_command(
                    user_input,
                    result
                )

                save_chat(
                    conversation_id,
                    user_input,
                    str(result)
                )

                return jsonify({
                    "response": str(result)
                })
        # ===================================
        # GENERIC MEMORY LOOKUP
        # ===================================

        best_match = None
        best_score = 0

        for key, value in list_memories():

            readable_key = (
                key.replace(
                    "_",
                    " "
                )
                .lower()
            )

            score = fuzz.token_set_ratio(
            text,
            readable_key
            )

            if score > best_score:

                best_score = score
                best_match = (
                    readable_key,
                    value
                )
        print(
            f"BEST MATCH: {best_match}"
        )

        print(
            f"BEST SCORE: {best_score}"
        )
        if best_match and best_score >= 80:

            key, value = best_match

            return jsonify({
                "response":
                f"Your {key} is {value}."
            })
        # -----------------------------
        # Gemini Fallback
        # -----------------------------

        memories = list_memories()

        memory_context = ""

        for key, value in memories:

            memory_context += (
                f"{key}: {value}\n"
            )

        recent_history = ""     
        # -----------------------------
        # Document Context
        # -----------------------------

        document_context = ""

        document = DOCUMENTS.get(
            conversation_id,
            {}
        )

        if document:

            document_context = f"""
        ========================
        UPLOADED DOCUMENT
        ========================

        File Name:
        {document.get("name", "")}

        The user has uploaded this document.

        Use this document ONLY if the user's request refers to:
        - this
        - this document
        - this file
        - summarize
        - analyze
        - explain
        - brief
        - extract
        - key points

        If the user's request is unrelated, ignore this document completely.

        DOCUMENT CONTENT:

        {document.get("content", "")[:12000]}

        ========================
        END OF DOCUMENT
        ========================
        """
        # -----------------------------
        # Prompt
        # -----------------------------

        prompt = f"""
        You are VEERA AI, an intelligent desktop assistant.

        Memory Vault:

        {memory_context}

        Recent Conversation:

        {recent_history}

        {document_context}

        Instructions:

        1. Use Memory Vault only when relevant.
        2. Use recent conversation only when relevant.
        3. Use the uploaded document ONLY if it appears above.
        4. If no document appears above, ignore any previous uploaded documents.
        5. Never assume a document exists.
        6. Be concise, accurate and helpful.

        User Request:
        {user_input}

        Assistant:
        """

        model_name = get_model()



        print(f"Using Model: {model_name}")

        print("=" * 80)
        print("CONVERSATION:", conversation_id)
        print("HAS DOCUMENT:", has_document)
        print("DOCUMENT NAME:", document.get("name", "None"))
        print("DOCUMENT LENGTH:", len(document.get("content", "")))
        print("=" * 80)

        try:

            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            ai_response = (
                response.text.strip()
                if response.text
                else "No response generated."
            )
            speak(ai_response[:300])
        except Exception as e:

            print("Gemini Error:", e)

            ai_response = (
                f"Gemini Error: {str(e)}"
            )

        log_command(
            user_input,
            ai_response
        )

        save_chat(
            conversation_id,
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
                "response": str(e)
            }), 500
    
@app.route("/api/chat-history")
def chat_history():

    return jsonify({
        "history":
        get_history()[::-1]
    })

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

@app.route("/api/memory/add", methods=["POST"])
def add_memory():

    try:

        data = request.get_json()

        key = data.get("key", "").strip()
        value = data.get("value", "").strip()

        if not key or not value:

            return jsonify({
                "success": False,
                "message": "Missing key or value"
            }), 400

        from memory import save_memory

        save_memory(
        key,
        value
        )

        return jsonify({
            "success": True
        })
    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@app.route("/api/memory/update", methods=["POST"])
def update_memory():

    try:

        data = request.get_json()

        key = data.get(
            "key",
            ""
        ).strip()

        value = data.get(
            "value",
            ""
        ).strip()

        from memory import save_memory

        save_memory(
            key,
            value
        )

        return jsonify({
            "success": True
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    

@app.route("/api/memory/delete", methods=["POST"])
def delete_memory_api():

    try:

        data = request.get_json()

        key = data.get(
            "key",
            ""
        ).strip()

        if not key:

            return jsonify({
                "success": False
            }), 400

        from memory import delete_memory

        success = delete_memory(key)

        return jsonify({
            "success": success
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    
    
    
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
    
@app.route("/screenshots/<filename>")
def serve_screenshot(filename):

    return send_from_directory(
    "Screenshots",
    filename
    )

@app.route("/api/settings", methods=["GET"])
def get_settings():

    try:

        with open(
            "settings.json",
            "r",
            encoding="utf-8"
        ) as f:

            settings = json.load(f)

        return jsonify(settings)

    except Exception as e:

        return jsonify(
            {
                "error": str(e)
            }
        ), 500

@app.route(
    "/api/upload",
    methods=["POST"]
)
def upload_file():

    global DOCUMENTS

    try:

        if "file" not in request.files:

            return jsonify({
                "error":
                "No file uploaded"
            }), 400

        file = request.files["file"]

        if file.filename == "":

            return jsonify({
                "error":
                "No file selected"
            }), 400

        filename = secure_filename(
            file.filename
        )

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        file.save(filepath)

        notify(
            "VEERA Upload",
            filename
        )

        content = ""

        try:

            # TXT

            if filename.lower().endswith(
                ".txt"
            ):

                with open(
                    filepath,
                    "r",
                    encoding="utf-8"
                ) as f:

                    content = f.read()

            # PDF

            elif filename.lower().endswith(
                ".pdf"
            ):

                reader = PdfReader(
                    filepath
                )

                pages = []

                for page in reader.pages:

                    text = page.extract_text()

                    if text:

                        pages.append(text)

                content = "\n".join(
                    pages
                )

            # DOCX

            elif filename.lower().endswith(
                ".docx"
            ):

                doc = Document(
                    filepath
                )

                paragraphs = []

                for para in doc.paragraphs:

                    paragraphs.append(
                        para.text
                    )

                content = "\n".join(
                    paragraphs
                )

            else:

                content = (
                    "Unsupported file type."
                )

        except Exception as e:

            content = (
                f"Read Error: {str(e)}"
            )

        # Save document globally

        conversation_id = request.form.get(
            "conversationId",
            "default"
        )

        DOCUMENTS[conversation_id] = {
            "name": filename,
            "content": content
        }

        print("=" * 50)
        print("DOCUMENT STORED")
        print("Conversation:", conversation_id)
        print("File:", filename)
        print("Length:", len(content))
        print("=" * 50)

        return jsonify({

            "success": True,

            "filename": filename,

            "message": "Document uploaded successfully."

        })

    except Exception as e:

        return jsonify({

                "success": False,

                "error": str(e)

            }), 500
    
@app.route("/api/settings", methods=["POST"])
def save_settings():

    try:

        data = request.json

        with open(
            "settings.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )

        return jsonify(
            {
                "success": True
            }
        )

    except Exception as e:

        return jsonify(
            {
                "error": str(e)
            }
        ), 500
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
