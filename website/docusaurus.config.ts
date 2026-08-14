import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'minicloud Crew Agent',
  tagline: 'Three-agent CrewAI pipeline for compliance-validated AI research',
  favicon: 'img/favicon.ico',
  url: 'https://andrelair-platform.github.io',
  baseUrl: '/minicloud-crew-agent/',
  organizationName: 'andrelair-platform',
  projectName: 'minicloud-crew-agent',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  i18n: {defaultLocale: 'en', locales: ['en']},
  markdown: {mermaid: true},
  themes: ['@docusaurus/theme-mermaid'],
  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: '/',
        },
        blog: false,
        theme: {customCss: './src/css/custom.css'},
      } satisfies Preset.Options,
    ],
  ],
  themeConfig: {
    navbar: {
      title: 'minicloud-crew-agent',
      items: [
        {href: 'https://andrelair-platform.github.io/minicloud-platform-docs/', label: 'Platform docs', position: 'right'},
        {href: 'https://github.com/andrelair-platform/minicloud-crew-agent', label: 'GitHub', position: 'right'},
      ],
    },
    prism: {
      additionalLanguages: ['python', 'bash', 'yaml', 'json'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
