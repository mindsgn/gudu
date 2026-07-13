import {
  clampScrollPercent,
  getDefaultLessonStatus,
  getProgressStatusForUpdate,
  isLessonOpenable,
} from "@/lib/lesson-progress";

describe("lib/lesson-progress", () => {
  it("clamps scroll percent into the valid range", () => {
    expect(clampScrollPercent(-12)).toBe(0);
    expect(clampScrollPercent(101)).toBe(100);
  });

  it("derives unlocked status for the first lesson only", () => {
    expect(getDefaultLessonStatus(1)).toBe("unlocked");
    expect(getDefaultLessonStatus(2)).toBe("locked");
  });

  it("marks partial progress as in progress", () => {
    expect(
      getProgressStatusForUpdate({
        currentStatus: "unlocked",
        nextScrollPercent: 42,
      }),
    ).toBe("in_progress");
  });

  it("never unlocks a locked lesson through scroll updates", () => {
    expect(
      getProgressStatusForUpdate({
        currentStatus: "locked",
        nextScrollPercent: 52,
      }),
    ).toBe("locked");
  });

  it("treats completed lessons as openable", () => {
    expect(isLessonOpenable("completed")).toBe(true);
    expect(isLessonOpenable("locked")).toBe(false);
  });
});
