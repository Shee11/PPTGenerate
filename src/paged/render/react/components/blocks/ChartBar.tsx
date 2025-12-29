'use client';

/**
 * ChartBar Component (L2 Block)
 * 
 * Semantic bar chart component using Recharts.
 * Automatically styled based on current theme.
 * 
 * Usage:
 * ```mdx
 * <ChartBar 
 *   title="Sales by Quarter"
 *   data={[
 *     { label: "Q1", value: 100 },
 *     { label: "Q2", value: 150 },
 *     { label: "Q3", value: 120 }
 *   ]}
 *   height="md"
 * />
 * ```
 */

import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import type { ChartDataPoint, Size } from '@/utils/types';

// =============================================================================
// Types
// =============================================================================

export interface CalloutData {
  /** Callout intent: info, warning, success, error */
  intent?: 'info' | 'warning' | 'success' | 'error';
  /** Callout title */
  title?: string;
  /** Callout text content */
  text: string;
}

export interface ChartBarProps {
  /** Chart data points */
  data: ChartDataPoint[];
  /** Chart title */
  title?: string;
  /** Chart subtitle */
  subtitle?: string;
  /** Chart height size */
  height?: Size;
  /** Optional integrated callout */
  callout?: CalloutData;
}

// =============================================================================
// Constants
// =============================================================================

const heightMap: Record<Size, number> = {
  sm: 150,
  md: 250,
  lg: 350,
  full: 400,
};

// =============================================================================
// Component
// =============================================================================

/**
 * ChartBar Component
 * 
 * Renders a responsive bar chart with theme-aware colors.
 * Supports integrated slots for title, subtitle, and callout.
 * 
 * @param data - Array of { label, value } objects
 * @param title - Optional chart title
 * @param subtitle - Optional chart subtitle
 * @param height - Chart height (sm, md, lg, full)
 * @param callout - Optional integrated callout
 */
export function ChartBar({
  data,
  title,
  subtitle,
  height = 'md',
  callout,
}: ChartBarProps): JSX.Element {
  const chartHeight = heightMap[height] || heightMap.md;
  
  // Determine callout class based on intent
  const calloutClass = callout 
    ? `block-callout callout-${callout.intent || 'info'}`
    : '';
  
  // Ensure data has valid values and is properly formatted
  const validData = (data || []).map(d => ({
    ...d,
    label: d.label || d.name || '',
    value: typeof d.value === 'number' && !isNaN(d.value) ? d.value : 0,
  })).filter(d => d.label);
  
  return (
    <div className="chart-block">
      {/* Block Header */}
      {(title || subtitle) && (
        <div className="block-header">
          {title && <h3 className="block-title">{title}</h3>}
          {subtitle && <p className="block-subtitle">{subtitle}</p>}
        </div>
      )}
      
      {/* Main Chart Content */}
      {validData.length > 0 && (
        <ResponsiveContainer width="100%" height={chartHeight}>
          <BarChart
            data={validData}
            margin={{ top: 10, right: 10, left: 0, bottom: 5 }}
          >
            <CartesianGrid 
              strokeDasharray="3 3" 
              stroke="var(--theme-border)"
              vertical={false}
            />
            <XAxis 
              dataKey="label" 
              tick={{ fill: 'var(--theme-text-muted)', fontSize: 12 }}
              axisLine={{ stroke: 'var(--theme-border)' }}
              tickLine={false}
            />
            <YAxis 
              tick={{ fill: 'var(--theme-text-muted)', fontSize: 12 }}
              axisLine={false}
              tickLine={false}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: 'var(--theme-surface)',
                border: '1px solid var(--theme-border)',
                borderRadius: 'var(--theme-radius)',
                color: 'var(--theme-text)',
              }}
            />
            <Bar 
              dataKey="value" 
              fill="var(--theme-primary)"
              radius={[4, 4, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      )}
      
      {/* Integrated Callout */}
      {callout && (
        <div className={calloutClass}>
          {callout.title && <strong className="callout-title">{callout.title}</strong>}
          <span className="callout-text">{callout.text}</span>
        </div>
      )}
    </div>
  );
}

// =============================================================================
// Exports
// =============================================================================

export default ChartBar;
