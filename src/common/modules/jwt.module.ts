import { Module } from "@nestjs/common";
import { JwtModule as NestJwtModule, JwtModuleOptions } from "@nestjs/jwt";

export const JwtOptions: JwtModuleOptions = {
  secret: process.env.JWT_SECRET,
  global: true,
  signOptions: {
    algorithm: "HS512",
  },
};

@Module({ imports: [NestJwtModule.register(JwtOptions)] })
export class JwtModule {}
