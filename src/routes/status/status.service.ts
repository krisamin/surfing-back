import { Injectable } from "@nestjs/common";
import { InjectModel } from "@nestjs/mongoose";
import { Model } from "mongoose";

import { StatusList, StatusType } from "src/common/types";

import { Config, ConfigDocument } from "src/schemas";

@Injectable()
export class StatusService {
  constructor(
    @InjectModel(Config.name)
    private ConfigModel: Model<ConfigDocument>,
  ) {}

  async get(): Promise<StatusType> {
    const status = await this.ConfigModel.findOne({ key: "status" });
    const statusValue = (status?.value || "EOL") as StatusType;

    if (!StatusList.includes(statusValue)) return "EOL";
    return statusValue;
  }
}
