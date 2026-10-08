export const siteConstants = {
  siteName: process.env.SITE_NAME || 'Valmath Consulting',
  outcomes: [
    { name: 'Modernize', description: 'Modernize legacy SAP landscapes.' },
    { name: 'Integrate', description: 'Connect SAP with the wider enterprise ecosystem.' },
    { name: 'Optimize', description: 'Improve business processes and system performance.' },
    { name: 'Scale', description: 'Build scalable enterprise architecture.' },
    { name: 'Operate', description: 'Keep SAP reliable through structured support and managed services.' },
    { name: 'Innovate', description: 'Use BTP, data, automation, and AI where they create measurable value.' },
  ],
  capabilities: ['SAP Advisory', 'Implementation', 'Integration', 'Development', 'Migration', 'Managed Services'],
  problemOptions: [
    { problem: 'Modernize SAP', service: 'SAP Advisory & Strategy', url: '/services/sap-consulting/' },
    { problem: 'Migrate to S/4HANA', service: 'SAP S/4HANA', url: '/services/sap-s4hana/' },
    { problem: 'Integrate SAP', service: 'SAP Integration', url: '/services/sap-integration/' },
    { problem: 'Improve performance', service: 'SAP AMS & Managed Services', url: '/services/sap-ams/' },
    { problem: 'Reduce support backlog', service: 'SAP AMS & Managed Services', url: '/services/sap-ams/' },
    { problem: 'Build SAP extensions', service: 'SAP BTP', url: '/services/sap-btp/' },
    { problem: 'Improve reporting', service: 'SAP Data, Analytics & AI', url: '/services/sap-data-analytics/' },
    { problem: 'Strengthen security', service: 'SAP Development', url: '/services/sap-development/' },
    { problem: 'Need SAP expertise', service: 'SAP Advisory & Strategy', url: '/services/sap-consulting/' },
    { problem: 'Not sure', service: 'Talk to an SAP Expert', url: '/contact/' },
  ],
};
