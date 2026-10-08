import { PrismaClient } from '@prisma/client';
import fs from 'fs';
import path from 'path';

const prisma = new PrismaClient();
const dir = path.resolve(process.cwd(), 'prisma/source-data');

const read = (name: string) => {
  const file = path.join(dir, name);
  if (!fs.existsSync(file)) throw new Error(`Missing required seed file: ${file}`);
  return JSON.parse(fs.readFileSync(file, 'utf8'));
};

async function faq(targetType: string, targetId: number, faqs: any[] = []) {
  for (let i = 0; i < faqs.length; i++) {
    const [question, answer] = Array.isArray(faqs[i]) ? faqs[i] : [faqs[i].question, faqs[i].answer];
    await prisma.faq.create({ data: { targetType, targetId, question, answer, sortOrder: i } });
  }
}

async function seedTeamMembers() {
  const members = [
    {
      name: 'Bhawani Singh',
      role: 'SAP ABAP Developer',
      imageUrl: '/team/bhawani-singh.webp',
      linkedinUrl: 'https://www.linkedin.com/',
      category: 'Technical',
      expertise: 'SAP ABAP development, reports, ALV, Smart Forms and SAP technical solutions.',
      modules: 'SAP ABAP, SAP MM',
      technologies: 'ABAP, ALV, Smart Forms, SQL, Python, Django',
      industries: 'Manufacturing, Enterprise IT',
      certifications: '',
      sortOrder: 1,
    },
    {
      name: 'Dheeraj Nishad',
      role: 'SAP S/4HANA FICO Consultant',
      imageUrl: '/team/dheeraj-nishad.webp',
      linkedinUrl: 'https://www.linkedin.com/in/dheeraj-nishad-a52b23206',
      category: 'Functional',
      expertise: 'SAP FICO, financial management, implementation, rollout, production support, migration and SAP integration.',
      modules: 'SAP FI/CO, S/4HANA',
      technologies: 'SAP FICO, SAP Integration, SAP S/4HANA',
      industries: 'Manufacturing, Enterprise IT',
      certifications: '',
      sortOrder: 2,
    },
  ];

  for (const member of members) {
    await prisma.teamMember.upsert({
      where: { id: member.sortOrder },
      update: member,
      create: member,
    });
  }
}

