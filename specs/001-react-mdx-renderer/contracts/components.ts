/**
 * React Component Prop Interfaces
 * 
 * This file defines the TypeScript interfaces for all React components
 * in the React MDX presentation system.
 * 
 * IMPORTANT: These interfaces define what the AGENT can use (L1-L3).
 * Internal implementation details (className, style) are NOT exposed.
 */

import { ReactNode } from 'react';

// =============================================================================
// SHARED TYPES
// =============================================================================

/** Semantic size variants */
export type Size = 'sm' | 'md' | 'lg' | 'full';

/** Visual style variants */
export type Variant = 'default' | 'primary' | 'outline' | 'ghost';

/** Semantic intent for callouts and alerts */
export type Intent = 'info' | 'warning' | 'success' | 'danger';

/** Split ratio for two-column layouts */
export type SplitRatio = '1:1' | '2:1' | '1:2' | '3:1' | '1:3';

/** Grid column count */
export type GridCols = 2 | 3 | 4;

/** Heading levels */
export type HeadingLevel = 1 | 2 | 3 | 4 | 5 | 6;

/** Text variants */
export type TextVariant = 'default' | 'lead' | 'caption' | 'code';

/** Chart types */
export type ChartType = 'bar' | 'line' | 'pie' | 'donut';

/** Chart data point */
export interface ChartDataPoint {
  label: string;
  value: number;
}

/** Metric data */
export interface MetricData {
  value: string;
  label: string;
  change?: number;
  changeLabel?: string;
  icon?: string;
}

/** Table column definition */
export interface TableColumn {
  key: string;
  label: string;
  align?: 'left' | 'center' | 'right';
}

// =============================================================================
// L1: LAYOUT COMPONENTS
// =============================================================================

/**
 * LayoutCover - Title slide layout
 * 
 * Usage:
 * ```mdx
 * <LayoutCover>
 *   <Heading level={1}>Title</Heading>
 *   <Text>Subtitle</Text>
 * </LayoutCover>
 * ```
 */
export interface LayoutCoverProps {
  children: ReactNode;
  /** Theme override */
  theme?: string;
  /** Vibe modifier */
  vibe?: string;
}

/**
 * LayoutSplit - Two-column layout with compound slots
 * 
 * Usage:
 * ```mdx
 * <LayoutSplit ratio="2:1">
 *   <LayoutSplit.Left>Left content</LayoutSplit.Left>
 *   <LayoutSplit.Right>Right content</LayoutSplit.Right>
 * </LayoutSplit>
 * ```
 */
export interface LayoutSplitProps {
  children: ReactNode;
  /** Column width ratio */
  ratio?: SplitRatio;
  /** Theme override */
  theme?: string;
  /** Vibe modifier */
  vibe?: string;
}

export interface LayoutSplitSlotProps {
  children: ReactNode;
}

/**
 * LayoutGrid - Multi-column grid layout
 * 
 * Usage:
 * ```mdx
 * <LayoutGrid cols={3}>
 *   <LayoutGrid.Col>Column 1</LayoutGrid.Col>
 *   <LayoutGrid.Col>Column 2</LayoutGrid.Col>
 *   <LayoutGrid.Col>Column 3</LayoutGrid.Col>
 * </LayoutGrid>
 * ```
 */
export interface LayoutGridProps {
  children: ReactNode;
  /** Number of columns (2-4) */
  cols?: GridCols;
  /** Theme override */
  theme?: string;
  /** Vibe modifier */
  vibe?: string;
}

export interface LayoutGridColProps {
  children: ReactNode;
}

/**
 * LayoutFullBleed - Full-screen background with content overlay
 * 
 * Usage:
 * ```mdx
 * <LayoutFullBleed background="https://example.com/image.jpg">
 *   <Heading level={1}>Overlay Title</Heading>
 * </LayoutFullBleed>
 * ```
 */
export interface LayoutFullBleedProps {
  children: ReactNode;
  /** Background image URL */
  background: string;
  /** Overlay opacity (0-1) */
  overlay?: number;
  /** Theme override */
  theme?: string;
  /** Vibe modifier */
  vibe?: string;
}

