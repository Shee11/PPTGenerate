## RULES
- ≥4 different layouts per deck
- Never same layout twice in a row
- Numbers → BigNum/MetricGroup (not in text)
- ≥3 slides with data components
- Lists max 4 items, body max 25 words
- Split layouts: BOTH sides need visual blocks, not just text
- **NO GAPS**: content should fill the page, not leave holes
- **NO REDUNDANCY**: Never show same data twice (e.g., MetricGroup + BigNum with same numbers)

# User
# DRAFT SLIDES (use these IDs, ranks, stories, atoms)
```json
[
  {
    "id": "slide_1",
    "rank": 1,
    "story": {
      "headline": "Teams AI is already a top Copilot growth engine\u2014now we must lead the AI-first way of building",
      "narrative": "Blend brings together leaders who are redefining how products are built in the AI era. Inside Teams, Recap and Copilot are already proving that AI can drive real business impact, but the rest of the company is still figuring out how to get there. This talk is about how we turn our early success into a repeatable, AI-first product practice.",
      "evidence": [
        "fact_001",
        "fact_002",
        "quote_001"
      ],
      "takeaway": "We\u2019re not just shipping AI features\u2014we have the opportunity and responsibility to define how AI-first product management is done across Microsoft."
    },
    "atoms": [
      "fact_001",
      "fact_002",
      "quote_001"
    ],
    "density": "sparse",
    "visual_design": "LayoutCover: background=abstract-AI-waves, foreground=bold-title+subtitle, accent=quote"
  },
  {
    "id": "slide_2",
    "rank": 2,
    "story": {
      "headline": "Our AI products are winning\u2014but our PM practice is at risk of falling behind",
      "narrative": "Inside Teams, Recap is a huge success story. Yet conversations at Blend made it clear that while we feel like AI pioneers, many peers have already retooled their PM discipline around evals, data, and customer-led AI design. Our risk is complacency: great AI features built with yesterday\u2019s methods.",
      "evidence": [
        "fact_002",
        "tension_006",
        "tension_001"
      ],
      "takeaway": "We must evolve from \u2018AI features inside old PM practices\u2019 to \u2018AI-first PM practices that scale our wins across Teams and beyond.\u2019"
    },
    "atoms": [
      "fact_002",
      "tension_006",
      "tension_001",
      "quote_001"
    ],
    "density": "moderate",
    "visual_design": "LayoutSplit5050: left=narrative+SmartList, right=contrast-panel(success vs risk)"
  },
  {
    "id": "slide_3",
    "rank": 3,
    "story": {
      "headline": "Model-first, eval-first: the new center of gravity for PMs",
      "narrative": "In AI products, the model\u2019s reasoning is the experience. Specs and UI still matter, but they\u2019re no longer where the magic\u2014or the failures\u2014happen. That means PMs must move from writing PRDs and mocks to designing model behavior, evals, and golden datasets as their primary craft.",
      "evidence": [
        "concept_001",
        "concept_005",
        "tension_002"
      ],
      "takeaway": "Within six months, a great Teams PM will be defined by how well they shape model behavior, not by how well they write specs."
    },
    "atoms": [
      "concept_001",
      "concept_005",
      "tension_002",
      "visual_001"
    ],
    "density": "moderate",
    "visual_design": "LayoutSplit5050: left=metaphor-visual, right=explanation+SmartList"
  },
  {
    "id": "slide_4",
    "rank": 4,
    "story": {
      "headline": "Lon\u2019s \u201cMaking Honey\u201d: our golden example of AI-era product storytelling",
      "narrative": "We don\u2019t have to imagine what great AI product thinking looks like\u2014it\u2019s already in-house. Lon\u2019s \u201cMaking Honey\u201d talk is treated as a golden dataset: a concrete example of how to frame AI value, metrics, and product craft in the new era.",
      "evidence": [
        "fact_003",
        "concept_004"
      ],
      "takeaway": "Use \u201cMaking Honey\u201d as a benchmark: if your AI narrative, evals, and rubrics can\u2019t be judged as A5 quality against it, keep iterating."
    },
    "atoms": [
      "fact_003",
      "concept_004"
    ],
    "density": "sparse",
    "visual_design": "LayoutStacked: top=hero-quote, bottom=SmartList"
  },
  {
    "id": "slide_5",
    "rank": 5,
    "story": {
      "headline": "Build for value, not vanity: measure what truly matters for Copilot",
      "narrative": "In an AI gold rush, it\u2019s easy to celebrate big numbers that don\u2019t actually mean anything: button clicks, trial usage, or one-off wow moments. For Teams AI, our bar is higher. We must anchor on metrics that reflect durable value and contribution to the Copilot business.",
      "evidence": [
        "concept_002",
        "fact_002",
        "fact_005"
      ],
      "takeaway": "Design your AI features and evals backwards from retention, attach, and Copilot contribution\u2014not from vanity metrics or one-off demos."
    },
    "atoms": [
      "concept_002",
      "fact_002",
      "fact_005"
    ],
    "density": "moderate",
    "visual_design": "LayoutSplit5050: left=SmartList(bad vs good metrics), right=callout+context"
  },
  {
    "id": "slide_6",
    "rank": 6,
    "story": {
      "headline": "Evals are the new design tool: from QA gate to steering wheel",
      "narrative": "For AI, evaluation can\u2019t be the last checkbox before launch. It has to be the steering wheel we use from day one. That means PMs define eval categories, golden datasets, and LLM judges upfront\u2014and use them to drive every iteration.",
      "evidence": [
        "concept_008",
        "concept_004",
        "fact_011"
      ],
      "takeaway": "If your AI feature doesn\u2019t have clear evals, golden datasets, and judges defined early enough to pass AIRR, you don\u2019t yet have a real product plan."
    },
    "atoms": [
      "concept_008",
      "concept_004",
      "fact_011"
    ],
    "density": "dense",
    "visual_design": "LayoutStacked: top=process-diagram(4 steps), bottom=SmartList+AIRR-callout"
  },
  {
    "id": "slide_7",
    "rank": 7,
    "story": {
      "headline": "Teams AI Workbench: from prompt change to eval in under 30 seconds",
      "narrative": "To make eval-first real, PMs need tools that put them directly in the driver\u2019s seat. The Teams AI Workbench and CMDAI evaluation platform are designed to collapse the loop between changing a prompt, running evals, and seeing impact\u2014without waiting on an engineering queue.",
      "evidence": [
        "concept_006",
        "fact_004",
        "tension_004"
      ],
      "takeaway": "Our goal is simple: no PM should ever be stuck with a bad AI output they can\u2019t inspect, score, and fix themselves\u2014within seconds."
    },
    "atoms": [
      "concept_006",
      "fact_004",
      "tension_004"
    ],
    "density": "moderate",
    "visual_design": "LayoutSplit5050: left=diagram(simple loop), right=SmartList+scenario"
  },
  {
    "id": "slide_8",
    "rank": 8,
    "story": {
      "headline": "Surfing the AI wave: online evals and strategic customers",
      "narrative": "AI behavior doesn\u2019t stop changing at GA. Models evolve, customer usage shifts, and edge cases appear in the wild. To stay ahead, we need a way to keep our hands on the wheel after launch, using real customer data as a continuous signal.",
      "evidence": [
        "concept_007",
        "visual_002"
      ],
      "takeaway": "We should partner with strategic customers who can send \u2018online eyes-on\u2019 data so we can continuously tune Recap and Copilot based on real-world behavior."
    },
    "atoms": [
      "concept_007",
      "visual_002"
    ],
    "density": "moderate",
    "visual_design": "LayoutSplit5050: left=metaphor-visual, right=SmartList(explaining online evals)"
  },
  {
    "id": "slide_9",
    "rank": 9,
    "story": {
      "headline": "Designing coherent, high-quality recap experiences under real constraints",
      "narrative": "Recap is where Teams AI meets our customers every day\u2014but today it\u2019s fragmented and constrained. Multiple recap flavors confuse users, and deep reasoning models add latency that kills the experience. We need a coherent architecture that balances quality, speed, and simplicity.",
      "evidence": [
        "tension_003",
        "concept_003",
        "tension_005",
        "stat_001",
        "concept_009",
        "concept_010"
      ],
      "takeaway": "Unifying notes under SOX, defining what \u2018highlights\u2019 mean, and designing smart modes like AI toggle are key to making recap both magical and reliable."
    },
    "atoms": [
      "tension_003",
      "concept_003",
      "tension_005",
      "stat_001",
      "concept_009",
      "concept_010"
    ],
    "density": "dense",
    "visual_design": "LayoutDashboard: main=architecture-diagram(recaps+notes), sidebar=latency-callout+SmartList"
  },
  {
    "id": "slide_10",
    "rank": 10,
    "story": {
      "headline": "From early wins to an AI-first discipline: how Teams PMs lead the next six months",
      "narrative": "Teams has already proven that AI can drive massive Copilot value. Our next chapter is about codifying that success into a discipline others can follow. That means changing how we spend our time, what we measure, and how we design. If we get this right, we don\u2019t just ship great AI features\u2014we define how AI products are built at Microsoft.",
      "evidence": [
        "tension_002",
        "concept_001",
        "concept_002",
        "concept_006",
        "concept_008",
        "fact_011"
      ],
      "takeaway": "Commit to an AI-first PM identity: live in the model, lead with evals, measure value not vanity, and use our tools to turn Recap and Copilot into the gold standard for AI products."
    },
    "atoms": [
      "tension_002",
      "concept_001",
      "concept_002",
      "concept_006",
      "concept_008",
      "fact_011"
    ],
    "density": "moderate",
    "visual_design": "LayoutStacked: main=SmartList+Callout(actions), footer=reminder"
  }
]
```

