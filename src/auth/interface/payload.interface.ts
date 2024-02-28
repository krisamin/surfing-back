import { Types } from "mongoose";

export interface Payload {
  _id: Types.ObjectId;
  refresh: boolean;
}

export interface OAuthPayload {
  data: {
    type: string;
    email: string;
    name: string;
    studentId: {
      grade: number;
      class: number;
      number: number;
    };
  };
}
