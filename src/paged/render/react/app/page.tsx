'use client';

/**
 * Index Page - Presentation Viewer
 * 
 * Entry point for the presentation. Displays the slide deck with navigation.
 */

import React from 'react';
import { SlideContainer, SlideWrapper } from '@/components';
import { LayoutCover, LayoutSplit, LayoutGrid } from '@/components/layouts';
import { Heading, Text, Callout } from '@/components/atoms';
import { SmartList, ChartBar, MetricGroup } from '@/components/blocks';

/**
 * Demo Presentation
 * 
 * This is a sample presentation demonstrating the available components.
 * In production, slides would be loaded from MDX files.
 */
export default function HomePage(): JSX.Element {
  return (
    <SlideContainer currentSlide={0}>
      {/* Slide 1: Cover */}
      <SlideWrapper index={0} isActive={true}>
        <LayoutCover>
          <Heading level={1}>React MDX Renderer</Heading>
          <Text variant="lead">Strictly Semantic Presentations</Text>
        </LayoutCover>
      </SlideWrapper>
      
      {/* Slide 2: Split Layout */}
      <SlideWrapper index={1} isActive={false}>
        <LayoutSplit ratio="2:1">
          <LayoutSplit.Left>
            <Heading level={2}>Key Features</Heading>
            <SmartList 
              items={[
                'Semantic components only',
                'No raw HTML or CSS',
                'Theme-aware styling',
                'Compound component patterns',
              ]}
            />
          </LayoutSplit.Left>
          <LayoutSplit.Right>
            <Callout intent="info" title="Pro Tip">
              All styling is handled internally via CSS variables.
            </Callout>
          </LayoutSplit.Right>
        </LayoutSplit>
      </SlideWrapper>
      
      {/* Slide 3: Grid with Metrics */}
      <SlideWrapper index={2} isActive={false}>
        <LayoutGrid cols={2}>
          <LayoutGrid.Col>
            <Heading level={2}>Performance</Heading>
            <MetricGroup 
              metrics={[
                { value: '<2s', label: 'Render Time', change: -15 },
                { value: '<500KB', label: 'Export Size' },
              ]}
              cols={1}
            />
          </LayoutGrid.Col>
          <LayoutGrid.Col>
            <Heading level={2}>Usage</Heading>
            <ChartBar 
              title="Adoption Rate"
              data={[
                { label: 'Q1', value: 100 },
                { label: 'Q2', value: 250 },
                { label: 'Q3', value: 400 },
                { label: 'Q4', value: 600 },
              ]}
              height="md"
            />
          </LayoutGrid.Col>
        </LayoutGrid>
      </SlideWrapper>
    </SlideContainer>
  );
}
