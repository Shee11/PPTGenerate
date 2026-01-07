/**
 * MetricStrip Component (L2 Block)
 * 
 * Inline horizontal compact metrics row.
 * Shows multiple metrics in a single horizontal strip with icons.
 * 
 * Usage:
 * ```mdx
 * <MetricStrip 
 *   title="Key Stats"
 *   metrics={[
 *     { icon: "📊", value: "99.9%", label: "Uptime" },
 *     { icon: "⚡", value: "10x", label: "Faster" },
 *     { icon: "👥", value: "1M+", label: "Users" }
 *   ]}
 * />
 * ```
 */

import React from 'react';

// =============================================================================
// Types
// =============================================================================

export interface MetricStripItem {
  /** Optional icon (emoji or icon name) */
  icon?: string;
  /** Metric value */
  value: string;
  /** Metric label */
  label: string;
}

export interface MetricStripProps {
  /** Array of metrics to display */
  metrics: MetricStripItem[];
  /** Optional title above the strip */
  title?: string;
}

// =============================================================================
// Styles
// =============================================================================

const styles = {
  container: {
    display: 'flex',
    flexWrap: 'wrap' as const,
    gap: '16px',
    padding: '16px 20px',
    background: 'var(--surface)',
    borderRadius: '12px',
    margin: '8px 0',
  },
  title: {
    width: '100%',
    fontSize: '18px',
    fontWeight: 600,
    color: 'var(--text)',
    marginBottom: '8px',
    paddingBottom: '8px',
    borderBottom: '1px solid rgba(255,255,255,0.1)',
  },
  item: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    padding: '8px 16px',
    background: 'rgba(255,255,255,0.05)',
    borderRadius: '8px',
    borderLeft: '3px solid var(--accent)',
  },
  icon: {
    fontSize: '18px',
    opacity: 0.8,
  },
  value: {
    fontSize: '24px',
    fontWeight: 700,
    color: 'var(--accent)',
  },
  label: {
    fontSize: '14px',
    color: 'var(--muted)',
  },
};

// =============================================================================
// Component
// =============================================================================

export function MetricStrip({ metrics, title }: MetricStripProps): JSX.Element {
  return (
    <div className="metric-strip" style={styles.container}>
      {title && (
        <div className="metric-strip-title" style={styles.title}>
          {title}
        </div>
      )}
      {metrics.map((metric, index) => (
        <div 
          key={index} 
          className="metric-strip-item" 
          style={styles.item}
        >
          {metric.icon && (
            <span className="strip-icon" style={styles.icon} aria-hidden="true">
              {metric.icon}
            </span>
          )}
          <span className="strip-value" style={styles.value}>
            {metric.value}
          </span>
          <span className="strip-label" style={styles.label}>
            {metric.label}
          </span>
        </div>
      ))}
    </div>
  );
}

export default MetricStrip;
