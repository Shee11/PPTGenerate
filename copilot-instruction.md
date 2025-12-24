# Copilot Instructions

## Python Environment

Always use `.venv\Scripts\python.exe` instead of `python` when running Python commands:

```powershell
.venv\Scripts\python.exe -m cli.uce_render ...
```

## HTTP Server for Slidev Viewing

When testing Slidev output:
1. **Do NOT start a new HTTP server** - assume one is already running on port 8080
2. Server typically serves from `output/<project>/dist`
3. If no server is running, user will start it manually

## Chrome MCP for Web Testing

When verifying rendered slides or web pages:
1. **Always open the page first** using `mcp_io_github_chr_new_page` before taking snapshots
2. Use `mcp_io_github_chr_take_snapshot` to capture the page state
3. Use `mcp_io_github_chr_list_pages` to see open pages
4. Do NOT use `open_simple_browser` - use Chrome MCP tools instead

Example flow:
```
1. mcp_io_github_chr_new_page with url http://localhost:8080/
2. mcp_io_github_chr_take_snapshot to verify content
```

## CLI E2E Test Command

When asked to "run e2e cli" or "test e2e", execute this command:

```powershell
.venv\Scripts\python.exe -m cli.uce_render --source data/context/career_talk.txt --user-instruction "Generate slides, target audience is entry, mid level devs" --output examples/career_talk_e2e.html --verbose
```

This command:
- Uses the career talk source file
- Targets entry/mid-level developers
- Generates slides with full LLM-based content generation
- Outputs to examples directory
- Shows verbose logging for debugging

## Stage-based Pipeline Command

For todo-based pipeline with stages:

```powershell
.venv\Scripts\python.exe -m cli --source data/context/career_talk.txt --user-instruction "Create 5 slides with dark neon theme" --stage render --output output/test_neon --verbose
```

Output structure:
- `output/<name>/slides.md` - Slidev markdown source
- `output/<name>/slides.json` - Raw slide data for debugging
- `output/<name>/dist/` - Built Slidev HTML (serve via HTTP)

## Re-export with Different Project Theme

To re-export an existing slide with a different project theme (e.g., cyberpunk, duolingo):

1. **Add/update `project` field** at the top of `state.json`:
   ```json
   {
     "project": "cyberpunk",
     "todos": { ... }
   }
   ```

2. **Override todos to keep only export** - remove all other todos and keep only export with no dependencies:
   ```json
   {
     "project": "cyberpunk",
     "todos": {
       "todos": [
         {
           "id": "export",
           "type": "export",
           "status": "pending",
           "params": {
             "layout_engine": "slidev",
             "output_format": "html",
             "output_path": null
           },
           "created_at": "2025-12-24T08:20:15.103666",
           "started_at": null,
           "completed_at": null,
           "error": null,
           "depends_on": []
         }
       ]
     },
     "source": { ... }
   }
   ```

3. **Run the CLI**:
   ```powershell
   .venv\Scripts\python.exe -m cli.uce_render --state output/<slide_folder>/state.json --output output/<slide_folder>
   ```

Available project themes:
- `slidev` (default) - Professional business styling
- `duolingo` - Playful Duolingo-style with bright colors
- `cyberpunk` - Futuristic neon aesthetic with glows and HUD frames
