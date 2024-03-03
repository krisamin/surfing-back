import { HttpModule } from "@nestjs/axios";
import { Module } from "@nestjs/common";
import { MongooseModule } from "@nestjs/mongoose";
import { PassportModule } from "@nestjs/passport";

import { ConfigModule, JwtModule } from "src/common";

import {
  User,
  UserSchema,
  Token,
  TokenSchema,
  Circle,
  CircleSchema,
} from "src/schemas";

import { AuthController } from "./controllers/auth.controller";
import { AuthService } from "./providers/auth.service";
import { JwtStrategy } from "./strategies";

@Module({
  imports: [
    MongooseModule.forFeature([
      { name: User.name, schema: UserSchema },
      { name: Token.name, schema: TokenSchema },
      { name: Circle.name, schema: CircleSchema },
    ]),
    ConfigModule,
    JwtModule,
    PassportModule,
    HttpModule,
  ],
  controllers: [AuthController],
  providers: [AuthService, JwtStrategy],
  exports: [AuthService],
})
export class AuthModule {}
