'use client';

import { useRouter } from "next/navigation";

export default function HomePage() {
  const router = useRouter();

  const handleStart = () => {
    router.push("/dashboard");
  };

  return (
    <main className="landing-container">
      <div className="header">
        <h1>AI-Wildlife Monitoring</h1>
        <p>Advanced real-time detection and species classification system</p>
      </div>

      <div className="insights-grid">
        <div className="insight-card">
          <div className="insight-icon">🎯</div>
          <h3>YOLOv8 Detection</h3>
          <p>State-of-the-art object detection with 95%+ accuracy for wildlife species identification</p>
        </div>
        <div className="insight-card">
          <div className="insight-icon">⚡</div>
          <h3>Real-Time Alerts</h3>
          <p>Instant notifications when endangered or protected species are detected</p>
        </div>
        <div className="insight-card">
          <div className="insight-icon">📊</div>
          <h3>Analytics Dashboard</h3>
          <p>Comprehensive insights with species tracking, population trends, and activity patterns</p>
        </div>
        <div className="insight-card">
          <div className="insight-icon">🌍</div>
          <h3>Conservation Focus</h3>
          <p>Supporting wildlife preservation through AI-powered monitoring</p>
        </div>
      </div>

      <div className="action">
        <button onClick={handleStart} className="start-button">
          Start Monitoring
        </button>
      </div>
    </main>
  );
}

