# Next-Gen Speech & Interpreter — LT Executive Review

**December 25, 2025**

## **Executive Summary**

We are converging Teams speech experiences (Interpreter, Captions/Transcription) onto a unified, multilingual stack with stronger entity accuracy and reliability, while introducing Turn‑by‑Turn (TBT) Interpreter to solve accuracy and flow gaps in interactive meetings. Multilingual STT shipped to R0/R1; Transcript Enricher is correcting high‑value meetings at scale; Batch S2S display models have raised readability across Tier‑1 locales. Admin reporting and metering workstreams are underway to make usage and quality visible to customers and field.

## **Business Impact**

*   Interpreter adoption and engagement continue to trend up; usage depth (>5‑min sessions) increased and retention holds in the 11–13% range. Reliability consistently \~99%+.
*   Transcript quality gains reduce Copilot and Recap DSAT: Batch‑only traffic and display model upgrades improve readability and entity accuracy without increasing CoGS; Enricher corrects names and domain entities in the scenarios that matter most.
*   Multilingual STT eliminates setup friction (auto language detection + code‑switch tolerance), reducing gibberish and unlocking bilingual meetings for global customers.
*   Admin Center usage reporting (CFR) and metering integration lay the foundation for enterprise governance and value articulation (tenant adoption, meeting types, language pairs).


## **Top Customer Pain Points (Why this matters)**

*	Accuracy on technical terms, names, numbers/units; translations perceived as too literal in simultaneous mode
*	Latency and meeting flow in SIM, esp. alignment with shared content; first‑sentence delay sensitivity
*	Tone/naturalness in JP/KR; occasional gender/voice mismatches where voice simulation is off
*	Cross‑tenant/guest licensing clarity and interpreted audio not captured in recordings


## **Latest Progress (FY26 H1)**

### **Interpreter (SIM + TBT)**
*	SIM: Semantic mode enabled in lower rings; TTS acceleration (1.2×–1.35×) reduces accumulated translated audio latency; reliability ~99%+.
*	Calling & MTR: SIM enabled across rings; CSS meeting‑level license check live for first support group.
*	TBT: R0 available; early JP/KR customer/GBB feedback shows strong accuracy and clearer turn‑taking; known limits include 25 concurrent sessions and edge‑case behaviors under complex turns.

### **Multilingual STT**
* Unified multi‑recognizer endpoint with auto language detection; 9 languages enabled in preview; R0/R1 completed; ongoing adaptation, phrase‑hint and segmentation tuning.

### **Transcript Enricher**
*	R4 rollout at 50% for EN/JP and 10% for FR/DE/PT/ES; 1.8M+ meetings weekly enhanced; strong online reliability; scenario‑driven correction metrics (Project Sync, Enterprise Review, Stakeholder Forums).
*	In‑meeting enrichment architecture aligned; R0 target January 2026; multilingual support planned for CY2026 Q1.

### **Transcription++**:
*	Elevating transcription into an enterprise understanding layer: tiered model stack, stronger grounding/enrichment (global + custom dictionaries, dynamic vocabulary), governance‑by‑design, multilingual by default.

## **Improvements Plan (Next 1–2 Quarters)**

*	Expand TBT capacity, stabilize edge‑cases; UX cues for turn etiquette; evaluation pipeline for accuracy/tone/flow
*	GA multilingual STT (Tier‑1 focus) with improved code‑switching and segmentation; continue adaptation + biasing
*	Enricher GA completion for Tier‑1 + multilingual extension; integrate tenant auto‑dictionary (SLPv2) and dynamic vocabulary
*	Admin Center usage dashboard public preview (target Mar 31, 2026) and metering validation
*	Latency work: first‑sentence telemetry, segmentation improvements and end‑to‑end pipeline tuning


## **Vision & Strategy (6–12 months)**

