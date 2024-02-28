import { UserDocument } from "src/schemas";

declare module "express" {
  interface Request {
    user?: UserDocument;
  }
}