**Atoms**: {
  "id": "atoms_85e12575684e3267",
  "model": "FactAtom",
  "contexts": [
    {
      "id": "fact_001",
      "rank": 1,
      "state": "draft",
      "abstract": "Blend is an annual event for product and design leaders to share AI product direction and practices",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 60,
        "length": 260,
        "line_number": null
      },
      "visual": "timeline",
      "created_at": "2026-01-07T18:13:35.056459",
      "metadata": {},
      "text": "Blend is a once-a-year opportunity for product and design leaders to come together and share plans about product direction and best practices, with a strong focus on AI and leadership topics.",
      "category": "context"
    },
    {
      "id": "fact_002",
      "rank": 2,
      "state": "draft",
      "abstract": "Teams Recap is a major contributor to the Copilot business",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 780,
        "length": 260,
        "line_number": null
      },
      "visual": "big-number",
      "created_at": "2026-01-07T18:13:35.056834",
      "metadata": {},
      "text": "Within the Teams organization, Recap is described as a \"huge hit\" and one of the biggest contributors to the Copilot business, alongside Teams Copilot and Facilitator.",
      "category": "status"
    },
    {
      "id": "tension_001",
      "rank": 3,
      "state": "draft",
      "abstract": "Most teams are still figuring out how to integrate AI, while Teams already ships impactful AI features",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 840,
        "length": 320,
        "line_number": null
      },
      "visual": "comparison-table",
      "created_at": "2026-01-07T18:13:35.056901",
      "metadata": {},
      "text": "Many product teams across the company are still trying to figure out how to blend AI into their products, whereas the Teams team already has successful AI features like Recap and Teams Copilot that materially contribute to the Copilot business.",
      "tension_type": "status-gap",
      "resolution_hint": "Use Teams\u2019 AI successes as a model and accelerate AI-first practices across the org."
    },
    {
      "id": "concept_001",
      "rank": 4,
      "state": "draft",
      "abstract": "Model-first / eval-first product development should redefine PM work",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 1200,
        "length": 420,
        "line_number": null
      },
      "visual": "flow",
      "created_at": "2026-01-07T18:13:35.057019",
      "metadata": {},
      "text": "The organization is shifting to \"model first\" or \"eval first\" product development, where defining, testing, and iterating on model behavior and evaluation criteria becomes central to how PMs design and ship products.",
      "concept_type": "method",
      "supporting_facts": [
        "fact_010",
        "fact_011",
        "fact_012"
      ]
    },
    {
      "id": "tension_002",
      "rank": 5,
      "state": "draft",
      "abstract": "PM roles must transform to AI-first within six months",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 1440,
        "length": 520,
        "line_number": null
      },
      "visual": "timeline",
      "created_at": "2026-01-07T18:13:35.057390",
      "metadata": {},
      "text": "Han-yi challenges PMs to compare their role on November 19 with their role six months later, expecting a significant shift toward AI-first responsibilities such as eval writing, model understanding, and outcome-driven product work.",
      "tension_type": "transformation",
      "resolution_hint": "Embed AI-first expectations into development lifecycle and provide tools and training for PMs to become strong eval writers and graders."
    },
    {
      "id": "concept_002",
      "rank": 6,
      "state": "draft",
      "abstract": "Build for value, not vanity metrics like superficial usage counts",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 1980,
        "length": 360,
        "line_number": null
      },
      "visual": "comparison-table",
      "created_at": "2026-01-07T18:13:35.057405",
      "metadata": {},
      "text": "The team should \"build for value, not vanity\" by avoiding large but meaningless metrics and instead focusing on measures like retention, attach, and contribution to the Copilot business that reflect real customer value.",
      "concept_type": "principle",
      "supporting_facts": []
    },
    {
      "id": "tension_003",
      "rank": 7,
      "state": "draft",
      "abstract": "Teams recap experiences are fragmented across four different recap surfaces",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 2220,
        "length": 420,
        "line_number": null
      },
      "visual": "diagram",
      "created_at": "2026-01-07T18:13:35.057417",
      "metadata": {},
      "text": "Within Teams there are four different recap experiences\u2014Recap AI summary, Facilitator loop notes, Copilot meeting recap, and detailed Copilot recap\u2014creating confusion for users about the differences and when each appears.",
      "tension_type": "fragmentation",
      "resolution_hint": "Drive coherence and personalization across recap surfaces so users see a unified, tailored experience."
    },
    {
      "id": "concept_003",
      "rank": 8,
      "state": "draft",
      "abstract": "Consolidate notes and recap ownership into the SOX team for coherence",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 2460,
        "length": 320,
        "line_number": null
      },
      "visual": "org-chart",
      "created_at": "2026-01-07T18:13:35.057429",
      "metadata": {},
      "text": "Han-yi proposes transitioning notes, notes conversion, and notes storage into the SOX team so that a single team can lead coherence and personalization for recap experiences across Teams surfaces.",
      "concept_type": "solution",
      "supporting_facts": [
        "tension_003"
      ]
    },
    {
      "id": "quote_001",
      "rank": 9,
      "state": "draft",
      "abstract": "\u201cWe are one of the biggest contributors to the Copilot business.\u201d",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 900,
        "length": 120,
        "line_number": null
      },
      "visual": "quote-card",
      "created_at": "2026-01-07T18:13:35.057455",
      "metadata": {},
      "quote": "We are one of the biggest contributors to the Copilot business.",
      "attribution": "Han-yi Shaw",
      "context": "Describing the impact of Teams Recap and related features on Copilot revenue and usage."
    },
    {
      "id": "fact_003",
      "rank": 10,
      "state": "draft",
      "abstract": "Lon\u2019s \u201cMaking Honey\u201d talk is treated as a golden dataset for great presentations",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 2880,
        "length": 520,
        "line_number": null
      },
      "visual": "none",
      "created_at": "2026-01-07T18:13:35.057554",
      "metadata": {},
      "text": "Lon\u2019s \"Making Honey\" presentation about building intelligent value in Teams is held up as a golden dataset and benchmark for an excellent AI-era presentation, cited as a 5/5 (or even 6/5) example to measure other outputs against.",
      "category": "context"
    },
    {
      "id": "concept_004",
      "rank": 11,
      "state": "draft",
      "abstract": "Golden datasets and rubrics define what \u201cA5\u201d quality looks like for AI output",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 3120,
        "length": 720,
        "line_number": null
      },
      "visual": "diagram",
      "created_at": "2026-01-07T18:13:35.057568",
      "metadata": {},
      "text": "PMs must create golden datasets and detailed rubrics that define what a top-tier (\"A5\") output looks like in terms of precision, brevity, organization, correctness, and tone, so that LLM judges can consistently evaluate model quality at scale.",
      "concept_type": "method",
      "supporting_facts": [
        "fact_003",
        "fact_011"
      ]
    },
    {
      "id": "concept_005",
      "rank": 12,
      "state": "draft",
      "abstract": "The model output, not the UI, is the product in AI experiences",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 3960,
        "length": 520,
        "line_number": null
      },
      "visual": "before-after",
      "created_at": "2026-01-07T18:13:35.057578",
      "metadata": {},
      "text": "In AI-first products, the model\u2019s reasoning and output are the core product experience; UI, specs, and mockups remain necessary but are no longer the focal point for user value or satisfaction.",
      "concept_type": "insight",
      "supporting_facts": [
        "fact_010"
      ]
    },
    {
      "id": "visual_001",
      "rank": 13,
      "state": "draft",
      "abstract": "Pottery metaphor for continuously shaping model behavior",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 4320,
        "length": 260,
        "line_number": null
      },
      "visual": "illustration",
      "created_at": "2026-01-07T18:13:35.057604",
      "metadata": {},
      "description": "A potter shaping clay on a spinning wheel, where small adjustments dramatically change the vessel\u2019s shape, illustrating how prompt and meta-prompt tweaks mold probabilistic model behavior into the desired customer experience.",
      "visual_category": "metaphor",
      "related_atom": "concept_005"
    },
    {
      "id": "concept_006",
      "rank": 14,
      "state": "draft",
      "abstract": "Teams AI Workbench and CMDAI eval platform democratize AI debugging for PMs",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 5040,
        "length": 720,
        "line_number": null
      },
      "visual": "architecture",
      "created_at": "2026-01-07T18:13:35.057688",
      "metadata": {},
      "text": "The Teams AI Workbench system and CMDAI evaluation platform aim to let PMs directly change prompts, run evals, and see scores (e.g., Prism) in under 30 seconds, without heavy engineering dependencies, enabling all disciplines to directly impact AI outcomes.",
      "concept_type": "solution",
      "supporting_facts": [
        "fact_004",
        "fact_005"
      ]
    },
    {
      "id": "fact_004",
      "rank": 15,
      "state": "draft",
      "abstract": "Lon\u2019s AI Workbench vision: prompt change to eval in <30 seconds",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 5400,
        "length": 260,
        "line_number": null
      },
      "visual": "big-number",
      "created_at": "2026-01-07T18:13:35.057700",
      "metadata": {},
      "text": "Lon\u2019s Teams AI Workbench vision includes the goal of \"prompt change to eval in less than 30 seconds,\" enabling rapid iteration on prompts and evaluations by PMs and other disciplines.",
      "category": "definition"
    },
    {
      "id": "tension_004",
      "rank": 16,
      "state": "draft",
      "abstract": "Current PMs can\u2019t easily debug bad AI summaries like round-robin meetings",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 5760,
        "length": 720,
        "line_number": null
      },
      "visual": "storyboard",
      "created_at": "2026-01-07T18:13:35.057745",
      "metadata": {},
      "text": "When Facilitator produced a poor summary of a round-robin meeting, the PM had no direct way to inspect the LLM grader\u2019s score or adjust the prompt, and had to manually craft a better summary via Catalyst and then go through engineering to change behavior.",
      "tension_type": "tooling-gap",
      "resolution_hint": "Give PMs direct access to system prompts, eval tools, and real meeting data so they can iterate on quality without engineering bottlenecks."
    },
    {
      "id": "concept_007",
      "rank": 17,
      "state": "draft",
      "abstract": "Adopt OpenAI-style \u201cninja\u201d online evals with strategic customers",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 6360,
        "length": 420,
        "line_number": null
      },
      "visual": "flow",
      "created_at": "2026-01-07T18:13:35.057757",
      "metadata": {},
      "text": "The team wants to emulate OpenAI\u2019s practice of working with select strategic customers who can send \"online eyes-on\" data when issues occur, enabling continuous post-GA evaluation and iteration based on real-world usage.",
      "concept_type": "method",
      "supporting_facts": []
    },
    {
      "id": "fact_005",
      "rank": 18,
      "state": "draft",
      "abstract": "AI and fundamentals are priority one and two; everything else is priority ten",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 2460,
        "length": 520,
        "line_number": null
      },
      "visual": "priority-ladder",
      "created_at": "2026-01-07T18:13:35.057768",
      "metadata": {},
      "text": "The org is moving into a world where AI and fundamentals (e.g., AV quality, reliability) are priority one and two, and everything else is effectively priority ten; without strong fundamentals, there is no right to talk about AI.",
      "category": "principle"
    },
    {
      "id": "tension_005",
      "rank": 19,
      "state": "draft",
      "abstract": "Upgrading to GPT\u20115.1 deep reasoning caused unacceptable latency in meetings",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 6840,
        "length": 420,
        "line_number": null
      },
      "visual": "before-after",
      "created_at": "2026-01-07T18:13:35.057783",
      "metadata": {},
      "text": "Switching to GPT\u20115.1 with deep reasoning for Catalyst stage two added roughly 9\u201312 seconds to P75 latency, making meeting recaps too slow and forcing a hold on shipping that configuration.",
      "tension_type": "performance-trade-off",
      "resolution_hint": "Control when deep reasoning is used and tune models to balance quality with strict latency budgets for in-meeting scenarios."
    },
    {
      "id": "stat_001",
      "rank": 20,
      "state": "draft",
      "abstract": "Deep reasoning added ~9\u201312 seconds to P75 latency for Catalyst",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 6960,
        "length": 260,
        "line_number": null
      },
      "visual": "big-number",
      "created_at": "2026-01-07T18:13:35.057807",
      "metadata": {},
      "value": "9\u201312 seconds",
      "label": "Additional P75 latency from GPT\u20115.1 deep reasoning",
      "context": "Latency impact when MSAI turned on GPT\u20115.1 deep reasoning by default for Catalyst stage two, making recap responses too slow in meetings."
    },
    {
      "id": "concept_008",
      "rank": 21,
      "state": "draft",
      "abstract": "Eval must move from end-of-cycle QA to front-and-center design tool",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 7320,
        "length": 640,
        "line_number": null
      },
      "visual": "flow",
      "created_at": "2026-01-07T18:13:35.057889",
      "metadata": {},
      "text": "Evaluation can no longer be a final QA step; PMs must define eval categories, golden datasets, and LLM judges at the very beginning of the product lifecycle and treat evals as their primary design tool, more central than Figma or traditional specs.",
      "concept_type": "insight",
      "supporting_facts": [
        "fact_011"
      ]
    },
    {
      "id": "fact_011",
      "rank": 22,
      "state": "draft",
      "abstract": "AIRR (AI Readiness Review) will complement UXRS and ERS",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 8040,
        "length": 360,
        "line_number": null
      },
      "visual": "checklist",
      "created_at": "2026-01-07T18:13:35.057900",
      "metadata": {},
      "text": "In addition to UXRS and ERS, the org will introduce AI Readiness Reviews (AIRR), where PMs must answer how they will approach evals, golden datasets, and engineering integration for AI features before shipping.",
      "category": "process"
    },
    {
      "id": "visual_002",
      "rank": 23,
      "state": "draft",
      "abstract": "Surfing metaphor: model as wave, eval as surfboard, UI as foam",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 8280,
        "length": 520,
        "line_number": null
      },
      "visual": "illustration",
      "created_at": "2026-01-07T18:13:35.057913",
      "metadata": {},
      "description": "A surfer riding a powerful wave at night with only a surfboard and faint light, where the wave represents the unpredictable AI model, the surfboard represents evals, and the white foam on top represents UI that can\u2019t save you from a bad wave.",
      "visual_category": "metaphor",
      "related_atom": "concept_008"
    },
    {
      "id": "tension_006",
      "rank": 24,
      "state": "draft",
      "abstract": "Teams PM org is behind other orgs in becoming true AI PMs",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 9000,
        "length": 520,
        "line_number": null
      },
      "visual": "none",
      "created_at": "2026-01-07T18:13:35.057925",
      "metadata": {},
      "text": "Cathy notes that while they once felt like leading-edge AI PMs, conversations at Blend revealed that many other organizations have already converted PM practices to start from customer thinking, evaluation mastery, and deep model understanding, leaving this team behind.",
      "tension_type": "competitive-gap",
      "resolution_hint": "Accelerate AI PM upskilling, embed eval and model literacy into specs, and adopt practices seen in more advanced orgs."
    },
    {
      "id": "concept_009",
      "rank": 25,
      "state": "draft",
      "abstract": "AI mode / ephemeral transcript switch to unlock recap without explicit recording",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 10560,
        "length": 720,
        "line_number": null
      },
      "visual": "diagram",
      "created_at": "2026-01-07T18:13:35.057937",
      "metadata": {},
      "text": "To support recap in Copilot-only mode without explicit transcription or recording buttons, Han-yi suggests an \"AI mode\" toggle (similar to Office\u2019s AutoSave) that implicitly turns on ephemeral transcription and enables recap, Facilitator, and other AI features.",
      "concept_type": "solution",
      "supporting_facts": []
    },
    {
      "id": "concept_010",
      "rank": 26,
      "state": "draft",
      "abstract": "Video recap needs clear eval definition of what counts as a highlight",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 11880,
        "length": 520,
        "line_number": null
      },
      "visual": "storyboard",
      "created_at": "2026-01-07T18:13:35.057948",
      "metadata": {},
      "text": "For future video recap experiences, the team must define what constitutes a highlight (e.g., leader quotes, key decisions, insights) and build evals and golden datasets around that, potentially using LLMs as brainstorming partners to explore formats like soundbites vs summaries.",
      "concept_type": "method",
      "supporting_facts": [
        "concept_004"
      ]
    }
  ]
}
**Instructions**: Start with a title slide
Balance content density

