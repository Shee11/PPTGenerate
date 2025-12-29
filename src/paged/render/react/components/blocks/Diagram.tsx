/**
 * Diagram Component (L2 Block)
 * 
 * Renders Mermaid diagrams for processes, architectures, timelines, etc.
 * Uses client-side rendering with mermaid.js
 * 
 * Usage:
 * ```mdx
 * <Diagram
 *   id="flow_001"
 *   type="flowchart"
 *   title="Data Pipeline"
 *   code={`
 *     graph LR
 *       A[Raw Data] --> B[Process]
 *       B --> C[Clean Data]
 *   `}
 * />
 * ```
 */

'use client';

import React, { useEffect, useRef, useState } from 'react';

// =============================================================================
// Types
// =============================================================================

export type DiagramType = 
  | 'flowchart'    // Process flows, workflows
  | 'sequence'     // Sequence diagrams  
  | 'class'        // Class diagrams
  | 'state'        // State machines
  | 'er'           // Entity relationship
  | 'gantt'        // Timeline/gantt charts
  | 'pie'          // Pie charts
  | 'journey'      // User journeys
  | 'mindmap'      // Mind maps
  | 'timeline';    // Timelines

export interface DiagramProps {
  /** Unique identifier for the diagram */
  id: string;
  /** Type of diagram */
  type?: DiagramType;
  /** Mermaid code defining the diagram */
  code: string;
  /** Optional title */
  title?: string;
  /** Optional caption */
  caption?: string;
  /** Theme: 'default' | 'dark' | 'forest' | 'neutral' */
  theme?: 'default' | 'dark' | 'forest' | 'neutral';
}

// =============================================================================
// Component
// =============================================================================

/**
 * Diagram Component
 * 
 * Renders Mermaid diagrams with proper styling.
 * Falls back to code display if mermaid is not available.
 */
export function Diagram({
  id,
  type = 'flowchart',
  code,
  title,
  caption,
  theme = 'default',
}: DiagramProps): JSX.Element {
  const containerRef = useRef<HTMLDivElement>(null);
  const [rendered, setRendered] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [svg, setSvg] = useState<string>('');

  useEffect(() => {
    const renderDiagram = async () => {
      try {
        // Dynamic import of mermaid
        const mermaid = (await import('mermaid')).default;
        
        // Initialize mermaid with theme
        mermaid.initialize({
          startOnLoad: false,
          theme: 'base',
          securityLevel: 'loose',
          fontFamily: 'system-ui, -apple-system, sans-serif',
          fontSize: 14,
          themeVariables: {
            primaryColor: '#f0f4ff',
            primaryTextColor: '#1e293b',
            primaryBorderColor: '#7c3aed',
            lineColor: '#7c3aed',
            secondaryColor: '#f8fafc',
            tertiaryColor: '#e2e8f0',
            background: '#ffffff',
            mainBkg: '#f0f4ff',
            nodeBorder: '#7c3aed',
            clusterBkg: '#f8fafc',
            titleColor: '#1e293b',
            edgeLabelBackground: '#ffffff',
          },
          flowchart: {
            curve: 'basis',
            padding: 20,
            nodeSpacing: 50,
            rankSpacing: 50,
            htmlLabels: true,
            useMaxWidth: true,
          },
        });

        // Clean code - ensure proper line breaks and sanitize special characters
        let cleanCode = code.trim();
        
        // Replace problematic Unicode characters that break Mermaid parsing
        cleanCode = cleanCode
          .replace(/[\u2010-\u2015]/g, '-')  // Replace various dashes with regular hyphen
          .replace(/[\u2018\u2019]/g, "'")   // Replace smart single quotes
          .replace(/[\u201C\u201D]/g, '"')   // Replace smart double quotes
          .replace(/\u2026/g, '...')         // Replace ellipsis
          .replace(/\u00A0/g, ' ')           // Replace non-breaking space
          .replace(/&/g, ' and ')            // Replace ampersand (breaks Mermaid parsing)
          .replace(/\+\+/g, ' Plus');        // Replace ++ (breaks Mermaid parsing)
        
        // Escape parentheses inside square bracket node labels to prevent Mermaid parsing errors
        // Mermaid interprets (text) as a stadium shape, so we need to escape them
        cleanCode = cleanCode.replace(/\[([^\]]*)\]/g, (match, content) => {
          // Replace parentheses with HTML entities inside node labels
          const escapedContent = content
            .replace(/\(/g, '#40;')
            .replace(/\)/g, '#41;');
          return `[${escapedContent}]`;
        });
        
        // Generate unique ID for this render
        const renderId = `mermaid-${id}-${Date.now()}`;
        
        // Render the diagram
        const { svg: renderedSvg } = await mermaid.render(renderId, cleanCode);
        setSvg(renderedSvg);
        setRendered(true);
        setError(null);
      } catch (err) {
        console.error('Mermaid render error:', err);
        setError(err instanceof Error ? err.message : 'Failed to render diagram');
        setRendered(false);
      }
    };

    renderDiagram();
  }, [code, id, theme]);

  return (
    <div className="diagram-block" id={id} data-diagram-type={type}>
      {title && (
        <div className="diagram-title">{title}</div>
      )}
      
      <div 
        ref={containerRef}
        className="diagram-container"
      >
        {error ? (
          <div className="diagram-error">
            <div className="diagram-error-message">Diagram render error</div>
            <pre className="diagram-code">{code}</pre>
          </div>
        ) : rendered ? (
          <div 
            className="diagram-svg"
            dangerouslySetInnerHTML={{ __html: svg }}
          />
        ) : (
          <div className="diagram-loading">
            <div className="diagram-spinner" />
            <span>Rendering diagram...</span>
          </div>
        )}
      </div>
      
      {caption && (
        <div className="diagram-caption">{caption}</div>
      )}
    </div>
  );
}

