import { triggerHaptic, withHaptic } from "@/lib/haptics";
import * as Haptics from "expo-haptics";

describe("lib/haptics", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe("triggerHaptic", () => {
    it("calls impactAsync with Light style by default", async () => {
      await triggerHaptic();
      expect(Haptics.impactAsync).toHaveBeenCalledWith(
        Haptics.ImpactFeedbackStyle.Light,
      );
    });

    it("calls impactAsync with correct style for each type", async () => {
      await triggerHaptic("light");
      expect(Haptics.impactAsync).toHaveBeenCalledWith(
        Haptics.ImpactFeedbackStyle.Light,
      );

      await triggerHaptic("medium");
      expect(Haptics.impactAsync).toHaveBeenCalledWith(
        Haptics.ImpactFeedbackStyle.Medium,
      );

      await triggerHaptic("heavy");
      expect(Haptics.impactAsync).toHaveBeenCalledWith(
        Haptics.ImpactFeedbackStyle.Heavy,
      );
    });

    it("does not throw when haptics fail", async () => {
      (Haptics.impactAsync as jest.Mock).mockRejectedValueOnce(
        new Error("not supported"),
      );
      await expect(triggerHaptic("light")).resolves.toBeUndefined();
    });
  });

  describe("withHaptic", () => {
    it("returns undefined when handler is undefined", () => {
      const result = withHaptic(undefined);
      expect(result).toBeUndefined();
    });

    it("returns a function that calls the original handler", () => {
      const handler = jest.fn();
      const wrapped = withHaptic(handler);
      wrapped?.("arg1", "arg2");
      expect(handler).toHaveBeenCalledWith("arg1", "arg2");
    });

    it("triggers haptic when wrapped function is called", () => {
      const handler = jest.fn();
      const wrapped = withHaptic(handler, "heavy");
      wrapped?.();
      expect(Haptics.impactAsync).toHaveBeenCalledWith(
        Haptics.ImpactFeedbackStyle.Heavy,
      );
    });

    it("returns the same value as the original handler", () => {
      const handler = jest.fn().mockReturnValue(42);
      const wrapped = withHaptic(handler);
      const result = wrapped?.();
      expect(result).toBe(42);
    });
  });
});
