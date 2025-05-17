import React, { useEffect, useState } from "react";
import MapView, { Marker } from "react-native-maps";
import { StyleSheet, View, Dimensions, Text, ActivityIndicator } from "react-native";
import { CHANNEL_ID, API_BASE } from "@/services/constants";

type Observation = {
  userId: string;
  userName: string;
  species: string;
  description: string;
  location: { latitude: number; longitude: number };
  createdAt: string;
};

export default function MapScreen() {
  const [observations, setObservations] = useState<Observation[]>([]);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    // Could also use useFocusEffect from @react-navigation/native if you want to refresh every time user opens the map
    const fetchObservations = async () => {
      setLoading(true);
      setErr(null);
      try {
        const resp = await fetch(`${API_BASE}/channels/${CHANNEL_ID}/messages`);
        if (!resp.ok) throw new Error("Failed to load observations");
        const data = await resp.json();
        setObservations(data); // expects array
      } catch (e: any) {
        setErr(e.message);
      } finally {
        setLoading(false);
      }
    };
    fetchObservations();
  }, []);

  const initialRegion =
    observations.length > 0
      ? {
          latitude: observations[0].location.latitude,
          longitude: observations[0].location.longitude,
          latitudeDelta: 0.04,
          longitudeDelta: 0.04,
        }
      : {
          latitude: 45.3271,
          longitude: 13.5684,
          latitudeDelta: 0.5,
          longitudeDelta: 0.5,
        };

  return (
    <View style={styles.container}>
      {loading ? (
        <ActivityIndicator style={{ flex: 1 }} size="large" color="#4CAF50" />
      ) : (
        <MapView style={styles.map} initialRegion={initialRegion}>
          {observations.map((obs, idx) => (
            <Marker
              key={obs.createdAt + idx}
              coordinate={obs.location}
              title={obs.species}
              description={obs.description}
              pinColor="red"
            />
          ))}
        </MapView>
      )}
      {err && (
        <View style={styles.overlay}>
          <Text style={styles.error}>{err}</Text>
        </View>
      )}
      {!loading && observations.length === 0 && (
        <View style={styles.overlay}>
          <Text style={styles.emptyText}>No observations yet!</Text>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  map: {
    width: Dimensions.get("window").width,
    height: Dimensions.get("window").height,
  },
  overlay: {
    position: "absolute",
    top: 80,
    left: 0,
    right: 0,
    alignItems: "center",
  },
  error: {
    color: "#b71c1c",
    backgroundColor: "rgba(255,255,255,0.85)",
    padding: 8,
    borderRadius: 8,
    fontWeight: "bold",
  },
  emptyText: {
    backgroundColor: "rgba(255,255,255,0.85)",
    padding: 8,
    borderRadius: 8,
    color: "#4CAF50",
    fontWeight: "bold",
    fontSize: 16,
    marginTop: 40,
  },
});
