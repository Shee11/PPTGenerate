from graphviz import Digraph
import os

def generate_diagram():
    dot = Digraph(comment='UCE Pipeline Data Flow', format='jpg')
    dot.attr(rankdir='TB')  # Top to Bottom for clearer sequential flow
    dot.attr(dpi='300')     # Higher resolution
    
    # Defaults
    dot.attr('node', fontname='Arial', fontsize='12')
    dot.attr('edge', fontname='Arial', fontsize='10')

    # Groups/Subgraphs to organize the State vs Tools
    
    # Inputs
    with dot.subgraph(name='cluster_inputs') as c:
        c.attr(label='Inputs', color='lightgrey')
        c.node('User', 'User Instruction', shape='ellipse', fillcolor='white', style='filled')
        c.node('Source', 'Source Text', shape='note', fillcolor='white', style='filled')

    # Merged Steps (Process + Output State)
    dot.attr('node', shape='box', style='filled', fillcolor='#E6F3FF')
    
    dot.node('Step1', '1. Constitution\n\n[Output]\nRules, Tone, Exclusions')
    dot.node('Step2', '2. Atoms\n\n[Output]\nFacts, Quotes, Contexts, Visuals')
    dot.node('Step3', '3. Theme\n\n[Output]\nColors, Fonts, ID')
    dot.node('Step4', '4. Story\n\n[Output]\nDraft Slides\n(Story, Visual Design, Atom Refs)')
    dot.node('Step5', '5. Content\n\n[Output]\nActive Slides\n(Layouts & Components)')
    dot.node('Step6', '6. Export\n\n[Action]\nRender & Build')
    
    dot.node('FileMDX', 'Output: slides.mdx', shape='note', fillcolor='white', style='filled')

    # Connections
    
    # 1. Constitution
    dot.edge('User', 'Step1')

    # 2. Atoms
    dot.edge('Source', 'Step2')
    dot.edge('Step1', 'Step2', label='Guidance')

    # 3. Theme
    dot.edge('Step1', 'Step3', label='Vibe')

    # 4. Story
    dot.edge('Step2', 'Step4')
    dot.edge('Step1', 'Step4', label='Constraints')

    # 5. Content
    dot.edge('Step4', 'Step5')
    dot.edge('Step2', 'Step5', label='Details')
    dot.edge('Step3', 'Step5')
    dot.edge('Step1', 'Step5', label='Prefs')

    # Step 6
    dot.edge('Step5', 'Step6')
    dot.edge('Step3', 'Step6')
    dot.edge('Step6', 'FileMDX')
    
    # Output file
    dot.node('FileMDX', 'Output: slides.mdx', shape='note', fillcolor='white', style='filled')

    try:
        # Save source first
        output_path = 'pipeline_flow'
        dot.save(output_path + '.dot')
        print(f"DOT source saved to {output_path}.dot")
        
        # Try to render
        dot.render(output_path, view=False)
        print(f"Diagram saved to {output_path}.jpg")
    except Exception as e:
        print(f"\nWarning: Could not render image (Graphviz binary missing?).")
        print(f"You can view the diagram by pasting the content of {output_path}.dot into https://dreampuf.github.io/GraphvizOnline/")
        print("\nHere is the DOT source for convenience:\n")
        print(dot.source)

if __name__ == "__main__":
    generate_diagram()
