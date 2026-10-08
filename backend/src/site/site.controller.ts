import { Controller, Get } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { siteConstants } from './site.constants';

@Controller('site')
export class SiteController {
  constructor(private readonly prisma: PrismaService) {}

  @Get('home')
  async home() {
    const [services, industries, caseStudies] = await Promise.all([
      this.prisma.service.findMany({ where: { featured: true }, orderBy: { sortOrder: 'asc' }, take: 8 }),
      this.prisma.industry.findMany({ orderBy: { sortOrder: 'asc' }, take: 6 }),
      this.prisma.caseStudy.findMany({ orderBy: { sortOrder: 'asc' }, take: 3 }),
    ]);

    return {
      siteName: siteConstants.siteName,
      services,
      industries,
      caseStudies,
      outcomes: siteConstants.outcomes,
      capabilities: siteConstants.capabilities,
      problemOptions: siteConstants.problemOptions,
    };
  }
}
