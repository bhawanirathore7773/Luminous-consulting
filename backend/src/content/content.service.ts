import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class ContentService {
  constructor(private readonly prisma: PrismaService) {}

  services() {
    return this.prisma.service.findMany({
      orderBy: { sortOrder: 'asc' },
      include: { listItems: true, faqs: true },
    });
  }

  service(slug: string) {
    return this.prisma.service.findUnique({
      where: { slug },
      include: { listItems: true, faqs: true, relatedFrom: { include: { to: true } } },
    });
  }

  industries() {
    return this.prisma.industry.findMany({
      orderBy: { sortOrder: 'asc' },
      include: { listItems: true, faqs: true },
    });
  }

  industry(slug: string) {
    return this.prisma.industry.findUnique({
      where: { slug },
      include: { listItems: true, faqs: true, serviceRelations: { include: { service: true } } },
    });
  }

  solutions() {
    return this.prisma.solution.findMany({
      orderBy: { sortOrder: 'asc' },
      include: { faqs: true, serviceRelations: { include: { service: true } } },
    });
  }

  solution(slug: string) {
    return this.prisma.solution.findUnique({
      where: { slug },
      include: { faqs: true, serviceRelations: { include: { service: true } } },
    });
  }

  caseStudies() {
    return this.prisma.caseStudy.findMany({ orderBy: { sortOrder: 'asc' } });
  }

  caseStudy(slug: string) {
    return this.prisma.caseStudy.findUnique({ where: { slug } });
  }

  insights() {
    return this.prisma.article.findMany({
      orderBy: { publishedDate: 'desc' },
    });
  }

  insight(slug: string) {
    return this.prisma.article.findUnique({ where: { slug } });
  }

  expertise() {
    return this.prisma.expertiseItem.findMany({ orderBy: [{ category: 'asc' }, { sortOrder: 'asc' }] });
  }

  team() {
    return this.prisma.teamMember.findMany({ orderBy: [{ category: 'asc' }, { sortOrder: 'asc' }] });
  }

  legal(slug: string) {
    return this.prisma.legalPage.findUnique({ where: { slug } });
  }
}
