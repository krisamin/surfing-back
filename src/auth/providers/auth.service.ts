import { HttpService } from "@nestjs/axios";
import { Injectable, HttpStatus } from "@nestjs/common";
import { ConfigService } from "@nestjs/config";
import { JwtService } from "@nestjs/jwt";
import { InjectModel } from "@nestjs/mongoose";
import { Model, Types } from "mongoose";
import { firstValueFrom } from "rxjs";

import { Exception } from "src/common";

import { User, UserDocument, Token, TokenDocument } from "src/schemas";

import { TokenDto, TokensResponseDto } from "../dto";
import { OAuthPayload, Payload } from "../interface";

@Injectable()
export class AuthService {
  constructor(
    private readonly configService: ConfigService,
    private readonly jwtService: JwtService,
    private readonly httpService: HttpService,

    @InjectModel(User.name)
    private userModel: Model<UserDocument>,

    @InjectModel(Token.name)
    private tokenModel: Model<TokenDocument>,
  ) {}

  async getPublicKey(): Promise<string> {
    try {
      const publicKey = await firstValueFrom(
        this.httpService.get<string>("https://dimigo.in/auth/public"),
      );
      return publicKey.data;
    } catch (err) {
      throw new Exception(HttpStatus.INTERNAL_SERVER_ERROR, "publicKeyError");
    }
  }

  async decodeToken(token: string): Promise<OAuthPayload> {
    const publicKey = await this.getPublicKey();

    try {
      return await this.jwtService.verifyAsync(token, {
        secret: publicKey,
      });
    } catch (err) {
      throw new Exception(HttpStatus.BAD_REQUEST, "invalidToken");
    }
  }

  async login(token: string): Promise<TokensResponseDto> {
    const payload = await this.decodeToken(token);
    const { data } = payload;

    if (data.type != "student")
      throw new Exception(HttpStatus.BAD_REQUEST, "invalidUserType");

    const userData = {
      email: data.email,
      name: data.name,
      grade: data.studentId.grade,
      class: data.studentId.class,
      number: data.studentId.number,
    };
    console.log(userData);

    const user = await this.userModel.findOneAndUpdate(
      { email: userData.email },
      userData,
      {
        upsert: true,
        new: true,
      },
    );

    return await this.createToken(user._id);
  }

  async createToken(userId: Types.ObjectId): Promise<TokensResponseDto> {
    const user = await this.userModel.findById(userId).lean();

    const access = await this.jwtService.signAsync(
      { ...user, refresh: false },
      {
        expiresIn: "30m",
      },
    );

    const refresh = await this.jwtService.signAsync(
      { _id: userId, refresh: true },
      {
        expiresIn: "1y",
      },
    );

    await new this.tokenModel({
      user: userId,
      token: refresh,
    }).save();

    return {
      access,
      refresh,
    };
  }

  async removeRefreshToken(token: string): Promise<void> {
    await this.tokenModel.findOneAndDelete({
      token: token,
    });
  }

  async verifyRefreshToken(token: string): Promise<Payload> {
    try {
      const payload: Payload = await this.jwtService.verifyAsync(token, {
        secret: this.configService.get<string>("JWT_SECRET"),
      });
      if (!payload.refresh)
        throw new Exception(HttpStatus.BAD_REQUEST, "invalidRefreshToken");

      const clientToken = await this.tokenModel.findOne({ token }).lean();
      if (!clientToken)
        throw new Exception(HttpStatus.UNAUTHORIZED, "invalidRefreshToken");

      return payload;
    } catch (err) {
      if (err.name == "TokenExpiredError") {
        throw new Exception(HttpStatus.UNAUTHORIZED, "tokenExpired");
      }
      throw new Exception(HttpStatus.UNAUTHORIZED, "invalidRefreshToken");
    }
  }

  async refresh(data: TokenDto): Promise<TokensResponseDto> {
    const { _id: userId } = await this.verifyRefreshToken(data.token);
    await this.removeRefreshToken(data.token);

    return await this.createToken(userId);
  }

  async logout(data: TokenDto): Promise<string> {
    await this.removeRefreshToken(data.token);

    return "success";
  }
}
