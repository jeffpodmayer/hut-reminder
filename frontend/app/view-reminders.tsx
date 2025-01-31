import { View, Text, StyleSheet, TextInput } from "react-native";

const ViewRemindersScreen = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>View Your Reminders</Text>
      <TextInput
        style={styles.input}
        placeholder="Search reminders..."
        placeholderTextColor="#666"
      />
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
  title: {
    fontSize: 24,
    fontWeight: "bold",
  },
  input: {
    width: "80%",
    height: 40,
    borderWidth: 1,
    borderColor: "#ccc",
    borderRadius: 5,
    padding: 10,
    marginTop: 20,
  },
});
