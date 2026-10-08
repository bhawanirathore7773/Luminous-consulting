import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class ContentService {
  constructor(private readonly prisma: PrismaService) {}

  services() { return this.prisma.service.findMany({ orderBy:{sortOrder:'asc'}, include:{listItems:true,relatedFrom:{include:{to:true}}} }); }
  service(slug:string) { return this.prisma.service.findUnique({where:{slug},include:{listItems:true,relatedFrom:{include:{to:true}}}}); }

  industries() { return this.prisma.industry.findMany({orderBy:{sortOrder:'asc'},include:{listItems:true}}); }
  industry(slug:string) { return this.prisma.industry.findUnique({where:{slug},include:{listItems:true,serviceRelations:{include:{service:true}}}}); }

  solutions() { return this.prisma.solution.findMany({orderBy:{sortOrder:'asc'},include:{listItems:true,serviceRelations:{include:{service:true}},relatedFrom:{include:{to:true}}}}); }
  solution(slug:string) { return this.prisma.solution.findUnique({where:{slug},include:{listItems:true,serviceRelations:{include:{service:true}},relatedFrom:{include:{to:true}}}}); }

  caseStudies() { return this.prisma.caseStudy.findMany({orderBy:{sortOrder:'asc'},include:{industry:true,relatedServices:{include:{service:true}}}}); }
  caseStudy(slug:string) { return this.prisma.caseStudy.findUnique({where:{slug},include:{industry:true,relatedServices:{include:{service:true}}}}); }

  insights() { return this.prisma.article.findMany({orderBy:{publishedDate:'desc'},include:{relatedServiceLinks:{include:{service:true}},relatedArticleFrom:{include:{to:true}}}}); }
  insight(slug:string) { return this.prisma.article.findUnique({where:{slug},include:{relatedServiceLinks:{include:{service:true}},relatedArticleFrom:{include:{to:true}}}}); }

  expertise() { return this.prisma.expertiseItem.findMany({orderBy:[{category:'asc'},{sortOrder:'asc'}]}); }
  team() { return this.prisma.teamMember.findMany({orderBy:[{category:'asc'},{sortOrder:'asc'}]}); }
  legal(slug:string) { return this.prisma.legalPage.findUnique({where:{slug}}); }
}
