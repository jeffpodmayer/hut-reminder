import { View, Text, StyleSheet } from "react-native";

const ViewRemindersScreen = () => {
  return (
    <View style={styles.container}>
      <Text>View YOUR Reminders Screen</Text>
    </View>
  );
};

export default ViewRemindersScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
});
