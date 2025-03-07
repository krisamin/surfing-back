import os from "os";

import { Injectable, Logger } from "@nestjs/common";
import _ from "lodash";

import { ClusterDto, Deployment } from "src/common";

@Injectable()
export class AppService {
  private cluster: ClusterDto;
  private readonly logger = new Logger(AppService.name);

  private DisplayMode = {
    development: "Development Mode",
    production: "Production Mode",
  };

  async onModuleInit() {
    await this.getBackendInfo();
    this.logger.log(`Package name: ${this.cluster.name}`);
    this.logger.log(`Package version: ${this.cluster.version}`);
    this.logger.log(`Package description: ${this.cluster.description}`);
    this.logger.log(`Package author: ${this.cluster.author}`);
    this.logger.log(`Cluster name: ${this.cluster.hostname}`);
    this.logger.log(`Cluster mode: ${this.DisplayMode[this.cluster.mode]}`);
  }

  async getBackendInfo(): Promise<ClusterDto> {
    if (this.cluster) return this.cluster;

    const packageFile = await import(`${process.cwd()}/package.json`);
    const packageInfo = _.pick(packageFile, [
      "name",
      "version",
      "description",
      "author",
    ]);

    const hostname = os.hostname();
    const mode = (process.env.NODE_ENV as Deployment) || "development";

    this.cluster = { ...packageInfo, hostname, mode };
    return this.cluster;
  }
}
