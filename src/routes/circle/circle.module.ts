import { HttpModule } from "@nestjs/axios";
import { Module } from "@nestjs/common";
import { MongooseModule } from "@nestjs/mongoose";

import { Circle, CircleSchema } from "src/schemas";

import { CircleController } from "./circle.controller";
import { CircleService } from "./circle.service";

@Module({
  imports: [
    MongooseModule.forFeature([{ name: Circle.name, schema: CircleSchema }]),
    HttpModule,
  ],
  controllers: [CircleController],
  providers: [CircleService],
  exports: [CircleService],
})
export class FrigoModule {}