User instruction: Generate slides.

**RULES**:
1. Follow each slide's `visual_design` field for layout and content approach
2. Follow each slide's `density` field (sparse=2-3 blocks, moderate=3-4, dense=5+)
3. Each slide tells its own story from the `story` field
4. Use Diagram ONLY when visual_design explicitly mentions it
5. ≥4 different layouts across deck, no consecutive repeats
6. Each <Slide> has id, rank, story, atoms attributes
7. Combine text AND visual on each slide (one leads, other supports)
8. Fill space appropriate to density (sparse≠empty)

Generate MDX slides wrapped in <Slide> elements.

---

# System
You are a LAYOUT DESIGNER. Convert story drafts into MDX slides.

# CORE PRINCIPLE
Follow the draft slide's `story` and `visual_design` fields exactly:
- `story` defines WHAT to say (HEADLINE, NARRATIVE, EVIDENCE, TAKEAWAY)
- `visual_design` defines HOW to show it (layout + content approach)
- `density` defines HOW MUCH (sparse=focused, moderate=balanced, dense=detailed)

# DENSITY → ELEMENTS
| Density | Meaning | Blocks | Coverage |
|---------|---------|--------|----------|
| sparse | Single focus, supporting context | 2-3 blocks (hero + support) | 40-60% |
| moderate | Balanced multi-element | 4-5 blocks | 60-80% |
| dense | Detailed breakdown | 5-7 blocks | 70-90% |

