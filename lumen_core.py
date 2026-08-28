import os
import json
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Configuración del Estado Cuántico / Simulación Real
STATE_FILE = "quantum_state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {
        "mass": 1.0,
        "energy_potential": "1e40 J",
        "quantum_state": "|Ψ⟩ = α|0⟩ + β|1⟩",
        "scaling_factor": 1.0,
        "modules": ["Server", "PhysicsEngine", "AutoProgrammer"]
    }

def save_state(data):
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=4)

HTML_INTERFACE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ecosistema Lumen - Núcleo Escalar</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        body { margin: 0; overflow: hidden; background: #020208; font-family: monospace; color: #00ffcc; }
        #overlay { position: absolute; top: 10px; left: 10px; z-index: 100; background: rgba(0,0,0,0.8); padding: 15px; border: 1px solid #00ffcc; border-radius: 5px; }
        button { background: #00ffcc; color: #000; border: none; padding: 8px 12px; cursor: pointer; font-weight: bold; margin-top: 10px; }
    </style>
</head>
<body>
    <div id="overlay">
        <h2>PROYECTO LUMEN: NÚCLEO NANO-ESCALAR</h2>
        <div id="status">Estado: Inicializando matriz física...</div>
        <button onclick="triggerAutoProg()">Autoprogramar / Escalar</button>
    </div>

    <script>
        // Configuración de escena 3D (Three.js)
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // Representación tridimensional del Núcleo ("Grano de Mostaza")
        const geometry = new THREE.IcosahedronGeometry(1, 4);
        const material = new THREE.MeshBasicMaterial({ color: 0x00ffcc, wireframe: true });
        const coreNode = new THREE.Mesh(geometry, material);
        scene.add(coreNode);

        // Campo cuántico periférico
        const particlesGeo = new THREE.BufferGeometry();
        const count = 500;
        const positions = new Float32Array(count * 3);
        for(let i=0; i<count*3; i++) {
            positions[i] = (Math.random() - 0.5) * 8;
        }
        particlesGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        const particlesMat = new THREE.PointsMaterial({ size: 0.03, color: 0xff0077 });
        const particleSystem = new THREE.Points(particlesGeo, particlesMat);
        scene.add(particleSystem);

        camera.position.z = 4;

        function animate() {
            requestAnimationFrame(animate);
            coreNode.rotation.x += 0.005;
            coreNode.rotation.y += 0.01;
            particleSystem.rotation.y -= 0.002;
            renderer.render(scene, camera);
        }
        animate();

        function triggerAutoProg() {
            fetch('/api/autoprogram', { method: 'POST' })
                .then(res => res.json())
                .then(data => {
                    document.getElementById('status').innerText = "Factor de escala: " + data.state.scaling_factor.toFixed(2);
                    coreNode.scale.setScalar(data.state.scaling_factor);
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_INTERFACE)

@app.route('/api/state', methods=['GET'])
def get_state():
    return jsonify(load_state())

@app.route('/api/autoprogram', methods=['POST'])
def autoprogram():
    state = load_state()
    # Modificación dinámica de parámetros y crecimiento escalar
    state["scaling_factor"] = round(state["scaling_factor"] * 1.15, 2)
    state["modules"].append(f"DynamicModule_{len(state['modules']) + 1}")
    save_state(state)
    return jsonify({"status": "Autoprogramación ejecutada", "state": state})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
