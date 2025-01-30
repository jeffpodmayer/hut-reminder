import { View, Text, StyleSheet } from "react-native";

const SetReminderScreen = () => {
  return (
    <View style={styles.container}>
      <Text>Set Reminders Screen</Text>
    </View>
  );
};

export default SetReminderScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
});
