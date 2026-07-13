import React from "react";
import { View, StyleSheet } from "react-native";

export const Block: React.FC = () => <View style={styles.block} />;

const styles = StyleSheet.create({
  block: {
    backgroundColor: "#fff",
    height: 100,
    width: 100,
    borderRadius: 20,
  },
});
