import { createWriteStream, existsSync } from "fs";
import { join } from "path";

import { HttpService } from "@nestjs/axios";
import { Injectable } from "@nestjs/common";
import { ConfigService } from "@nestjs/config";
import { InjectModel } from "@nestjs/mongoose";
import { Model } from "mongoose";
import Sheets from "node-sheets";

import { Circle, CircleDocument } from "src/schemas";

@Injectable()
export class CircleService {
  constructor(
    private readonly configService: ConfigService,
    private readonly httpService: HttpService,

    @InjectModel(Circle.name)
    private circleModel: Model<CircleDocument>,
  ) {}

  async get(): Promise<CircleDocument[]> {
    return await this.circleModel.find();
  }

  async download(id: string): Promise<void> {
    const path = join(process.cwd(), "public/assets", id);
    if (existsSync(path)) return;
    const writer = createWriteStream(path);
    const response = await this.httpService.axiosRef({
      url: "https://drive.usercontent.google.com/download?id=" + id,
      method: "GET",
      responseType: "stream",
    });
    response.data.pipe(writer);
  }

  async refresh(): Promise<string> {
    const gs = new Sheets("1v83EQMKi-FkLcgLov2MP9Iel6UfeOERtrQ90-6J_ozE");
    await gs.authorizeApiKey(this.configService.get("GOOGLE_SHEET_KEY"));
    const tables = await gs.tables("설문지 응답 시트1!A:O");

    for (const row of tables.rows) {
      if (row["이메일 주소"]?.stringValue === undefined) continue;
      console.log(row);
      const iconUrl = new URL(row["🌆 동아리 로고"]?.stringValue || "");
      const iconId = iconUrl.searchParams.get("id");
      if (iconId) {
        await this.download(iconId);
      }

      const circle = {
        email: row["이메일 주소"]?.stringValue || null,
        icon: iconUrl.searchParams.get("id") || null,
        name: row["😎 동아리 이름"]?.stringValue || null,
        slogun: row["🔫 동아리 슬로건"]?.stringValue || null,
        category: row["🪪 동아리 카테고리"]?.stringValue || null,
        introducing: row["📝 동아리 소개"]?.stringValue || null,
        history: row["🎧 활동 내역"]?.stringValue || null,
        award: row["🏆 수상 내역"]?.stringValue || null,
        video: row["🎥 동아리 홍보 영상(Youtube URL)"]?.stringValue || null,
        instagram: row["📷 인스타그램(URL)"]?.stringValue
          ? row["📷 인스타그램(URL)"].stringValue.split("?")[0]
          : null,
        website: row["🛜 동아리 웹 사이트(URL)"]?.stringValue
          ? row["🛜 동아리 웹 사이트(URL)"].stringValue.startsWith("http")
            ? row["🛜 동아리 웹 사이트(URL)"].stringValue.split("?")[0]
            : `http://${row["🛜 동아리 웹 사이트(URL)"].stringValue.split("?")[0]}`
          : null,
      };

      await this.circleModel.updateOne({ email: circle.email }, circle, {
        upsert: true,
      });
    }

    return "success";
  }
}
