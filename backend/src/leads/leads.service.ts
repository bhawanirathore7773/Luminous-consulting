import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateLeadDto } from './dto/create-lead.dto';

@Injectable()
export class LeadsService {
  constructor(private readonly prisma: PrismaService) {}

  create(dto: CreateLeadDto) {
    if (dto.website) return null;
    const { website, ...lead } = dto;
    return this.prisma.lead.create({
      data: {
        ...lead,
        source: 'contact_page',
      },
    });
  }
}
