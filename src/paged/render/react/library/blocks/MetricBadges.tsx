/**
 * MetricBadges Component (L2 Block)
 * 
 * Compact badge array for displaying many small metrics.
 * Shows metrics as pill-shaped badges with icons.
 * 
 * Usage:
 * ```mdx
 * <MetricBadges 
 *   badges={[
 *     { icon: "🌐", value: "9", label: "Languages" },
 *     { icon: "📍", value: "20", label: "Regions" },
 *     { icon: "✅", value: "99%", label: "Accuracy" }
 *   ]}
 * />
 * ```
 */

import React from 'react';

// =============================================================================
// Types
// =============================================================================

export interface BadgeItem {
  /** Icon (emoji or icon name) */
  icon?: string;
  /** Badge value */
  value: string;
  /** Badge label */
  label: string;
}

export interface MetricBadgesProps {
  /** Array of badges to display */
  badges: BadgeItem[];
}

// =============================================================================
// Styles
// =============================================================================

const styles = {
  container: {
    display: 'flex',
    flexWrap: 'wrap' as const,
    gap: '10px',
    margin: '8px 0',
  },
  badge: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '6px',
    padding: '8px 14px',
    background: 'var(--surface)',
    borderRadius: '20px',
    border: '1px solid rgba(255,255,255,0.1)',
    fontSize: '14px',
  },
  icon: {
    fontSize: '14px',
    opacity: 0.8,
  },
  label: {
    color: 'var(--muted)',
  },
  value: {
    fontWeight: 700,
    color: 'var(--accent)',
  },
};

// =============================================================================
// Component
// =============================================================================

export function MetricBadges({ badges }: MetricBadgesProps): JSX.Element {
  return (
    <div className="metric-badges" style={styles.container}>
      {badges.map((badge, index) => (
        <div key={index} className="metric-badge" style={styles.badge}>
          {badge.icon && (
            <span className="badge-icon" style={styles.icon} aria-hidden="true">
              {badge.icon}
            </span>
          )}
          <span className="badge-label" style={styles.label}>
            {badge.label}
          </span>
          <span className="badge-value" style={styles.value}>
            {badge.value}
          </span>
        </div>
      ))}
    </div>
  );
}

export default MetricBadges;
