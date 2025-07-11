# Sentinel Data Processing

A Node.js application to access Sentinel satellite data and calculate NDVI (Normalized Difference Vegetation Index) values for given coordinates.

## Features

- Access Sentinel-2 satellite data via Sentinel Hub API
- Calculate NDVI values for specific coordinates
- Support for date range queries
- Cloud coverage filtering
- Batch processing for multiple coordinates

## Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure API credentials:**
   - Copy `.env.example` to `.env`
   - Sign up for Sentinel Hub API at https://www.sentinel-hub.com/
   - Add your client ID and secret to the `.env` file

3. **Run the application:**
   ```bash
   npm start
   ```

## Usage

### Basic Usage

```javascript
const { calculateNDVI } = require('./src/ndvi-calculator');

// Calculate NDVI for specific coordinates
const result = await calculateNDVI({
  latitude: 46.16,
  longitude: 14.27,
  startDate: '2023-06-01',
  endDate: '2023-06-30',
  cloudCoverage: 10 // Max cloud coverage percentage
});

//Output
Test 1: Single coordinate NDVI calculation
-------------------------------------------
Input parameters: {
  latitude: 46.16,
  longitude: 14.27,
  startDate: '2023-06-01',
  endDate: '2023-06-30',
  cloudCoverage: 30
}
🔍 Searching for Sentinel-2 data...
   Location: 46.16, 14.27
   Period: 2023-06-01 to 2023-06-30
   Max cloud coverage: 30%
🧪 Using mock data mode (no real API calls)
📅 Found 6 available dates
🎯 Using date: 2023-06-11 (6.5% clouds)
🧪 Using mock data mode (no real API calls)
✅ NDVI calculated: 0.532 (Dense vegetation)
✅ Single NDVI calculation successful
Result: { ndvi: 0.532, interpretation: 'Dense vegetation', date: '2023-06-11' }