/**
 * LayoutTimeline - Horizontal timeline with steps
 * 
 * Usage:
 * ```mdx
 * <LayoutTimeline>
 *   <LayoutTimeline.Header>Timeline Title</LayoutTimeline.Header>
 *   <LayoutTimeline.Step>Step 1</LayoutTimeline.Step>
 *   <LayoutTimeline.Step>Step 2</LayoutTimeline.Step>
 * </LayoutTimeline>
 * ```
 */
export interface LayoutTimelineProps {
  children: ReactNode;
  /** Theme override */
  theme?: string;
  /** Vibe modifier */
  vibe?: string;
}

export interface LayoutTimelineSlotProps {
  children: ReactNode;
  /** Step title (for Step slot) */
  title?: string;
  /** Step date (for Step slot) */
  date?: string;
}

/**
 * LayoutDashboard - Metrics dashboard with chart area
 * 
 * Usage:
 * ```mdx
 * <LayoutDashboard>
 *   <LayoutDashboard.Header>Dashboard Title</LayoutDashboard.Header>
 *   <LayoutDashboard.Metric><MetricGroup metrics={[...]} /></LayoutDashboard.Metric>
 *   <LayoutDashboard.Chart><ChartBar data={[...]} /></LayoutDashboard.Chart>
 * </LayoutDashboard>
 * ```
 */
export interface LayoutDashboardProps {
  children: ReactNode;
  /** Theme override */
  theme?: string;
  /** Vibe modifier */
  vibe?: string;
}

export interface LayoutDashboardSlotProps {
  children: ReactNode;
}

// =============================================================================
// L2: BLOCK COMPONENTS
// =============================================================================

/**
 * ChartBar - Bar chart visualization
 * 
 * Usage:
 * ```mdx
 * <ChartBar 
 *   title="Sales by Quarter"
 *   data={[{label: "Q1", value: 100}, {label: "Q2", value: 150}]}
 *   height="md"
 * />
 * ```
 */
export interface ChartBarProps {
  /** Chart data points */
  data: ChartDataPoint[];
  /** Chart title */
  title?: string;
  /** Chart height */
  height?: Size;
}

/**
 * ChartLine - Line chart visualization
 */
export interface ChartLineProps {
  data: ChartDataPoint[];
  title?: string;
  height?: Size;
  /** Show area fill under line */
  area?: boolean;
}

/**
 * ChartPie - Pie/donut chart visualization
 */
export interface ChartPieProps {
  data: ChartDataPoint[];
  title?: string;
  /** Donut style (with hole) */
  donut?: boolean;
}

/**
 * MetricGroup - KPI metrics display
 * 
 * Usage:
 * ```mdx
 * <MetricGroup 
 *   metrics={[
 *     {value: "$2.4M", label: "Revenue", change: 12},
 *     {value: "89%", label: "Satisfaction"}
 *   ]}
 *   cols={2}
 * />
 * ```
 */
export interface MetricGroupProps {
  /** Metric data array */
  metrics: MetricData[];
  /** Number of columns */
  cols?: 1 | 2 | 3 | 4;
}

/**
 * TableData - Data table display
 * 
 * Usage:
 * ```mdx
 * <TableData 
 *   columns={[{key: "name", label: "Name"}, {key: "value", label: "Value"}]}
 *   rows={[{name: "Item 1", value: "100"}, {name: "Item 2", value: "200"}]}
 * />
 * ```
 */
export interface TableDataProps {
  /** Column definitions */
  columns: TableColumn[];
  /** Row data */
  rows: Record<string, string | number>[];
  /** Show header row */
  showHeader?: boolean;
  /** Visual variant */
  variant?: Variant;
}

/**
 * SmartList - Enhanced bullet/number list
 * 
 * Usage:
 * ```mdx
 * <SmartList 
 *   items={["Point one", "Point two", "Point three"]}
 *   ordered={false}
 * />
 * ```
 */
export interface SmartListProps {
  /** List items */
  items: string[];
  /** Ordered (numbered) list */
  ordered?: boolean;
  /** Icon for each item */
  icon?: string;
  /** Visual size */
  size?: Size;
}

/**
 * QuoteBlock - Blockquote with attribution
 * 
 * Usage:
 * ```mdx
 * <QuoteBlock 
 *   text="The only way to do great work is to love what you do."
 *   author="Steve Jobs"
 *   attribution="Stanford Commencement, 2005"
 * />
 * ```
 */
export interface QuoteBlockProps {
  /** Quote text */
  text: string;
  /** Author name */
  author?: string;
  /** Attribution (role, date, etc.) */
  attribution?: string;
  /** Visual variant */
  variant?: Variant;
}

