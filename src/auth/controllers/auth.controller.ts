import { Body, Controller, Get, Post, Query, Res } from "@nestjs/common";
import { ApiTags, ApiOperation, ApiOkResponse } from "@nestjs/swagger";
import { Response } from "express";

import { TokenDto, TokensResponseDto } from "../dto";
import { AuthService } from "../providers";

@ApiTags("Auth")
@Controller("auth")
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  @ApiOperation({ summary: "로그인" })
  @Get()
  async login(@Query("token") token: string, @Res() res: Response) {
    res.redirect(await this.authService.login(token));
  }

  @ApiOperation({ summary: "토큰 갱신" })
  @ApiOkResponse({ type: TokensResponseDto })
  @Post("refresh")
  async refresh(@Body() data: TokenDto): Promise<TokensResponseDto> {
    return await this.authService.refresh(data);
  }

  @ApiOperation({ summary: "로그아웃" })
  @ApiOkResponse({
    schema: {
      type: "string",
      example: "success",
    },
  })
  @Post("logout")
  async logout(@Body() data: TokenDto): Promise<string> {
    await this.authService.logout(data);
    return "success";
  }
}