*	Unify speech stack for Captions/Transcription/Interpreter; multilingual by default; simplify pipelines and schemas
*	Make entity accuracy the north star: global + custom dictionaries, dynamic vocabulary, and Enricher in/after meeting
*	Strengthen governance: metering, admin reporting, quality gates and ringed rollout discipline
*	Broaden language coverage (e.g., zh‑TW, NL, VI, TH) and market‑specific tone quality (JP/KR) to win competitive head‑to‑head
*	Explore offline/fast catch‑up transcription to reduce CoGS while preserving enterprise experience bars
*	Recording parity for interpreted audio (multi‑track options) to unlock multilingual recap and compliance scenarios


## **Risks & Asks to LT**

*	GPU capacity and substrate LLM onboarding timelines for real‑time models; maintain fallback paths with compliance controls
*	SPOF/error‑handling maturity and incident monitoring alignment across rings and environments
*	Admin reporting CFR data cooking ownership and data latency; align IDEAs + PM on contracts
*	Responsible AI: guardrails for harassment/misgendering risks; tone control improvements in JP/KR


## **KPI Snapshot (Latest Interpreter Signals)**

| Metric                | Value                  |
| --------------------- | ---------------------- |
| MAU                   | **136k (+1.9% MoM)**   |
| WAU                   | **38.3k (−2.5% WoW)**  |
| Monthly Meeting Count | **106k (+5.4% MoM)**   |
| >5‑min Meeting Rate   | **62.2% (+2.1% MoM)**  |
| E2E Reliability       | **99.38% (+0.2% MoM)** |
| CSAT                  | **71% (−2% MoM)**      |


# 🚀 **Next‑Gen Speech Intelligence in Teams (6–12 Month Vision & Strategy)**

*A unified vision for real‑time multilingual understanding across meetings, calls, and future AI agents.*

## **1. Where We Are Today — Latest Progress**

### **1.1 Simultaneous Interpreter (SIM) — Quality, Stability, User Experience**
Recent engineering syncs show major progress in model quality, latency, UX, and name/entity adaptation:

#### **Model Quality Improvements**

*	**Semantic Mode** advancing through controlled rollout (Ring 0). Enables better long‑segment coherence and semantic‑level translation.
*	**Phrase segmentation fix** to prevent splitting common phrases across segments, improving readability.
*	**Name adaptation and global dictionary** integration entering end‑to‑end testing, though recall still below expectation ( < 50% in JP‑EN), with plans to incorporate both source+target language signals.

#### **Phi‑4 Model & LLM‑based Improvements**

*	Teams and Speech are exploring **Phi‑4‑based streaming translation** for SIM; early results indicate better semantic preservation in some scenarios.
*	Internal discussions validate Phi‑4’s value especially in **long‑segment semantic reasoning**, complementing ST‑based streaming models.


#### **Latency & UX Enhancements**

*	**Speedup mode** now product‑enabled.
*	**Audio prefix (“audio introduction before first translation”)** added to mask first‑turn RTT and reduce user‑perceived latency.
*	**Auto‑update spoken language detection** shipped with the multilingual STT rollout, reducing mis‑detect and eliminating forced manual switching. (via multilingual STT rollout notes)


#### **Customer Pain Points (from recent meetings)**

*	**Slow first translation turn**, especially in bilingual meetings. Addressed by audio prefix.
*	**Improper segmentation** causing semantic breaks → being fixed through LM‑based segmentation scoring.
*	**Name mistranslation** still common (JP/EN especially). Global dictionary model under training; cluster issues being escalated.
*	**Harassment / tone issues** observed in extremely rare cases due to gender defaults in ST model → tracking under Responsible AI.


### **1.2 Turn‑by‑Turn Interpreter (TBT) — Major Accuracy & User Control Upgrade**
TBT is progressing quickly and now available in internal validation container form:

#### **TBT Improvements**

*	**Core client/backend integration nearly complete; internal validation ongoing.**
*	TBT fixes core SIM pain points:
  *	Reduces translation overlap
  *	Clarifies who is speaking
  *	Handles structured discussions better (e.g., board meetings, lectures)


#### **Model Stack for TBT**

