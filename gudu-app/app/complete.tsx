import { StyleSheet, View, Text } from "react-native";
import { useRouter } from "expo-router";
import { useCallback, useState } from "react";
import { useFocusEffect } from "expo-router";
import * as Haptics from "expo-haptics";
import { AnimatedScrollProgress } from "@/shared/ui/micro-interactions/animated-scroll-progress";
import { useSharedValue } from "react-native-reanimated";
import { CircularProgress } from "@/shared/ui/organisms/circular-progress";
import { SymbolView } from "expo-symbols";
import { EnrichedMarkdownText } from "react-native-enriched-markdown";
import { content } from "@/constants/backend";

export default function Backend() {
  const router = useRouter();
  const [isReady, setReady] = useState<boolean>();

  useFocusEffect(
    useCallback(() => {
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy);

      return () => {
        Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Soft);
      };
    }, []),
  );

  return <View style={styles.container}></View>;
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "black",
    color: "white",
  },
});
