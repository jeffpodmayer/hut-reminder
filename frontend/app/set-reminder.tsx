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
import { useEffect, useState } from "react";
import { Select, SelectItem, IndexPath } from "@ui-kitten/components";

const SetReminderScreen = () => {
  const [email, setEmail] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);
  const [emailError, setEmailError] = useState<string>("");
  const [huts, setHuts] = useState<any[]>([]);
  const [selectedHuts, setSelectedHuts] = useState<IndexPath[]>([]);
  const [error, setError] = useState<string>("");

  const [dateRange, setDateRange] = useState<{
    startDate: dayjs.Dayjs | null;
    endDate: dayjs.Dayjs | null;
  }>({
    startDate: null,
    endDate: null,
  });

  useEffect(() => {
    const fetchHuts = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/get-all-huts");
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        setHuts(data); // Set the huts state with the fetched data
      } catch (error) {
        if (error instanceof Error) {
          setError(error.message); // Set error message if there's an error
        } else {
          setError("An unknown error occurred."); // Fallback for unknown error types
        }
      } finally {
        setIsLoading(false); // Set loading to false after fetching
      }
    };

    fetchHuts();
  }, []);

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
    if (selectedHuts.length === 0) {
      Alert.alert("Error", "Please select at least one hut!");
      return false;
    }
    return true;
  };

  const onSave = () => {
    if (!validateForm()) return;
    setIsLoading(true);

    // Prepare the data to send
    const hutIds = selectedHuts.map((id) => Number(id));

    createReminder(
      email,
      dateRange.startDate ? dateRange.startDate.format("YYYY-MM-DD") : "",
      dateRange.endDate ? dateRange.endDate.format("YYYY-MM-DD") : "",
      hutIds
    )
      .then(() => {
        Alert.alert("Success", "Reminder saved successfully!", [
          {
            text: "OK",
            onPress: () => {
              // Optionally navigate to another screen
            },
          },
        ]);
      })
      .catch((error) => {
        Alert.alert("Error", "Failed to save reminder.");
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  const createReminder = async (
    email: string,
    startDate: string,
    endDate: string,
    hutIds: number[]
  ) => {
    try {
      const response = await fetch("http://your-backend-url/api/reminders", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_email: email,
          start_date: startDate,
          end_date: endDate,
          hut_ids: hutIds,
        }),
      });

      const data = await response.json();
      if (response.ok) {
        console.log("Reminder created:", data);
        // Optionally, navigate to another screen or show a success message
      } else {
        console.error("Error creating reminder:", data.error);
      }
    } catch (error) {
      console.error("Network error:", error);
    }
  };

  const renderSelectedHuts = () => {
    if (selectedHuts.length === 0) return "Select Huts";
    if (selectedHuts.length === huts.length) return "All Huts Selected";
    return selectedHuts
      .map((indexPath) => huts[indexPath.row].name.split(" ")[0])
      .join(", ");
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
      <View style={styles.hutContainer}>
        <Text style={styles.inputLabel}>Select Huts</Text>
        <Select
          multiSelect={true}
          selectedIndex={selectedHuts}
          onSelect={(indexPaths) => setSelectedHuts(indexPaths)}
          value={renderSelectedHuts()}
          placeholder="Search Huts..."
          style={styles.select}
        >
          {huts.map((hut, index) => (
            <SelectItem key={hut.id.toString()} title={hut.name} />
          ))}
        </Select>
      </View>
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
  hutContainer: {
    justifyContent: "center",
    alignItems: "center",
    width: "100%",
    paddingTop: 45,
  },
  select: {},
  picker: {
    width: "90%",
    height: 50,
    borderWidth: 1,
    borderRadius: 10,
  },
  pickerItem: {
    fontSize: 20,
    fontWeight: "bold",
  },
  pickerItemLabel: {
    fontSize: 20,
    fontWeight: "bold",
  },
  pickerItemText: {
    fontSize: 20,
    fontWeight: "bold",
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
  modalContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "rgba(0, 0, 0, 0.5)",
  },
  modalItem: {
    padding: 10,
    borderBottomWidth: 1,
    borderBottomColor: "#ccc",
  },
});