* **GPT‑4o‑realtime** Uses + **Azure Voice Live API**, producing notably improved semantic and tone accuracy per vNext evaluation.

#### **Customer Relevance**

* TBT designed to support **formal customer meetings, public sector (Welsh gov), and high‑stakes enterprise conversations** needing turn precision. (Human‑interp fallback pressure from Welsh Gov noted).

## **2. Transcription Quality — Multilingual STT, Entity Enrichment, Live Captions**

### **2.1 Multilingual STT Model — Now Released to Ring 0 & Ring 1**

* **Full deployment completed** last week for Ring 0 and Ring 1.
* **Automatic language detection** reduces manual friction; major simplification for multilingual meetings.
* **Observed improvements**:
  * Phrase hint fix mitigates freeze >800ms.
  * Entity accuracy improved significantly in batch S2S:
    * Entity recall increased **65.42 → 74.76** (Type II) in PPE tests.


### **2.2 Transcription Enricher — Real‑time and Post‑Meeting**

* **Real-time enricher** now refining misrecognized **name entities** during meetings.
* Supports downstream AI features like:
  * Facilitator skills
  * Recap AI
  * Copilot grounding
* **Post-meeting enricher** launched earlier (R4), showing measurable benefit:
  * Overall transcription inaccuracy reduced **19.5% → 12.3%** (↓37%).
  * Domain entity errors ↓34%.
  * Accent/dialect issues ↓31%.
  * Corresponding **CSAT increased from 42.95% → 62.32%**.


### **2.3 Entity Correction (Global/Custom Dictionary)**

* Tier‑1 custom dictionary fully GA.
* Global dictionary under integration; dataset pending cluster issues.
* Early multilingual entity adaptation recalls still improving (current ~50% for JP/EN).


### **2.4 zh‑TW (Traditional Chinese) Transcription & Captioning**

* **ZHTW treated same as ZHCN**; STT updates completed, with internal testing planned.
* Issues in some locales still being debugged (e.g. Cantonese) — tracked as part of Tier‑2 language expansion.


## **3. Cross‑Cutting Approaches — Models, Evaluation, Infrastructure**

### **3.1 Unified Evaluation — LLM‑Based End‑to‑End Metrics**
You drove significant progress in evolving eval from model‑only to **end‑to‑end user‑perceived quality**:
* Now using **LLM-as-judge** metrics for transcription & interpreter.
* Produces consistent semantic, tone, latency, and entity scores across models.
* Enables apples‑to‑apples evaluation of:
  * ST
  * Semantic
  * Phi
  * GPT‑4o real-time
  * TBT pipeline
  * Multilingual STT

#### Business Value

* Accelerates iteration cycles
* Reduces human eval cost
* Improves decision accuracy for model rollouts
* Enables transparent tradeoff reporting to LT

### **3.2 GPU Infrastructure & Multi‑Recognizer**
To support next‑gen model families:
* Multi‑recognizer platform coming **January 2026** for Teams.
* Allows hot‑switch between STS and LRM/LLM‑based models.
* Foundational for **Phi‑4, LLM multimodal**, and **unified multilingual models**.
* Simplifies pipeline and unlocks faster experimentation.


## **4. North Star — 6–12 Month Vision**

### **1. Achieve >80% CSAT Interpreter Experience**
Anchored in vNext success criteria
* SIM for fluid conversations
* TBT for clarity in structured discussions
* Automatic mode switching based on meeting context (future vision)

### **2. Deploy Unified Multilingual Model (Transcription + Interpretation)**

* Speech team direction: unified multilingual model to simplify architecture and improve consistency.
* Explore **Phi‑4 multimodal** & GPT‑4o for high‑value scenarios.


### **3. Real‑Time Quality Enhancement Layer**

* Entity enrichment
* Latency mitigation (audio prefix, segmentation improvements)
* Biasing + adaptation framework (global/custom dictionary) that works across languages


### **4. End‑to‑End Reliability Across Global Meetings**

* Resource expansion (10→20 environments being evaluated).
* Robust error handling for Voice Life API, retry logic, and controller integration.

