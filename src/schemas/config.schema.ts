import { Prop, Schema, SchemaFactory } from "@nestjs/mongoose";
import { ApiProperty } from "@nestjs/swagger";
import { HydratedDocument } from "mongoose";

import { schemaOptions } from "./options";

export type ConfigDocument = HydratedDocument<Config>;
@Schema({
  ...schemaOptions,
})
export class Config {
  @ApiProperty()
  @Prop({
    required: true,
    type: String,
  })
  name: string;

  @ApiProperty()
  @Prop({
    required: true,
    type: String,
  })
  value: string;
}

export const ConfigSchema = SchemaFactory.createForClass(Config);
