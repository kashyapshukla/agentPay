import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    'intro',
    'user-journey',
    {
      type: 'category',
      label: 'Integration Use Cases',
      items: [
        'integrations/autogen-squad',
        'integrations/crewai-scrapers',
        'integrations/custom-fastapi',
      ],
    },
    'deployment',
    'api-reference',
  ],
};

export default sidebars;
