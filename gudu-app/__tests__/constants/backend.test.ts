import { content } from "@/constants/backend";

describe("constants/backend", () => {
  it("exports content as a string", () => {
    expect(typeof content).toBe("string");
  });

  it("contains HTTP lesson content", () => {
    expect(content).toContain("HTTP");
    expect(content).toContain("HyperText Transfer Protocol");
  });

  it("contains section headers", () => {
    expect(content).toContain("## What is HTTP?");
    expect(content).toContain("## Why does HTTP exist?");
    expect(content).toContain("## Core Concepts");
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
