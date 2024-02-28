import { Prop, Schema, SchemaFactory } from "@nestjs/mongoose";
import { ApiProperty } from "@nestjs/swagger";
import { HydratedDocument } from "mongoose";

import { schemaOptions } from "./options";

export type UserDocument = HydratedDocument<User>;
@Schema({
  ...schemaOptions,
})
export class User {
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
  name: string;

  @ApiProperty()
  @Prop({
    required: false,
    type: Number,
  })
  grade: number;

  @ApiProperty()
  @Prop({
    required: false,
    type: Number,
  })
  class: number;

  @ApiProperty()
  @Prop({
    required: false,
    type: Number,
  })
  number: number;
}

export const UserSchema = SchemaFactory.createForClass(User);
