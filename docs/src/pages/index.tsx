import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <p className={styles.heroDescription}>
          Stop handing your credit card to AI agents. Issue them strict, pre-funded debit cards instead.
        </p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Get Started — It's Free ⚡
          </Link>
          <Link
            className="button button--outline button--lg"
            to="https://agentpay-07bn.onrender.com/docs"
            style={{marginLeft: '1rem', color: 'white', borderColor: 'white'}}>
            Live API Docs →
          </Link>
        </div>
      </div>
    </header>
  );
}

const features = [
  {
    title: 'What is AgentPay?',
    description: (
      <>
        AgentPay is an open-source API platform that gives autonomous AI agents their own 
        <strong> digital identity</strong> and <strong>budget-bound wallets</strong>. 
        When you build AI agents with LangChain, AutoGen, or CrewAI, they inevitably need to 
        spend money — calling paid APIs, purchasing datasets, or accessing gated content. 
        AgentPay provides the financial guardrails so agents can operate autonomously without 
        draining your bank account.
      </>
    ),
  },
  {
    title: 'What is B2A?',
    description: (
      <>
        <strong>B2A (Business-to-Agent)</strong> is a new infrastructure category — just like 
        B2B (business-to-business) and B2C (business-to-consumer). As AI agents become autonomous 
        workers that browse the web, call APIs, and make purchasing decisions, businesses need 
        dedicated infrastructure to authenticate, authorize, and bill these non-human actors. 
        AgentPay is the first open-source B2A platform built specifically for this emerging economy.
      </>
    ),
  },
  {
    title: 'Why Not Just Use Stripe?',
    description: (
      <>
        Stripe requires human interaction — clicking buttons, entering card details, solving CAPTCHAs. 
        Autonomous agents can't do any of that. AgentPay provides <strong>programmatic, API-first 
        financial controls</strong> designed for machines: scoped API keys, atomic wallet debits with 
        row-level locking, real-time metering streams, and hard budget caps that automatically 
        block overspending. It's the middleware between your agents and real payment processors.
      </>
    ),
  },
];

const useCases = [
  {
    emoji: '🛡️',
    title: 'Prevent Runaway Costs',
    text: 'An agent in an infinite loop calling GPT-4 10,000 times = $300 bill. With AgentPay, set a 1,000-unit cap and the agent stops automatically.',
  },
  {
    emoji: '👥',
    title: 'Multi-Agent Budgets',
    text: 'Give each agent its own isolated wallet. See exactly which agent spent what. Block the rogue one without affecting others.',
  },
  {
    emoji: '🏢',
    title: 'Build SaaS Products',
    text: 'Building a platform where users deploy AI agents? Give each user\'s agent its own wallet with per-plan limits (Free: 100 units, Pro: 10,000).',
  },
  {
    emoji: '📊',
    title: 'Team Cost Visibility',
    text: '10 developers running experimental agents? Track who caused the $2,000 bill with per-agent hourly and daily usage buckets.',
  },
];

function FeaturesSection() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {features.map((feature, idx) => (
            <div key={idx} className={clsx('col col--4')}>
              <div className={styles.featureCard}>
                <Heading as="h3">{feature.title}</Heading>
                <p>{feature.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function UseCasesSection() {
  return (
    <section className={styles.useCases}>
      <div className="container">
        <Heading as="h2" className={styles.sectionTitle}>Real-World Use Cases</Heading>
        <div className="row">
          {useCases.map((item, idx) => (
            <div key={idx} className={clsx('col col--3')}>
              <div className={styles.useCaseCard}>
                <div className={styles.useCaseEmoji}>{item.emoji}</div>
                <Heading as="h4">{item.title}</Heading>
                <p>{item.text}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function HowItWorksSection() {
  return (
    <section className={styles.howItWorks}>
      <div className="container">
        <Heading as="h2" className={styles.sectionTitle}>How It Works</Heading>
        <div className={styles.steps}>
          <div className={styles.step}>
            <div className={styles.stepNumber}>1</div>
            <Heading as="h4">Issue Identity</Heading>
            <p>Create a scoped API key for your agent (<code>agnt_live_sk_...</code>). The agent gets a unique ID and its own isolated wallet.</p>
          </div>
          <div className={styles.step}>
            <div className={styles.stepNumber}>2</div>
            <Heading as="h4">Fund the Wallet</Heading>
            <p>The human developer pre-funds the wallet with a strict budget (e.g., $10). The agent has <strong>zero ability</strong> to top up its own wallet.</p>
          </div>
          <div className={styles.step}>
            <div className={styles.stepNumber}>3</div>
            <Heading as="h4">Agent Operates</Heading>
            <p>The agent calls APIs, purchases data, or executes tasks. Each action meters usage and atomically debits the wallet.</p>
          </div>
          <div className={styles.step}>
            <div className={styles.stepNumber}>4</div>
            <Heading as="h4">Budget Enforced</Heading>
            <p>When the budget runs out, the API returns an error. The agent stops gracefully. Your money is safe.</p>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home(): React.JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Agent Auth & Billing | ${siteConfig.title}`}
      description="AgentPay — Open-source B2A infrastructure giving autonomous AI agents digital identity and budget-bound wallets.">
      <HomepageHeader />
      <main>
        <FeaturesSection />
        <HowItWorksSection />
        <UseCasesSection />
      </main>
    </Layout>
  );
}
