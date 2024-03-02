export const StatusList = [
  "SUBMIT",
  "FIRST",
  "SECOND",
  "FINAL",
  "EOL",
] as const;
export type StatusType = (typeof StatusList)[number];
