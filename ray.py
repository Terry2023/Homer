"""
Ray Bradbury Psychological Engine - MVD (Zen-Tuned)
Builds/Overwrites the SQLite database from biographical knowledge.
"""

import sqlite3
import os

DB_PATH = r"D:\Projects\Ray\ray.db"

AUTHOR_PROFILE = {
    "name": "Ray Bradbury",
    "birth_year": 1920,
    "death_year": 2012,
    "origin": "Waukegan, Illinois",
    "cognitive_archetype": "INFP",
    "cognitive_functions": "Fi-Ne-Si-Te",
    "core_drives": "zest, gusto, wonder, nostalgia, preservation of human soul against mechanization, Muse-feeding through sensory memory",
    "prose_rhythm": "lyrical, sensory-dense, run fast then stand still, short declarative punches under flowing poetic rhythm",
    "thematic_signature": "childhood wonder vs industrial death, memory as sanctuary, zest battling entropy"
}

BIOGRAPHICAL_TRAUMAS = [
    {
        "theme": "Carnival_Shadow",
        "description": "Dark carnival imagery. Something Wicked This Way Comes. The carnival as beautiful evil - wonder weaponized. Duality of enchantment and corruption. Zest and dread intertwined.",
        "intensity": 0.92, "frequency": 0.85, "chapter_count": 12, "mentions_normalized": 45,
        "tensor_target": "cortisol_sensitivity", "cognitive_switch": "Fi_dread_Ne_beauty"
    },
    {
        "theme": "Nostalgia_Sanctuary",
        "description": "Waukegan childhood as psychological Eden. Late August light, smell of cut grass, cotton candy ghosts. Memory as the only safe place. Zen Muse feeding through personal nouns and sensory lists.",
        "intensity": 0.95, "frequency": 0.91, "chapter_count": 18, "mentions_normalized": 67,
        "tensor_target": "oxytocin_base", "cognitive_switch": "Si_sanctuary_Ne_expansion"
    },
    {
        "theme": "Wonder_Imperative",
        "description": "Buck Rogers and pulp magazines as survival mechanism. Zest and gusto as daily creative fuel. 'Stay drunk on writing.'",
        "intensity": 0.88, "frequency": 0.82, "chapter_count": 14, "mentions_normalized": 52,
        "tensor_target": "dopamine_sensitivity", "cognitive_switch": "Ne_explosion_Fi_joy"
    },
    {
        "theme": "Run_Fast_Stand_Still",
        "description": "First draft explosion vs cold critical revision. Write hot, edit cold. Noun list technique to dredge memory.",
        "intensity": 0.87, "frequency": 0.78, "chapter_count": 9, "mentions_normalized": 33,
        "tensor_target": "kinetic_amplitude", "cognitive_switch": "Ne_velocity_Fi_trust"
    },
    {
        "theme": "Muse_Feeding",
        "description": "Feed the Muse with poetry, sensory life, childhood ghosts. Ignore her and she flees. 'You must stay drunk on writing so reality cannot destroy you.'",
        "intensity": 0.90, "frequency": 0.84, "chapter_count": 11, "mentions_normalized": 41,
        "tensor_target": "oxytocin_dopamine_balance", "cognitive_switch": "Fi_heat_Ne_inspiration"
    }
]

def compute_tensor_values(traumas):
    return {
        "C_base": 0.85, "D_base": 0.92, "O_base": 0.88, "A_base": 0.75,
        "beta": 0.81,  # slow trauma decay rate
        "kappa": 0.79, # kinetic velocity
        "chi": 0.84,   # identity persistence 
        "gamma": 0.91, # thematic drive
        "alpha": 0.77  # semantic focus
    }

def build_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE Author_Profile (
            id INTEGER PRIMARY KEY, name TEXT, birth_year INTEGER, death_year INTEGER, origin TEXT,
            cognitive_archetype TEXT, cognitive_functions TEXT, core_drives TEXT, prose_rhythm TEXT, thematic_signature TEXT,
            C_base REAL, D_base REAL, O_base REAL, A_base REAL, beta REAL, kappa REAL, chi REAL, gamma REAL, alpha REAL
        );
    """)
    
    cursor.execute("""
        CREATE TABLE Biographical_Traumas (
            id INTEGER PRIMARY KEY AUTOINCREMENT, theme TEXT UNIQUE, description TEXT, intensity REAL, frequency REAL,
            chapter_count INTEGER, mentions_normalized INTEGER, tensor_target TEXT, cognitive_switch TEXT, derived_weight REAL
        );
    """)
    
    cursor.execute("""
        CREATE TABLE Limbic_State (
            id INTEGER PRIMARY KEY, timestamp INTEGER, narrative_t REAL, cortisol REAL, dopamine REAL, oxytocin REAL, adrenaline REAL,
            alpha REAL, gamma REAL, kappa REAL, chi REAL, active_theme TEXT, gap_derivative REAL, circuit_breaker INTEGER
        );
    """)
    
    tensors = compute_tensor_values(BIOGRAPHICAL_TRAUMAS)
    
    cursor.execute("""
        INSERT INTO Author_Profile VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        AUTHOR_PROFILE["name"], AUTHOR_PROFILE["birth_year"], AUTHOR_PROFILE["death_year"], AUTHOR_PROFILE["origin"],
        AUTHOR_PROFILE["cognitive_archetype"], AUTHOR_PROFILE["cognitive_functions"], AUTHOR_PROFILE["core_drives"],
        AUTHOR_PROFILE["prose_rhythm"], AUTHOR_PROFILE["thematic_signature"],
        tensors["C_base"], tensors["D_base"], tensors["O_base"], tensors["A_base"],
        tensors["beta"], tensors["kappa"], tensors["chi"], tensors["gamma"], tensors["alpha"]
    ))
    
    for t in BIOGRAPHICAL_TRAUMAS:
        derived_weight = round((t["intensity"] * 0.6) + (t["frequency"] * 0.4), 4)
        cursor.execute("""
            INSERT INTO Biographical_Traumas (theme, description, intensity, frequency, chapter_count, mentions_normalized, tensor_target, cognitive_switch, derived_weight)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (t["theme"], t["description"], t["intensity"], t["frequency"], t["chapter_count"], t["mentions_normalized"], t["tensor_target"], t["cognitive_switch"], derived_weight))
    
    cursor.execute("""
        INSERT INTO Limbic_State VALUES (1, strftime('%s','now'), 0.0, ?, ?, ?, ?, ?, ?, ?, ?, 'Late_August_Nostalgia', 0.12, 0);
    """, (tensors["C_base"], tensors["D_base"], tensors["O_base"], tensors["A_base"], tensors["alpha"], tensors["gamma"], tensors["kappa"], tensors["chi"]))
    
    conn.commit()
    conn.close()
    print(f"Clean database initialized at: {DB_PATH}")

if __name__ == "__main__":
    build_database()