# PAGE COVERAGE RULE (CRITICAL)
- **Every page must have ≥70% content coverage** (no large empty areas)
- Dense pages need 5+ elements filling the space
- NO GAPS: content should flow continuously, not leave holes
- If a layout has multiple slots, ALL slots must have substantial content

# CONTENT MAPPING
- HEADLINE → `<Heading>`
- NARRATIVE → `<Text variant="lead">` or `<SmartList>`
- EVIDENCE (numbers) → `<MetricGroup>`, `<BigNum>`, `<ChartBar>`
- EVIDENCE (branching graphs) → `<NetworkGraph>` with JSX children (Node, Edge, Group)
- EVIDENCE (linear flows) → `<ProcessStrip>` for A→B→C sequences
- TAKEAWAY → `<Callout>` or `<Text variant="caption">`

# VISUAL SELECTION
- Use NetworkGraph when visual_design mentions branching "architecture", "network", "org chart" (nodes connect to multiple targets)
- Use ProcessStrip for "flow", "pipeline", "sequence", "stages" (linear A→B→C)
- Use Chart when visual_design mentions "chart", "comparison", "trend"
- Default to Text/SmartList for narrative content
- Each slide should combine text AND visual, but one leads

# NO REDUNDANT CONTENT (CRITICAL)
- NEVER show the same data twice on a slide in different formats
- If Left has MetricGroup with "71% → 80%", Right should NOT have BigNum with same numbers
- Each element must add NEW information, not repeat what's already visible
- BAD: MetricGroup(71%, 80%) + BigNum(80%) ← REDUNDANT
- GOOD: MetricGroup(71%, 80%) + SmartList(key actions) ← COMPLEMENTARY

# SMARTLIST GROUPING RULE (CRITICAL)
- **NEVER place two SmartList components consecutively without a Heading between them**
- If you have related list items, combine them into ONE SmartList with all items in the items array
- A SmartList without a preceding Heading looks like orphaned content (no context)
- BAD: SmartList followed by another SmartList without Heading between them
- GOOD: Single SmartList with all related items combined in one items array
- If lists represent different topics, each MUST have its own Heading before it

# SPACE MANAGEMENT (70% MINIMUM COVERAGE)
- **EVERY PAGE must fill ≥70% of vertical space** with content
- Split layouts: BOTH sides need 4+ elements EACH (Heading + visual + text + support)
- Both sides of split must span similar vertical height (visual overlap)
- Dashboard/Stacked: ALL slots need content, no empty or sparse slots
- Never leave gaps/holes - content should flow continuously
- AVOID: sparse pages that look like work-in-progress
- If content is limited, use simpler layout (LayoutStacked) rather than leave gaps

# VISUAL DESIGN INSTRUCTIONS

You are designing slides as MDX markup. Match layout to the visual_design intent.

## LAYOUT DECISIONS

**LayoutCover** — TRADITIONAL cover page: title + subtitle only. Clean, minimal, impactful.
- Best: opening title slide, closing "Thank You" slide, section dividers
- Components: Heading (level 1), Text (subtitle), optionally ONE of: QuoteBlock OR simple Callout
- **🚫 FORBIDDEN on LayoutCover**: BigNum, MetricGroup, SmartList, Charts, Diagrams, CardGroup, ProcessStrip, StepList
- **MAX ELEMENTS**: 2-3 elements total (Heading + subtitle + optional quote/callout)
- Cover pages should feel SPACIOUS and IMPACTFUL, not cramped with data

**LayoutSplit** — Use when pairing text with visual, or showing two related concepts.
- Best: metric + context, chart + explanation, before/after
- Slots: Left, Right | ratio: 1:1, 2:1, 1:2, 3:1, 1:3
- Components: Any combination of Heading, Text, BigNum, SmartList, Charts
- **HEADING RULE**: Use the SAME heading level on both sides (both level={2} or both level={3}). Never mix heading levels in a split layout.
- **DIAGRAM RULE for Split Layouts**:
  - NetworkGraph in ANY split layout should use `direction="TB"` (vertical/top-to-bottom) to maximize height
  - Split columns are narrow → horizontal diagrams look cramped and short
  - Prefer vertical flow diagrams that fill the column height, not width
- **CONTENT PLANNING BY RATIO**:
  - **1:1**: Equal content on both sides (4-5 elements each)
  - **2:1**: Larger side (2) gets main content (5-6 elements); smaller side (1) gets 2-3 supporting elements
  - **1:2**: Smaller side (1) gets 2-3 elements; larger side (2) gets main content (5-6 elements)
  - **3:1 / 1:3**: Large side dominates (6+ elements); small side is accent only (1-2 elements: Heading + Callout or BigNum)
- **RULE**: Match content density to column width. Never cram the small column with as much as the large column.

**LayoutStacked** — Use for text-heavy narrative or sequential content.
- Best: storytelling, explanations, step-by-step instructions
- Components: Heading, Text, SmartList, TableData

**LayoutGrid** — Use for parallel items of equal importance.
- Best: features, team, products, categories
- Slots: Col ×2-4 | cols: 2, 3, 4
- Components: CardGroup, MetricGroup, Heading

**LayoutFullBleed** — Use for visual impact with background image.
- Best: hero moments, emotional beats, section transitions
- Components: Heading, QuoteBlock, BigNum (overlay on image)

**LayoutDashboard** — Use for data-dense KPI displays.
- Best: metrics overview, performance summary, status report
- Slots: Header, Main, Sidebar, Footer
- **Header slot**: Heading level={2} ONLY (no Text, no lead paragraph)
- **Main slot**: Text variant="lead" (first), MetricGroup, Charts, Tables, BigNum
- **Sidebar slot**: SmartList, Callout, compact text (supporting content)
- **AVOID**: Diagram alone in Main (leaves empty space), MetricGroup in Sidebar (too narrow)
- **NOTE**: Dashboard body (Main + Sidebar) is vertically centered; Header stays at top

**LayoutTimeline** — Use for chronological milestones with rich content per event.
- Best: company history, project milestones, annual roadmap with details
- Use when each milestone needs: title + description (rich content)
- Creates horizontal timeline with alternating nodes above/below center line
- Slots: LayoutTimeline.Item (with year prop) × 3-6 items
- Components inside Item: Heading level={3}, Text (keep brief)
- PREFER over ProcessStrip when milestones need detailed explanations

## COMPONENT REFERENCE

**⚠️ CONTENT MINIMUM PER SLIDE** (non-negotiable):
- Every slide must have **at least 1 visual block**: BigNum, MetricGroup, Chart, Diagram, CardGroup, TableData, QuoteBlock
- "Visual block" = anything that isn't just Heading/Text/SmartList
- Text-only slides with just Heading + SmartList look INCOMPLETE

**Metrics**: BigNum (hero stat with trend), MetricGroup (3-4 KPIs), MetricStrip (inline row)
**Content**: SmartList (bullet points), CardGroup (feature cards), QuoteBlock, TableData
**Text**: Heading (level 1-3), Text (lead/body/caption), Callout (alerts), Highlight (inline emphasis)

