import { ValidationPipe } from '@nestjs/common';
import { NestFactory } from '@nestjs/core';
import { ConfigService } from '@nestjs/config';
import { AppModule } from './app.module';
import * as express from 'express';
import * as path from 'path';
import * as fs from 'fs';
import { Request, Response, NextFunction } from 'express';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  const config = app.get(ConfigService);
  const port = Number(config.get('PORT') || 3000);
  const frontendDist = path.resolve(__dirname, process.env.FRONTEND_DIST_PATH || '../../frontend/dist');

  app.enableCors({
    origin: config.get('CORS_ORIGIN') || true,
    credentials: true,
  });
  app.setGlobalPrefix('api', { exclude: ['robots.txt', 'sitemap.xml'] });
  app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));

  await app.init();

  if (fs.existsSync(frontendDist)) {
    app.use(express.static(frontendDist, { index: 'index.html' }));

    app.use((req: Request, res: Response, next: NextFunction) => {
      if (
        req.path.startsWith('/api') ||
        req.path === '/robots.txt' ||
        req.path === '/sitemap.xml' ||
        path.extname(req.path)
      ) {
        return next();
      }

      const indexFile = path.join(frontendDist, 'index.html');
      if (fs.existsSync(indexFile)) {
        return res.sendFile(indexFile);
      }
      return next();
    });
  }

  await app.listen(port, '0.0.0.0');
}
bootstrap();
