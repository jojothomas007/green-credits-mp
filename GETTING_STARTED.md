# 🚀 Getting Started with Sentinel NDVI Calculator

## Quick Test (Using Mock Data)

The project is now configured to work with mock data so you can test it immediately!

### Step 1: Test with Mock Data

Run the test to see how the project works:

```bash
node test.js
```

Or run the main application:

```bash
node index.js
```

Or try your custom usage:

```bash
node your-usage.js
```

## 🔑 Setting Up Real Sentinel Hub API Access

To get real satellite data, you need to set up API credentials:

### Step 1: Sign Up for Sentinel Hub

1. Go to [https://www.sentinel-hub.com/](https://www.sentinel-hub.com/)
2. Click "Sign Up" and create a free account
3. Verify your email address

### Step 2: Create an OAuth Client

1. Log in to your Sentinel Hub dashboard
2. Go to "User Settings" → "OAuth clients"
3. Click "New OAuth client"
4. Fill in the details:
   - **Name**: "NDVI Calculator" (or any name you prefer)
   - **Redirect URLs**: Not needed for this application
   - **Grant Types**: Select "Client Credentials"
5. Click "Create"

### Step 3: Get Your Credentials

After creating the OAuth client, you'll see:
- **Client ID**: A string like `a1b2c3d4-e5f6-7890-abcd-ef1234567890`
- **Client Secret**: A longer string like `a1b2c3d4e5f6789...`

### Step 4: Update Your .env File

1. Open the `.env` file in your project
2. Replace the placeholder values:

```env
# Replace these with your actual credentials
SENTINEL_HUB_CLIENT_ID=your_actual_client_id_here
SENTINEL_HUB_CLIENT_SECRET=your_actual_client_secret_here

# Set to false to use real API data
USE_MOCK_DATA=false
```

### Step 5: Test with Real Data

```bash
node test.js
```

## 🌍 How to Use with Your Coordinates

### Single Location

```javascript
const { calculateNDVI } = require('./src/ndvi-calculator');

const result = await calculateNDVI({
  latitude: 28.6139,      // Your latitude
  longitude: 77.2090,     // Your longitude
  startDate: '2023-06-01',
  endDate: '2023-06-30',
  cloudCoverage: 20
});

console.log('NDVI:', result.ndvi);
```

### Multiple Locations

```javascript
const { processBatch } = require('./src/batch-processor');

const locations = [
  { lat: 28.6139, lon: 77.2090, id: 'Delhi' },
  { lat: 19.0760, lon: 72.8777, id: 'Mumbai' }
];

const results = await processBatch(locations, {
  startDate: '2023-06-01',
  endDate: '2023-06-30'
});
```

## 📊 Understanding NDVI Values

| NDVI Range | Interpretation | Typical Areas |
|------------|----------------|---------------|
| < 0.1      | Water/Bare soil | Rivers, deserts, urban areas |
| 0.1 - 0.2  | Sparse vegetation | Grasslands, early crops |
| 0.2 - 0.4  | Moderate vegetation | Mature crops, shrubland |
| 0.4 - 0.6  | Dense vegetation | Forests, healthy crops |
| > 0.6      | Very dense vegetation | Dense forests, peak growing season |

## 🔧 Common Parameters

### Date Selection
- Use dates during growing season for vegetation analysis
- Avoid winter months for northern latitudes
- Consider seasonal patterns in your region

### Cloud Coverage
- **10-20%**: Very strict, best quality data
- **20-30%**: Good balance of quality and availability
- **30-50%**: More data available, moderate quality

### Examples by Use Case

**Agriculture Monitoring:**
```javascript
cloudCoverage: 15,     // Strict for precision
startDate: '2023-05-01', // Growing season
endDate: '2023-09-30'
```

**Forest Health:**
```javascript
cloudCoverage: 25,     // Moderate tolerance
startDate: '2023-06-01', // Summer months
endDate: '2023-08-31'
```

**Urban Green Space:**
```javascript
cloudCoverage: 30,     // Higher tolerance
startDate: '2023-07-01', // Peak summer
endDate: '2023-07-31'
```

## 🚨 Troubleshooting

### Common Issues

1. **"Credentials not found"**
   - Check your `.env` file has the correct credentials
   - Make sure you replaced the placeholder values
   - Verify you copied the credentials correctly

2. **"No valid data found"**
   - Try increasing cloud coverage tolerance
   - Expand your date range
   - Check if the location has recent Sentinel-2 coverage

3. **"API request failed"**
   - Check your internet connection
   - Verify your Sentinel Hub account is active
   - Make sure you have sufficient API quota

### Testing Coordinates

Good test coordinates with reliable data:
- **Slovenia**: 46.16, 14.27 (forests)
- **California**: 36.7783, -119.4179 (agriculture)
- **Germany**: 51.1657, 10.4515 (mixed landscape)

## 📈 Next Steps

1. **Start with mock data** to understand the workflow
2. **Set up real API credentials** for actual satellite data
3. **Test with your specific coordinates**
4. **Adjust parameters** based on your use case
5. **Implement batch processing** for multiple locations
6. **Export results** to CSV for further analysis

## 💡 Pro Tips

- Sentinel-2 has a 5-day revisit time at the equator
- Cloud-free data is more available in dry seasons
- NDVI values vary significantly by season and location
- Use time series analysis to track vegetation changes
- Consider multiple years of data for trend analysis

Happy satellite data processing! 🛰️🌱
