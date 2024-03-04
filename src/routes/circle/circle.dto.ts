import { IsMongoId } from "class-validator";
import { IsBoolean, IsString } from "nestjs-swagger-dto";

export class SubmitDto {
  @IsString({
    description: "동아리 ID",
  })
  @IsMongoId()
  circle: string;

  @IsString({
    description: "질문1",
    minLength: 1,
    maxLength: 300,
  })
  question1: string;

  @IsString({
    description: "질문2",
    minLength: 1,
    maxLength: 300,
  })
  question2: string;

  @IsString({
    description: "질문3",
    minLength: 1,
    maxLength: 300,
  })
  question3: string;

  @IsString({
    description: "질문4",
    minLength: 1,
    maxLength: 300,
  })
  question4: string;
}

export class AdminDto {
  @IsString({
    description: "서류 ID",
  })
  @IsMongoId()
  submit: string;

  @IsBoolean({
    description: "합격 여부",
  })
  pass: boolean;
}

export class FinalDto {
  @IsString({
    description: "서류 ID",
  })
  @IsMongoId()
  submit: string;
}
