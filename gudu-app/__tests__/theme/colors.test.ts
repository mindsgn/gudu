import { colors } from "@/theme/colors";

describe("theme/colors", () => {
  it("exports all required color tokens", () => {
    expect(colors).toHaveProperty("background");
    expect(colors).toHaveProperty("surface");
    expect(colors).toHaveProperty("buttonBackground");
    expect(colors).toHaveProperty("buttonTextBackground");
    expect(colors).toHaveProperty("primary");
    expect(colors).toHaveProperty("primaryMuted");
    expect(colors).toHaveProperty("accent");
    expect(colors).toHaveProperty("danger");
    expect(colors).toHaveProperty("textPrimary");
    expect(colors).toHaveProperty("textSecondary");
    expect(colors).toHaveProperty("border");
  });

  it("has valid hex color values", () => {
    const hexRegex = /^#[0-9A-Fa-f]{6}$/;
    Object.entries(colors).forEach(([key, value]) => {
      expect(value).toMatch(hexRegex);
    });
  });

  it("has correct values", () => {
    expect(colors.background).toBe("#F2F4F5");
    expect(colors.surface).toBe("#15161A");
    expect(colors.primary).toBe("#16A34A");
    expect(colors.danger).toBe("#EF4444");
  });
});
