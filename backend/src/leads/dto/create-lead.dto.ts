import { IsEmail, IsOptional, IsString, MaxLength } from 'class-validator';

export class CreateLeadDto {
  @IsOptional()
  @IsString()
  website?: string;
  @IsString() @MaxLength(120) name!: string;
  @IsEmail() @MaxLength(255) workEmail!: string;
  @IsString() @MaxLength(150) company!: string;
  @IsOptional() @IsString() @MaxLength(120) jobTitle?: string;
  @IsOptional() @IsString() @MaxLength(100) country?: string;
  @IsOptional() @IsString() @MaxLength(40) phone?: string;
  @IsOptional() @IsString() @MaxLength(30) sapEnvironment?: string;
  @IsOptional() @IsString() @MaxLength(200) currentSapSystem?: string;
  @IsOptional() @IsString() @MaxLength(300) requiredServices?: string;
  @IsOptional() @IsString() @MaxLength(30) projectStage?: string;
  @IsOptional() @IsString() @MaxLength(30) timeline?: string;
  @IsOptional() @IsString() @MaxLength(30) estimatedScope?: string;
  @IsOptional() @IsString() message?: string;
}
