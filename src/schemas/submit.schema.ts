import { Prop, Schema, SchemaFactory } from "@nestjs/mongoose";
import { ApiProperty, ApiExtraModels, getSchemaPath } from "@nestjs/swagger";
import { HydratedDocument, Types } from "mongoose";

import { SubmitStatusEnum, SubmitStatusType } from "src/common/types";

import { Circle, User } from "src/schemas";

import { schemaOptions } from "./options";

export type SubmitDocument = HydratedDocument<Submit>;
@Schema({
  ...schemaOptions,
  timestamps: {
    createdAt: true,
    updatedAt: false,
  },
})
@ApiExtraModels(User)
export class Submit {
  @ApiProperty({
    oneOf: [{ $ref: getSchemaPath(User) }],
  })
  @Prop({
    required: true,
    type: Types.ObjectId,
    ref: "User",
  })
  user: Types.ObjectId;

  @ApiProperty({
    oneOf: [{ $ref: getSchemaPath(Circle) }],
  })
  @Prop({
    required: true,
    type: Types.ObjectId,
    ref: "Circle",
  })
  circle: Types.ObjectId;

  @ApiProperty()
  @Prop({
    required: true,
    type: String,
    maxlength: 300,
  })
  question1: string;

  @ApiProperty()
  @Prop({
    required: true,
    type: String,
    maxlength: 300,
  })
  question2: string;

  @ApiProperty()
  @Prop({
    required: true,
    type: String,
    maxlength: 300,
  })
  question3: string;

  @ApiProperty()
  @Prop({
    required: true,
    type: String,
    maxlength: 300,
  })
  question4: string;

  @ApiProperty()
  @Prop({
    required: true,
    type: String,
    enum: SubmitStatusEnum,
  })
  status: SubmitStatusType;
}

export const SubmitSchema = SchemaFactory.createForClass(Submit);
