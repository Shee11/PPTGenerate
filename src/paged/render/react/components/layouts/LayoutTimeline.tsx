/**
 * LayoutTimeline Component (L1 Layout)
 * 
 * Vertical timeline layout for chronological content.
 * Displays items along a central timeline with alternating positions.
 * 
 * Usage:
 * ```mdx
 * <LayoutTimeline>
 *   <LayoutTimeline.Item year="2020">
 *     <Heading level={3}>Event Title</Heading>
 *     <Text>Event description</Text>
 *   </LayoutTimeline.Item>
 *   <LayoutTimeline.Item year="2021">
 *     <Heading level={3}>Another Event</Heading>
 *     <Text>More details</Text>
 *   </LayoutTimeline.Item>
 * </LayoutTimeline>
 * ```
 */

import React, { type ReactNode } from 'react';
import type { ThemeName, VibeLevel } from '@/utils/types';

// =============================================================================
// Types
// =============================================================================

export interface LayoutTimelineProps {
  children: ReactNode;
  /** Theme override */
  theme?: ThemeName;
  /** Vibe modifier */
  vibe?: VibeLevel;
}

export interface LayoutTimelineItemProps {
  children: ReactNode;
  /** Year or date label */
  year?: string;
  /** Position (auto-alternates by default) */
  position?: 'left' | 'right';
  /** Highlighted item */
  highlighted?: boolean;
}

// =============================================================================
// Sub-Components
// =============================================================================

/**
 * LayoutTimeline.Item Component
 * 
 * Individual item in the timeline.
 */
function TimelineItem({
  children,
  year,
  position,
  highlighted = false,
}: LayoutTimelineItemProps): JSX.Element {
  return (
    <div 
      className={`timeline-item ${highlighted ? 'timeline-item-highlighted' : ''}`}
      data-position={position}
    >
      {year && (
        <div className="timeline-year">{year}</div>
      )}
      <div className="timeline-content">
        {children}
      </div>
    </div>
  );
}

// =============================================================================
// Component
// =============================================================================

/**
 * LayoutTimeline Component
 * 
 * Renders a vertical timeline layout for chronological content.
 * Child items alternate left/right along a central line.
 * 
 * @param children - Timeline items (LayoutTimeline.Item)
 * @param theme - Optional theme override
 * @param vibe - Optional vibe modifier
 */
export function LayoutTimeline({
  children,
  theme,
  vibe,
}: LayoutTimelineProps): JSX.Element {
  return (
    <div 
      className="layout-timeline"
      data-layout="timeline"
      data-theme={theme}
      data-vibe={vibe}
    >
      <div className="timeline-line" />
      <div className="timeline-items">
        {children}
      </div>
    </div>
  );
}

// Attach sub-component
LayoutTimeline.Item = TimelineItem;

// =============================================================================
// Exports
// =============================================================================

export default LayoutTimeline;
