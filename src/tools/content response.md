```mdx
<Slide id="slide_01" rank={1} story="cover: set the transformation thesis upfront" content="cover">
  <LayoutCover theme="dark">
    <Heading level={1}>Building AI-First PM Excellence in CMD</Heading>
    <Text variant="lead">From UI craft to model-centered, eval-first product making</Text>
    <QuoteBlock id="quote_001" author="Han-yi Shaw">
      Discipline Excellence &amp; Org Transformation — CMD / Teams · 2024-11-19
    </QuoteBlock>
  </LayoutCover>
</Slide>

<Slide id="slide_02" rank={2} story="Situation: CMD already powers high-impact AI experiences" content="Situation">
  <LayoutSplit ratio="1:1">
    <Left>
      <Heading level={2}>CMD already powers Microsoft’s biggest AI wins</Heading>
      <Text variant="lead">
        Recap, Teams Copilot, and Facilitator are core to Copilot business impact.
      </Text>
      <SmartList
        id="list_002_impact"
        items={[
          "Teams Recap is a major hit and a top Copilot business driver.",
          "Teams Copilot and Facilitator are central to intelligent meetings.",
          "CMD PMs shape recap, loop notes, and summaries customers use daily.",
          "Our work sits at the intersection of M365, Copilot, and Teams."
        ]}
      />
      <Callout intent="info" title="Strategic position today">
        Blend feedback consistently cites Teams AI experiences as exemplars of Microsoft’s AI story.
      </Callout>
    </Left>
    <Right>
      <Heading level={2}>Key AI assets we own</Heading>
      <MetricGroup id="metrics_002_assets" cols={2}>
        <Metric value="Recap" label="Hit Copilot feature" />
        <Metric value="Teams Copilot" label="Core meetings assistant" />
        <Metric value="Facilitator" label="Loop notes &amp; guidance" />
        <Metric value="Daily use" label="High-frequency AI scenarios" />
      </MetricGroup>
      <Text variant="body">
        How we evolve our PM craft will shape how customers experience Microsoft AI in meetings.
      </Text>
      <Text variant="caption">Speaker intent: anchor both pride and urgency.</Text>
    </Right>
  </LayoutSplit>
</Slide>

<Slide id="slide_03" rank={3} story="Complication: our PM craft and AI experiences are not yet AI-native" content="Complication">
  <LayoutDashboard>
    <Header>
      <Heading level={2}>Legacy PM habits and fragmented AI UX are eroding our edge</Heading>
    </Header>
    <Main>
      <Text variant="lead">
        We still operate like 2024 UI-first PMs while frontier teams run eval-first AI orgs.
      </Text>
      <SmartList
        id="list_003_gaps"
        items={[
          "Specs and docs are light on evals, prompts, rubrics, and model behavior.",
          "Few PMs can explain what model-first development means day-to-day.",
          "We lack fluency in eval design, golden datasets, and AI tradeoffs.",
          "Users see four different recap experiences with limited coherence."
        ]}
      />
      <TableData
        id="table_003_contrast"
        headers={["Today", "Needed"]}
        rows={[
          ["UI-first specs, late evals", "Eval-first, model-centered specs"],
          ["Feature lists and surfaces", "Scenario outcomes and model behavior"],
          ["Ad-hoc failures (e.g., round-robin)", "Defined eval scenarios with golden summaries"],
          ["Fragmented recap experiences", "Single coherent, personalized recap system"]
        ]}
      />
    </Main>
    <Sidebar>
      <Callout intent="warning" title="Constructive anxiety">
        Our current ways of working will not sustain our lead against eval-native AI teams.
      </Callout>
    </Sidebar>
  </LayoutDashboard>
</Slide>

<Slide id="slide_04" rank={4} story="Question + Answer (answer-first): define the new operating model we need" content="Question">
  <LayoutStacked>
    <Heading level={2}>We must become AI-first, eval-led PMs or we will fall behind</Heading>
    <Text variant="lead">
      CMD’s craft must shift from pixels and features to models, evals, and outcomes.
    </Text>

    <Heading level={3}>Our answer in one line</Heading>
    <Text>
      We will institutionalize an AI-first PM operating model built on eval-first development,
      shared AI tooling, and coherent AI experiences.
    </Text>

    <InventComponent
      id="three-pillars-diagram"
      name="ThreePillarsStrip"
      intent="Show three reinforcing pillars of the new AI-first PM operating model"
      essential_text="Pillar 1: AI-native PM skills; Pillar 2: CMD AI Workbench; Pillar 3: Coherent AI meeting experiences (SoCS-led)"
      visual_metaphor="Horizontal three-pillar bar or columns supporting a shared 'AI-first PM' roof"
      min_font_size="18px"
      space_allocation="Center of stacked layout, width-full, about one-third of slide height"
      notes="Each pillar labeled with a short title and 1-line descriptor; high contrast, simple shapes."
    />

    <Callout intent="info" title="Call to action">
      We are changing the PM operating model and expectations, not just adding tools.
    </Callout>
  </LayoutStacked>
</Slide>

<Slide id="slide_05" rank={5} story="Answer: define AI-first PM expectations and behaviors" content="Answer">
  <LayoutDashboard>
    <Header>
      <Heading level={2}>AI-first PMs treat the model and evals as primary design tools</Heading>
    </Header>
    <Main>
      <Text variant="lead">
        Specs and mocks remain necessary, but model behavior and eval quality become the focal point.
      </Text>
      <InventComponent
        id="pm-mindset-matrix"
        name="PmMindsetMatrix2x2"
        intent="Contrast old UI-first PM behavior with AI-first PM behavior across Design vs Eval axes"
        essential_text="Axes: Design focus vs Eval focus; Quadrants: Old UI-first, Old eval-late, AI-first design-led evals, AI-first eval-led design"
        visual_metaphor="2x2 matrix with the top-right quadrant highlighted as the AI-first target state"
        min_font_size="16px"
        space_allocation="Main area center, occupying roughly half of the main column height"
        notes="Include short labels like 'Pixels & features', 'Model & outcomes', 'Late testing', 'Eval-first'. Highlight AI-first quadrant."
      />
      <SmartList
        id="list_005_practice"
        items={[
          "Users will rate us on model output quality, not UI polish.",
          "The model output is the product; UI is the foam, not the wave.",
          "Our job is to mold probabilistic models into predictable experiences."
        ]}
      />
    </Main>
    <Sidebar>
      <Heading level={3}>What “AI-first PM” means</Heading>
      <SmartList
        id="list_005_expectations"
        items={[
          "Define golden datasets and rubrics for 5-star outcomes.",
          "Author and refine prompts and meta-prompts with intent.",
          "Design evals upfront and iterate primarily through them.",
          "Understand model limits and latency/quality tradeoffs."
        ]}
      />
      <Callout intent="success" title="New expectations and timelines">
        Within 1 month: every PM can answer how to be a great eval writer and grader. Within 6 months: more time in models/evals, less TPM-style work.
      </Callout>
    </Sidebar>
  </LayoutDashboard>
</Slide>

<Slide id="slide_06" rank={6} story="Answer: introduce the CMD AI Workbench and eval platform as enablers" content="Answer">
  <LayoutSplit ratio="1:1">
    <Left>
      <Heading level={2}>A shared CMD AI Workbench lets PMs mold model behavior</Heading>
      <Text variant="lead">
        Vision: prompt changes to eval in &lt;30 seconds, without engineering in the loop.
      </Text>
      <ProcessStrip
        id="process_006_workbench_flow"
        items={[
          { label: "Select scenario", status: "done" },
          { label: "Edit prompt &amp; rubric", status: "active" },
          { label: "Run evals", status: "pending" }
        ]}
      />
      <ProcessStrip
        id="process_006_workbench_flow_2"
        items={[
          { label: "Review scores", status: "pending" },
          { label: "Ship &amp; monitor", status: "pending" }
        ]}
      />
      <Text variant="caption">
        Simple prompt→eval loop: fast, PM-led, and grounded in real meetings.
      </Text>
    </Left>
    <Right>
      <Heading level={2}>What the Teams AI Workbench enables</Heading>
      <SmartList
        id="list_006_enablers"
        items={[
          "Prompt changes propagate to eval runs in under 30 seconds.",
          "PMs see Prism scores and eval metrics directly.",
          "Scenario-level testing using real meetings, not just static transcripts.",
          "Generate and evaluate flows integrated with full Teams business logic."
        ]}
      />
      <Heading level={3}>From prototypes to a CMD eval platform</Heading>
      <SmartList
        id="list_006_platform"
        items={[
          "Gradio tools proved value but lacked real app logic and meeting selection.",
          "Podcast customization UI now runs on full Teams logic with evals wired in.",
          "Next: extend into a CMDAI evaluation platform for all intelligent meeting features."
        ]}
      />
      <Callout intent="info" title="Online eyes-on">
        Embed OpenAI-style “ninja” feedback loops so strategic customers feed real issues into our eval pipeline.
      </Callout>
    </Right>
  </LayoutSplit>
</Slide>

<Slide id="slide_07" rank={7} story="Answer: focus on coherent, personalized AI meeting experiences" content="Answer">
  <LayoutStacked>
    <Heading level={2}>We will unify recap and notes into a coherent AI meeting experience</Heading>
    <Text variant="lead">
      Consolidating notes and recap logic in SoCS to drive coherence and personalization.
    </Text>

    <Heading level={3}>From fragmented to coherent</Heading>
    <TableData
      id="table_007_today_target"
      headers={["Today: fragmented", "Target: coherent &amp; personalized"]}
      rows={[
        ["Multiple recap flavors across surfaces", "Single recap experience across surfaces"],
        ["Users unsure which recap to trust", "Clear meeting-type detection and expectations"],
        ["In- and post-meeting not aligned", "Shared transcription and enrichment across flows"],
        ["Notes logic scattered across teams", "SoCS owns unified notes and recap storage"]
      ]}
    />

    <Heading level={3}>Consolidation and accountability</Heading>
    <SmartList
      id="list_007_consolidation"
      items={[
        "Move notes, conversion, and storage responsibilities into SoCS.",
        "Enable user-tailorable recaps (brevity vs detail, workflow fit).",
        "Hold PMs accountable for resolving cross-surface inconsistencies."
      ]}
    />
    <Callout intent="success">
      SoCS becomes the backbone for coherent, personalized AI meeting experiences.
    </Callout>
  </LayoutStacked>
</Slide>

<Slide id="slide_08" rank={8} story="Answer: institutionalize eval-first rituals and AIRR governance" content="Answer">
  <LayoutDashboard>
    <Header>
      <Heading level={2}>Eval-first development and AIRR will govern AI feature readiness</Heading>
    </Header>
    <Main>
      <Text variant="lead">
        AIRR adds AI-specific gates alongside UXRS and ERs to ensure quality and reliability.
      </Text>
      <InventComponent
        id="harvey-balls-readiness"
        name="HarveyBallsReadinessTable"
        intent="Show readiness across Skills, Evals, Tooling, and Post-GA loops using Harvey Balls"
        essential_text="Rows: Skills, Evals, Tooling, Post-GA loops; Columns: Current, Target; Each cell: empty/half/full Harvey ball"
        visual_metaphor="Readiness matrix where fuller Harvey balls indicate higher readiness toward AI-first standards"
        min_font_size="16px"
        space_allocation="Main area center, about half of main column height"
        notes="Label rows clearly; use legend for Harvey ball fill levels; emphasize gaps to close."
      />
      <SmartList
        id="list_008_eval_backbone"
        items={[
          "Define eval categories and rubrics at the start of the lifecycle.",
          "Use golden datasets and LL judges for consistent judgments at scale.",
          "Treat evals as the surfboard on the AI wave—without them, we surf blind."
        ]}
      />
    </Main>
    <Sidebar>
      <Heading level={3}>AI Readiness Review (AIRR)</Heading>
      <SmartList
        id="list_008_airr"
        items={[
          "Focuses on model behavior, eval coverage, and quality thresholds.",
          "Every AI feature must show golden datasets and wired-in eval tools.",
          "Post-GA, tracks online evals and ninja customer feedback loops."
        ]}
      />
      <Callout intent="info" title="Concrete application">
        Round-robin failures and model upgrades become explicit eval scenarios with 5-star benchmarks and latency/quality gates.
      </Callout>
    </Sidebar>
  </LayoutDashboard>
</Slide>

<Slide id="slide_09" rank={9} story="Commit: clarify priorities, risks, and next 6-month outcomes" content="Answer">
  <LayoutSplit ratio="1:1">
    <Left>
      <Heading level={2}>We will reprioritize around AI and fundamentals</Heading>
      <Text variant="lead">
        AI and fundamentals are P1/P2; everything else is P10.
      </Text>
      <ProcessStrip
        id="process_009_roadmap"
        items={[
          { label: "Now", status: "active" },
          { label: "1–3 months", status: "pending" },
          { label: "3–6 months", status: "pending" }
        ]}
      />
      <StepList
        id="steps_009_outcomes"
        items={[
          {
            label: "0–3 months",
            description: "Baseline PM AI fluency, early Workbench, pilot AIRR."
          },
          {
            label: "3–6 months",
            description: "Shift PM time into evals, coherent recap, first full AIRR feature."
          }
        ]}
      />
      <Text variant="caption">
        The roadmap converts strategy into time-bound commitments and tradeoffs.
      </Text>
    </Left>
    <Right>
      <Heading level={2}>Risks and mitigations</Heading>
      <SmartList
        id="list_009_risks"
        items={[
          "Risk: PMs see fundamentals as less important than AI. Mitigation: frame AV quality and reliability as P2 prerequisites for AI.",
          "Risk: Tooling lags intent. Mitigation: treat AI Workbench and CMDAI eval platform as shared infra, not side projects.",
          "Risk: Change fatigue. Mitigation: focus on a few visible wins (e.g., recap) under full eval-first discipline."
        ]}
      />
      <Callout intent="warning">
        We must be explicit about tradeoffs: some non-AI work will slow so AI and fundamentals can move faster.
      </Callout>
    </Right>
  </LayoutSplit>
</Slide>

<Slide id="slide_10" rank={10} story="ending: reinforce the call to action and invite commitment" content="ending">
  <LayoutStacked>
    <Heading level={2}>CMD will lead Microsoft’s next wave of AI product excellence</Heading>
    <Text variant="lead">
      If we master eval-first, model-centered PM, we define the standard for the company.
    </Text>

    <Heading level={3}>What leadership support we need</Heading>
    <SmartList
      id="list_010_support"
      items={[
        "Endorse AI-first PM expectations as baseline and support time for upskilling.",
        "Back CMD AI Workbench and CMDAI eval platform as shared infrastructure.",
        "Hold teams to AIRR standards and coherent AI experience goals, not just feature delivery."
      ]}
    />

    <Callout intent="success" title="Closing thought">
      The teams who master eval-first development will define the next generation of product excellence—let’s ensure CMD is one of them.
    </Callout>
  </LayoutStacked>
</Slide>
```