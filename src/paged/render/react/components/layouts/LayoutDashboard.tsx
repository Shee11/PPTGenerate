"use client";

/**
 * LayoutDashboard Component (L1 Layout)
 * 
 * Multi-panel dashboard layout for KPI and metric displays.
 * Supports flexible grid arrangements with named slots.
 * 
 * Sync Mode (default):
 * - Components in Main and Sidebar are aligned by row
 * - Headlines/lead text get their own rows
 * - Mismatched counts use N:1 or 1:N distribution
 * 
 * Usage:
 * ```mdx
 * <LayoutDashboard>
 *   <Header>
 *     <Heading level={2}>Dashboard Title</Heading>
 *   </Header>
 *   <Main>
 *     <ChartBar data={chartData} />
 *   </Main>
 *   <Sidebar>
 *     <MetricGroup metrics={metrics} />
 *   </Sidebar>
 * </LayoutDashboard>
 * ```
 */

import React, { type ReactNode, type ReactElement, Children, isValidElement } from 'react';
import type { ThemeName, VibeLevel } from '@/utils/types';

// =============================================================================
// Types
// =============================================================================

export interface LayoutDashboardProps {
  children: ReactNode;
  /** Layout variant */
  variant?: 'default' | 'wide-main' | 'sidebar-focus';
  /** Theme override */
  theme?: ThemeName;
  /** Vibe modifier */
  vibe?: VibeLevel;
  /** Disable sync mode - use independent flex columns */
  nosync?: boolean;
}

export interface DashboardSlotProps {
  children: ReactNode;
}

interface ComponentInfo {
  element: ReactElement;
  type: string;
  index: number;
  isHeadline: boolean;
}

interface GridRow {
  type: 'headline-full' | 'matched' | 'main-only' | 'sidebar-only' | 'one-to-many' | 'many-to-one';
  main: ComponentInfo[];
  sidebar: ComponentInfo[];
}

// =============================================================================
// Sub-Components (Slots) - exported for standalone use in MDX
// =============================================================================

/** Dashboard Header Slot */
export function Header({ children }: DashboardSlotProps): JSX.Element {
  return <div className="dashboard-header">{children}</div>;
}
Header.displayName = 'Header';

/** Dashboard Main Content Slot */
export function Main({ children }: DashboardSlotProps): JSX.Element {
  return (
    <div className="dashboard-main">
      <div className="dashboard-main-content">{children}</div>
    </div>
  );
}
Main.displayName = 'Main';

/** Dashboard Sidebar Slot */
export function Sidebar({ children }: DashboardSlotProps): JSX.Element {
  return (
    <div className="dashboard-sidebar">
      <div className="dashboard-sidebar-inner">{children}</div>
    </div>
  );
}
Sidebar.displayName = 'Sidebar';

/** Dashboard Footer Slot */
export function Footer({ children }: DashboardSlotProps): JSX.Element {
  return <div className="dashboard-footer">{children}</div>;
}
Footer.displayName = 'Footer';

// =============================================================================
// Helper Functions
// =============================================================================

/** Headline components that should get their own row */
const HEADLINE_TYPES = ['Heading', 'Title', 'SectionTitle', 'h1', 'h2', 'h3'];

/** Get component type name from element */
function getComponentType(element: ReactElement): string {
  const type = element.type;
  if (typeof type === 'string') return type;
  if (typeof type === 'function') {
    return (type as { displayName?: string }).displayName || type.name || 'Unknown';
  }
  return 'Unknown';
}

/** Check if component is a headline type */
function isHeadlineComponent(type: string, props?: Record<string, unknown>): boolean {
  if (type === 'Text' && props?.variant === 'lead') {
    return true;
  }
  return HEADLINE_TYPES.some(h => type.toLowerCase().includes(h.toLowerCase()));
}

