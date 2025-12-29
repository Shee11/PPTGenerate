# **Next‑Gen Speech & Interpreter — LT Executive Review**

**December 25, 2025**

## **Executive Summary**

We are converging Teams speech experiences (Interpreter, Captions/Transcription) onto a unified, multilingual stack with stronger entity accuracy and reliability, while introducing Turn‑by‑Turn (TBT) Interpreter to solve accuracy and flow gaps in interactive meetings. Multilingual STT shipped to R0/R1; Transcript Enricher is correcting high‑value meetings at scale; Batch S2S display models have raised readability across Tier‑1 locales. Admin reporting and metering workstreams are underway to make usage and quality visible to customers and field.

## **Business Impact**

*   Interpreter adoption and engagement continue to trend up; usage depth (>5‑min sessions) increased and retention holds in the 11–13% range. Reliability consistently \~99%+.
*   Transcript quality gains reduce Copilot and Recap DSAT: Batch‑only traffic and display model upgrades improve readability and entity accuracy without increasing CoGS; Enricher corrects names and domain entities in the scenarios that matter most.
*   Multilingual STT eliminates setup friction (auto language detection + code‑switch tolerance), reducing gibberish and unlocking bilingual meetings for global customers.
*   Admin Center usage reporting (CFR) and metering integration lay the foundation for enterprise governance and value articulation (tenant adoption, meeting types, language pairs).

## **Top Customer Pain Points (Why this matters)**

*   Accuracy on technical terms, names, numbers/units; translations perceived as too literal in simultaneous mode
*   Latency and meeting flow in SIM, especially alignment with shared content; first‑sentence delay sensitivity
*   Tone/naturalness in JP/KR; occasional gender/voice mismatches where voice simulation is off
*   Cross‑tenant/guest licensing clarity and interpreted audio not captured in recordings

## **Latest Progress (FY26 H1)**

### **Interpreter (SIM + TBT)**

*   **SIM**
    *   Semantic mode enabled in lower rings
    *   TTS acceleration (1.2×–1.35×) reduces accumulated translated audio latency
    *   Reliability \~99%+
    *   Calling & MTR: SIM enabled across rings; CSS meeting‑level license check live
*   **TBT**
    *   R0 available
    *   Early JP/KR customer/GBB feedback shows strong accuracy and clearer turn‑taking
    *   Known limits: 25 concurrent sessions and some edge‑case behaviors

### **Multilingual STT**

*   Unified multi‑recognizer endpoint with auto language detection
*   9 languages enabled in preview
*   R0/R1 completed; ongoing adaptation, phrase‑hint, segmentation tuning

### **Transcript Enricher**

*   R4 rollout at 50% for EN/JP; 10% for FR/DE/PT/ES
*   1.8M+ meetings weekly enhanced
*   Strong online reliability
*   Alignment with in‑meeting enrichment architecture
*   Multilingual support planned CY2026 Q1

### **Transcription++**

*   Enterprise understanding layer
*   Tiered model stack + grounding/enrichment
*   Global/custom dictionaries + dynamic vocabulary
*   Governance‑by‑design, multilingual by default

## **Improvements Plan (Next 1–2 Quarters)**

*   Expand TBT capacity, stabilize edge cases
*   UX cues for turn etiquette
*   Evaluation pipeline for accuracy/tone/flow
*   GA multilingual STT (Tier‑1 focus); improved code‑switching
*   Enricher GA for Tier‑1 + multilingual extension; tenant auto‑dictionary
*   Admin Center usage dashboard preview (target Mar 31, 2026)
*   First‑sentence telemetry, segmentation improvements, pipeline tuning

## **Vision & Strategy (6–12 months)**

*   Unified speech stack for Captions/Transcription/Interpreter
*   Entity accuracy as north star (global + custom dictionaries, dynamic vocabulary, Enricher)
*   Strengthened governance, quality gates, ringed rollout
*   Broaden language coverage (zh‑TW, NL, VI, TH) + market‑specific tone tuning for JP/KR
*   Offline/fast catch‑up transcription exploration
*   Recording parity for interpreted audio (multi‑track options)

## **Risks & Asks to LT**

