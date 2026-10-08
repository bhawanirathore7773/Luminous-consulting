import { Controller, Get, Param } from '@nestjs/common';
import { ContentService } from './content.service';

@Controller()
export class ContentController {
  constructor(private readonly content: ContentService) {}

  @Get('services') services() { return this.content.services(); }
  @Get('services/:slug') service(@Param('slug') slug: string) { return this.content.service(slug); }

  @Get('industries') industries() { return this.content.industries(); }
  @Get('industries/:slug') industry(@Param('slug') slug: string) { return this.content.industry(slug); }

  @Get('solutions') solutions() { return this.content.solutions(); }
  @Get('solutions/:slug') solution(@Param('slug') slug: string) { return this.content.solution(slug); }

  @Get('case-studies') caseStudies() { return this.content.caseStudies(); }
  @Get('case-studies/:slug') caseStudy(@Param('slug') slug: string) { return this.content.caseStudy(slug); }

  @Get('insights') insights() { return this.content.insights(); }
  @Get('insights/:slug') insight(@Param('slug') slug: string) { return this.content.insight(slug); }

  @Get('sap-expertise') expertise() { return this.content.expertise(); }
  @Get('team') team() { return this.content.team(); }

  @Get(':slug') legal(@Param('slug') slug: string) { return this.content.legal(slug); }
}