/** Extract component info from children */
function extractComponents(children: ReactNode): ComponentInfo[] {
  const components: ComponentInfo[] = [];
  let index = 0;
  
  Children.forEach(children, (child) => {
    if (isValidElement(child)) {
      const type = getComponentType(child);
      const props = child.props as Record<string, unknown>;
      components.push({
        element: child,
        type,
        index,
        isHeadline: isHeadlineComponent(type, props),
      });
      index++;
    }
  });
  
  return components;
}

/** Check if a component is a "light" trailing component that should group with previous */
function isTrailingComponent(comp: ComponentInfo): boolean {
  if (comp.type === 'Text') {
    return true;
  }
  return false;
}

/** Group trailing components with their preceding "heavy" components */
function groupTrailingComponents(components: ComponentInfo[]): ComponentInfo[][] {
  const groups: ComponentInfo[][] = [];
  let currentGroup: ComponentInfo[] = [];
  
  for (const comp of components) {
    if (isTrailingComponent(comp) && currentGroup.length > 0) {
      currentGroup.push(comp);
    } else {
      if (currentGroup.length > 0) {
        groups.push(currentGroup);
      }
      currentGroup = [comp];
    }
  }
  
  if (currentGroup.length > 0) {
    groups.push(currentGroup);
  }
  
  return groups;
}

/** Build grid rows from main and sidebar components with sync matching */
function buildSyncedGridRows(mainComponents: ComponentInfo[], sidebarComponents: ComponentInfo[]): GridRow[] {
  const rows: GridRow[] = [];
  
  // Separate headlines from body content
  const mainHeadlines: ComponentInfo[] = [];
  const mainBody: ComponentInfo[] = [];
  const sidebarHeadlines: ComponentInfo[] = [];
  const sidebarBody: ComponentInfo[] = [];
  
  let mainHeadlinesDone = false;
  let sidebarHeadlinesDone = false;
  
  for (const comp of mainComponents) {
    if (!mainHeadlinesDone && comp.isHeadline) {
      mainHeadlines.push(comp);
    } else {
      mainHeadlinesDone = true;
      mainBody.push(comp);
    }
  }
  
  for (const comp of sidebarComponents) {
    if (!sidebarHeadlinesDone && comp.isHeadline) {
      sidebarHeadlines.push(comp);
    } else {
      sidebarHeadlinesDone = true;
      sidebarBody.push(comp);
    }
  }
  
  // Process headlines
  const maxHeadlines = Math.max(mainHeadlines.length, sidebarHeadlines.length);
  for (let i = 0; i < maxHeadlines; i++) {
    const mainH = mainHeadlines[i];
    const sidebarH = sidebarHeadlines[i];
    
    if (mainH && sidebarH) {
      rows.push({ type: 'matched', main: [mainH], sidebar: [sidebarH] });
    } else if (mainH) {
      rows.push({ type: 'headline-full', main: [mainH], sidebar: [] });
    } else if (sidebarH) {
      rows.push({ type: 'headline-full', main: [], sidebar: [sidebarH] });
    }
  }
  
  // Group trailing components before matching
  const mainGroups = groupTrailingComponents(mainBody);
  const sidebarGroups = groupTrailingComponents(sidebarBody);
  
  const mainGroupCount = mainGroups.length;
  const sidebarGroupCount = sidebarGroups.length;
  
  if (mainGroupCount === 0 && sidebarGroupCount === 0) {
    return rows;
  }
  
  if (mainGroupCount === sidebarGroupCount) {
    for (let i = 0; i < mainGroupCount; i++) {
      rows.push({ type: 'matched', main: mainGroups[i], sidebar: sidebarGroups[i] });
    }
  } else if (mainGroupCount > sidebarGroupCount && sidebarGroupCount > 0) {
    const ratio = mainGroupCount / sidebarGroupCount;
    let mainIdx = 0;
    
    for (let sidebarIdx = 0; sidebarIdx < sidebarGroupCount; sidebarIdx++) {
      const nextBoundary = Math.round((sidebarIdx + 1) * ratio);
      const mainCombined: ComponentInfo[] = [];
      
      while (mainIdx < nextBoundary && mainIdx < mainGroupCount) {
        mainCombined.push(...mainGroups[mainIdx]);
        mainIdx++;
      }
      
      rows.push({
        type: mainCombined.length > 1 ? 'many-to-one' : 'matched',
        main: mainCombined,
        sidebar: sidebarGroups[sidebarIdx],
      });
    }
    
    while (mainIdx < mainGroupCount) {
      rows.push({ type: 'main-only', main: mainGroups[mainIdx], sidebar: [] });
      mainIdx++;
    }
  } else if (sidebarGroupCount > mainGroupCount && mainGroupCount > 0) {
    const ratio = sidebarGroupCount / mainGroupCount;
    let sidebarIdx = 0;
    
    for (let mainIdx = 0; mainIdx < mainGroupCount; mainIdx++) {
      const nextBoundary = Math.round((mainIdx + 1) * ratio);
      const sidebarCombined: ComponentInfo[] = [];
      
      while (sidebarIdx < nextBoundary && sidebarIdx < sidebarGroupCount) {
        sidebarCombined.push(...sidebarGroups[sidebarIdx]);
        sidebarIdx++;
      }
      
      rows.push({
        type: sidebarCombined.length > 1 ? 'one-to-many' : 'matched',
        main: mainGroups[mainIdx],
        sidebar: sidebarCombined,
      });
    }
    
    while (sidebarIdx < sidebarGroupCount) {
      rows.push({ type: 'sidebar-only', main: [], sidebar: sidebarGroups[sidebarIdx] });
      sidebarIdx++;
    }
  } else if (mainGroupCount > 0) {
    for (const group of mainGroups) {
      rows.push({ type: 'main-only', main: group, sidebar: [] });
    }
  } else {
    for (const group of sidebarGroups) {
      rows.push({ type: 'sidebar-only', main: [], sidebar: group });
    }
  }
  
  return rows;
}

