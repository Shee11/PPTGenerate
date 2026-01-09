'use client';

// This folder previously contained a duplicate MDXProvider that referenced
// non-existent '@/components/*' paths. Keep this file as a compatibility
// re-export so older imports continue to work.

export { mdxComponents, MDXProvider } from '@/library/core/MDXProvider';
export type { MDXProviderProps } from '@/library/core/MDXProvider';
export { default } from '@/library/core/MDXProvider';