async function main() {
  await seedTeamMembers();
  const initialized = await prisma.appInitialization.findUnique({ where: { id: 1 } });
  if (initialized) {
    console.log('Database initialization already completed; skipping seed.');
    return;
  }

  const services = read('services.json');
  for (const x of services) {
    const service = await prisma.service.upsert({
      where: { slug: x.slug },
      update: {
        name:x.name, shortSummary:x.short_summary, heroIntro:x.hero_intro,
        businessProblem:x.business_problem, deliveryApproach:x.delivery_approach,
        engagementModel:x.engagement_model, whoItsFor:x.who_its_for,
        ctaLabel:x.cta_label || 'Talk to an SAP Expert', featured:!!x.featured,
        sortOrder:x.order || 0, metaTitle:x.meta_title || null, metaDescription:x.meta_description || null
      },
      create: {
        slug:x.slug, name:x.name, shortSummary:x.short_summary, heroIntro:x.hero_intro,
        businessProblem:x.business_problem, deliveryApproach:x.delivery_approach,
        engagementModel:x.engagement_model, whoItsFor:x.who_its_for,
        ctaLabel:x.cta_label || 'Talk to an SAP Expert', featured:!!x.featured,
        sortOrder:x.order || 0, metaTitle:x.meta_title || null, metaDescription:x.meta_description || null
      }
    });
    await prisma.serviceListItem.deleteMany({where:{serviceId:service.id}});
    for (const section of ['what_we_solve','capabilities','technology','deliverables']) {
      const rows = x[section] || [];
      await prisma.serviceListItem.createMany({data:rows.map((text:string,i:number)=>({serviceId:service.id,section,text,sortOrder:i}))});
    }
    await prisma.faq.deleteMany({where:{targetType:'service',targetId:service.id}});
    await faq('service',service.id,x.faqs);
    await prisma.serviceRelation.deleteMany({where:{fromId:service.id}});
    for (const slug of x.related_services || []) {
      const to = await prisma.service.findUnique({where:{slug}});
      if (to) await prisma.serviceRelation.create({data:{fromId:service.id,toId:to.id}});
    }
  }

  const solutions = read('solutions.json');
  for (const x of solutions) {
    const solution = await prisma.solution.upsert({
      where:{slug:x.slug},
      update:{name:x.name,shortSummary:x.short_summary,heroIntro:x.hero_intro,businessProblem:x.business_problem,approach:x.approach,whoItsFor:x.who_its_for,ctaLabel:x.cta_label||'Talk to an SAP Expert',sortOrder:x.order||0,metaTitle:x.meta_title||null,metaDescription:x.meta_description||null},
      create:{slug:x.slug,name:x.name,shortSummary:x.short_summary,heroIntro:x.hero_intro,businessProblem:x.business_problem,approach:x.approach,whoItsFor:x.who_its_for,ctaLabel:x.cta_label||'Talk to an SAP Expert',sortOrder:x.order||0,metaTitle:x.meta_title||null,metaDescription:x.meta_description||null}
    });
    await prisma.solutionListItem.deleteMany({where:{solutionId:solution.id}});
    for (const section of ['what_this_includes','outcomes']) {
      const rows=x[section]||[];
      await prisma.solutionListItem.createMany({data:rows.map((text:string,i:number)=>({solutionId:solution.id,section,text,sortOrder:i}))});
    }
    await prisma.faq.deleteMany({where:{targetType:'solution',targetId:solution.id}});
    await faq('solution',solution.id,x.faqs);
    await prisma.solutionServiceRelation.deleteMany({where:{solutionId:solution.id}});
    for (const slug of x.related_services || []) {
      const service = await prisma.service.findUnique({where:{slug}});
      if (service) await prisma.solutionServiceRelation.create({data:{solutionId:solution.id,serviceId:service.id}});
    }
    await prisma.solutionRelation.deleteMany({where:{fromId:solution.id}});
    for (const slug of x.related_solutions || []) {
      const to = await prisma.solution.findUnique({where:{slug}});
      if (to) await prisma.solutionRelation.create({data:{fromId:solution.id,toId:to.id}});
    }
  }

  const industries = read('industries.json');
  for (const x of industries) {
    const industry=await prisma.industry.upsert({
      where:{slug:x.slug},
      update:{name:x.name,shortSummary:x.short_summary,heroIntro:x.hero_intro,sapLandscape:x.sap_landscape,outcomes:x.outcomes,ctaLabel:x.cta_label||'Discuss Your Industry Challenge',sortOrder:x.order||0,metaTitle:x.meta_title||null,metaDescription:x.meta_description||null},
      create:{slug:x.slug,name:x.name,shortSummary:x.short_summary,heroIntro:x.hero_intro,sapLandscape:x.sap_landscape,outcomes:x.outcomes,ctaLabel:x.cta_label||'Discuss Your Industry Challenge',sortOrder:x.order||0,metaTitle:x.meta_title||null,metaDescription:x.meta_description||null}
    });
    await prisma.industryListItem.deleteMany({where:{industryId:industry.id}});
    for(const section of ['challenges','processes','modules','integration_requirements','transformation_opportunities','typical_use_cases']){
      const rows=x[section]||[];
      await prisma.industryListItem.createMany({data:rows.map((text:string,i:number)=>({industryId:industry.id,section,text,sortOrder:i}))});
    }
    await prisma.faq.deleteMany({where:{targetType:'industry',targetId:industry.id}});
    await faq('industry',industry.id,x.faqs);
    await prisma.industryServiceRelation.deleteMany({where:{industryId:industry.id}});
    for (const slug of x.related_services || []) {
      const service = await prisma.service.findUnique({where:{slug}});
      if (service) await prisma.industryServiceRelation.create({data:{industryId:industry.id,serviceId:service.id}});
    }
  }

  const expertise=read('expertise.json');
  await prisma.expertiseItem.deleteMany();
  for(let i=0;i<expertise.length;i++){
    const [category,name]=expertise[i];
    await prisma.expertiseItem.create({data:{category,name,description:'',sortOrder:i}});
  }

  const cases=read('case_studies.json');
  for(const x of cases){
    const industry=x.industry_slug ? await prisma.industry.findUnique({where:{slug:x.industry_slug}}):null;
    const item=await prisma.caseStudy.upsert({
      where:{slug:x.slug},
      update:{title:x.title,shortSummary:x.short_summary,industryId:industry?.id||null,businessChallenge:x.business_challenge,sapEnvironment:x.sap_environment,objective:x.objective,approach:x.approach,solution:x.solution,technologyUsed:x.technology_used,outcome:x.outcome,sortOrder:x.order||0,metaTitle:x.meta_title||null,metaDescription:x.meta_description||null},
      create:{slug:x.slug,title:x.title,shortSummary:x.short_summary,industryId:industry?.id||null,businessChallenge:x.business_challenge,sapEnvironment:x.sap_environment,objective:x.objective,approach:x.approach,solution:x.solution,technologyUsed:x.technology_used,outcome:x.outcome,sortOrder:x.order||0,metaTitle:x.meta_title||null,metaDescription:x.meta_description||null}
    });
    await prisma.caseStudyServiceRelation.deleteMany({where:{caseStudyId:item.id}});
    for(const slug of x.related_services||[]){
      const service=await prisma.service.findUnique({where:{slug}});
      if(service) await prisma.caseStudyServiceRelation.create({data:{caseStudyId:item.id,serviceId:service.id}});
    }
  }

  const articles=read('insights.json');
  for(const x of articles){
    const article=await prisma.article.upsert({
      where:{slug:x.slug},
      update:{title:x.title,summary:x.summary,author:x.author||'SAP Practice Team',publishedDate:new Date(x.published_date),category:x.category,contentType:x.content_type,content:x.content,ctaLabel:x.cta_label||'Talk to an SAP Expert',sortOrder:x.order||0,metaTitle:x.meta_title||null,metaDescription:x.meta_description||null},
      create:{slug:x.slug,title:x.title,summary:x.summary,author:x.author||'SAP Practice Team',publishedDate:new Date(x.published_date),category:x.category,contentType:x.content_type,content:x.content,ctaLabel:x.cta_label||'Talk to an SAP Expert',sortOrder:x.order||0,metaTitle:x.meta_title||null,metaDescription:x.meta_description||null}
    });
    await prisma.articleServiceRelation.deleteMany({where:{articleId:article.id}});
    for(const slug of x.related_services||[]){
      const service=await prisma.service.findUnique({where:{slug}});
      if(service) await prisma.articleServiceRelation.create({data:{articleId:article.id,serviceId:service.id}});
    }
  }

  // Rebuild all cross-content relations after every entity exists. This makes
  // seeding independent of the order used in the canonical Django seed files.
  for (const x of services) {
    const from = await prisma.service.findUnique({ where: { slug: x.slug } });
    if (!from) continue;
    await prisma.serviceRelation.deleteMany({ where: { fromId: from.id } });
    for (const slug of x.related_services || []) {
      const to = await prisma.service.findUnique({ where: { slug } });
      if (to) await prisma.serviceRelation.create({ data: { fromId: from.id, toId: to.id } });
    }
  }

  for (const x of solutions) {
    const from = await prisma.solution.findUnique({ where: { slug: x.slug } });
    if (!from) continue;
    await prisma.solutionServiceRelation.deleteMany({ where: { solutionId: from.id } });
    for (const slug of x.related_services || []) {
      const service = await prisma.service.findUnique({ where: { slug } });
      if (service) await prisma.solutionServiceRelation.create({ data: { solutionId: from.id, serviceId: service.id } });
    }
    await prisma.solutionRelation.deleteMany({ where: { fromId: from.id } });
    for (const slug of x.related_solutions || []) {
      const to = await prisma.solution.findUnique({ where: { slug } });
      if (to) await prisma.solutionRelation.create({ data: { fromId: from.id, toId: to.id } });
    }
  }

  for (const x of industries) {
    const from = await prisma.industry.findUnique({ where: { slug: x.slug } });
    if (!from) continue;
    await prisma.industryServiceRelation.deleteMany({ where: { industryId: from.id } });
    for (const slug of x.related_services || []) {
      const service = await prisma.service.findUnique({ where: { slug } });
      if (service) await prisma.industryServiceRelation.create({ data: { industryId: from.id, serviceId: service.id } });
    }
  }

  for (const x of cases) {
    const from = await prisma.caseStudy.findUnique({ where: { slug: x.slug } });
    if (!from) continue;
    await prisma.caseStudyServiceRelation.deleteMany({ where: { caseStudyId: from.id } });
    for (const slug of x.related_services || []) {
      const service = await prisma.service.findUnique({ where: { slug } });
      if (service) await prisma.caseStudyServiceRelation.create({ data: { caseStudyId: from.id, serviceId: service.id } });
    }
  }

  for (const x of articles) {
    const from = await prisma.article.findUnique({ where: { slug: x.slug } });
    if (!from) continue;
    await prisma.articleServiceRelation.deleteMany({ where: { articleId: from.id } });
    for (const slug of x.related_services || []) {
      const service = await prisma.service.findUnique({ where: { slug } });
      if (service) await prisma.articleServiceRelation.create({ data: { articleId: from.id, serviceId: service.id } });
    }
  }

  const legalPages = read('legal.json');
  for (const x of legalPages) {
    await prisma.legalPage.upsert({
      where: { slug: x.slug },
      update: { title: x.title, content: x.content, metaTitle: x.meta_title || null, metaDescription: x.meta_description || null },
      create: { slug: x.slug, title: x.title, content: x.content, metaTitle: x.meta_title || null, metaDescription: x.meta_description || null },
    });
  }
  await prisma.appInitialization.create({ data: { id: 1 } });
  console.log('Database initialization and seed completed.');
}

main().catch(e=>{console.error(e);process.exit(1)}).finally(()=>prisma.$disconnect());
