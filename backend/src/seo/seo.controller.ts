import { Controller, Get, Res } from '@nestjs/common';
import { Response } from 'express';
import { PrismaService } from '../prisma/prisma.service';

@Controller()
export class SeoController {
  constructor(private readonly prisma: PrismaService) {}

  @Get('robots.txt')
  robots(@Res() res: Response) {
    const base = process.env.PUBLIC_URL || 'http://localhost:3000';
    res.type('text/plain').send('User-agent: *\nAllow: /\nSitemap: ' + base + '/sitemap.xml\n');
  }

  @Get('sitemap.xml')
  async sitemap(@Res() res: Response) {
    const base = (process.env.PUBLIC_URL || 'http://localhost:3000').replace(/\/$/, '');
    const staticUrls = [
      '', 'services/', 'solutions/', 'industries/', 'sap-expertise/', 'case-studies/',
      'about/', 'about/team/', 'approach/', 'insights/', 'contact/', 'assessment/',
      'careers/', 'privacy-policy/', 'terms/', 'cookie-policy/', 'disclaimer/', 'accessibility/'
    ];
    const [services,solutions,industries,cases,articles] = await Promise.all([
      this.prisma.service.findMany({select:{slug:true}}),
      this.prisma.solution.findMany({select:{slug:true}}),
      this.prisma.industry.findMany({select:{slug:true}}),
      this.prisma.caseStudy.findMany({select:{slug:true}}),
      this.prisma.article.findMany({select:{slug:true}})
    ]);
    const dynamicUrls = [
      ...services.map(x => 'services/'+x.slug+'/'),
      ...solutions.map(x => 'solutions/'+x.slug+'/'),
      ...industries.map(x => 'industries/'+x.slug+'/'),
      ...cases.map(x => 'case-studies/'+x.slug+'/'),
      ...articles.map(x => 'insights/'+x.slug+'/')
    ];
    const urls = [...staticUrls,...dynamicUrls];
    const escapeXml = (value: string) => value.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&apos;');\n    const xml = '<?xml version="1.0" encoding="UTF-8"?>' +
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
      urls.map(p => '<url><loc>'+escapeXml(base+'/'+p)+'</loc></url>').join('') +
      '</urlset>';
    res.type('application/xml').send(xml);
  }
}
