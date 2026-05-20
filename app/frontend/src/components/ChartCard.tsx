export default function ChartCard({ title, endpoint, children }: {
  title: string
  endpoint: string
  children: React.ReactNode
}) {
  return (
    <div className="chart-card">
      <div className="chart-header">
        <h2>{title}</h2>
        <code className="endpoint-badge">GET {endpoint}</code>
      </div>
      {children}
    </div>
  )
}
