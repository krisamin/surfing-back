import { Prop, Schema, SchemaFactory } from "@nestjs/mongoose";
import { ApiProperty } from "@nestjs/swagger";
import { HydratedDocument } from "mongoose";

import { schemaOptions } from "./options";

export type CircleDocument = HydratedDocument<Circle>;
@Schema({
  ...schemaOptions,
})
export class Circle {
  @ApiProperty()
  @Prop({
    required: true,
    type: String,
  })
  email: string;

  @ApiProperty()
  @Prop({
    required: true,
    type: String,
  })
  logo: string;

  @ApiProperty()
  @Prop({
    required: true,
    type: String,
  })
  name: string;

  @ApiProperty()
  @Prop({
    required: false,
    type: String,
  })
  slogun: string;

  @ApiProperty()
  @Prop({
    required: true,
    type: String,
  })
  category: string;

  @ApiProperty()
  @Prop({
    required: true,
    type: String,
  })
  introducing: string;

  @ApiProperty()
  @Prop({
    required: false,
    type: String,
  })
  history: string;

  @ApiProperty()
  @Prop({
    required: false,
    type: String,
  })
  award: string;

  @ApiProperty()
  @Prop({
    required: false,
    type: String,
  })
  video: string;

  @ApiProperty()
  @Prop({
    required: false,
    type: String,
  })
  instagram: string;

  @ApiProperty()
  @Prop({
    required: false,
    type: String,
  })
  website: string;
}

export const CircleSchema = SchemaFactory.createForClass(Circle);
