import { Body, Controller, Get, Post, Req, UseGuards } from "@nestjs/common";
import { ApiTags } from "@nestjs/swagger";
import { Request } from "express";

import { JwtAuthGuard } from "src/auth";

import { CircleDocument, SubmitDocument } from "src/schemas";

import { SubmitDto } from "./circle.dto";
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
}
