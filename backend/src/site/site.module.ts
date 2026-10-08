import { Module } from '@nestjs/common';
import { SiteController } from './site.controller';
import { PrismaModule } from '../prisma/prisma.module';

@Module({
  imports: [PrismaModule],
  controllers: [SiteController],
})
export class SiteModule {}
