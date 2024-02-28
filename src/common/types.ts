export enum UserEnum {
  ADMIN = "admin",
  STUDENT = "student",
  TEACHER = "teacher",
}
export type UserType = "admin" | "student" | "teacher";

export enum GenderEnum {
  MALE = "male",
  FEMALE = "female",
}
export type GenderType = "male" | "female";

export enum GradeEnum {
  GRADE1 = 1,
  GRADE2 = 2,
  GRADE3 = 3,
}
export type GradeType = 1 | 2 | 3;

export enum ClassEnum {
  CLASS1 = 1,
  CLASS2 = 2,
  CLASS3 = 3,
  CLASS4 = 4,
  CLASS5 = 5,
  CLASS6 = 6,
}
export type ClassType = 1 | 2 | 3 | 4 | 5 | 6;

export enum ApplicationEnum {
  INTERNAL = "internal",
  EXTERNAL = "external",
}
export type ApplicationType = "internal" | "external";
