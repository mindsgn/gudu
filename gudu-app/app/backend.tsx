import {
  StyleSheet,
  View,
  Text,
  ActivityIndicator,
  FlatListComponent,
  Dimensions,
} from "react-native";
import { useRouter } from "expo-router";
import { useCallback, useState, useEffect } from "react";
import { useFocusEffect } from "expo-router";
import * as Haptics from "expo-haptics";
import { AnimatedHeaderScrollView } from "@/shared/ui/organisms/animated-header-scrollview";
import { FlashList } from "@shopify/flash-list";
import { Button } from "@/components/shared/pressable-card";

const backendCourse = [
  { title: "HTTP" },
  { title: "API" },
  { title: "Authentication" },
  { title: "Database" },
  { title: "Caching" },
  { title: "Queues & Background" },
  { title: "Event Driven" },
  { title: "Distrubitated" },
  { title: "Monitoring & Observalibilty" },
  { title: "Security" },
  { title: "Deployment & Infrustracture" },
];

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

  return (
    <AnimatedHeaderScrollView
      largeTitle={"Backend"}
      subtitle="Backend First Principals"
    >
      <FlashList
        data={backendCourse}
        renderItem={(data) => {
          const { item } = data;
          return (
            <Button
              width={Dimensions.get("screen").width - 30}
              label={`${item.title}`}
              backgroundColor="black"
              color="white"
              onPress={() => {
                router.replace({ pathname: `/lesson` });
              }}
            />
          );
        }}
      />
    </AnimatedHeaderScrollView>
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
