import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function App() {
  const [captions, setCaptions] = useState<string>("Listening...");
  const [scamWarning, setScamWarning] = useState<string | null>(null);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws-live-stream');
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.transcript) setCaptions(data.transcript);
      if (data.scam_alert?.is_threat) {
        setScamWarning(data.scam_alert.warning_text);
      }
    };
    return () => ws.close();
  }, []);

  return (
    <View style={styles.container}>
      {scamWarning && (
        <View style={styles.warningBox}>
          <Text style={styles.warningText}>⚠️ {scamWarning}</Text>
        </View>
      )}
      <Text style={styles.captionText}>{captions}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#111', justifyContent: 'center', padding: 20 },
  captionText: { color: 'white', fontSize: 24, textAlign: 'center' },
  warningBox: { backgroundColor: 'red', padding: 20, borderRadius: 10, marginBottom: 40 },
  warningText: { color: 'white', fontSize: 20, fontWeight: 'bold', textAlign: 'center' }
});