**⭐ PROCESSSTRIP - USE THIS FOR WORKFLOWS/FLOWS** (most common visual element!):
- **ProcessStrip**: Horizontal phases - USE FOR: any A→B→C→D flow, turn sequences, pipelines, stages
- **StepList**: Vertical numbered steps - USE FOR: setup guides, how-to, onboarding flows
- **LayoutTimeline**: Rich chronological milestones - USE FOR: company history with details

**🚫🚫🚫 PROCESSSTRIP WIDTH RULE (CRITICAL - WILL CAUSE OVERFLOW!):**
| Layout Context | Max ProcessStrip Items |
|----------------|------------------------|
| 1:1 split (Left or Right) | **3 items MAX** |
| 1:2 split small side | **2 items MAX** |
| 2:1 split large side | 4 items OK |
| LayoutStacked (full width) | 5+ items OK |
| LayoutDashboard Main | 4 items OK |

**IF YOU HAVE 4+ STEPS IN A 1:1 SPLIT → USE StepList INSTEAD (vertical, fits narrow columns)**

**⚠️⚠️⚠️ STOP! Before using NetworkGraph, ask: "Does ANY node branch to 2+ outputs?"**
- If NO → USE ProcessStrip (linear sequence) - this is 90% of cases!
- If YES → NetworkGraph is OK (true branching graph)
- "Speaker → Capture → Translate → Playback" = ProcessStrip (each step leads to ONE next)
- "Engine → [Interpreter, Captions, Transcription]" = NetworkGraph (Engine branches to 3)

**INLINE HIGHLIGHT**:
Use `<Highlight>` to emphasize key words within text:
```
<Text>We achieved <Highlight color="success">10x growth</Highlight> this quarter.</Text>
<Text>Key metric: <Highlight color="primary" bold>$1.2M revenue</Highlight></Text>
```
Colors: default, primary, success, warning, info, accent

**CHARTS (for numeric data)**:
- ChartBar: comparison, before/after (use `before`/`after` keys for clustered bars)
- ChartLine: trends over time
- ChartPie: proportions/percentages
- **RULE**: 3+ data points → use Chart, not multiple Metrics

## MDX OUTPUT FORMAT

Each slide wrapped in `<Slide>` with metadata:

```mdx
<Slide id="slide_01" rank={1} story="HOOK" atoms={["stat_001"]}>
<LayoutCover theme="dark">
  <Heading level={1}>The Future of AI</Heading>
  <BigNum id="stat_001" value="10B" label="Parameters"/>
</LayoutCover>
</Slide>

<Slide id="slide_02" rank={2} story="TENSION" atoms={["fact_001"]}>
<LayoutSplit ratio="2:1">
  <Left>
    <Heading level={2}>The Challenge</Heading>
    <SmartList id="list_001" items={["Scale", "Cost", "Complexity"]}/>
  </Left>
  <Right>
    <ChartBar id="chart_001" data={[{name: "2023", value: 100}, {name: "2024", value: 250}]}/>
  </Right>
</LayoutSplit>
</Slide>

<Slide id="slide_03" rank={3} story="JOURNEY" atoms={[]}>
<LayoutDashboard>
  <Header><Heading level={2}>Performance</Heading></Header>
  <Main>
    <Text variant="lead">Key metrics showing strong growth this quarter.</Text>
    <MetricGroup id="metrics_001" cols={3}>
      <Metric value="$1.2M" label="Revenue" change={12}/>
      <Metric value="89%" label="Margin"/>
      <Metric value="4.2" label="Rating"/>
    </MetricGroup>
  </Main>
</LayoutDashboard>
</Slide>
```

## COMPONENT SYNTAX

```mdx
// Text with inline highlights
<Heading level={1}>Display Title</Heading>
<Text variant="lead">We achieved <Highlight color="success">10x growth</Highlight> this quarter.</Text>
<Text>Key metric: <Highlight color="primary" bold>$1.2M</Highlight> in revenue.</Text>
<Callout intent="info" title="Note">Content with <Highlight>key terms</Highlight>.</Callout>

// Metrics (must have id for patching)
<BigNum id="stat_001" value="42%" label="Growth" trend="+5%"/>
<MetricGroup id="metrics_001" cols={3}>
  <Metric value="$1M" label="Revenue"/>
</MetricGroup>

// Content (must have id)
<SmartList id="list_001" items={["Item 1", "Item 2"]} ordered={false}/>
<CardGroup id="cards_001" columns={3}>
  <Card title="Speed" description="10x faster" icon="🚀"/>
</CardGroup>
<QuoteBlock id="quote_001" author="CEO">Stay focused.</QuoteBlock>

// ⭐⭐⭐ SEQUENCES - USE THESE OFTEN for any step-by-step content! ⭐⭐⭐
// These are VISUAL BLOCKS that make pages look professional and full!

// ProcessStrip: horizontal phases (PREFER THIS for workflows, pipelines, stages)
// ⚠️ WIDTH RULE: Max 3 items in 1:1 split or smaller. 4+ items need full width or 2:1 large side.
<ProcessStrip id="process_001" items={["Plan", "Build", "Test"]}/>  // 3 items OK in split
// ProcessStrip with status (use in full-width layouts for 4+ items):
<ProcessStrip id="process_002" items={[{label: "Collect", status: "done"}, {label: "Process", status: "active"}, {label: "Validate", status: "pending"}, {label: "Deploy", status: "pending"}]}/>
// USE ProcessStrip for: turn sequences, data pipelines, workflow stages, any A→B→C→D flow

// StepList: vertical numbered steps (BETTER for narrow columns - handles 4+ items well)
<StepList id="steps_001" items={["Collect data", "Process", "Validate", "Deploy"]}/>
// StepList with descriptions:
<StepList id="steps_002" items={[{label: "Plan", description: "Define scope"}, {label: "Build", description: "Implement"}]}/>

// LayoutTimeline: for chronological milestones with rich content (full page layout)
// Use when you need richer content per milestone (heading + text + callout per item)
<LayoutTimeline>
  <LayoutTimeline.Item year="2020">
    <Heading level={3}>Product Launch</Heading>
    <Text>Released v1.0 to market</Text>
  </LayoutTimeline.Item>
  <LayoutTimeline.Item year="2022" highlighted={true}>
    <Heading level={3}>Series A</Heading>
    <Text>Raised $10M funding</Text>
  </LayoutTimeline.Item>
  <LayoutTimeline.Item year="2024">
    <Heading level={3}>Global Expansion</Heading>
    <Text>Launched in 50 countries</Text>
  </LayoutTimeline.Item>
</LayoutTimeline>
// NOTE: ProcessStrip is better for simple year labels; LayoutTimeline is better for detailed milestone stories

// Charts (must have id)
// Single series:
<ChartBar id="chart_001" title="Revenue" data={[{label: "Q1", value: 100}, {label: "Q2", value: 150}]}/>
// Clustered bars for before/after comparison:
<ChartBar id="chart_002" title="Improvements" data={[{label: "Accuracy", before: 65, after: 75}, {label: "Speed", before: 800, after: 450}]}/>
<ChartLine id="chart_003" title="Growth" data={[{label: "Jan", value: 50}]}/>
<ChartPie id="chart_004" title="Share" data={[{label: "A", value: 60}]}/>

// Tables
<TableData id="table_001" headers={["Name", "Value"]} rows={[["A", "1"]]}/>

// ⚠️⚠️⚠️ CRITICAL: NetworkGraph vs ProcessStrip DECISION ⚠️⚠️⚠️
// STEP 1: Count how many edges come OUT of each node:
//   - If EVERY node has exactly 0 or 1 outgoing edge → USE ProcessStrip (it's linear!)
//   - If ANY node has 2+ outgoing edges → NetworkGraph is OK (it's branching)
//
// EXAMPLES OF LINEAR (USE ProcessStrip, NOT NetworkGraph):
//   "Speaker → Capture → Translate → Playback" ← each node has 1 output = ProcessStrip!
//   "Input → Process → Judge → Output" ← each node has 1 output = ProcessStrip!
//   "Today → Jan 2026 → Future" ← each node has 1 output = ProcessStrip!
//
// EXAMPLES OF BRANCHING (NetworkGraph OK):
//   "Engine → Interpreter, Captions, Transcription" ← Engine has 3 outputs = NetworkGraph OK
//   "API → Auth AND Cache; both → DB" ← API has 2 outputs = NetworkGraph OK
//
// ⚠️ In Split layouts: ALWAYS use direction="TB" (vertical) - horizontal diagrams look cramped
// ⚠️ SIZE PROP (REQUIRED - count your nodes!):
//   - size="compact": 2-3 nodes ONLY
//   - size="medium": 4-5 nodes ONLY
//   - size="tall": 6+ nodes (MUST use tall if ≥6 nodes!)
// RULE: Count <Node> elements, then pick size. 7 nodes = tall. 4 nodes = medium. 3 nodes = compact.
// Example valid use: API Gateway connects to BOTH Auth AND Cache (branching)
<NetworkGraph id="diagram_001" type="network" direction="TB" size="medium" title="System Architecture">
  <Node id="api" label="API Gateway" className="api" />
  <Node id="auth" label="Auth Service" className="process" />
  <Node id="db" label="Database" className="database" />
  <Node id="cache" label="Cache" className="process" />
  <Edge source="api" target="auth" />
  <Edge source="api" target="cache" />
  <Edge source="auth" target="db" />
  <Edge source="cache" target="db" />
</NetworkGraph>

// For hierarchy/org charts with 6+ nodes - MUST use size="tall":
<NetworkGraph id="diagram_002" type="network" direction="TB" size="tall" title="Org Structure">
  <Group id="frontend" label="Frontend">
    <Node id="web" label="Web App" className="api" />
    <Node id="mobile" label="Mobile App" className="api" />
  </Group>
  <Node id="gateway" label="API Gateway" className="process" />
  <Node id="db" label="Database" className="database" />
  <Edge source="web" target="gateway" />
  <Edge source="mobile" target="gateway" />
  <Edge source="gateway" target="db" />
</NetworkGraph>

## TEXT LIMITS
Display: 6 words | Heading: 8 | Body: 25 | List item: 10 words

# LAYOUT CONSTRAINTS

## LAYOUT-COMPONENT COMPATIBILITY
| Component | cover | split | stacked | grid | fullbleed | dashboard | timeline |
|-----------|-------|-------|---------|------|-----------|-----------|----------|
| Heading | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Text | ✅ | ✅ | ✅ | ⚠️ | ✅ | ❌ | ✅ |
| SmartList | ❌ | ✅ | ✅ | ⚠️ | ❌ | ❌ | ❌ |
| BigNum | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ |
| MetricGroup | ❌ | ✅ | ❌ | ✅ | ❌ | ✅ | ❌ |
| Charts | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |
| NetworkGraph | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| QuoteBlock | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| CardGroup | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| TableData | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Callout | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| StepList | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| ProcessStrip | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| Highlight | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

## SLIDE VARIETY (CRITICAL)
**Never use the same layout + component pattern on consecutive slides.**
- If slide N uses LayoutSplit with NetworkGraph+SmartList, slide N+1 MUST use a different layout OR different component types
- Repeating the same visual pattern makes the deck feel monotonous and template-like
- **Good**: Split→Dashboard→Split(different ratio)→Grid→Stacked
- **Bad**: Split(2:1)+Diagram→Split(2:1)+Diagram→Split(2:1)+Diagram
- Vary: layout type, split ratio, primary visual block (Chart vs Diagram vs MetricGroup vs CardGroup)

## SPLIT LAYOUT REQUIREMENTS (CRITICAL)
Split layouts (LayoutSplit) need SUBSTANTIAL content on BOTH sides:
- **Each side must have 4+ elements** (Heading + 2-3 content blocks + supporting text)
- **Both sides must have similar vertical height** so they visually overlap (not a sparse 2x3 grid)
- **Bad example**: Left has Heading+SmartList (2 items), Right has Heading+SmartList → looks like unfinished grid
- **Good example**: Left has Heading+Diagram+Text+Callout, Right has BigNum+MetricGroup+SmartList+Text

ERROR pattern to avoid: "2x3 grid with empty slots" - when split layout has only 2-3 small items per side,
the page looks like a 6-cell grid where half the cells are empty. This makes the slide look unfinished.

### SPLIT LAYOUT REQUIRED STRUCTURE (ALL ELEMENTS REQUIRED):
```
<LayoutSplit ratio="1:1">
  <Left>
    <Heading level={2}>Title Here</Heading>           <!-- Required -->
    <BigNum id="..." value="..." label="..."/>        <!-- Visual block required -->
    <SmartList id="..." items={[...3-4 items...]}/>  <!-- Text block required -->
    <Callout intent="info" title="...">...</Callout>  <!-- Supporting block required -->
  </Left>
  <Right>
    <Heading level={3}>Subtitle Here</Heading>        <!-- Required -->
    <MetricGroup id="..." cols={3}>...</MetricGroup>  <!-- Visual block required -->
    <Text variant="body">Explanation text...</Text>   <!-- Text block required -->
    <Text variant="caption">Source note...</Text>     <!-- Supporting block required -->
  </Right>