/**
 * ImageBlock - Image with caption
 * 
 * Usage:
 * ```mdx
 * <ImageBlock 
 *   src="https://example.com/image.jpg"
 *   alt="Description"
 *   caption="Figure 1: Example image"
 * />
 * ```
 */
export interface ImageBlockProps {
  /** Image URL */
  src: string;
  /** Alt text (required for accessibility) */
  alt: string;
  /** Caption text */
  caption?: string;
  /** Image size */
  size?: Size;
}

/**
 * CardGroup - Group of cards
 * 
 * Usage:
 * ```mdx
 * <CardGroup cols={2}>
 *   <CardGroup.Card title="Card 1">Content 1</CardGroup.Card>
 *   <CardGroup.Card title="Card 2">Content 2</CardGroup.Card>
 * </CardGroup>
 * ```
 */
export interface CardGroupProps {
  children: ReactNode;
  /** Number of columns */
  cols?: GridCols;
}

export interface CardGroupCardProps {
  children: ReactNode;
  /** Card title */
  title?: string;
  /** Card icon */
  icon?: string;
}

// =============================================================================
// L3: ATOM COMPONENTS
// =============================================================================

/**
 * Heading - Heading typography
 * 
 * Usage:
 * ```mdx
 * <Heading level={1}>Main Title</Heading>
 * <Heading level={2}>Section Title</Heading>
 * ```
 */
export interface HeadingProps {
  children: ReactNode;
  /** Heading level (1-6) */
  level?: HeadingLevel;
}

/**
 * Text - Paragraph/body typography
 * 
 * Usage:
 * ```mdx
 * <Text>Regular paragraph text</Text>
 * <Text variant="lead">Lead paragraph</Text>
 * <Text variant="caption">Caption text</Text>
 * ```
 */
export interface TextProps {
  children: ReactNode;
  /** Text variant */
  variant?: TextVariant;
}

/**
 * Callout - Highlighted message box
 * 
 * Usage:
 * ```mdx
 * <Callout intent="info">This is an informational note.</Callout>
 * <Callout intent="warning">This is a warning.</Callout>
 * ```
 */
export interface CalloutProps {
  children: ReactNode;
  /** Semantic intent */
  intent?: Intent;
  /** Callout title */
  title?: string;
}

// =============================================================================
// COMPONENT REGISTRY (for MDXProvider)
// =============================================================================

/**
 * All components available in MDX context.
 * Agent can ONLY use these components - no raw HTML.
 */
export interface ComponentRegistry {
  // L1: Layouts
  LayoutCover: React.FC<LayoutCoverProps>;
  LayoutSplit: React.FC<LayoutSplitProps> & {
    Left: React.FC<LayoutSplitSlotProps>;
    Right: React.FC<LayoutSplitSlotProps>;
  };
  LayoutGrid: React.FC<LayoutGridProps> & {
    Col: React.FC<LayoutGridColProps>;
  };
  LayoutFullBleed: React.FC<LayoutFullBleedProps>;
  LayoutTimeline: React.FC<LayoutTimelineProps> & {
    Header: React.FC<LayoutTimelineSlotProps>;
    Step: React.FC<LayoutTimelineSlotProps>;
  };
  LayoutDashboard: React.FC<LayoutDashboardProps> & {
    Header: React.FC<LayoutDashboardSlotProps>;
    Metric: React.FC<LayoutDashboardSlotProps>;
    Chart: React.FC<LayoutDashboardSlotProps>;
  };
  
  // L2: Blocks
  ChartBar: React.FC<ChartBarProps>;
  ChartLine: React.FC<ChartLineProps>;
  ChartPie: React.FC<ChartPieProps>;
  MetricGroup: React.FC<MetricGroupProps>;
  TableData: React.FC<TableDataProps>;
  SmartList: React.FC<SmartListProps>;
  QuoteBlock: React.FC<QuoteBlockProps>;
  ImageBlock: React.FC<ImageBlockProps>;
  CardGroup: React.FC<CardGroupProps> & {
    Card: React.FC<CardGroupCardProps>;
  };
  
  // L3: Atoms
  Heading: React.FC<HeadingProps>;
  Text: React.FC<TextProps>;
  Callout: React.FC<CalloutProps>;
}
