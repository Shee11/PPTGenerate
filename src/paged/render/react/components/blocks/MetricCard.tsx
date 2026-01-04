/**
 * MetricCard Component (L2 Block)
 * 
 * Segmented summary card with categorized metrics.
 * Shows metrics with icons in a card layout (vertical or horizontal).
 * 
 * Usage:
 * ```mdx
 * <MetricCard 
 *   title="Performance"
 *   layout="horizontal"
 *   metrics={[
 *     { icon: "📈", value: "+40%", label: "Revenue Growth" },
 *     { icon: "💰", value: "-20%", label: "Cost Reduction" },
 *     { icon: "⭐", value: "72", label: "NPS Score" }
 *   ]}
 * />
 * ```
 */

import React from 'react';

// =============================================================================
// Types
// =============================================================================

export interface MetricCardItem {
  /** Icon (emoji or icon name) */
  icon?: string;
  /** Metric value */
  value: string;
  /** Metric label */
  label: string;
}

export interface MetricCardProps {
  /** Array of metrics to display */
  metrics: MetricCardItem[];
  /** Optional title for the card */
  title?: string;
  /** Layout direction: vertical (stacked) or horizontal (side by side) */
  layout?: 'vertical' | 'horizontal';
}

// =============================================================================
// Styles
// =============================================================================

const styles = {
  container: {
    background: 'var(--surface)',
    borderRadius: '16px',
    padding: '20px',
    margin: '8px 0',
  },
  title: {
    fontSize: '20px',
    fontWeight: 600,
    color: 'var(--text)',
    marginBottom: '16px',
    paddingBottom: '12px',
    borderBottom: '2px solid var(--accent)',
  },
  gridVertical: {
    display: 'grid',
    gridTemplateColumns: '1fr',
    gap: '16px',
  },
  gridHorizontal: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
    gap: '16px',
  },
  item: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    padding: '12px 16px',
    background: 'rgba(255,255,255,0.03)',
    borderRadius: '10px',
    transition: 'background 0.2s',
  },
  iconContainer: {
    fontSize: '24px',
    width: '40px',
    height: '40px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: 'rgba(var(--accent-rgb, 124, 58, 237), 0.15)',
    borderRadius: '10px',
    flexShrink: 0,
  },
  content: {
    flex: 1,
  },
  label: {
    fontSize: '14px',
    color: 'var(--muted)',
    marginBottom: '2px',
  },
  value: {
    fontSize: '22px',
    fontWeight: 700,
    color: 'var(--accent)',
  },
};

// =============================================================================
// Component
// =============================================================================

export function MetricCard({ 
  metrics, 
  title, 
  layout = 'vertical' 
}: MetricCardProps): JSX.Element {
  const gridStyle = layout === 'horizontal' 
    ? styles.gridHorizontal 
    : styles.gridVertical;

  return (
    <div className="metric-card" style={styles.container}>
      {title && (
        <div className="metric-card-title" style={styles.title}>
          {title}
        </div>
      )}
      <div 
        className={`metric-card-grid ${layout}`} 
        style={gridStyle}
      >
        {metrics.map((metric, index) => (
          <div 
            key={index} 
            className="metric-card-item" 
            style={styles.item}
          >
            {metric.icon && (
              <div className="card-icon" style={styles.iconContainer}>
                {metric.icon}
              </div>
            )}
            <div className="card-content" style={styles.content}>
              <div className="card-label" style={styles.label}>
                {metric.label}
              </div>
              <div className="card-value" style={styles.value}>
                {metric.value}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default MetricCard;
