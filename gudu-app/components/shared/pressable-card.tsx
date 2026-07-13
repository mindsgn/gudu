import React from "react";
import { ActivityIndicator, Pressable, StyleSheet, Text } from "react-native";
import { colors } from "@/theme/colors";
import { typography } from "@/theme/typography";
import * as Haptics from "expo-haptics";

export const Button: React.FC<{
  label: string;
  onPress: () => void;
  width?: number;
  testID?: string;
  accessibilityLabel?: string;
  progress?: boolean;
  disabled?: boolean;
  backgroundColor?: string;
  color?: string;
}> = ({
  label,
  onPress,
  width = 150,
  testID,
  accessibilityLabel,
  progress = false,
  disabled = false,
  backgroundColor = colors.buttonBackground,
  color = colors.buttonTextBackground,
}) => (
  <Pressable
    testID={testID}
    accessibilityLabel={accessibilityLabel ?? label}
    accessibilityRole="button"
    accessibilityState={{ disabled }}
    disabled={disabled || progress}
    style={[
      styles.button,
      {
        width,
        backgroundColor,
        opacity: disabled ? 0.55 : 1,
      },
    ]}
    onPress={onPress}
    onPressIn={() => {
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy);
    }}
    onPressOut={() => {
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Rigid);
    }}
  >
    {progress ? (
      <ActivityIndicator />
    ) : (
      <Text
        style={[
          styles.buttonText,
          {
            color,
          },
        ]}
      >
        {label}
      </Text>
    )}
  </Pressable>
);

const styles = StyleSheet.create({
  button: {
    marginTop: 8,
    borderRadius: 20,
    paddingVertical: 20,
    paddingHorizontal: 20,
    alignItems: "flex-start",
    alignSelf: "center",
  },
  buttonText: {
    ...typography.button,
    fontWeight: "700",
  },
});
