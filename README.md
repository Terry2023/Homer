# Ray Bradbury Psychological Engine

Local-first author substrate for preserving narrative voice beyond prompt engineering. Builds a limbic-state SQLite database from biographical trauma weights, then injects that psychological architecture into Ollama models at inference time.

Built for Terry's Sovereign Narrative Engine research — see Zenodo DOI 10.5281/zenodo.20316602

## What it does

Not RAG. Not fine-tuning. This is affective-state injection:

1. **ray.py** builds `ray.db` with Bradbury's cognitive profile (INFP, Fi-Ne-Si-Te), five formative traumas, and baseline neurotransmitter tensors
2. **generational.py** loads the top trauma weights, computes inference parameters from limbic state, and fires a volley through local models
3. Output preserves prose rhythm, thematic signature, and emotional register — without ever mentioning "write like Bradbury"

Current prime: **gemma3:27b-it-qat** (temperature 0.874, top_p 0.692, repeat_penalty 1.252)

## Quick Start

```bash
# 1. Clone and enter
git clone https://github.com/terry2023/ray-bradbury-engine
cd ray-bradbury-engine

# 2. Build the psychological database
python ray.py
# Creates ./ray.db with Author_Profile, Biographical_Traumas, Limbic_State

# 3. Ensure Ollama is running with Gemma 3
ollama pull gemma3:27b-it-qat
ollama serve

# 4. Fire the volley
python generational.py
# Outputs to ./volley_results/output_gemma3_27b-it-qat.txt
