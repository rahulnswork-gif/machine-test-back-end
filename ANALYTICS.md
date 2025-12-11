# Analytics API Documentation

## Endpoint
`GET /api/v1/analytics/stats`

# Analytics API Documentation

## Endpoint
`GET /api/v1/analytics/stats`

## Parameters
- `start_date` (optional): Start date in `YYYY-MM-DD` format. **Defaults to user creation date if not provided.**
- `end_date` (optional): End date in `YYYY-MM-DD` format. **Defaults to current date if not provided.**
- `timezone` (optional): Timezone for date grouping (e.g., `UTC`, `Asia/Kolkata`, `America/New_York`). **Defaults to `UTC`.**

## Description
Returns comprehensive bookmark statistics for graph visualization with intelligent date handling:
- **Smart Defaults**: 
  - If `start_date` is missing, it uses the **user's account creation date**.
  - If `end_date` is missing, it uses **today's date**.
- **Timezone Support**: Groups and filters data based on the provided `timezone`.
- **Date Range Filtering**: Filters data between `start_date` and `end_date`.
- **Zero-Filling**: Automatically fills missing dates in the range with 0 counts.
- **Dynamic Labeling**: Automatically adjusts date labels based on duration:
  - Duration ≤ 30 days: `DD-MM-YYYY` (Daily view)
  - Duration > 30 days: `MM-YYYY` (Monthly view)
  - Duration > 365 days: `YYYY` (Yearly view)

## Authentication
Requires JWT token in Authorization header.

## Response Format

```json
{
  "bookmarks_per_period": {
    "periods": ["11-12-2025", "12-12-2025"],
    "counts": [0, 6],
    "label_format": "%d-%m-%Y",
    "duration_days": 2
  },
  "repos_per_owner": {
    "owners": ["pallets", "encode", "pydantic", "sqlalchemy", "tiangolo"],
    "counts": [2, 1, 1, 1, 1]
  },
  "summary": {
    "total_bookmarks": 6,
    "total_owners": 5,
    "date_range": {
      "start": "2025-12-11",
      "end": "2025-12-12"
    }
  }
}
```

## Graph Visualizations

### 1. Bookmarks Over Time (Line/Bar Chart)
Shows total bookmarks created over time, with zero-filled dates and appropriate labels.

**Data:** `bookmarks_per_period`

**Chart.js Example:**
```javascript
const ctx = document.getElementById('bookmarksChart').getContext('2d');
new Chart(ctx, {
  type: 'line',
  data: {
    labels: data.bookmarks_per_period.periods,
    datasets: [{
      label: 'Bookmarks Created',
      data: data.bookmarks_per_period.counts,
      borderColor: 'rgb(75, 192, 192)',
      tension: 0.1,
      fill: true
    }]
  },
  options: {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: `Bookmarks Over Time (${data.bookmarks_per_period.duration_days} days)`
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1
        }
      }
    }
  }
});
```

### 2. Repositories Per Owner (Pie/Bar Chart)
Shows distribution of bookmarked repositories by owner.

**Data:** `repos_per_owner`

**Chart.js Example:**
```javascript
const ctx = document.getElementById('ownersChart').getContext('2d');
new Chart(ctx, {
  type: 'pie',
  data: {
    labels: data.repos_per_owner.owners,
    datasets: [{
      label: 'Repositories',
      data: data.repos_per_owner.counts,
      backgroundColor: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)',
        'rgb(75, 192, 192)',
        'rgb(153, 102, 255)'
      ]
    }]
  },
  options: {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: 'Repositories Per Owner'
      }
    }
  }
});
```

### 3. Owner Activity Timeline (Stacked Area/Line Chart)
Shows how many repositories from each owner were bookmarked over time.

**Data:** `repos_per_owner_timeline`

**Chart.js Example:**
```javascript
// Group data by owner
const ownerData = {};
data.repos_per_owner_timeline.forEach(item => {
  if (!ownerData[item.owner]) {
    ownerData[item.owner] = { dates: [], counts: [] };
  }
  ownerData[item.owner].dates.push(item.date);
  ownerData[item.owner].counts.push(item.count);
});

// Create datasets
const datasets = Object.keys(ownerData).map((owner, index) => ({
  label: owner,
  data: ownerData[owner].counts,
  borderColor: `hsl(${index * 60}, 70%, 50%)`,
  backgroundColor: `hsla(${index * 60}, 70%, 50%, 0.5)`,
  fill: true
}));

const ctx = document.getElementById('timelineChart').getContext('2d');
new Chart(ctx, {
  type: 'line',
  data: {
    labels: [...new Set(data.repos_per_owner_timeline.map(d => d.date))],
    datasets: datasets
  },
  options: {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: 'Owner Activity Over Time'
      }
    },
    scales: {
      y: {
        stacked: true
      }
    }
  }
});
```

## React Example (with Recharts)

```jsx
import React, { useEffect, useState } from 'react';
import {
  LineChart, Line, BarChart, Bar, PieChart, Pie,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, Cell
} from 'recharts';

function AnalyticsDashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/analytics/stats', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    .then(res => res.json())
    .then(setData);
  }, []);

  if (!data) return <div>Loading...</div>;

  // Prepare data for Recharts
  const bookmarksData = data.bookmarks_per_date.dates.map((date, i) => ({
    date,
    count: data.bookmarks_per_date.counts[i]
  }));

  const ownersData = data.repos_per_owner.owners.map((owner, i) => ({
    owner,
    count: data.repos_per_owner.counts[i]
  }));

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  return (
    <div>
      <h2>Analytics Dashboard</h2>
      
      {/* Bookmarks Over Time */}
      <div>
        <h3>Bookmarks Over Time</h3>
        <LineChart width={600} height={300} data={bookmarksData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="count" stroke="#8884d8" />
        </LineChart>
      </div>

      {/* Repositories Per Owner */}
      <div>
        <h3>Repositories Per Owner</h3>
        <PieChart width={400} height={400}>
          <Pie
            data={ownersData}
            dataKey="count"
            nameKey="owner"
            cx="50%"
            cy="50%"
            outerRadius={100}
            label
          >
            {ownersData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </div>

      {/* Summary Stats */}
      <div>
        <h3>Summary</h3>
        <p>Total Bookmarks: {data.summary.total_bookmarks}</p>
        <p>Total Owners: {data.summary.total_owners}</p>
        <p>Date Range: {data.summary.date_range.start} to {data.summary.date_range.end}</p>
      </div>
    </div>
  );
}

export default AnalyticsDashboard;
```

## Testing

Run the test script:
```bash
python3 test_analytics.py
```

Expected output:
```
📊 SUMMARY
  Total Bookmarks: 6
  Total Owners: 5
  Date Range: 2025-12-11 to 2025-12-11

📅 BOOKMARKS PER DATE
  2025-12-11: 6 bookmark(s)

👤 REPOSITORIES PER OWNER (Total)
  pallets: 2 repo(s)
  encode: 1 repo(s)
  pydantic: 1 repo(s)
  sqlalchemy: 1 repo(s)
  tiangolo: 1 repo(s)
```

## Use Cases

1. **Track Bookmarking Activity**: See when you're most active
2. **Identify Favorite Owners**: See which GitHub users you bookmark most
3. **Analyze Trends**: Understand your bookmarking patterns over time
4. **Dashboard Widgets**: Display stats in your frontend

## Notes

- All dates are in ISO format (YYYY-MM-DD)
- Counts are aggregated by date (not datetime)
- Owners are sorted by count (descending)
- Timeline data is sorted by date, then owner
- Empty response if user has no bookmarks
