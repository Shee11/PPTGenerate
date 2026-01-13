/**
 * CardGroup Component (L2 Block)
 *
 * Supports 3 layouts:
 * - default: icon/image and text stacked in one column
 * - left: icon/image on the left with a divider
 * - top: icon/image in a separate top circle
 */

import React, { Children, isValidElement, type ReactNode } from 'react';
import type { CardData, CardLayout, CardMediaSize, Size, GridCols } from '@/utils/types';

// =============================================================================
// Types
// =============================================================================

export interface CardProps extends CardData {
  children?: ReactNode;
  /** Size variant for individual card */
  size?: Size;
  /** Per-card layout variant */
  layout?: CardLayout;
  /** Per-card media (icon/image) size variant */
  mediaSize?: CardMediaSize;
}

export interface CardGroupProps {
  /** Array of card data (optional if using Card children) */
  cards?: CardData[];
  /** Card children (optional if using cards prop) */
  children?: ReactNode;
  /** Number of columns */
  columns?: GridCols;
  /** Card size variant */
  size?: Size;
  /** Card visual variant */
  variant?: 'default' | 'outline' | 'filled';
  /** Card layout variant (applies to all cards unless overridden per card) */
  layout?: CardLayout;
  /** Media (icon/image) size variant (applies to all cards unless overridden per card) */
  mediaSize?: CardMediaSize;
  /** Optional id for the card group */
  id?: string;
}

function getMediaSizeVars(mediaSize?: CardMediaSize): React.CSSProperties | undefined {
  if (!mediaSize) return undefined;

  const map: Record<CardMediaSize, {
    media: string;
    icon: string;
    topMedia: string;
    topIcon: string;
    topCircle: string;
    topOffset: string;
  }> = {
    sm: {
      media: '2.5rem',
      icon: '1.75rem',
      topMedia: '3rem',
      topIcon: '2.25rem',
      topCircle: '4.25rem',
      topOffset: '-2rem',
    },
    md: {
      media: '3rem',
      icon: '2rem',
      topMedia: '3.5rem',
      topIcon: '2.5rem',
      topCircle: '4.75rem',
      topOffset: '-2.25rem',
    },
    lg: {
      media: '3.5rem',
      icon: '3.25rem',
      topMedia: '4.25rem',
      topIcon: '3rem',
      topCircle: '5.75rem',
      topOffset: '-2.75rem',
    },
  };

  const s = map[mediaSize];
  return {
    ['--card-media-size' as any]: s.media,
    ['--card-icon-font-size' as any]: s.icon,
    ['--card-top-media-size' as any]: s.topMedia,
    ['--card-top-icon-font-size' as any]: s.topIcon,
    ['--card-top-circle-size' as any]: s.topCircle,
    ['--card-top-circle-top' as any]: s.topOffset,
  };
}

function renderMedia(card: CardData): ReactNode {
  if (card.image) {
    return (
      <div className="card-media">
        <img className="card-media-img" src={card.image} alt="" loading="lazy" />
      </div>
    );
  }
  if (card.icon) {
    return (
      <div className="card-media">
        <span className="card-media-icon">{card.icon}</span>
      </div>
    );
  }
  return null;
}

function renderCardInner(card: CardData, layout: CardLayout): ReactNode {
  if (layout === 'left') {
    return (
      <>
        {renderMedia(card)}
        <div className="card-divider" aria-hidden="true" />
        <div className="card-content">
          <h3 className="card-title">{card.title}</h3>
          {card.description && <p className="card-description">{card.description}</p>}
        </div>
      </>
    );
  }

  if (layout === 'top') {
    return (
      <>
        <div className="card-top-circle">{renderMedia(card)}</div>
        <div className="card-content">
          <h3 className="card-title">{card.title}</h3>
          {card.description && <p className="card-description">{card.description}</p>}
        </div>
      </>
    );
  }

  // default
  return (
    <>
      {renderMedia(card)}
      <div className="card-content">
        <h3 className="card-title">{card.title}</h3>
        {card.description && <p className="card-description">{card.description}</p>}
      </div>
    </>
  );
}

// =============================================================================
// Card Component
// =============================================================================

export function Card({
  title,
  description,
  icon,
  image,
  link,
  size = 'md',
  layout = 'default',
  mediaSize,
}: CardProps): JSX.Element {
  const sizeClass = {
    sm: 'card-sm',
    md: 'card-md',
    lg: 'card-lg',
    full: 'card-lg',
  }[size];

  const card: CardData = { title, description, icon, image, link, layout, mediaSize };
  const style = getMediaSizeVars(mediaSize);

  return (
    <div className={`card ${sizeClass} card-layout-${layout}`} data-layout={layout} style={style}>
      {renderCardInner(card, layout)}

      {link && (
        <div className="card-footer">
          <span className="card-link">Learn more →</span>
        </div>
      )}
    </div>
  );
}
Card.displayName = 'Card';

// =============================================================================
// CardGroup Component
// =============================================================================

export function CardGroup({
  cards,
  children,
  columns = 3,
  size = 'md',
  variant = 'default',
  layout = 'top',
  mediaSize = 'lg',
  id,
}: CardGroupProps): JSX.Element {
  const sizeClass = {
    sm: 'card-sm',
    md: 'card-md',
    lg: 'card-lg',
    full: 'card-lg',
  }[size];

  const cardsFromChildren: CardData[] = [];
  if (!cards && children) {
    Children.forEach(children, (child) => {
      if (isValidElement(child)) {
        const displayName = (child.type as { displayName?: string })?.displayName;
        if (displayName === 'Card' || (child.type as any) === Card) {
          const props = child.props as CardProps;
          cardsFromChildren.push({
            title: props.title,
            description: props.description,
            icon: props.icon,
            image: props.image,
            link: props.link,
            layout: props.layout,
            mediaSize: props.mediaSize,
          });
        }
      }
    });
  }

  const resolvedCards = cards || cardsFromChildren;

  return (
    <div
      className={`card-group layout-grid-${columns}`}
      data-columns={columns}
      data-variant={variant}
      data-layout={layout}
      id={id}
    >
      {resolvedCards.map((card, index) => {
        const resolvedLayout: CardLayout = (card.layout || layout || 'default');
        const resolvedMediaSize: CardMediaSize | undefined = card.mediaSize || mediaSize;
        const style = getMediaSizeVars(resolvedMediaSize);
        return (
          <div
            key={index}
            className={`card ${sizeClass} card-${variant} card-layout-${resolvedLayout}`}
            data-layout={resolvedLayout}
            style={style}
          >
            {renderCardInner(card, resolvedLayout)}

            {card.link && (
              <div className="card-footer">
                <span className="card-link">Learn more →</span>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

export default CardGroup;
