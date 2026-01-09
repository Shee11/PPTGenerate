// Chart Types - TypeScript Interface Definitions
// Feature: 003-extended-chart-types

/**
 * Supported chart types for MDX rendering
 */
export type ChartType =
  | 'area'
  | 'bar'
  | 'barStats'
  | 'bubble'
  | 'doughnut'
  | 'pie'
  | 'line'
  | 'polarArea'
  | 'radar';

/**
 * Base chart data point
 */
export interface ChartDataPoint {
  /** Display label for the data point */
  label: string;
  
  /** Primary numeric value */
  value: number;
  
  /** Optional: Override color for this point */
  color?: string;
  
  // Cluster chart extensions
  /** Optional: "Before" value for comparison charts */
  before?: number;
  
  /** Optional: "After" value for comparison charts */
  after?: number;
  
  // Bubble chart extensions
  /** Optional: X coordinate (bubble/scatter) */
  x?: number;
  
  /** Optional: Y coordinate (bubble/scatter) */
  y?: number;
  
  /** Optional: Size dimension (bubble) */
  size?: number;
}

/**
 * Chart block props for MDX components
 */
export interface ChartBlockProps {
  /** Type of chart to render */
  type: ChartType;
  
  /** Data points to visualize */
  data: ChartDataPoint[];
  
  /** Chart title (optional) */
  title?: string;
  
  /** Chart subtitle (optional) */
  subtitle?: string;
  
  /** Color scheme override */
  colors?: string[];
  
  /** Show legend (default: true for pie/doughnut) */
  showLegend?: boolean;
  
  /** Show grid lines (default: true for bar/line/area) */
  showGrid?: boolean;
  
  /** Animation enabled (default: true) */
  animated?: boolean;
}

// Individual chart component props

export interface AreaChartProps {
  data: ChartDataPoint[];
  title?: string;
  colors?: string[];
  showGrid?: boolean;
  curve?: 'smooth' | 'linear';
  gradient?: boolean;
}

export interface BarChartProps {
  data: ChartDataPoint[];
  title?: string;
  colors?: string[];
  showGrid?: boolean;
  clustered?: boolean;
}

export interface BarStatsProps {
  data: ChartDataPoint[];
  title?: string;
  colors?: string[];
  showLabels?: boolean;
  sortDescending?: boolean;
}

export interface BubbleChartProps {
  data: ChartDataPoint[];
  title?: string;
  colors?: string[];
  showGrid?: boolean;
  xLabel?: string;
  yLabel?: string;
}

export interface PieChartProps {
  data: ChartDataPoint[];
  title?: string;
  colors?: string[];
  showLegend?: boolean;
  variant?: 'pie' | 'donut';
}

export interface PolarAreaProps {
  data: ChartDataPoint[];
  title?: string;
  colors?: string[];
  showLegend?: boolean;
}

export interface RadarChartProps {
  data: ChartDataPoint[];
  title?: string;
  colors?: string[];
  fillOpacity?: number;
  showDots?: boolean;
}
