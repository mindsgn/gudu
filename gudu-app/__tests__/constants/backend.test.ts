import { content } from "@/constants/backend";

describe("constants/backend", () => {
  it("exports content as a string", () => {
    expect(typeof content).toBe("string");
  });

  it("contains normalized backend lesson content", () => {
    expect(content).toContain("How Computers Represent Information");
    expect(content).toContain("Estimated study time");
  });

  it("contains section headers", () => {
    expect(content).toContain("## 1. Chapter Introduction");
    expect(content).toContain("## 2. Fundamental Concepts");
    expect(content).toContain("## 13. Summary");
  });

  it("is a non-empty string", () => {
    expect(content.length).toBeGreaterThan(0);
  });

  it("contains markdown formatting", () => {
    expect(content).toContain("#");
    expect(content).toContain("```");
    expect(content).toContain("**");
  });
});