// =============================================================================
// Sync Body Renderer
// =============================================================================

interface SyncBodyProps {
  rows: GridRow[];
}

function SyncBody({ rows }: SyncBodyProps): JSX.Element {
  return (
    <div 
      className="dashboard-body dashboard-body-sync"
      style={{
        display: 'grid',
        gridTemplateColumns: '1fr minmax(400px, 480px)',
        gap: '40px',
        alignContent: 'center',
        alignItems: 'stretch',
        flex: 1,
        minHeight: 0,
      }}
    >
      {rows.map((row, rowIndex) => {
        const rowKey = `row-${rowIndex}`;
        
        // Full-width headline row
        if (row.type === 'headline-full') {
          const headline = row.main[0] || row.sidebar[0];
          return (
            <div 
              key={rowKey}
              className="dashboard-row dashboard-row-headline"
              style={{ 
                gridColumn: '1 / -1',
                display: 'flex',
                justifyContent: row.main[0] ? 'flex-start' : 'flex-end',
              }}
            >
              {headline.element}
            </div>
          );
        }
        
        // Main-only row
        if (row.type === 'main-only') {
          return (
            <React.Fragment key={rowKey}>
              <div 
                className="dashboard-cell dashboard-cell-main"
                style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}
              >
                {row.main.map((comp, i) => (
                  <div key={`main-${i}`} className="dashboard-cell-item">
                    {comp.element}
                  </div>
                ))}
              </div>
              <div className="dashboard-cell dashboard-cell-sidebar dashboard-cell-empty" />
            </React.Fragment>
          );
        }
        
        // Sidebar-only row
        if (row.type === 'sidebar-only') {
          return (
            <React.Fragment key={rowKey}>
              <div className="dashboard-cell dashboard-cell-main dashboard-cell-empty" />
              <div 
                className="dashboard-cell dashboard-cell-sidebar"
                style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}
              >
                {row.sidebar.map((comp, i) => (
                  <div key={`sidebar-${i}`} className="dashboard-cell-item">
                    {comp.element}
                  </div>
                ))}
              </div>
            </React.Fragment>
          );
        }
        
        // Matched or N:1 / 1:N rows
        return (
          <React.Fragment key={rowKey}>
            <div 
              className="dashboard-cell dashboard-cell-main"
              style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '1rem',
                alignSelf: 'stretch',
              }}
            >
              {row.main.map((comp, i) => (
                <div key={`main-${i}`} className="dashboard-cell-item">
                  {comp.element}
                </div>
              ))}
            </div>
            <div 
              className="dashboard-cell dashboard-cell-sidebar"
              style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '1rem',
                alignSelf: 'stretch',
                background: 'var(--theme-surface, #f8fafc)',
                borderRadius: '1rem',
                padding: '1.25rem',
              }}
            >
              {row.sidebar.map((comp, i) => (
                <div key={`sidebar-${i}`} className="dashboard-cell-item">
                  {comp.element}
                </div>
              ))}
            </div>
          </React.Fragment>
        );
      })}
    </div>
  );
}

