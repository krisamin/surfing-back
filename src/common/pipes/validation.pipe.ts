import { ValidationPipe as NestValidationPipe } from "@nestjs/common";

export const ValidationPipe = () => {
  return new NestValidationPipe({
    whitelist: true,
    transform: true,
  });
};
