import { Controller, Get } from "@nestjs/common";
import { ApiTags } from "@nestjs/swagger";

import { StatusType } from "src/common/types";

import { StatusService } from "./status.service";

@ApiTags("Status")
@Controller("status")
export class StatusController {
  constructor(private readonly statusService: StatusService) {}

  @Get()
  async status(): Promise<StatusType> {
    return this.statusService.get();
  }
}
