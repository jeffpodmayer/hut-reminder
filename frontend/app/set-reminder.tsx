import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
} from "react-native";
import DateTimePicker from "react-native-ui-datepicker";
import dayjs from "dayjs";
import { useState } from "react";

const SetReminderScreen = () => {
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

  return (
    <View style={styles.container}>
      <View style={styles.emailContainer}>
        <Text style={styles.inputLabel}>Enter Your Email</Text>
        <TextInput
          style={styles.input}
          placeholder="Enter Email"
          clearButtonMode="while-editing"
          autoComplete="email"
          keyboardType="email-address"
        />
      </View>
      <View style={styles.dateContainer}>
        <Text style={styles.inputLabel}>Date Range of Reminder</Text>
        <Text style={styles.description}>
          This will notify you of any opening within that date range.
        </Text>
        <DateTimePicker
          mode="range"
          startDate={
            dateRange.startDate ? dateRange.startDate.toDate() : undefined
          }
          endDate={dateRange.endDate ? dateRange.endDate.toDate() : undefined}
          onChange={(params) => handleDateChange(params)}
          calendarTextStyle={{ color: "black" }} // Day/Month/Year text color
          selectedTextStyle={{ color: "white" }} // Text color of selected dates
          selectedItemColor="#0047FF"
        />
      </View>
      <TouchableOpacity style={styles.button}>
        <Text style={styles.buttonText}>Save Reminder</Text>
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
});
