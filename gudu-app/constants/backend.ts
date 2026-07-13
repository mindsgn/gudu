import { curriculumSeed } from "@/constants/curriculum";

const backendCourse = curriculumSeed.courses.find(
  (course) => course.slug === "backend",
);

export const content =
  backendCourse?.modules[0]?.lessons[0]?.markdown ?? "";
