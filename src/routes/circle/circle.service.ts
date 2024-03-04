import { createWriteStream, existsSync } from "fs";
import { join } from "path";

import { HttpService } from "@nestjs/axios";
import { HttpStatus, Inject, Injectable, forwardRef } from "@nestjs/common";
import { ConfigService } from "@nestjs/config";
import { InjectModel } from "@nestjs/mongoose";
import { Model, Types } from "mongoose";
import Sheets from "node-sheets";

import { Exception } from "src/common";

import {
  Circle,
  CircleDocument,
  Submit,
  SubmitDocument,
  UserDocument,
} from "src/schemas";

import { StatusService } from "../status/status.service";

import { AdminDto, FinalDto, SubmitDto } from "./circle.dto";

@Injectable()
export class CircleService {
  constructor(
    private readonly configService: ConfigService,
    private readonly httpService: HttpService,

    @InjectModel(Circle.name)
    private circleModel: Model<CircleDocument>,

    @InjectModel(Submit.name)
    private submitModel: Model<SubmitDocument>,

    @Inject(forwardRef(() => StatusService))
    private statusService: StatusService,
  ) {}

  async getCircle(id: Types.ObjectId): Promise<CircleDocument> {
    const circle = await this.circleModel.findById(id);
    if (!circle) throw new Exception(HttpStatus.NOT_FOUND, "circleNotFound");

    return circle;
  }

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
      const logoUrl = new URL(row["🌆 동아리 로고"]?.stringValue || "");
      const logoId = logoUrl.searchParams.get("id");
      if (logoId) {
        await this.download(logoId);
      }

      const circle = {
        email: row["이메일 주소"]?.stringValue || null,
        logo: logoUrl.searchParams.get("id") || null,
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

  async my(user: UserDocument): Promise<SubmitDocument[]> {
    const submit = await this.submitModel
      .find({
        user: new Types.ObjectId(user._id),
      })
      .populate("circle");

    const status = await this.statusService.get();
    switch (status) {
      case "FIRST": {
        return submit.map((s) => {
          s.status = "SUBMIT";
          return s;
        });
      }
      case "SECOND": {
        return submit.map((s) => {
          if (s.status === "SECOND" || s.status === "SECONDREJECT")
            s.status = "FIRST";
          return s;
        });
      }
      default: {
        return submit;
      }
    }
  }

  async submit(user: UserDocument, data: SubmitDto): Promise<SubmitDocument> {
    const circle = await this.circleModel.findById(data.circle);
    const userId = new Types.ObjectId(user._id);

    const exist = await this.submitModel.findOne({
      user: userId,
      circle: circle._id,
    });
    if (exist)
      throw new Exception(HttpStatus.BAD_REQUEST, "이미 제출하였습니다.");

    const exists = await this.submitModel.find({ user: userId });
    if (exists.length >= 3)
      throw new Exception(
        HttpStatus.BAD_REQUEST,
        "최대 3개까지만 제출 가능합니다.",
      );

    const submit = new this.submitModel({
      user: userId,
      circle: circle._id,
      question1: data.question1,
      question2: data.question2,
      question3: data.question3,
      question4: data.question4,
      status: "SUBMIT",
    });
    await submit.save();

    return submit;
  }

  async admin(
    user: UserDocument & {
      admin: Types.ObjectId;
    },
  ): Promise<SubmitDocument[]> {
    const admin = new Types.ObjectId(user.admin);
    if (!admin) return [];

    const submit = await this.submitModel
      .find({
        circle: admin,
      })
      .populate("user");

    return submit;
  }

  async first(
    user: UserDocument & {
      admin: Types.ObjectId;
    },
    data: AdminDto,
  ): Promise<SubmitDocument> {
    const admin = new Types.ObjectId(user.admin);
    if (!admin) new Exception(HttpStatus.BAD_REQUEST, "권한이 없습니다.");

    const submit = await this.submitModel.findById(data.submit);
    if (!submit) throw new Exception(HttpStatus.NOT_FOUND, "submitNotFound");

    if (["SUBMIT", "FIRST", "FIRSTREJECT"].includes(submit.status)) {
      submit.status = data.pass ? "FIRST" : "FIRSTREJECT";
      await submit.save();
    }

    return submit;
  }

  async second(
    user: UserDocument & {
      admin: Types.ObjectId;
    },
    data: AdminDto,
  ): Promise<SubmitDocument> {
    const admin = new Types.ObjectId(user.admin);
    if (!admin) new Exception(HttpStatus.BAD_REQUEST, "권한이 없습니다.");

    const submit = await this.submitModel.findById(data.submit);
    if (!submit) throw new Exception(HttpStatus.NOT_FOUND, "submitNotFound");

    if (["FIRST", "SECOND", "SECONDREJECT"].includes(submit.status)) {
      submit.status = data.pass ? "SECOND" : "SECONDREJECT";
      await submit.save();
    }

    return submit;
  }

  async final(user: UserDocument, data: FinalDto): Promise<SubmitDocument> {
    const userId = new Types.ObjectId(user._id);
    const submit = await this.submitModel.findOne({
      _id: data.submit,
      user: userId,
    });

    const exist = await this.submitModel.findOne({
      user: userId,
      status: "FINAL",
    });
    if (exist)
      throw new Exception(
        HttpStatus.BAD_REQUEST,
        "이미 최종 선택을 하였습니다.",
      );

    if (submit.status !== "SECOND")
      throw new Exception(
        HttpStatus.BAD_REQUEST,
        "최종 합격한 동아리만 최종 선택이 가능합니다.",
      );

    submit.status = "FINAL";
    await submit.save();

    return submit;
  }
}
