import { StyleSheet, View, ActivityIndicator } from "react-native";
import { useRouter } from "expo-router";
import { useCallback, useState, useEffect } from "react";
import { useFocusEffect } from "expo-router";
import * as Haptics from "expo-haptics";
import { Block } from "@/shared/ui/organisms/block";

export default function Splash() {
  const router = useRouter();
  const [isReady, setReady] = useState<boolean>(false);

  useFocusEffect(
    useCallback(() => {
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy);

      return () => {
        Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Soft);
      };
    }, []),
  );

  useEffect(() => {
    isReady ? router.replace("/home") : null;

    setTimeout(() => {
      setReady(true);
    }, 2000);
  }, [isReady]);

  return (
    <View style={styles.container}>
      <Block
        width={50}
        height={50}
        borderRadius={0}
        borderWidth={4}
        speed={1}
        base={"#333340"}
        glow={"#c0c8e0"}
        background={"#000"}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "black",
  },
});