// =============================================================================
// Component
// =============================================================================

/**
 * LayoutDashboard Component
 * 
 * Renders a dashboard-style layout with header, main, sidebar, and footer slots.
 * 
 * @param children - Dashboard slots (Header, Main, Sidebar, Footer)
 * @param variant - Layout variant affecting proportions
 * @param theme - Optional theme override
 * @param vibe - Optional vibe modifier
 * @param nosync - Disable sync mode (use traditional flex layout)
 */
export function LayoutDashboard({
  children,
  variant = 'default',
  theme,
  vibe,
  nosync = false,
}: LayoutDashboardProps): JSX.Element {
  // Extract slots from children
  let header: ReactNode = null;
  let mainSlot: ReactElement | null = null;
  let sidebarSlot: ReactElement | null = null;
  let footer: ReactNode = null;
  
  Children.forEach(children, (child) => {
    if (!isValidElement(child)) return;
    
    const displayName = (child.type as any).displayName;
    const componentType = child.type;

    // Match both standalone and compound component patterns
    if (displayName === 'Header' || displayName === 'LayoutDashboard.Header' || componentType === Header) {
      header = child;
    } else if (displayName === 'Main' || displayName === 'LayoutDashboard.Main' || componentType === Main) {
      mainSlot = child;
    } else if (displayName === 'Sidebar' || displayName === 'LayoutDashboard.Sidebar' || componentType === Sidebar) {
      sidebarSlot = child;
    } else if (displayName === 'Footer' || displayName === 'LayoutDashboard.Footer' || componentType === Footer) {
      footer = child;
    }
  });
  
  // Variant classes
  const variantClass = {
    default: 'dashboard-default',
    'wide-main': 'dashboard-wide-main',
    'sidebar-focus': 'dashboard-sidebar-focus',
  }[variant];
  
  // NoSync mode: Use traditional layout
  if (nosync) {
    return (
      <div 
        className={`layout-dashboard layout-dashboard-nosync ${variantClass}`}
        data-layout="dashboard"
        data-sync="false"
        data-variant={variant}
        data-theme={theme}
        data-vibe={vibe}
      >
        {header}
        <div className="dashboard-body">
          {mainSlot}
          {sidebarSlot}
        </div>
        {footer}
      </div>
    );
  }
  
  // Sync mode: Extract and match components
  const mainChildren = mainSlot?.props?.children;
  const sidebarChildren = sidebarSlot?.props?.children;
  
  const mainComponents = extractComponents(mainChildren);
  const sidebarComponents = extractComponents(sidebarChildren);
  
  const rows = buildSyncedGridRows(mainComponents, sidebarComponents);
  
  return (
    <div 
      className={`layout-dashboard layout-dashboard-sync ${variantClass}`}
      data-layout="dashboard"
      data-sync="true"
      data-variant={variant}
      data-theme={theme}
      data-vibe={vibe}
    >
      {header}
      <SyncBody rows={rows} />
      {footer}
    </div>
  );
}

// Attach sub-components
LayoutDashboard.Header = Header;
LayoutDashboard.Main = Main;
LayoutDashboard.Sidebar = Sidebar;
LayoutDashboard.Footer = Footer;

// =============================================================================
// Exports
// =============================================================================

export default LayoutDashboard;
