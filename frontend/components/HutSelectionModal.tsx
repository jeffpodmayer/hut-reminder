import React from "react";
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
  huts: any[];
  selectedHuts: string[];
  onHutToggle: (hutId: string) => void;
  isLoading: boolean;
}

export const HutSelectionModal: React.FC<HutSelectionModalProps> = ({
  isVisible,
  onClose,
  huts,
  selectedHuts,
  onHutToggle,
  isLoading,
}) => {
  return (
    <Modal transparent={true} visible={isVisible} animationType="slide">
      <View style={styles.modalContainer}>
        <View style={styles.modalContent}>
          <Text style={styles.title}>Select Huts</Text>
          <Text style={styles.subtitle}>Choose 1 or more</Text>
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
            style={[styles.button, isLoading && styles.buttonDisabled]}
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
  title: {
    fontSize: 20,
    fontWeight: "bold",
    marginBottom: 5,
  },
  subtitle: {
    marginBottom: 15,
  },
  hutList: {
    maxHeight: 400,
    width: "100%",
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
    backgroundColor: "green",
    padding: 15,
    borderRadius: 10,
    width: "50%",
    alignItems: "center",
    marginTop: 10,
  },
  buttonText: {
    color: "white",
    fontSize: 16,
    fontWeight: "bold",
  },
  buttonDisabled: {
    opacity: 0.6,
  },
});
