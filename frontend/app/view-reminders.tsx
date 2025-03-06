import {
  View,
  Text,
  TextInput,
  ScrollView,
  TouchableOpacity,
} from "react-native";
import { useState } from "react";
import dayjs from "dayjs";
import { AntDesign } from "@expo/vector-icons";
import { viewRemindersStyles } from "../styles/screens/viewReminders";

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

const ViewRemindersScreen = () => {
  const [email, setEmail] = useState("");
  const [userReminders, setUserReminders] = useState<Reminder[]>([]);

  const formatDateRange = (startDate: string, endDate: string) => {
    const start = dayjs(startDate).format("MMM. D, YYYY");
    const end = dayjs(endDate).format("MMM. D, YYYY");
    return `${start} - ${end}`;
  };

  const handleSearch = () => {
    if (!email.trim()) {
      setUserReminders([]);
      return;
    }

    // Filter MOCK_REMINDERS based on email
    const filteredReminders = MOCK_REMINDERS.filter(
      (reminder) => reminder.email.toLowerCase() === email.toLowerCase()
    );
    setUserReminders(filteredReminders);
  };

  const handleEdit = (reminderId: string) => {
    // - Make PUT request to backend endpoint (e.g., /api/reminders/{reminderId})
    // - Send updated reminder data
    // - Refresh reminders list after successful update
    console.log("Edit reminder:", reminderId);
  };

  const handleDelete = (reminderId: string) => {
    // - Remove from UI immediately
    // - Restore if API call fails
  };

  return (
    <View style={viewRemindersStyles.container}>
      <Text style={viewRemindersStyles.title}>Enter Email</Text>
      <View style={viewRemindersStyles.searchContainer}>
        <TextInput
          style={viewRemindersStyles.input}
          placeholder="Enter your email"
          placeholderTextColor="#666"
          value={email}
          onChangeText={setEmail}
          autoCapitalize="none"
          keyboardType="email-address"
          clearButtonMode="while-editing"
        />
        <TouchableOpacity
          style={viewRemindersStyles.searchButton}
          onPress={handleSearch}
        >
          <Text style={viewRemindersStyles.buttonText}>Search</Text>
        </TouchableOpacity>
      </View>
      <Text style={viewRemindersStyles.title}>Your Reminders</Text>
      <ScrollView style={viewRemindersStyles.remindersList}>
        {userReminders.map((reminder) => (
          <View key={reminder.id} style={viewRemindersStyles.reminderCard}>
            <View>
              <Text style={viewRemindersStyles.hutName}>{reminder.hut}</Text>
              <Text style={viewRemindersStyles.dateRange}>
                {formatDateRange(reminder.startDate, reminder.endDate)}
              </Text>
            </View>
            <View style={viewRemindersStyles.cardActions}>
              <TouchableOpacity
                onPress={() => handleEdit(reminder.id)}
                style={viewRemindersStyles.actionButton}
              >
                <AntDesign name="edit" size={28} color="#0047FF" />
              </TouchableOpacity>
              <TouchableOpacity
                onPress={() => handleDelete(reminder.id)}
                style={viewRemindersStyles.actionButton}
              >
                <AntDesign name="delete" size={28} color="#FF0000" />
              </TouchableOpacity>
            </View>
          </View>
        ))}
        {userReminders.length === 0 && email !== "" && (
          <Text style={viewRemindersStyles.noReminders}>
            No reminders found for this email
          </Text>
        )}
      </ScrollView>
    </View>
  );
};

export default ViewRemindersScreen;
