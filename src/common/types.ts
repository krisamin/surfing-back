export const StatusList = [
  "SUBMIT",
  "FIRST",
  "SECOND",
  "FINAL",
  "EOL",
] as const;
export type StatusType = (typeof StatusList)[number];

export enum SubmitStatusEnum {
  SUBMIT = "SUBMIT",
  FIRST = "FIRST",
  FIRSTREJECT = "FIRSTREJECT",
  SECOND = "SECOND",
  SECONDREJECT = "SECONDREJECT",
  FINAL = "FINAL",
}
export type SubmitStatusType =
  | "SUBMIT"
  | "FIRST"
  | "FIRSTREJECT"
  | "SECOND"
  | "SECONDREJECT"
  | "FINAL";
