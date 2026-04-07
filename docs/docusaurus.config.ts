import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'AgentPay',
  tagline: 'B2A Infrastructure for Autonomous Agents',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  url: 'https://agentpay.dev',
  baseUrl: '/',

  organizationName: 'kashyapshukla',
  projectName: 'agentPay',

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl:
            'https://github.com/kashyapshukla/agentPay/tree/main/docs/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'AgentPay',
      logo: {
        alt: 'AgentPay Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Docs',
        },
        {
          href: 'https://github.com/kashyapshukla/agentPay',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Documentation',
          items: [
            {
              label: 'Getting Started',
              to: '/docs/intro',
            },
            {
              label: 'API Reference',
              to: '/docs/api-reference',
            },
            {
              label: 'Deployment',
              to: '/docs/deployment',
            },
          ],
        },
        {
          title: 'Source',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/kashyapshukla/agentPay',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} AgentPay. Open-source under MIT License.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
