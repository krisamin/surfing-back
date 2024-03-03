import { HttpModule } from "@nestjs/axios";
import { Module, forwardRef } from "@nestjs/common";
import { MongooseModule } from "@nestjs/mongoose";

import {
  User,
  UserSchema,
  Circle,
  CircleSchema,
  Submit,
  SubmitSchema,
} from "src/schemas";

import { StatusModule } from "../status/status.module";

import { CircleController } from "./circle.controller";
import { CircleService } from "./circle.service";

@Module({
  imports: [
    MongooseModule.forFeature([{ name: User.name, schema: UserSchema }]),
    MongooseModule.forFeature([{ name: Circle.name, schema: CircleSchema }]),
    MongooseModule.forFeature([{ name: Submit.name, schema: SubmitSchema }]),
    forwardRef(() => StatusModule),
    HttpModule,
  ],
  controllers: [CircleController],
  providers: [CircleService],
  exports: [CircleService],
})
export class CircleModule {}
