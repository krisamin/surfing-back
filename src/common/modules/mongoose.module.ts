import { Module } from "@nestjs/common";
import { ConfigService } from "@nestjs/config";
import {
  MongooseModule as NestMongooseModule,
  MongooseModuleAsyncOptions,
} from "@nestjs/mongoose";

import { ConfigModule } from "./config.module";

export const Mongooseoptions: MongooseModuleAsyncOptions = {
  imports: [ConfigModule],
  useFactory: async (configService: ConfigService) => ({
    uri: configService.get<string>("MONGO_URI"),
    dbName: "surfing",

    connectionFactory: (connection) => {
      return connection;
    },
  }),
  inject: [ConfigService],
};

@Module({ imports: [NestMongooseModule.forRootAsync(Mongooseoptions)] })
export class MongooseModule {}
