import {
  View,
  Text,
  Modal,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
} from "react-native";

interface HutSelectionModalProps {
  isVisible: boolean;
  onClose: () => void;
  huts: Array<{ id: number; name: string }>;
  selectedHuts: string[];
  onHutToggle: (hutId: string) => void;
  isLoading: boolean;
}

export const HutSelectionModal = ({
  isVisible,
  onClose,
  huts,
  selectedHuts,
  onHutToggle,
  isLoading,
}: HutSelectionModalProps) => {
  return (
    <Modal transparent={true} visible={isVisible} animationType="slide">
      <View style={styles.modalContainer}>
        <View style={styles.modalContent}>
          <Text style={styles.inputLabel}>Select Huts</Text>
          <Text style={styles.description}>Choose 1 or more</Text>
          <ScrollView style={styles.hutList}>
            {huts.map((hut) => (
              <TouchableOpacity
                key={hut.id}
                style={[
                  styles.hutOption,
                  selectedHuts.includes(hut.id.toString()) &&
                    styles.hutOptionSelected,
                ]}
                onPress={() => onHutToggle(hut.id.toString())}
              >
                <Text style={styles.hutOptionText}>{hut.name}</Text>
              </TouchableOpacity>
            ))}
          </ScrollView>
          <TouchableOpacity
            style={[
              styles.button,
              isLoading && styles.buttonDisabled,
              { width: "50%", backgroundColor: "green" },
            ]}
            onPress={onClose}
          >
            <Text style={styles.buttonText}>Done</Text>
          </TouchableOpacity>
        </View>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  modalContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "rgba(0, 0, 0, 0.5)",
  },
  modalContent: {
    backgroundColor: "white",
    padding: 20,
    borderRadius: 10,
    width: "80%",
    alignItems: "center",
  },
  inputLabel: {
    fontSize: 20,
    fontWeight: "bold",
  },
  description: {
    paddingBottom: 15,
    paddingTop: 10,
    textAlign: "center",
    width: "80%",
  },
  hutList: {
    maxHeight: 400,
    width: "100%",
    borderWidth: 1,
    borderRadius: 10,
    borderColor: "#ccc",
    marginBottom: 10,
  },
  hutOption: {
    padding: 15,
    borderBottomWidth: 1,
    borderBottomColor: "#ccc",
    backgroundColor: "white",
  },
  hutOptionSelected: {
    backgroundColor: "#e6efff",
  },
  hutOptionText: {
    fontSize: 16,
  },
  button: {
    borderColor: "none",
    borderWidth: 2,
    padding: 15,
    margin: 10,
    borderRadius: 10,
    alignItems: "center",
  },
  buttonText: {
    fontSize: 25,
    color: "white",
  },
  buttonDisabled: {
    opacity: 0.6,
  },
});