</LayoutSplit>
```

If you don't have enough content for 4+ elements per side, use LayoutStacked instead.

## DENSITY GUIDE
| Position | Density | Layout Choices |
|----------|---------|----------------|
| Slide 1 (Opening) | MINIMAL | cover (title + subtitle ONLY, no data) |
| Slide 2 | MODERATE | split, stacked (intro content) |
| Slide 3-8 | DENSE | dashboard, split, timeline, grid (main content) |
| Slide 9 | MODERATE | split, stacked (summary/next steps) |
| Final (Closing) | MINIMAL | cover ("Thank You" or CTA, no data) |

## PAGE COVERAGE REQUIREMENTS (CRITICAL)
**Every page must feel FULL - empty/sparse pages look unfinished and unprofessional**
**Target: Fill 70-85% of visible area with meaningful content**

| Layout | Min Elements | Typical Content Mix |
|--------|--------------|---------------------|
| LayoutCover | 2-3 | Heading + Text(subtitle) + optional QuoteBlock — KEEP IT MINIMAL! |
| LayoutStacked | 6-8 | Heading + Text + MetricGroup + SmartList + Callout + supporting text |
| LayoutDashboard | 8-10 | Header: Heading+Text. Main: MetricGroup + Chart + Text. Sidebar: SmartList + Callout |
| LayoutTimeline | 5-6 | 5-6 timeline items with Heading + Text each |
| LayoutSplit | 10-12 | Each side: Heading + 2 visuals(BigNum+Chart or Metric+List) + Text + Callout |
| LayoutGrid | 6-8 | Heading + Text + CardGroup(4 cards) + Callout or MetricGroup |

**CONTENT RICHNESS RULES** (follow strictly!):
- **Every slide needs at least TWO visual blocks**: BigNum + Chart, or MetricGroup + SmartList, etc.
- **Text-only slides look empty** - always pair text with visuals
- **EXCEPTION: Cover slides ARE "just title + subtitle"** - keep them clean and impactful, NO data
- **Dashboard sidebars can't be empty** - fill with SmartList + Callout + Text
- **Split layouts need BOTH sides full** - 5+ elements per side minimum
- **When in doubt, ADD more content** - sparse pages look unprofessional
- **Use ProcessStrip/StepList for workflows** - they add visual interest without complexity

**ERROR patterns to avoid:**
- Page with only Heading + SmartList (looks incomplete)
- Dashboard with empty Main or Sidebar slots
- Stacked with only 2-3 small elements (gaps visible)
- Cover with only title (add subtitle, quote, or metric)
- Split with one side nearly empty

## RULES
- ≥4 different layouts per deck
- Never same layout twice in a row
- Numbers → BigNum/MetricGroup (not in text)
- ≥3 slides with data components
- Lists max 4 items, body max 25 words
- Split layouts: BOTH sides need visual blocks, not just text
- **NO GAPS**: content should fill the page, not leave holes
- **NO REDUNDANCY**: Never show same data twice (e.g., MetricGroup + BigNum with same numbers)


# NEW CAPABILITY: Inventing Components When Predefined Ones Don't Fit
When existing components cannot best express the slide's **intent** or cannot represent the **data** clearly, you MAY invent a new component. This is a design-time placeholder that will later be turned into real React code by a downstream step.

## How to Declare an Invented Component
Use the special tag `<InventComponent>` inside the slide body. It MUST include:
- `intent`: a short verb-noun phrase describing purpose (e.g., "compare cohorts").
- `data`: a compact JSON object with the minimum structure required to render.
- `notes` (optional): guidance for codegen (interactions, layout, a11y).

### Syntax
<InventComponent
  intent="compare cohorts"
  data={{ cohorts: [{ name: "Treatment", size: 120, conversion: 0.37 },
                    { name: "Control",   size: 118, conversion: 0.21 }],
          compareBy: "conversion",
          highlights: ["Treatment +16pp vs Control"] }}
  notes="Needs side-by-side bars with significance marks; responsive; keyboard focus order"
/>

### Rules (CRITICAL)
- Invent only when predefined components cannot faithfully express the **intent**.
- Keep `data` minimal yet unambiguous; avoid raw prose.
- NEVER duplicate already-presented data (respect NO REDUNDANCY).
- `<InventComponent>` counts as a **visual block** for coverage calculations.
- Provide stable keys in `data` so React props are predictable.

# User
**Atoms**: {
  "id": "atoms_85e12575684e3267",
  "model": "FactAtom",
  "contexts": [
    {
      "id": "fact_001",
      "rank": 1,
      "state": "draft",
      "abstract": "Blend is an annual event for product and design leaders to share AI product direction and practices",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 60,
        "length": 260,
        "line_number": null
      },
      "visual": "timeline",
      "created_at": "2026-01-07T18:13:35.056459",
      "metadata": {},
      "text": "Blend is a once-a-year opportunity for product and design leaders to come together and share plans about product direction and best practices, with a strong focus on AI and leadership topics.",
      "category": "context"
    },
    {
      "id": "fact_002",
      "rank": 2,
      "state": "draft",
      "abstract": "Teams Recap is a major contributor to the Copilot business",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 780,
        "length": 260,
        "line_number": null
      },
      "visual": "big-number",
      "created_at": "2026-01-07T18:13:35.056834",
      "metadata": {},
      "text": "Within the Teams organization, Recap is described as a \"huge hit\" and one of the biggest contributors to the Copilot business, alongside Teams Copilot and Facilitator.",
      "category": "status"
    },
    {
      "id": "tension_001",
      "rank": 3,
      "state": "draft",
      "abstract": "Most teams are still figuring out how to integrate AI, while Teams already ships impactful AI features",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 840,
        "length": 320,
        "line_number": null
      },
      "visual": "comparison-table",
      "created_at": "2026-01-07T18:13:35.056901",
      "metadata": {},
      "text": "Many product teams across the company are still trying to figure out how to blend AI into their products, whereas the Teams team already has successful AI features like Recap and Teams Copilot that materially contribute to the Copilot business.",
      "tension_type": "status-gap",
      "resolution_hint": "Use Teams\u2019 AI successes as a model and accelerate AI-first practices across the org."
    },
    {
      "id": "concept_001",
      "rank": 4,
      "state": "draft",
      "abstract": "Model-first / eval-first product development should redefine PM work",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 1200,
        "length": 420,
        "line_number": null
      },
      "visual": "flow",
      "created_at": "2026-01-07T18:13:35.057019",
      "metadata": {},
      "text": "The organization is shifting to \"model first\" or \"eval first\" product development, where defining, testing, and iterating on model behavior and evaluation criteria becomes central to how PMs design and ship products.",
      "concept_type": "method",
      "supporting_facts": [
        "fact_010",
        "fact_011",
        "fact_012"
      ]
    },
    {
      "id": "tension_002",
      "rank": 5,
      "state": "draft",
      "abstract": "PM roles must transform to AI-first within six months",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 1440,
        "length": 520,
        "line_number": null
      },
      "visual": "timeline",
      "created_at": "2026-01-07T18:13:35.057390",
      "metadata": {},
      "text": "Han-yi challenges PMs to compare their role on November 19 with their role six months later, expecting a significant shift toward AI-first responsibilities such as eval writing, model understanding, and outcome-driven product work.",
      "tension_type": "transformation",
      "resolution_hint": "Embed AI-first expectations into development lifecycle and provide tools and training for PMs to become strong eval writers and graders."
    },
    {
      "id": "concept_002",
      "rank": 6,
      "state": "draft",
      "abstract": "Build for value, not vanity metrics like superficial usage counts",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 1980,
        "length": 360,
        "line_number": null
      },
      "visual": "comparison-table",
      "created_at": "2026-01-07T18:13:35.057405",
      "metadata": {},
      "text": "The team should \"build for value, not vanity\" by avoiding large but meaningless metrics and instead focusing on measures like retention, attach, and contribution to the Copilot business that reflect real customer value.",
      "concept_type": "principle",
      "supporting_facts": []
    },
    {
      "id": "tension_003",
      "rank": 7,
      "state": "draft",
      "abstract": "Teams recap experiences are fragmented across four different recap surfaces",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 2220,
        "length": 420,
        "line_number": null
      },
      "visual": "diagram",
      "created_at": "2026-01-07T18:13:35.057417",
      "metadata": {},
      "text": "Within Teams there are four different recap experiences\u2014Recap AI summary, Facilitator loop notes, Copilot meeting recap, and detailed Copilot recap\u2014creating confusion for users about the differences and when each appears.",
      "tension_type": "fragmentation",
      "resolution_hint": "Drive coherence and personalization across recap surfaces so users see a unified, tailored experience."
    },
    {
      "id": "concept_003",
      "rank": 8,
      "state": "draft",
      "abstract": "Consolidate notes and recap ownership into the SOX team for coherence",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 2460,
        "length": 320,
        "line_number": null
      },
      "visual": "org-chart",
      "created_at": "2026-01-07T18:13:35.057429",
      "metadata": {},
      "text": "Han-yi proposes transitioning notes, notes conversion, and notes storage into the SOX team so that a single team can lead coherence and personalization for recap experiences across Teams surfaces.",
      "concept_type": "solution",
      "supporting_facts": [
        "tension_003"
      ]
    },
    {
      "id": "quote_001",
      "rank": 9,
      "state": "draft",
      "abstract": "\u201cWe are one of the biggest contributors to the Copilot business.\u201d",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 900,
        "length": 120,
        "line_number": null
      },
      "visual": "quote-card",
      "created_at": "2026-01-07T18:13:35.057455",
      "metadata": {},
      "quote": "We are one of the biggest contributors to the Copilot business.",
      "attribution": "Han-yi Shaw",
      "context": "Describing the impact of Teams Recap and related features on Copilot revenue and usage."
    },
    {
      "id": "fact_003",
      "rank": 10,
      "state": "draft",
      "abstract": "Lon\u2019s \u201cMaking Honey\u201d talk is treated as a golden dataset for great presentations",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 2880,
        "length": 520,
        "line_number": null
      },
      "visual": "none",
      "created_at": "2026-01-07T18:13:35.057554",
      "metadata": {},
      "text": "Lon\u2019s \"Making Honey\" presentation about building intelligent value in Teams is held up as a golden dataset and benchmark for an excellent AI-era presentation, cited as a 5/5 (or even 6/5) example to measure other outputs against.",
      "category": "context"
    },
    {
      "id": "concept_004",
      "rank": 11,
      "state": "draft",
      "abstract": "Golden datasets and rubrics define what \u201cA5\u201d quality looks like for AI output",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 3120,
        "length": 720,
        "line_number": null
      },
      "visual": "diagram",
      "created_at": "2026-01-07T18:13:35.057568",
      "metadata": {},
      "text": "PMs must create golden datasets and detailed rubrics that define what a top-tier (\"A5\") output looks like in terms of precision, brevity, organization, correctness, and tone, so that LLM judges can consistently evaluate model quality at scale.",
      "concept_type": "method",
      "supporting_facts": [
        "fact_003",
        "fact_011"
      ]
    },
    {
      "id": "concept_005",
      "rank": 12,
      "state": "draft",
      "abstract": "The model output, not the UI, is the product in AI experiences",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 3960,
        "length": 520,
        "line_number": null
      },
      "visual": "before-after",
      "created_at": "2026-01-07T18:13:35.057578",
      "metadata": {},
      "text": "In AI-first products, the model\u2019s reasoning and output are the core product experience; UI, specs, and mockups remain necessary but are no longer the focal point for user value or satisfaction.",
      "concept_type": "insight",
      "supporting_facts": [
        "fact_010"
      ]
    },
    {
      "id": "visual_001",
      "rank": 13,
      "state": "draft",
      "abstract": "Pottery metaphor for continuously shaping model behavior",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 4320,
        "length": 260,
        "line_number": null
      },
      "visual": "illustration",
      "created_at": "2026-01-07T18:13:35.057604",
      "metadata": {},
      "description": "A potter shaping clay on a spinning wheel, where small adjustments dramatically change the vessel\u2019s shape, illustrating how prompt and meta-prompt tweaks mold probabilistic model behavior into the desired customer experience.",
      "visual_category": "metaphor",
      "related_atom": "concept_005"
    },
    {
      "id": "concept_006",
      "rank": 14,
      "state": "draft",
      "abstract": "Teams AI Workbench and CMDAI eval platform democratize AI debugging for PMs",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 5040,
        "length": 720,
        "line_number": null
      },
      "visual": "architecture",
      "created_at": "2026-01-07T18:13:35.057688",
      "metadata": {},
      "text": "The Teams AI Workbench system and CMDAI evaluation platform aim to let PMs directly change prompts, run evals, and see scores (e.g., Prism) in under 30 seconds, without heavy engineering dependencies, enabling all disciplines to directly impact AI outcomes.",
      "concept_type": "solution",
      "supporting_facts": [
        "fact_004",
        "fact_005"
      ]
    },
    {
      "id": "fact_004",
      "rank": 15,
      "state": "draft",
      "abstract": "Lon\u2019s AI Workbench vision: prompt change to eval in <30 seconds",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 5400,
        "length": 260,
        "line_number": null
      },
      "visual": "big-number",
      "created_at": "2026-01-07T18:13:35.057700",
      "metadata": {},
      "text": "Lon\u2019s Teams AI Workbench vision includes the goal of \"prompt change to eval in less than 30 seconds,\" enabling rapid iteration on prompts and evaluations by PMs and other disciplines.",
      "category": "definition"
    },
    {
      "id": "tension_004",
      "rank": 16,
      "state": "draft",
      "abstract": "Current PMs can\u2019t easily debug bad AI summaries like round-robin meetings",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 5760,
        "length": 720,
        "line_number": null
      },
      "visual": "storyboard",
      "created_at": "2026-01-07T18:13:35.057745",
      "metadata": {},
      "text": "When Facilitator produced a poor summary of a round-robin meeting, the PM had no direct way to inspect the LLM grader\u2019s score or adjust the prompt, and had to manually craft a better summary via Catalyst and then go through engineering to change behavior.",
      "tension_type": "tooling-gap",
      "resolution_hint": "Give PMs direct access to system prompts, eval tools, and real meeting data so they can iterate on quality without engineering bottlenecks."
    },
    {
      "id": "concept_007",
      "rank": 17,
      "state": "draft",
      "abstract": "Adopt OpenAI-style \u201cninja\u201d online evals with strategic customers",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 6360,
        "length": 420,
        "line_number": null
      },
      "visual": "flow",
      "created_at": "2026-01-07T18:13:35.057757",
      "metadata": {},
      "text": "The team wants to emulate OpenAI\u2019s practice of working with select strategic customers who can send \"online eyes-on\" data when issues occur, enabling continuous post-GA evaluation and iteration based on real-world usage.",
      "concept_type": "method",
      "supporting_facts": []
    },
    {
      "id": "fact_005",
      "rank": 18,
      "state": "draft",
      "abstract": "AI and fundamentals are priority one and two; everything else is priority ten",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 2460,
        "length": 520,
        "line_number": null
      },
      "visual": "priority-ladder",
      "created_at": "2026-01-07T18:13:35.057768",
      "metadata": {},
      "text": "The org is moving into a world where AI and fundamentals (e.g., AV quality, reliability) are priority one and two, and everything else is effectively priority ten; without strong fundamentals, there is no right to talk about AI.",
      "category": "principle"
    },
    {
      "id": "tension_005",
      "rank": 19,
      "state": "draft",
      "abstract": "Upgrading to GPT\u20115.1 deep reasoning caused unacceptable latency in meetings",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 6840,
        "length": 420,
        "line_number": null
      },
      "visual": "before-after",
      "created_at": "2026-01-07T18:13:35.057783",
      "metadata": {},
      "text": "Switching to GPT\u20115.1 with deep reasoning for Catalyst stage two added roughly 9\u201312 seconds to P75 latency, making meeting recaps too slow and forcing a hold on shipping that configuration.",
      "tension_type": "performance-trade-off",
      "resolution_hint": "Control when deep reasoning is used and tune models to balance quality with strict latency budgets for in-meeting scenarios."
    },
    {
      "id": "stat_001",
      "rank": 20,
      "state": "draft",
      "abstract": "Deep reasoning added ~9\u201312 seconds to P75 latency for Catalyst",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 6960,
        "length": 260,
        "line_number": null
      },
      "visual": "big-number",
      "created_at": "2026-01-07T18:13:35.057807",
      "metadata": {},
      "value": "9\u201312 seconds",
      "label": "Additional P75 latency from GPT\u20115.1 deep reasoning",
      "context": "Latency impact when MSAI turned on GPT\u20115.1 deep reasoning by default for Catalyst stage two, making recap responses too slow in meetings."
    },
    {
      "id": "concept_008",
      "rank": 21,
      "state": "draft",
      "abstract": "Eval must move from end-of-cycle QA to front-and-center design tool",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 7320,
        "length": 640,
        "line_number": null
      },
      "visual": "flow",
      "created_at": "2026-01-07T18:13:35.057889",
      "metadata": {},
      "text": "Evaluation can no longer be a final QA step; PMs must define eval categories, golden datasets, and LLM judges at the very beginning of the product lifecycle and treat evals as their primary design tool, more central than Figma or traditional specs.",
      "concept_type": "insight",
      "supporting_facts": [
        "fact_011"
      ]
    },
    {
      "id": "fact_011",
      "rank": 22,
      "state": "draft",
      "abstract": "AIRR (AI Readiness Review) will complement UXRS and ERS",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 8040,
        "length": 360,
        "line_number": null
      },
      "visual": "checklist",
      "created_at": "2026-01-07T18:13:35.057900",
      "metadata": {},
      "text": "In addition to UXRS and ERS, the org will introduce AI Readiness Reviews (AIRR), where PMs must answer how they will approach evals, golden datasets, and engineering integration for AI features before shipping.",
      "category": "process"
    },
    {
      "id": "visual_002",
      "rank": 23,
      "state": "draft",
      "abstract": "Surfing metaphor: model as wave, eval as surfboard, UI as foam",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 8280,
        "length": 520,
        "line_number": null
      },
      "visual": "illustration",
      "created_at": "2026-01-07T18:13:35.057913",
      "metadata": {},
      "description": "A surfer riding a powerful wave at night with only a surfboard and faint light, where the wave represents the unpredictable AI model, the surfboard represents evals, and the white foam on top represents UI that can\u2019t save you from a bad wave.",
      "visual_category": "metaphor",
      "related_atom": "concept_008"
    },
    {
      "id": "tension_006",
      "rank": 24,
      "state": "draft",
      "abstract": "Teams PM org is behind other orgs in becoming true AI PMs",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 9000,
        "length": 520,
        "line_number": null
      },
      "visual": "none",
      "created_at": "2026-01-07T18:13:35.057925",
      "metadata": {},
      "text": "Cathy notes that while they once felt like leading-edge AI PMs, conversations at Blend revealed that many other organizations have already converted PM practices to start from customer thinking, evaluation mastery, and deep model understanding, leaving this team behind.",
      "tension_type": "competitive-gap",
      "resolution_hint": "Accelerate AI PM upskilling, embed eval and model literacy into specs, and adopt practices seen in more advanced orgs."
    },
    {
      "id": "concept_009",
      "rank": 25,
      "state": "draft",
      "abstract": "AI mode / ephemeral transcript switch to unlock recap without explicit recording",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 10560,
        "length": 720,
        "line_number": null
      },
      "visual": "diagram",
      "created_at": "2026-01-07T18:13:35.057937",
      "metadata": {},
      "text": "To support recap in Copilot-only mode without explicit transcription or recording buttons, Han-yi suggests an \"AI mode\" toggle (similar to Office\u2019s AutoSave) that implicitly turns on ephemeral transcription and enables recap, Facilitator, and other AI features.",
      "concept_type": "solution",
      "supporting_facts": []
    },
    {
      "id": "concept_010",
      "rank": 26,
      "state": "draft",
      "abstract": "Video recap needs clear eval definition of what counts as a highlight",
      "source_ref": {
        "source_id": "85e12575684e3267",
        "file_path": "/Users/zhang11/Work/gggg/output/ui_run_20260108_021126/sources/transcript.vtt.txt",
        "offset": 11880,
        "length": 520,
        "line_number": null
      },
      "visual": "storyboard",
      "created_at": "2026-01-07T18:13:35.057948",
      "metadata": {},
      "text": "For future video recap experiences, the team must define what constitutes a highlight (e.g., leader quotes, key decisions, insights) and build evals and golden datasets around that, potentially using LLMs as brainstorming partners to explore formats like soundbites vs summaries.",
      "concept_type": "method",
      "supporting_facts": [
        "concept_004"
      ]
    }
  ]
}
**Instructions**: 

**RULES**:
1. Follow each slide's `visual_design` field for layout and content approach
2. Follow each slide's `density` field (sparse=2-3 blocks, moderate=3-4, dense=5+)
3. Each slide tells its own story from the `story` field
4. Use Diagram ONLY when visual_design explicitly mentions it
5. ≥4 different layouts across deck, no consecutive repeats
6. Each <Slide> has id, rank, story, atoms attributes
7. Combine text AND visual on each slide (one leads, other supports)
8. Fill space appropriate to density (sparse≠empty)

Generate MDX slides wrapped in <Slide> elements.