import { HttpException } from "@nestjs/common";

export class Exception extends HttpException {
  constructor(status: number, message: string, data?: any) {
    super(
      {
        status,
        message,
        data,
      },
      status,
    );
  }
}
