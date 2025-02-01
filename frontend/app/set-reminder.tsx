import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  Alert,
} from "react-native";
import DateTimePicker from "react-native-ui-datepicker";
import dayjs from "dayjs";
import { useState } from "react";

const SetReminderScreen = () => {
  const [email, setEmail] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);
  const [emailError, setEmailError] = useState<string>("");

  const [dateRange, setDateRange] = useState<{
    startDate: dayjs.Dayjs | null;
    endDate: dayjs.Dayjs | null;
  }>({
    startDate: null,
    endDate: null,
  });

  const handleDateChange = (params: { startDate: any; endDate: any }) => {
    const { startDate, endDate } = params;

    setDateRange({
      startDate: startDate ? dayjs(startDate) : null,
      endDate: endDate ? dayjs(endDate) : null,
    });
  };

  const validateForm = () => {
    // Reset error
    setEmailError("");

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email) {
      setEmailError("Email is required");
      return false;
    }
    if (!emailRegex.test(email)) {
      setEmailError("Please enter a valid email");
      return false;
    }
    if (!dateRange.startDate || !dateRange.endDate) {
      Alert.alert("Error", "Please select a date range");
      return false;
    }
    return true;
  };

  const onSave = () => {
    if (!validateForm()) return;

    // This is where you'll eventually add the API call
    Alert.alert("Success", "Form is valid! Ready for backend integration.");
  };

  return (
    <View style={styles.container}>
      <View style={styles.emailContainer}>
        <Text style={styles.inputLabel}>Enter Your Email</Text>
        <TextInput
          style={[styles.input, emailError && styles.inputError]}
          placeholder="Enter Email"
          clearButtonMode="while-editing"
          autoComplete="email"
          keyboardType="email-address"
          value={email}
          onChangeText={(text) => {
            setEmail(text);
            setEmailError(""); // Clear error when typing
          }}
        />
        {emailError ? <Text style={styles.errorText}>{emailError}</Text> : null}
      </View>
      {/* Add View for selecting wehat Hut - look up select React components */}
      <View style={styles.dateContainer}>
        <Text style={styles.inputLabel}>Date Range of Reminder</Text>
        <Text style={styles.description}>
          This will notify you of any opening at any hut within that date range.
        </Text>
        <DateTimePicker
          mode="range"
          startDate={
            dateRange.startDate ? dateRange.startDate.toDate() : undefined
          }
          endDate={dateRange.endDate ? dateRange.endDate.toDate() : undefined}
          onChange={(params) => handleDateChange(params)}
          calendarTextStyle={{ color: "black" }}
          selectedTextStyle={{ color: "white" }}
          selectedItemColor="#0047FF"
        />
      </View>
      {/* Display dates on screen here */}
      <TouchableOpacity
        style={[styles.button, isLoading && styles.buttonDisabled]}
        onPress={onSave}
        disabled={isLoading}
      >
        <Text style={styles.buttonText}>
          {isLoading ? "Saving..." : "Save Reminder"}
        </Text>
      </TouchableOpacity>
    </View>
  );
};

export default SetReminderScreen;

const styles = StyleSheet.create({
  container: {
    justifyContent: "flex-start",
    alignItems: "center",
  },
  emailContainer: {
    justifyContent: "center",
    alignItems: "center",
    width: "100%",
    paddingTop: 45,
    paddingHorizontal: 20,
  },
  inputLabel: {
    fontSize: 20,
    fontWeight: "bold",
  },
  input: {
    height: 50,
    margin: 12,
    borderWidth: 1,
    padding: 15,
    width: "95%",
    borderRadius: 10,
  },
  dateContainer: {
    justifyContent: "center",
    alignItems: "center",
    paddingTop: 50,
    width: "90%",
    marginBottom: 15,
  },
  description: {
    paddingBottom: 15,
    paddingTop: 10,
    textAlign: "center", // Center the text
    width: "80%", // Ensure it takes up full width of its container
  },

  // CREATE MASTER STYLES SHEET FOR BUTTON BELOW
  buttonContainer: {
    position: "absolute",
    bottom: 50,
    width: "100%",
    alignItems: "center",
  },
  button: {
    borderColor: "none",
    borderWidth: 2,
    padding: 15,
    margin: 10,
    borderRadius: 10,
    width: "90%",
    alignItems: "center",
    backgroundColor: "#0047FF",
  },
  buttonText: {
    fontSize: 25,
    color: "white",
  },
  inputError: {
    borderColor: "red",
  },
  errorText: {
    color: "red",
    fontSize: 12,
    marginTop: -8,
    marginBottom: 8,
  },
  buttonDisabled: {
    opacity: 0.6,
  },
});