*   GPU capacity and substrate LLM onboarding timelines for real‑time models
*   SPOF/error‑handling maturity and incident monitoring
*   CFR data cooking ownership and latency
*   Responsible AI guardrails for harassment/misgendering; tone control improvements in JP/KR

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

#### **Model Quality Improvements**

*   Semantic Mode rollout (Ring 0) → better long‑segment coherence
*   Phrase segmentation fix for readability
*   Name adaptation + global dictionary integration under testing (JP‑EN recall <50%, improving)

#### **Phi‑4 Model & LLM‑based Improvements**

*   Phi‑4‑based streaming translation exploration
*   Early results show improved semantic preservation
*   Stronger long‑segment reasoning complementing ST streaming

#### **Latency & UX Enhancements**

*   Speedup mode product‑enabled
*   Audio prefix to mask first‑turn RTT
*   Auto‑update spoken language detection shipped with multilingual STT

#### **Customer Pain Points**

*   Slow first translation → addressed by audio prefix
*   Improper segmentation → LM‑based segmentation scoring
*   Name mistranslation → global dictionary training
*   Rare harassment/tone issues (gender defaults) → Responsible AI tracking

### **1.2 Turn‑by‑Turn Interpreter (TBT)**

#### **TBT Improvements**

*   Core client/backend integration nearly complete
*   Reduces translation overlap
*   Clarifies speaker identity
*   Better for structured discussions (board meetings, lectures)

#### **Model Stack**

*   GPT‑4o‑realtime + Azure Voice Live API
*   Improved semantic and tone accuracy

#### **Customer Relevance**

*   Designed for formal meetings, public sector (e.g., Welsh Gov), enterprise high‑stakes conversations

## **2. Transcription Quality — Multilingual STT, Entity Enrichment, Live Captions**

### **2.1 Multilingual STT Model**

*   Deployment completed for R0/R1
*   Auto language detection simplifies setup
*   Phrase hint fix for >800ms freeze
*   Entity recall improvements (65.42 → 74.76 Type II)

### **2.2 Transcript Enricher**

**Real‑time Enricher**

*   Fixes name entity errors in‑meeting
*   Supports Recap AI, Copilot grounding, Facilitator skills

**Post‑meeting Enricher**

*   Inaccuracy reduced 19.5% → 12.3% (↓37%)
*   Entity errors ↓34%
*   Accent/dialect issues ↓31%
*   CSAT improved 42.95% → 62.32%

### **2.3 Entity Correction (Global/Custom Dictionary)**

*   Tier‑1 custom dictionary GA
*   Global dictionary integration pending cluster fix
*   Multilingual entity recall improving (\~50% JP/EN)

### **2.4 zh‑TW Transcription & Captioning**

*   Treated same as zh‑CN; STT updates completed
*   Internal testing planned
*   Cantonese issues tracked under Tier‑2 language expansion

## **3. Cross‑Cutting Approaches — Models, Evaluation, Infrastructure**

### **3.1 Unified Evaluation — LLM‑Based End‑to‑End Metrics**

*   LLM‑as‑judge for transcription & interpreter
*   Produces semantic, tone, latency, entity scores
*   Enables consistent evaluation across: ST, Semantic, Phi, GPT‑4o realtime, TBT, Multilingual STT
*   Accelerates iteration, reduces human cost, improves rollout decisions

### **3.2 GPU Infrastructure & Multi‑Recognizer**

*   Multi‑recognizer platform coming Jan 2026
*   Hot‑switch between STS and LRM/LLM models
*   Foundational for Phi‑4, LLM multimodal, unified multilingual models
*   Simplifies pipeline and boosts experimentation

## **4. North Star — 6–12 Month Vision**

### **1. Achieve >80% CSAT Interpreter Experience**

*   SIM for fluid conversations
*   TBT for structured clarity
*   Future: automatic mode switching

### **2. Unified Multilingual Model**

*   Speech team direction: unified transcription + interpretation
*   Explore Phi‑4 multimodal & GPT‑4o

### **3. Real‑Time Quality Enhancement Layer**

*   Entity enrichment
*   Latency mitigation
*   Biasing + adaptation across languages

### **4. End‑to‑End Reliability Across Global Meetings**

*   Resource expansion (10→20 environments)
*   Robust error handling + retry logic