// =============================================================================
// Convenience Components for Common Patterns
// =============================================================================

export interface FlowchartProps {
  id: string;
  title?: string;
  steps: Array<{
    id: string;
    label: string;
  }>;
  direction?: 'LR' | 'TD' | 'RL' | 'BT';
}

/**
 * Flowchart - Simplified flowchart generation
 */
export function Flowchart({
  id,
  title,
  steps,
  direction = 'LR',
}: FlowchartProps): JSX.Element {
  // Generate mermaid code from steps
  const nodes = steps.map(s => `${s.id}[${s.label}]`).join('\n    ');
  const edges = steps.slice(0, -1).map((s, i) => 
    `${s.id} --> ${steps[i + 1].id}`
  ).join('\n    ');
  
  const code = `graph ${direction}
    ${nodes}
    ${edges}`;

  return (
    <Diagram
      id={id}
      type="flowchart"
      title={title}
      code={code}
    />
  );
}

export interface ProcessDiagramProps {
  id: string;
  title?: string;
  input: string;
  output: string;
  steps: string[];
}

/**
 * ProcessDiagram - Input → Steps → Output pattern
 */
export function ProcessDiagram({
  id,
  title,
  input,
  output,
  steps,
}: ProcessDiagramProps): JSX.Element {
  const stepNodes = steps.map((s, i) => `S${i}[${s}]`).join('\n    ');
  const stepEdges = steps.length > 0 
    ? `IN --> S0\n    ` + steps.slice(0, -1).map((_, i) => `S${i} --> S${i + 1}`).join('\n    ') + `\n    S${steps.length - 1} --> OUT`
    : 'IN --> OUT';
  
  const code = `graph LR
    IN([${input}])
    ${stepNodes}
    OUT([${output}])
    ${stepEdges}`;

  return (
    <Diagram
      id={id}
      type="flowchart"
      title={title}
      code={code}
    />
  );
}

// =============================================================================
// Exports
// =============================================================================

export default Diagram;
