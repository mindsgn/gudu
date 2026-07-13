import { typography } from "@/theme/typography";

describe("theme/typography", () => {
  it("exports all required typography tokens", () => {
    expect(typography).toHaveProperty("title");
    expect(typography).toHaveProperty("button");
    expect(typography).toHaveProperty("balance");
    expect(typography).toHaveProperty("subtitle");
    expect(typography).toHaveProperty("body");
    expect(typography).toHaveProperty("caption");
  });

  it("has valid font sizes for all tokens", () => {
    Object.entries(typography).forEach(([key, value]) => {
      expect(value.fontSize).toBeGreaterThan(0);
      expect(typeof value.fontSize).toBe("number");
    });
  });

  it("has valid font weights for all tokens", () => {
    Object.entries(typography).forEach(([key, value]) => {
      expect(value.fontWeight).toBeDefined();
      expect(typeof value.fontWeight).toBe("string");
    });
  });

  it("has fontFamily set to System for all tokens", () => {
    Object.entries(typography).forEach(([key, value]) => {
      expect(value.fontFamily).toBe("System");
    });
  });

  it("title has correct values", () => {
    expect(typography.title.fontSize).toBe(28);
    expect(typography.title.fontWeight).toBe("800");
  });

  it("body has correct values", () => {
    expect(typography.body.fontSize).toBe(14);
    expect(typography.body.fontWeight).toBe("400");
  });

  it("caption has correct values", () => {
    expect(typography.caption.fontSize).toBe(12);
    expect(typography.caption.fontWeight).toBe("400");
  });
});
