import { Body, Controller, Get, Post, Req, UseGuards } from "@nestjs/common";
import { ApiTags } from "@nestjs/swagger";
import { Request } from "express";
import { Types } from "mongoose";

import { JwtAuthGuard } from "src/auth";

import { CircleDocument, SubmitDocument, UserDocument } from "src/schemas";

import { AdminDto, FinalDto, SubmitDto } from "./circle.dto";
import { CircleService } from "./circle.service";

@ApiTags("Circle")
@Controller("circle")
export class CircleController {
  constructor(private readonly circleService: CircleService) {}

  @Get()
  async get(): Promise<CircleDocument[]> {
    return this.circleService.get();
  }

  @Get("update")
  async refresh(): Promise<string> {
    return this.circleService.refresh();
  }

  @UseGuards(JwtAuthGuard)
  @Get("my")
  async my(@Req() req: Request): Promise<SubmitDocument[]> {
    return await this.circleService.my(req.user);
  }

  @UseGuards(JwtAuthGuard)
  @Post("submit")
  async submit(
    @Req() req: Request,
    @Body() data: SubmitDto,
  ): Promise<SubmitDocument> {
    return await this.circleService.submit(req.user, data);
  }

  @UseGuards(JwtAuthGuard)
  @Get("admin")
  async admin(@Req() req: Request): Promise<SubmitDocument[]> {
    return await this.circleService.admin(
      req.user as UserDocument & {
        admin: Types.ObjectId;
      },
    );
  }

  @UseGuards(JwtAuthGuard)
  @Post("first")
  async first(
    @Req() req: Request,
    @Body() data: AdminDto,
  ): Promise<SubmitDocument> {
    return await this.circleService.first(
      req.user as UserDocument & {
        admin: Types.ObjectId;
      },
      data,
    );
  }

  @UseGuards(JwtAuthGuard)
  @Post("second")
  async second(
    @Req() req: Request,
    @Body() data: AdminDto,
  ): Promise<SubmitDocument> {
    return await this.circleService.second(
      req.user as UserDocument & {
        admin: Types.ObjectId;
      },
      data,
    );
  }

  @UseGuards(JwtAuthGuard)
  @Post("final")
  async final(
    @Req() req: Request,
    @Body() data: FinalDto,
  ): Promise<SubmitDocument> {
    return await this.circleService.final(req.user as UserDocument, data);
  }
}
