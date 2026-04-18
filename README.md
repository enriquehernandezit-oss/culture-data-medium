# CultureDelta

**🔗 Live app → [culture-delta.streamlit.app](https://culture-delta.streamlit.app)**

## Demo

https://github.com/user-attachments/assets/877f2a26-6a6a-42b8-b204-2c73e185bc60

> Map how markets and culture shift over time.

CultureDelta is a multi-agent AI system that maps exactly how a market, behavior, or cultural space changed between two points in time — the language people used, the values they held, and the behaviors that emerged or faded. It tells you not just where a market is today, but the direction and velocity of its drift — and where it is heading next.

---

## What is a Cultural Delta?

Delta (Δ) = the measurable difference between two states over time.

Most market research gives you a snapshot of today. CultureDelta gives you the **delta** — the trajectory, the drift, and the forward signal. The difference between knowing where a market is and knowing where it's going.

---

## What It Produces

For any topic and two time periods, CultureDelta outputs:

- **Language Shifts** — how the vocabulary around the topic changed and what that reveals
- **Value & Attitude Shifts** — what people cared about, feared, or valued and how that evolved
- **Emerged Behaviors** — new patterns that appeared in the later period
- **Faded Behaviors** — what was common before but has since declined
- **Forward Signal** — where this market is heading in the next 2 years
- **The Opportunity** — the specific business or positioning opportunity the delta reveals

---

## How It Works

Three Claude agents work in sequence — two in parallel:

### Agent breakdown

| Agent | Job | Tools |
|---|---|---|
| Agent 1 — Then researcher | Searches web + Reddit for the earlier period | Tavily API, Reddit API |
| Agent 2 — Now researcher | Searches web + Reddit for the later period | Tavily API, Reddit API |
| Agent 3 — Synthesizer | Compares both summaries, maps shifts, extracts forward signal | Claude API only — pure reasoning |

**Key engineering detail:** Agents 1 and 2 run simultaneously using Python's `ThreadPoolExecutor` — cutting total research time roughly in half compared to sequential execution.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Web app + deployment |
| Claude API (Haiku 4.5) | Multi-agent tool use + synthesis |
| Tavily API | Real-time web search |
| Reddit API | Community signal scanning |
| ThreadPoolExecutor | Parallel agent execution |

---

## Run Locally

```bash
git clone https://github.com/enriquehernandezit-oss/culture-delta-medium.git
cd culture-delta-medium
conda activate earlysignal
pip install -r requirements.txt
```

Create a `.env` file:

```bash
streamlit run app.py
```

---

## Example Analyses

- `athletic wear 2019 → 2025`
- `remote work 2019 → 2024`
- `crypto 2017 → 2023`
- `fast food 2015 → 2025`
- `luxury fashion 2010 → 2024`
- `social media 2015 → 2025`

---

Built by **Enrique C. Hernandez** — [LinkedIn](https://linkedin.com/in/enriquechernandez)

*Part of a 5-project AI portfolio. Each project is progressively more complex.*
