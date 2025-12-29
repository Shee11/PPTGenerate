import re

mdx = '<SmartList items={["a", "b"]} subtitle="Why this matters" />'
print("MDX:", mdx)

match = re.search(r'<SmartList\s+items=\{(\[.*?\])\}([^/]*?)\s*/>', mdx)
if match:
    items_json = match.group(1)
    extra_props = match.group(2)
    print("items_json:", repr(items_json))
    print("extra_props:", repr(extra_props))
    
    # Fix: Use word boundary or space prefix to match exact prop names
    title_match = re.search(r'(?:^|\s)title="([^"]*)"', extra_props)
    subtitle_match = re.search(r'(?:^|\s)subtitle="([^"]*)"', extra_props)
    print("title_match:", title_match)
    print("subtitle_match:", subtitle_match.group(1) if subtitle_match else None)
else:
    print("No match!")
