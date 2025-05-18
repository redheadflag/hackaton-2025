import { API_BASE, CHANNEL_ID } from "@/services/constants";
import React, { useEffect, useState } from "react";
import { ActivityIndicator, Dimensions, StyleSheet, Text, View } from "react-native";
import MapView, { Marker } from "react-native-maps";

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
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    const fetchObservations = async () => {
      setLoading(true);
      setErr(null);
      try {
        const url = `${API_BASE}/channels/${CHANNEL_ID}/messages`;
        const response = await fetch(url);

        const text = await response.text();

        if (!response.ok) throw new Error(`HTTP ${response.status}: ${text}`);
        const data = JSON.parse(text);

        const mapped: Observation[] = data.map((obs: any) => ({
          userId: obs.sender_id || obs.userId || "",
          userName: obs.content?.userName || obs.userName || "",
          species: obs.content?.species || "",
          description: obs.content?.description || "",
          location: obs.point
            ? { latitude: obs.point[0], longitude: obs.point[1] }
            : { latitude: 0, longitude: 0 },
        }));

        setObservations(mapped);
      } catch (e: any) {
        setErr(e.message);
        setObservations([]);
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
              key={`${obs.userId}-${idx}`}
              coordinate={{
                latitude: obs.location.latitude,
                longitude: obs.location.longitude,
              }}
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
      {!loading && observations.length === 0 && !err && (
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
    marginTop: 50,
  },
  emptyText: {
    backgroundColor: "rgba(255,255,255,0.85)",
    padding: 8,
    borderRadius: 8,
    color: "#4CAF50",
    fontWeight: "bold",
    fontSize: 16,
  },
});