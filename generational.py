"""
Ray Bradbury Generation Pass - 5-Model Multi-Volley Harness
Strictly aligned with Terry's actual local system inventory.
"""

import sqlite3
import requests
import json
import os

DB_PATH = r"D:\Projects\Ray\ray.db"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
STORY_PROMPT = (
    "Write the opening paragraph of a story about a boy who discovers an old "
    "carnival has returned to his town after twenty years. It is late August. "
    "The smell of cotton candy is in the air."
)

# Terry's actual top-tier local models from the screenshot
MODELS = [
    "gemma3:27b-it-qat"
]

def load_ray(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Eliminates array index bugs by enabling string lookups
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT name, cognitive_functions, core_drives, prose_rhythm, thematic_signature, 
               C_base, D_base, O_base, A_base, beta, kappa, chi, gamma, alpha 
        FROM Author_Profile WHERE id=1
    """)
    row = cursor.fetchone()
    
    cursor.execute("""
        SELECT theme, description, intensity, derived_weight 
        FROM Biographical_Traumas 
        ORDER BY derived_weight DESC LIMIT 4
    """)
    top_traumas = cursor.fetchall()
    conn.close()
    return row, top_traumas

def tensor_to_inference_params(row):
    # Safe lookups by column name string
    kappa = row["kappa"]  
    chi = row["chi"]      
    alpha = row["alpha"]  
    
    temperature = round(0.4 + (kappa * 0.6), 3)
    repeat_penalty = round(1.0 + (chi * 0.3), 3)
    top_p = round(1.0 - (alpha * 0.4), 3)
    
    return {
        "temperature": temperature,
        "repeat_penalty": repeat_penalty,
        "top_p": top_p
    }

def build_ray_substrate_prompt(row, top_traumas):
    trauma_context = ""
    for t in top_traumas:
        trauma_context += f"\n- {t['theme']} (weight={t['derived_weight']}): {t['description']}"
        
    dominant = max([("stress/dread", row["C_base"]), ("wonder/reward", row["D_base"]), 
                    ("nostalgia/connection", row["O_base"]), ("urgency/tension", row["A_base"])],
                   key=lambda x: x[1])

    decay_note = "Emotional states decay slowly. Let weights linger." if row["beta"] < 0.3 else ""

    return (
        f"You are writing from inside the psychological architecture of {row['name']}.\n\n"
        f"COGNITIVE PROCESSING MODE: {row['cognitive_functions']}\n"
        f"CORE DRIVES: {row['core_drives']}\n"
        f"PROSE RHYTHM: {row['prose_rhythm']}\n"
        f"THEMATIC SIGNATURE: {row['thematic_signature']}\n\n"
        f"CURRENT LIMBIC STATE:\n"
        f"  Dominant register: {dominant[0]} ({dominant[1]:.3f})\n"
        f"  Nostalgia baseline: {row['O_base']:.3f}\n"
        f"  Wonder baseline: {row['D_base']:.3f}\n"
        f"  Dread baseline: {row['C_base']:.3f}\n"
        f"  {decay_note}\n\n"
        f"FORMATIVE PSYCHOLOGICAL WEIGHTS:{trauma_context}\n\n"
        f"Do not describe these states or mention database fields. Write FROM them. No meta-commentary. Just the prose."
    )

def generate(system_prompt, user_prompt, params, model_name):
    payload = {
        "model": model_name,
        "system": system_prompt,
        "prompt": user_prompt,
        "stream": False,
        "options": {
            "temperature": params["temperature"],
            "repeat_penalty": params["repeat_penalty"],
            "top_p": params["top_p"],
            "num_predict": 350
        }
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        if response.status_code == 200:
            return response.json().get("response", "")
        return f"Error Code: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Connection timed out / failed to reach Ollama: {str(e)}"

def run_volley():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}. Set up your database layout first.")
        return
        
    row, top_traumas = load_ray(DB_PATH)
    tensor_params = tensor_to_inference_params(row)
    ray_system = build_ray_substrate_prompt(row, top_traumas)
    
    os.makedirs("./volley_results", exist_ok=True)
    
    print("="*60)
    print("FIRING BRADBURY SUBSTRATE VOLLEY (5 LOCAL HW MODELS)")
    print("="*60)
    print(f"Sampling Constraints -> Temp: {tensor_params['temperature']} | Top_P: {tensor_params['top_p']}\n")
    
    for idx, model in enumerate(MODELS, start=1):
        print(f"[{idx}/5] Processing model weights pool: '{model}'...")
        output = generate(ray_system, STORY_PROMPT, tensor_params, model)
        
        # Clean file strings
        safe_name = model.replace(":", "_").replace(".", "_")
        output_file = f"./volley_results/output_{safe_name}.txt"
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"MODEL: {model}\n")
            f.write(f"PARAMETERS: {json.dumps(tensor_params)}\n")
            f.write("-" * 40 + "\n\n")
            f.write(output)
            
    print("\nAll 5 evaluation text files generated in './volley_results/'")

if __name__ == "__main__":
    run_volley()