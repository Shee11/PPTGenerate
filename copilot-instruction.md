# Copilot Instructions

## CLI E2E Test Command

When asked to "run e2e cli" or "test e2e", execute this command:

```powershell
python -m cli.uce_render --source data/context/career_talk.txt --user-instruction "Generate slides, target audience is entry, mid level devs" --output examples/career_talk_e2e.html --verbose
```

This command:
- Uses the career talk source file
- Targets entry/mid-level developers
- Generates slides with full LLM-based content generation
- Outputs to examples directory
- Shows verbose logging for debugging
