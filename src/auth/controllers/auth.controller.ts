import { Body, Controller, Get, Post, Query } from "@nestjs/common";
import { ApiTags, ApiOperation, ApiOkResponse } from "@nestjs/swagger";

import { TokenDto, TokensResponseDto } from "../dto";
import { AuthService } from "../providers";

@ApiTags("Auth")
@Controller("auth")
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  @ApiOperation({ summary: "로그인" })
  @ApiOkResponse({ type: TokensResponseDto })
  @Get()
  async login(@Query("token") token: string): Promise<TokensResponseDto> {
    return await this.authService.login(token);
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
