import {
  View,
  Text,
  StyleSheet,
  TextInput,
  ScrollView,
  TouchableOpacity,
} from "react-native";
import { useState } from "react";
import dayjs from "dayjs";
import { MaterialIcons } from "@expo/vector-icons";

// Define a type for our reminder object
type Reminder = {
  id: string;
  email: string;
  startDate: string;
  endDate: string;
  hut: string;
};

// Static reminder data for testing
const MOCK_REMINDERS: Reminder[] = [
  {
    id: "1",
    email: "test@example.com",
    startDate: "2024-04-01",
    endDate: "2024-04-05",
    hut: "Brewster Hut",
  },
  {
    id: "2",
    email: "test@example.com",
    startDate: "2024-05-10",
    endDate: "2024-05-15",
    hut: "Mueller Hut",
  },
  {
    id: "3",
    email: "other@example.com",
    startDate: "2024-06-20",
    endDate: "2024-06-25",
    hut: "French Ridge Hut",
  },
];

// TODO: API Integration
// - Add types that match backend response structure
type APIReminder = {
  // Ensure these match exactly what Python backend returns
  id: string; // Check if backend uses string or number
  email: string;
  startDate: string; // Confirm date format from backend
  endDate: string;
  hut: string;
  // Add any additional fields backend might return
};

const ViewRemindersScreen = () => {
  const [email, setEmail] = useState("");
  const [userReminders, setUserReminders] = useState<Reminder[]>([]);
  // TODO: Add API error handling state
  const [isLoading, setIsLoading] = useState(false);
  const [apiError, setApiError] = useState<string>("");

  const formatDateRange = (startDate: string, endDate: string) => {
    const start = dayjs(startDate).format("MMM. D, YYYY");
    const end = dayjs(endDate).format("MMM. D, YYYY");
    return `${start} - ${end}`;
  };

  const handleSearch = () => {
    // TODO: Add request cancellation if user searches again quickly
    // TODO: Add pagination if backend supports it
    // TODO: Add sorting/filtering if backend supports it
  };

  const handleEdit = (reminderId: string) => {
    // TODO: API Integration
    // - Make PUT request to backend endpoint (e.g., /api/reminders/{reminderId})
    // - Send updated reminder data
    // - Refresh reminders list after successful update
    console.log("Edit reminder:", reminderId);
  };

  const handleDelete = (reminderId: string) => {
    // TODO: Add optimistic updates
    // - Remove from UI immediately
    // - Restore if API call fails
    // TODO: Consider batch delete functionality if backend supports it
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Enter Email</Text>
      <View style={styles.searchContainer}>
        <TextInput
          style={styles.input}
          placeholder="Enter your email"
          placeholderTextColor="#666"
          value={email}
          onChangeText={setEmail}
          autoCapitalize="none"
          keyboardType="email-address"
          clearButtonMode="while-editing"
        />
        <TouchableOpacity style={styles.searchButton} onPress={handleSearch}>
          <Text style={styles.buttonText}>Search</Text>
        </TouchableOpacity>
      </View>
      <Text style={styles.title}>Your Reminders</Text>
      <ScrollView style={styles.remindersList}>
        {userReminders.map((reminder) => (
          <View key={reminder.id} style={styles.reminderCard}>
            <View>
              <Text style={styles.hutName}>{reminder.hut}</Text>
              <Text style={styles.dateRange}>
                {formatDateRange(reminder.startDate, reminder.endDate)}
              </Text>
            </View>
            <View style={styles.cardActions}>
              <TouchableOpacity
                onPress={() => handleEdit(reminder.id)}
                style={styles.actionButton}
              >
                <MaterialIcons name="edit" size={24} color="#0047FF" />
              </TouchableOpacity>
              <TouchableOpacity
                onPress={() => handleDelete(reminder.id)}
                style={styles.actionButton}
              >
                <MaterialIcons name="delete" size={24} color="#FF0000" />
              </TouchableOpacity>
            </View>
          </View>
        ))}
        {userReminders.length === 0 && email !== "" && (
          <Text style={styles.noReminders}>
            No reminders found for this email
          </Text>
        )}
      </ScrollView>
    </View>
  );
};

export default ViewRemindersScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: "#fff",
  },
  title: {
    fontSize: 25,
    fontWeight: "bold",
    marginBottom: 10,
    borderBottomWidth: 1,
    borderBottomColor: "#ccc",
    paddingBottom: 10,
  },
  searchContainer: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 20,
  },
  input: {
    flex: 1,
    height: 40,
    borderWidth: 1,
    borderColor: "#ccc",
    borderRadius: 5,
    padding: 10,
    marginRight: 10,
  },
  searchButton: {
    backgroundColor: "#0047FF",
    padding: 10,
    borderRadius: 5,
    width: 80,
    alignItems: "center",
  },
  buttonText: {
    color: "white",
    fontWeight: "bold",
  },
  remindersList: {
    flex: 1,
  },
  reminderCard: {
    backgroundColor: "#f5f5f5",
    padding: 15,
    borderRadius: 10,
    marginBottom: 10,
    borderWidth: 1,
    borderColor: "#eee",
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  hutName: {
    fontSize: 18,
    fontWeight: "bold",
    marginBottom: 5,
  },
  dateRange: {
    color: "#666",
  },
  noReminders: {
    textAlign: "center",
    color: "#666",
    marginTop: 20,
  },
  cardActions: {
    flexDirection: "row",
    alignItems: "center",
  },
  actionButton: {
    padding: 5,
    marginLeft: 10,
  },
});
