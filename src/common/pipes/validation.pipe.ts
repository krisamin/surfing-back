import { ValidationPipe as NestValidationPipe } from "@nestjs/common";

import { globalOpcode } from "../opcode";

export const ValidationPipe = () => {
  return new NestValidationPipe({
    whitelist: true,
    transform: true,
    exceptionFactory: (details) => globalOpcode.ValidateFailed({ details }),
  });
};
