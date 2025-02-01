import { router } from "expo-router";
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

// TODO: API Integration
// - Add API base URL configuration (likely need environment variables)
// - Add API authentication headers/tokens if required
// - Consider adding API request timeout settings

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

  // TODO: Add state for API errors
  const [apiError, setApiError] = useState<string>("");

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
      setEmailError("Email is required!");
      return false;
    }
    if (!emailRegex.test(email)) {
      setEmailError("Please enter a valid email!");
      return false;
    }
    if (!dateRange.startDate || !dateRange.endDate) {
      Alert.alert("Error", "Please select a date range!");
      return false;
    }
    return true;
  };

  // TODO: API Integration
  // - Create API service/client for all reminder-related API calls
  // - Add error handling for network failures
  // - Add loading states for API calls
  // - Consider adding retry logic for failed requests

  const onSave = () => {
    // TODO: Format dates to match backend expectations
    // - Ensure timezone handling is consistent
    // - Consider using ISO 8601 format for dates
    // - Ensure date format matches Python backend parsing

    // TODO: Add request body type validation
    // type ReminderRequest = {
    //   email: string;
    //   startDate: string;
    //   endDate: string;
    //   hut: string;
    // };

    if (!validateForm()) return;
    setIsLoading(true);

    // TODO: API Integration
    // - Make POST request to backend endpoint (e.g., /api/reminders)
    // - Request body should include:
    //   {
    //     email: string,
    //     startDate: string (ISO format),
    //     endDate: string (ISO format),
    //     hut: string
    //   }
    // - Add proper error handling for:
    //   - Network errors
    //   - Validation errors from backend
    //   - Server errors
    // - Show appropriate error messages to user
    // - Only navigate away on successful response

    Alert.alert("Success", "Reminder saved successfully!", [
      {
        text: "OK",
        onPress: () => {
          router.replace("/");
          // TODO: Add navigation to ViewRemindersScreen
        },
      },
    ]);
    setIsLoading(false);
  };

  return (
    <View style={styles.container}>
      <View style={styles.emailContainer}>
        <Text style={styles.inputLabel}>Enter Your Email</Text>
        <TextInput
          style={[styles.input, emailError && styles.inputError]}
          placeholder="Enter Email"
          autoCapitalize="none"
          clearButtonMode="while-editing"
          autoComplete="email"
          keyboardType="email-address"
          value={email}
          onChangeText={(text) => {
            setEmail(text);
            setEmailError("");
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
