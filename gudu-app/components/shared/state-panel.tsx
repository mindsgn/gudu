import { ActivityIndicator, StyleSheet, Text, View } from "react-native";
import { Button } from "@/components/shared/pressable-card";
import { colors } from "@/theme/colors";
import { typography } from "@/theme/typography";

type Props = {
  title: string;
  message: string;
  actionLabel?: string;
  onAction?: () => void;
  progress?: boolean;
  testID?: string;
};

export const StatePanel = ({
  title,
  message,
  actionLabel,
  onAction,
  progress = false,
  testID,
}: Props) => {
  return (
    <View testID={testID} style={styles.card}>
      <Text style={styles.title}>{title}</Text>
      <Text style={styles.message}>{message}</Text>
      {progress ? <ActivityIndicator color={colors.accent} /> : null}
      {actionLabel && onAction ? (
        <Button
          accessibilityLabel={actionLabel}
          label={actionLabel}
          onPress={onAction}
          width={240}
        />
      ) : null}
    </View>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.surface,
    borderRadius: 20,
    padding: 24,
    gap: 16,
  },
  title: {
    ...typography.subtitle,
    color: colors.buttonTextBackground,
  },
  message: {
    ...typography.body,
    color: colors.textSecondary,
    lineHeight: 22,
  },
});
