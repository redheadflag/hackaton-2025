import { API_BASE, CHANNEL_ID, USER_ID, USER_NAME } from "@/services/constants";
import { getCurrentLocation } from "@/services/LocationService";
import React, { useState } from "react";
import { ActivityIndicator, KeyboardAvoidingView, Platform, StyleSheet, Text, TextInput, TouchableOpacity, View } from "react-native";

export default function HomeScreen() {
  const [location, setLocation] = useState<{ latitude: number, longitude: number } | null>(null);
  const [errMsg, setErrMsg] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [loadingLocation, setLoadingLocation] = useState(false);

  // Form state
  const [species, setSpecies] = useState('');
  const [description, setDescription] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [submitMsg, setSubmitMsg] = useState('');

  // Handle "Add Observation" button press
  const handleAddObservation = async () => {
    setErrMsg('');
    setLoadingLocation(true);
    try {
      const coords = await getCurrentLocation();
      setLocation(coords);
      setShowForm(true);
    } catch (err: any) {
      setErrMsg(err.message);
    } finally {
      setLoadingLocation(false);
    }
  };

  // Handle form submit
  const handleSubmit = async () => {
  if (!species.trim() || !description.trim()) {
    setSubmitMsg("Please fill in all fields.");
    return;
  }
  if (!location) {
    setSubmitMsg("Could not get current location.");
    return;
  }
  setSubmitting(true);
  setSubmitMsg('');
  try {
    const payload = {
      userId: USER_ID,
      // userName: USER_NAME,
      title: species.trim(),
      content: {message: description.trim()},
      location: location,
      // createdAt: new Date().toISOString(),
    };
    // Compose the full URL
    const url = `${API_BASE}/channels/${CHANNEL_ID}/messages`;
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) throw new Error("Failed to submit observation");
    setSubmitMsg("Observation submitted!");
    setSpecies('');
    setDescription('');
    setShowForm(false);
    setLocation(null);
  } catch (error: any) {
    setSubmitMsg("Error: " + error.message);
  } finally {
    setSubmitting(false);
  }
};

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === "ios" ? "padding" : undefined}
    >
      {!showForm ? (
        <View style={{ alignItems: "center" }}>
          {errMsg ? <Text style={styles.error}>{errMsg}</Text> : null}
          <Text style={styles.text}>
            Press the button when you find something interesting!
          </Text>

          <TouchableOpacity
            style={styles.button}
            onPress={handleAddObservation}
            activeOpacity={0.8}
            disabled={loadingLocation}
          >
            <Text style={styles.buttonText}>
              {loadingLocation ? "Getting Location..." : "Add Observation"}
            </Text>
            {loadingLocation && <ActivityIndicator color="#fff" style={{ marginLeft: 8 }} />}
          </TouchableOpacity>
        </View>
      ) : (
        <View style={styles.form}>
          <Text style={styles.formTitle}>Submit Observation</Text>
          {location && (
            <Text style={styles.locSmall}>
              Lat: {location.latitude.toFixed(6)}, Lon: {location.longitude.toFixed(6)}
            </Text>
          )}
          <TextInput
            style={styles.input}
            placeholder="Species name"
            placeholderTextColor={"black"}
            value={species}
            onChangeText={setSpecies}
          />
          <TextInput
            style={[styles.input, styles.textarea]}
            placeholder="Description"
            placeholderTextColor={"black"}
            value={description}
            onChangeText={setDescription}
            multiline
            numberOfLines={3}
          />
          {submitMsg ? <Text style={styles.submitMsg}>{submitMsg}</Text> : null}
          <View style={{ flexDirection: "row", justifyContent: "space-between", width: "100%" }}>
            <TouchableOpacity
              style={[styles.button, { backgroundColor: "#ccc", flex: 1, marginRight: 8 }]}
              onPress={() => { setShowForm(false); setLocation(null); }}
              disabled={submitting}
            >
              <Text style={[styles.buttonText, { color: "#444" }]}>Cancel</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[styles.button, { flex: 2 }]}
              onPress={handleSubmit}
              disabled={submitting}
            >
              <Text style={styles.buttonText}>{submitting ? "Submitting..." : "Submit"}</Text>
            </TouchableOpacity>
          </View>
        </View>
      )}
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#FFF5E1", // beige
    justifyContent: "center",
    alignItems: "center",
    padding: 16,
  },
  text: {
    marginBottom: 24,
    fontSize: 16,
    color: "#333",
    textAlign: 'center',
    fontWeight: '700',
  },
  button: {
    backgroundColor: "#4CAF50", // appealing green
    borderRadius: 28,
    paddingVertical: 16,
    paddingHorizontal: 32,
    marginVertical: 16,
    alignItems: "center",
    elevation: 2, // for Android shadow
    flexDirection: "row",
    justifyContent: "center"
  },
  buttonText: {
    color: "#FFF",
    fontWeight: "bold",
    fontSize: 18,
    letterSpacing: 1,
  },
  form: {
    backgroundColor: "#fff",
    borderRadius: 18,
    padding: 20,
    width: "100%",
    maxWidth: 380,
    elevation: 4,
    alignItems: "stretch",
  },
  formTitle: {
    fontSize: 20,
    fontWeight: "bold",
    color: "#4CAF50",
    marginBottom: 10,
    textAlign: "center",
  },
  input: {
    borderWidth: 1,
    borderColor: "#4CAF50",
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    marginBottom: 14,
    backgroundColor: "#FFF5E1",
  },
  textarea: {
    minHeight: 60,
    textAlignVertical: "center",
  },
  error: {
    color: "#b71c1c",
    marginBottom: 12,
  },
  submitMsg: {
    color: "#4CAF50",
    fontWeight: "bold",
    marginBottom: 10,
    textAlign: "center",
  },
  locSmall: {
    fontSize: 12,
    color: "#888",
    marginBottom: 8,
    textAlign: "center",
  },
});
