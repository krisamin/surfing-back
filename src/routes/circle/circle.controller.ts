import { Controller, Get } from "@nestjs/common";
import { ApiTags } from "@nestjs/swagger";

import { CircleDocument } from "src/schemas";

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
}
