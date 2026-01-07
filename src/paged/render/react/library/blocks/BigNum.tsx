/**
 * BigNum Component (L2 Block)
 * 
 * Hero metric display - single large number with label.
 * Used for highlighting a standout KPI or statistic.
 * 
 * Usage:
 * ```mdx
 * <BigNum 
 *   value="136k" 
 *   label="Monthly Active Users"
 *   sublabel="Growing 12% MoM"
 * />
 * ```
 */

import React from 'react';

// =============================================================================
// Types
// =============================================================================

export interface BigNumProps {
  /** The main metric value */
  value: string;
  /** Label describing the metric */
  label?: string;
  /** Optional secondary label/context */
  sublabel?: string;
  /** Optional icon */
  icon?: string;
  /** Optional accent color override */
  accentColor?: string;
}

// =============================================================================
// Styles
// =============================================================================

const styles = {
  container: {
    textAlign: 'center' as const,
    padding: '32px 24px',
    background: 'var(--surface)',
    borderRadius: '12px',
    margin: '8px 0',
  },
  value: {
    fontSize: '64px',
    fontWeight: 800,
    color: 'var(--accent)',
    lineHeight: 1.1,
  },
  label: {
    fontSize: '20px',
    fontWeight: 600,
    color: 'var(--text)',
    marginTop: '8px',
  },
  sublabel: {
    fontSize: '16px',
    color: 'var(--muted)',
    marginTop: '4px',
  },
  icon: {
    fontSize: '32px',
    marginBottom: '8px',
    opacity: 0.8,
  },
};

// =============================================================================
// Component
// =============================================================================

export function BigNum({ 
  value, 
  label, 
  sublabel,
  icon,
  accentColor 
}: BigNumProps): JSX.Element {
  const valueStyle = accentColor 
    ? { ...styles.value, color: accentColor }
    : styles.value;

  return (
    <div className="big-num" style={styles.container}>
      {icon && (
        <div style={styles.icon} aria-hidden="true">
          {icon}
        </div>
      )}
      <div className="big-num-value" style={valueStyle}>
        {value}
      </div>
      {label && (
        <div className="big-num-label" style={styles.label}>
          {label}
        </div>
      )}
      {sublabel && (
        <div className="big-num-sublabel" style={styles.sublabel}>
          {sublabel}
        </div>
      )}
    </div>
  );
}

export default BigNum;
