# 🎬 IMDb Graph Analysis

This project explores relationships within IMDb data by modeling actors, titles, and roles as a graph. It implements pathfinding and search algorithms to answer questions like:

- How many connections away are two actors?
- What's the shortest path between them?
- What genres connect them the most?

The project uses custom graph structures, a heap-based priority queue, and TSV processing logic.

---

## 🧠 Features

- 📈 Custom graph implementation (`graph.py`, `heapdict.py`)
- 🔍 BFS, Dijkstra, and genre-aware search algorithms
- 🎭 IMDb dataset parsing (`name-basics-f.tsv`, `title-basics-f.tsv`, `title-principals-f.tsv`)
- 🧩 Utility functions in `functions.py` and `sudoku.py` (for testing structure or extended search logic)
- 🔧 Two modes of traversal:
  - `grafo_a.py`: Standard graph traversal
  - `grafo_b.py`: Enhanced genre-weighted traversal

---

## 🖼️ Preview

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/IMDB_Logo_2016.svg/512px-IMDB_Logo_2016.svg.png" width="150" alt="IMDb logo" />

_(Optional: You can replace this logo with a real image of your graph output or notebook visualization later)_

---

## 🗃️ Dataset

IMDb filtered data:
- `name-basics-f.tsv`: Actors/actresses
- `title-basics-f.tsv`: Titles and genres
- `title-principals-f.tsv`: Cast per title

---

## 🚀 Getting Started

1. Clone the repo  
```bash
git clone https://github.com/your-username/imdb-graph-analysis.git
cd imdb-graph-analysis
```
2. Install dependencies (if needed)

3. Run any of the traversal modes:
```bash
python grafo_a.py
python grafo_b.py
```
---

## 🛠️ Technologies

This project was developed using:

- **Python 3.11**
- **Graph theory algorithms** (BFS, Dijkstra, etc.)
- **Custom data structures** (`Graph`, `HeapDict`)
- **IMDb TSV data processing**
- **Modular architecture** for search logic, file parsing, and actor-title relations

---

## 👩‍💻 Author

**Serena Feldberg**  
🎓 AI Engineering student at **Universidad de San Andrés**  
📧 [serenafeldberg@gmail.com](mailto:serenafeldberg@gmail.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/serenafeldberg/)

---

> “The shortest path between two actors might just be one movie away.” 🎥
