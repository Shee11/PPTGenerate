/**
 * LayoutStacked Component (L1 Layout)
 * 
 * Single-column layout for dense text content.
 * Content is distributed vertically across the page.
 * 
 * Usage:
 * ```mdx
 * <LayoutStacked>
 *   <Heading level={2}>Title</Heading>
 *   <Text>Paragraph 1...</Text>
 *   <SmartList items={[...]} />
 *   <Text>Paragraph 2...</Text>
 *   <Callout intent="info">Important note</Callout>
 * </LayoutStacked>
 * ```
 */

import React, { type ReactNode } from 'react';
import type { ThemeName, VibeLevel } from '@/utils/types';

// =============================================================================
// Types
// =============================================================================

export interface LayoutStackedProps {
  children: ReactNode;
  /** Text alignment */
  align?: 'left' | 'center';
  /** Theme override */
  theme?: ThemeName;
  /** Vibe modifier */
  vibe?: VibeLevel;
}

// =============================================================================
// Main Component
// =============================================================================

/**
 * LayoutStacked Component
 * 
 * Renders a single-column layout with content distributed vertically.
 * Best for text-heavy pages with multiple paragraphs and sections.
 * 
 * @param children - Content elements (headings, text, lists, callouts)
 * @param align - Text alignment ('left' or 'center')
 * @param theme - Optional theme override
 * @param vibe - Optional vibe modifier
 */
export function LayoutStacked({
  children,
  align = 'left',
  theme,
  vibe,
}: LayoutStackedProps): JSX.Element {
  const alignClass = align === 'center' ? 'align-center' : 'align-left';
  
  return (
    <div
      className={`layout-stacked ${alignClass}`}
      data-layout="stacked"
      data-align={align}
      data-theme={theme}
      data-vibe={vibe}
    >
      {children}
    </div>
  );
}

LayoutStacked.displayName = 'LayoutStacked';
