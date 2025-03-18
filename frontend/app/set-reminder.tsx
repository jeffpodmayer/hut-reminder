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
import { useNavigation } from "@react-navigation/native";
import { HutSelectionModal } from "../components/HutSelectionModal";
import { router } from "expo-router";

interface Reminder {
  id: string;
  user_email: string;
  start_date: string;
  end_date: string;
  huts: number[];
  hut_id?: number;
}

interface SetReminderScreenProps {
  isEditing?: boolean;
  reminderToEdit?: Reminder;
}

const SetReminderScreen = ({
  isEditing,
  reminderToEdit,
}: SetReminderScreenProps) => {
  const [email, setEmail] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);
  const [emailError, setEmailError] = useState<string>("");
  const [huts, setHuts] = useState<any[]>([]);
  const [selectedHuts, setSelectedHuts] = useState<string[]>([]);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const navigation = useNavigation();
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
        setHuts(data);
      } catch (error) {
        Alert.alert("Error", "Failed to fetch huts");
      } finally {
        setIsLoading(false);
      }
    };

    fetchHuts();
  }, []);

  useEffect(() => {
    if (isEditing && reminderToEdit) {
      setEmail(reminderToEdit.user_email);
      setSelectedHuts([reminderToEdit.hut_id?.toString() || ""]);
      setDateRange({
        startDate: dayjs(reminderToEdit.start_date),
        endDate: dayjs(reminderToEdit.end_date),
      });
    }
  }, [isEditing, reminderToEdit]);

  const handleDateChange = (params: { startDate: any; endDate: any }) => {
    const { startDate, endDate } = params;

    setDateRange({
      startDate: startDate ? dayjs(startDate) : null,
      endDate: endDate ? dayjs(endDate) : null,
    });
  };

  const validateForm = () => {
    setEmailError("");
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

  const createReminder = async (
    email: string,
    startDate: string,
    endDate: string,
    hutIds: number[]
  ) => {
    const reminder: Reminder = {
      user_email: email,
      start_date: startDate,
      end_date: endDate,
      huts: hutIds,
      id: "",
    };

    try {
      const response = await fetch("http://127.0.0.1:5000/create-reminder", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(reminder),
      });

      if (!response.ok) {
        throw new Error(`Failed to create reminder: ${response.status}`);
      }
    } catch (error) {
      console.error("Network error:", error);
      throw error;
    }
  };

  const updateReminder = async (
    reminderId: string,
    updatedData: Partial<Reminder>
  ) => {
    const response = await fetch(
      `http://127.0.0.1:5000/update-reminder/${reminderId}`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedData),
      }
    );

    if (!response.ok) {
      throw new Error("Failed to update reminder");
    }
  };

  const onSave = async () => {
    if (!validateForm()) return;
    setIsLoading(true);

    try {
      if (isEditing && reminderToEdit) {
        await updateReminder(reminderToEdit.id, {
          user_email: email,
          start_date: dateRange.startDate?.format("YYYY-MM-DD"),
          end_date: dateRange.endDate?.format("YYYY-MM-DD"),
          hut_id: Number(selectedHuts[0]),
        });
      } else {
        const hutIds = selectedHuts.map((id) => Number(id));
        await createReminder(
          email,
          dateRange.startDate ? dateRange.startDate.format("YYYY-MM-DD") : "",
          dateRange.endDate ? dateRange.endDate.format("YYYY-MM-DD") : "",
          hutIds
        );
      }
      router.push("/");
    } catch (error) {
      console.error("Error:", error);
      Alert.alert("Error", "Failed to save reminder.");
    } finally {
      setIsLoading(false);
    }
  };

  const toggleHutSelection = (hutId: string) => {
    setSelectedHuts((prev) =>
      prev.includes(hutId)
        ? prev.filter((id) => id !== hutId)
        : [...prev, hutId]
    );
  };

  const toggleModal = () => {
    setIsModalVisible(!isModalVisible);
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
        <TouchableOpacity
          style={[
            styles.hutsButton,
            selectedHuts.length > 0 && {
              backgroundColor: "green",
              borderColor: "white",
            },
          ]}
          onPress={toggleModal}
        >
          <Text style={styles.hutsButtonText}>
            {selectedHuts.length > 0 ? (
              <Text style={{ color: "white" }}>
                {selectedHuts.length} hut{selectedHuts.length > 1 ? "s" : ""}{" "}
                selected
              </Text>
            ) : (
              "Select Huts"
            )}
          </Text>
        </TouchableOpacity>
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
      <HutSelectionModal
        isVisible={isModalVisible}
        onClose={toggleModal}
        huts={huts}
        selectedHuts={selectedHuts}
        onHutToggle={toggleHutSelection}
        isLoading={isLoading}
      />
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
    paddingBottom: 10,
  },
  hutContainer: {
    justifyContent: "center",
    alignItems: "center",
    width: "100%",
    paddingTop: 5,
  },
  dateContainer: {
    justifyContent: "center",
    alignItems: "center",
    paddingTop: 30,
    width: "90%",
  },
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
  doneButtonText: {
    fontSize: 25,
    color: "black",
  },

  hutsButtonText: {
    fontSize: 20,
    fontWeight: "bold",
  },
  hutsButton: {
    borderColor: "black",
    borderWidth: 2,
    padding: 15,
    borderRadius: 10,
    width: "85%",
    alignItems: "center",
    backgroundColor: "lightgray",
  },
});
