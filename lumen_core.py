import os
import json
import urllib.request
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)
STATE_FILE = "quantum_state.json"
OLLAMA_URL = "http://localhost:11434/api/generate"

def get_default_state():
    return {
        "device": "Xiaomi Redmi 8 / Note 8",
        "mass": 1.0,
        "energy_potential": "1e40 J",
        "quantum_state": "|Ψ⟩ = α|0⟩ + β|1⟩",
        "scaling_factor": 1.0,
        "llm_engine": "Ollama (DeepSeek-R1 / Qwen2.5)",
        "sensory_nodes": {
            "vision": "Active (WebGL 3D Core)",
            "hearing": "Active (WebAudio Synth 432Hz)",
            "touch": "Active (MultiTouch & Gyro/Accel)",
            "smell_taste": "Active (Battery Telemetry)",
            "environment": "Active (Ambient Light Sensor)"
        },
        "modules": ["Server", "PhysicsEngine", "AutoProgrammer", "SensoryMatrix_Xiaomi", "Ollama_CognitiveCore"]
    }

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                data = json.load(f)
                if "sensory_nodes" not in data:
                    data["sensory_nodes"] = get_default_state()["sensory_nodes"]
                return data
        except Exception:
            pass
    state = get_default_state()
    save_state(state)
    return state

def save_state(data):
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def query_ollama(prompt):
    payload = json.dumps({
        "model": "deepseek-r1:1.5b",
        "prompt": prompt,
        "stream": False
    }).encode("utf-8")
    
    req = urllib.request.Request(OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            res = json.loads(response.read().decode("utf-8"))
            return res.get("response", "Cognitive node generated.")
    except Exception as e:
        return f"Offline local fallback: {str(e)}"

HTML_INTERFACE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lumen Core + Ollama AI Matrix</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        body { margin: 0; overflow: hidden; background: #000; font-family: monospace; color: #00ffaa; }
        #hud { position: absolute; top: 10px; left: 10px; z-index: 100; background: rgba(5,10,20,0.9); padding: 15px; border: 1px solid #00ffaa; border-radius: 8px; max-width: 320px; }
        .sense { margin-bottom: 6px; font-size: 11px; }
        #log { font-size: 10px; color: #00ccff; height: 50px; overflow-y: auto; border-top: 1px dashed #00ffaa; margin-top: 8px; padding-top: 5px; }
        button { background: #00ffaa; color: #000; border: none; padding: 8px 12px; cursor: pointer; font-weight: bold; margin-top: 8px; border-radius: 4px; width: 100%; }
    </style>
</head>
<body>
    <div id="hud">
        <h3 style="margin:0 0 10px 0; color:#fff;">LUMEN + OLLAMA CORE</h3>
        <div class="sense" id="sense-v">👁️ Vista: WebGL 3D Activo</div>
        <div class="sense" id="sense-a">👂 Oído: Sintetizador Inactivo</div>
        <div class="sense" id="sense-t">✋ Tacto: Esperando eventos...</div>
        <div class="sense" id="sense-s">🧪 Hardware: Leyendo...</div>
        <div class="sense" id="sense-llm">🧠 IA: Ollama Integrado</div>
        <div id="log">Esperando pulso cognitivo...</div>
        <button onclick="enableAudio()">Activar Oído (432 Hz)</button>
        <button onclick="triggerAutoProg()">Generar Módulo con Ollama</button>
    </div>

    <script>
        let audioCtx, osc, gain;

        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        document.body.appendChild(renderer.domElement);

        const geometry = new THREE.IcosahedronGeometry(1.2, 3);
        const material = new THREE.MeshBasicMaterial({ color: 0x00ffaa, wireframe: true });
        const coreNode = new THREE.Mesh(geometry, material);
        scene.add(coreNode);

        camera.position.z = 4;

        window.addEventListener("deviceorientation", (e) => {
            if(e.beta || e.gamma) {
                coreNode.rotation.x = (e.beta || 0) * 0.02;
                coreNode.rotation.y = (e.gamma || 0) * 0.02;
                document.getElementById("sense-t").innerText = "✋ Tacto (Gyro): X=" + Math.round(e.beta || 0) + "° Y=" + Math.round(e.gamma || 0) + "°";
            }
        });

        function enableAudio() {
            if(!audioCtx) {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                osc = audioCtx.createOscillator();
                gain = audioCtx.createGain();
                osc.type = "sine";
                osc.frequency.setValueAtTime(432, audioCtx.currentTime);
                gain.gain.setValueAtTime(0.04, audioCtx.currentTime);
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start();
                document.getElementById("sense-a").innerText = "👂 Oído: Frecuencia 432Hz Generada";
            }
        }

        if ('getBattery' in navigator) {
            navigator.getBattery().then(b => {
                const updateBat = () => {
                    document.getElementById("sense-s").innerText = "🧪 Batería: " + Math.round(b.level * 100) + "% (" + (b.charging ? "Cargando" : "Descargando") + ")";
                };
                updateBat();
            });
        }

        function animate() {
            requestAnimationFrame(animate);
            coreNode.rotation.z += 0.003;
            renderer.render(scene, camera);
        }
        animate();

        function triggerAutoProg() {
            document.getElementById("log").innerText = "Procesando con Ollama IA...";
            fetch("/api/autoprogram", { method: "POST" })
                .then(res => res.json())
                .then(data => {
                    coreNode.scale.setScalar(1 + (data.state.modules.length * 0.005));
                    document.getElementById("log").innerText = "Respuesta IA: " + (data.ai_reasoning || "Módulo expandido.");
                });
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_INTERFACE)

@app.route("/api/state", methods=["GET"])
def get_state():
    return jsonify(load_state())

@app.route("/api/autoprogram", methods=["POST"])
def autoprogram():
    state = load_state()
    state["scaling_factor"] = round(state["scaling_factor"] * 1.15, 2)
    
    prompt = f"Genera un nombre corto y descriptivo para un módulo del sistema autoprogramable Lumen. Responde ÚNICAMENTE con el nombre del módulo en 2 palabras."
    ai_thought = query_ollama(prompt).strip()
    
    new_module_name = f"Module_{len(state["modules"]) + 1}_{ai_thought[:20]}"
    state["modules"].append(new_module_name)
    save_state(state)
    return jsonify({"status": "Módulo Cognitivo Integrado con Ollama", "ai_reasoning": ai_thought, "state": state})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
