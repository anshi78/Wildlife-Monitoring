// C:\...\frontend\app\dashboard\page.js
'use client';

import { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';

export default function DashboardPage() {
  const [detections, setDetections] = useState([]);
  const [liveImage, setLiveImage] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isOnline, setIsOnline] = useState(false);

  const prevImageUrl = useRef(null);
  const router = useRouter();

  // "Ghost-Fix": Hardcode the key to bypass .env issues
  const API_KEY = "MySuperSecretKey2025";
  // You can still use .env for the URL if you create a .env.local file
  // Or just hardcode it for now:
  const API_URL = process.env.NEXT_PUBLIC_API_URL;

  // Fetch detections and live frame
  useEffect(() => {
    const fetchData = async () => {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000);

        const [detectionsRes, liveFrameRes] = await Promise.all([
          fetch(`${API_URL}/detections/`, { 
            headers: { 'X-API-KEY': API_KEY },
            signal: controller.signal 
          }),
          fetch(`${API_URL}/live-frame?t=${Date.now()}`, {
            signal: controller.signal
          }), 
        ]);
        
        clearTimeout(timeoutId);

        if (detectionsRes.ok) {
          setDetections(await detectionsRes.json());
        } else {
          console.error('Detections fetch failed:', detectionsRes.status, await detectionsRes.text());
        }

        if (liveFrameRes.ok) {
          const blob = await liveFrameRes.blob();
          if (prevImageUrl.current) URL.revokeObjectURL(prevImageUrl.current);
          const newUrl = URL.createObjectURL(blob);
          prevImageUrl.current = newUrl;
          setLiveImage(newUrl);
        } else if (liveFrameRes.status !== 404) {
          console.error('Live frame fetch failed:', liveFrameRes.status);
        }
        
        setIsOnline(true);
      } catch (err) {
        if (err.name === 'AbortError') {
          console.log('Fetch timed out (Backend might be offline or sleeping)');
        } else {
          console.error('Fetch error:', err);
        }
        setIsOnline(false);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5000); // Poll every 5 seconds

    return () => {
      clearInterval(interval);
      if (prevImageUrl.current) URL.revokeObjectURL(prevImageUrl.current);
    };
  }, []); // Empty dependency array means this runs once on mount

  // --- Derived stats ---
  const totalDetections = detections.length;
  const uniqueSpecies = new Set(detections.map(d => d.species)).size;
  const lastDetection =
    totalDetections > 0
      ? `${Math.round((Date.now() - new Date(detections[0].timestamp).getTime()) / 60000)}m ago`
      : 'Never';

  const speciesCounts = detections.reduce((acc, { species }) => {
    acc[species] = (acc[species] || 0) + 1;
    return acc;
  }, {});

  // Add your species icons here
  const speciesIcons = {
    deer: '🦌', boar: '🐗', elephant: '🐘', monkey: '🐒', leopard: '🐆',
    person: '🚶', bird: '🐦', // etc.
  };

  // --- Chart Data Processing ---
  const timelineDataMap = [...detections].reverse().reduce((acc, { timestamp }) => {
    const date = new Date(timestamp);
    const time = `${date.getHours().toString().padStart(2, '0')}:00`; 
    acc[time] = (acc[time] || 0) + 1;
    return acc;
  }, {});
  const timelineData = Object.keys(timelineDataMap).map(time => ({ time, count: timelineDataMap[time] }));

  const barChartData = Object.entries(speciesCounts).map(([name, count]) => ({
    name: name.charAt(0).toUpperCase() + name.slice(1),
    count
  }));

  // --- Loading screen ---
  if (isLoading && !detections.length) {
    return (
      <div className="loading-screen">
        <div className="loading-text">Loading dashboard...</div>
      </div>
    );
  }

  // --- Main render (Your JSX from the file) ---
  return (
    <div className="dashboard-wrapper">
      {/* Background */}
      <div className="bg-gradient">
        <div className="bg-gradient-overlay"></div>
      </div>

      <div className="dashboard-container">
        {/* Header */}
        <div className="dashboard-header">
          <div className="header-content">
            <div className="header-icon"></div>
            <h1 className="header-title">AI Wildlife Monitoring</h1>
            <p className="header-subtitle">
              Advanced YOLOv8 detection system with real-time species classification
            </p>
          </div>
          <button onClick={() => router.push('/')} className="logout-button">
            Back to Home
          </button>
        </div>

        {/* Main Grid */}
        <div className="main-grid">
          {/* Detection Panel */}
          <div className="glass-card detection-panel">
            <div className="panel-header">
              <h2 className="panel-title">Live Detection Feed</h2>
              <div className={`status-badge ${isOnline ? 'status-online' : 'status-offline'}`}>
                <div className="status-dot"></div>
                <span className="status-text">{isOnline ? 'System Online' : 'System Offline'}</span>
              </div>
            </div>

            <div className="camera-feed">
              {liveImage ? (
                <img src={liveImage} alt="Live feed" className="camera-image" />
              ) : (
                <div className="camera-overlay">
                  <div className="camera-overlay-icon">📡</div>
                  <div className="camera-overlay-text">
                    {isOnline ? "Awaiting first detection..." : "System Offline"}
                  </div>
                </div>
              )}
            </div>

            <div className="species-grid">
              {Object.entries(speciesCounts).map(([species, count]) => (
                <div key={species} className="species-card">
                  <div className="species-icon">{speciesIcons[species.toLowerCase()] || '🐾'}</div>
                  <div className="species-name">{species.charAt(0).toUpperCase() + species.slice(1)}</div>
                  <div className="species-count">{count} detected</div>
                </div>
              ))}
            </div>
          </div>

          {/* Stats Panel */}
          <div className="stats-panel">
            <div className="glass-card stat-card">
              <div className="stat-accent"></div>
              <div className="stat-number">{totalDetections}</div>
              <div className="stat-label">Total Detections</div>
            </div>
            <div className="glass-card stat-card">
              <div className="stat-accent"></div>
              <div className="stat-number">{uniqueSpecies}</div>
              <div className="stat-label">Unique Species</div>
            </div>
            <div className="glass-card stat-card">
              <div className="stat-accent"></div>
              <div className="stat-number last-detection">{lastDetection}</div>
              <div className="stat-label">Last Detection</div>
            </div>
          </div>
        </div>

        {/* Analytics Section */}
        <div className="analytics-grid">
          <div className="glass-card analytics-card">
            <h3 className="analytics-title">Detection Activity (Over Time)</h3>
            <div className="chart-container">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={timelineData}>
                  <defs>
                    <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#22c55e" stopOpacity={0.8}/>
                      <stop offset="95%" stopColor="#22c55e" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="time" stroke="#94a3b8" />
                  <YAxis stroke="#94a3b8" allowDecimals={false} />
                  <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', color: '#fff' }} />
                  <Area type="monotone" dataKey="count" stroke="#22c55e" fillOpacity={1} fill="url(#colorCount)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
          
          <div className="glass-card analytics-card">
            <h3 className="analytics-title">Species Distribution</h3>
            <div className="chart-container">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={barChartData}>
                  <XAxis dataKey="name" stroke="#94a3b8" />
                  <YAxis stroke="#94a3b8" allowDecimals={false} />
                  <Tooltip cursor={{fill: 'rgba(255,255,255,0.05)'}} contentStyle={{ backgroundColor: '#1e293b', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', color: '#fff' }} />
                  <Bar dataKey="count" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Alerts */}
        <div className="glass-card alerts-section">
          <div className="alerts-header">
            <span className="alerts-icon">⚠️</span>
            <h3 className="alerts-title">Recent Alerts</h3>
          </div>
          {detections.slice(0, 3).length > 0 ? (
            <div className="alerts-list">
              {detections.slice(0, 3).map((detection, idx) => {
                const minutesAgo = Math.max(
                  0,
                  Math.round((Date.now() - new Date(detection.timestamp).getTime()) / 60000)
                );
                return (
                  <div key={idx} className="alert-item">
                    <div className="alert-time">{minutesAgo}m ago</div>
                    <div className="alert-message">
                      <span>{speciesIcons[detection.species.toLowerCase()] || '🐾'}</span>
                      <span>
                        {detection.species.charAt(0).toUpperCase() + detection.species.slice(1)} detected
                        ({Math.round(detection.confidence * 100)}% confidence)
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="no-alerts">No recent alerts</div>
          )}
        </div>
      </div>
    </div>
  );
}