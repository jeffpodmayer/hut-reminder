import { View, Text, StyleSheet, TextInput } from "react-native";

const SetReminderScreen = () => {
  return (
    <View style={styles.container}>
      <View style={styles.emailContainer}>
        <Text style={styles.inputLabel}>Enter Email</Text>
        <TextInput
          style={styles.input}
          placeholder="Enter Email"
          clearButtonMode="while-editing"
          autoComplete="email"
          keyboardType="email-address"
        />
      </View>
      <View style={styles.dateContainer}>
        <Text style={styles.inputLabel}>Dates of Reminder</Text>
      </View>
    </View>
  );
};

export default SetReminderScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "flex-start",
    alignItems: "center",
  },
  emailContainer: {
    justifyContent: "center",
    alignItems: "center",
    paddingTop: 50,
  },
  inputLabel: {
    fontSize: 20,
    fontWeight: "bold",
  },
  input: {
    height: 40,
    width: 250,
    margin: 12,
    borderWidth: 1,
    padding: 10,
  },
  dateContainer: {
    marginTop: 15,
  },
});
