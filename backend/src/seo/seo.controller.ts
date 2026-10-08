import { Controller, Get, Res } from '@nestjs/common';
import { Response } from 'express';

@Controller()
export class SeoController {
  @Get('robots.txt')
  robots(@Res() res: Response) {
    res.type('text/plain').send('User-agent: *\nAllow: /\nSitemap: /sitemap.xml\n');
  }

  @Get('sitemap.xml')
  sitemap(@Res() res: Response) {
    const base = process.env.PUBLIC_URL || 'http://localhost:3000';
    const urls = ['', 'services/', 'solutions/', 'industries/', 'sap-expertise/', 'case-studies/', 'about/', 'insights/', 'contact/', 'assessment/', 'careers/', 'privacy-policy/', 'terms/', 'cookie-policy/', 'disclaimer/', 'accessibility/'];
    const xml = '<?xml version="1.0" encoding="UTF-8"?>' +
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
      urls.map(path => '<url><loc>' + base + '/' + path + '</loc></url>').join('') +
      '</urlset>';
    res.type('application/xml').send(xml);
  }
}
