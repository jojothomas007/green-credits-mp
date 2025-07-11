// Quick start guide for using the Sentinel NDVI Calculator
// Save this as your-usage.js and run with: node your-usage.js

const { calculateNDVI } = require('./src/ndvi-calculator');
const { processBatch } = require('./src/batch-processor');

// Example: Calculate NDVI for your specific coordinates
async function calculateNDVIForYourLocation() {
  try {
    console.log('🛰️  Calculating NDVI for your coordinates...\n');
    
    // Replace these with your actual coordinates
    const yourCoordinates = {
      latitude: 28.6139,     // Example: New Delhi, India
      longitude: 77.2090,
      startDate: '2023-06-01',
      endDate: '2023-06-30',
      cloudCoverage: 25      // Maximum acceptable cloud coverage %
    };
    
    console.log('📍 Input parameters:');
    console.log(`   Latitude: ${yourCoordinates.latitude}`);
    console.log(`   Longitude: ${yourCoordinates.longitude}`);
    console.log(`   Date range: ${yourCoordinates.startDate} to ${yourCoordinates.endDate}`);
    console.log(`   Max cloud coverage: ${yourCoordinates.cloudCoverage}%\n`);
    
    const result = await calculateNDVI(yourCoordinates);
    
    console.log('✅ NDVI Calculation Results:');
    console.log('============================');
    console.log(`🌱 NDVI Value: ${result.ndvi}`);
    console.log(`📅 Image Date: ${result.date}`);
    console.log(`☁️  Cloud Coverage: ${result.cloudCoverage}%`);
    console.log(`🔍 Vegetation Type: ${result.interpretation}`);
    console.log(`📊 Data Quality: ${result.quality === 1 ? 'Good' : 'Moderate'}`);
    console.log(`🛰️  Source: ${result.metadata.source}`);
    
    // Interpret the results
    console.log('\n📖 NDVI Interpretation:');
    console.log('========================');
    if (result.ndvi < 0.1) {
      console.log('🏔️  This area appears to be water, bare soil, or urban area');
    } else if (result.ndvi < 0.3) {
      console.log('🌾 This area has sparse vegetation or early crop growth');
    } else if (result.ndvi < 0.6) {
      console.log('🌿 This area has moderate to dense vegetation');
    } else {
      console.log('🌳 This area has very dense, healthy vegetation');
    }
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    
    if (error.message.includes('credentials')) {
      console.log('\n💡 Setup required:');
      console.log('1. Sign up for free at: https://www.sentinel-hub.com/');
      console.log('2. Get your Client ID and Client Secret');
      console.log('3. Update the .env file with your credentials');
      console.log('4. Run this script again');
    }
  }
}

// Example: Process multiple locations at once
async function processMultipleLocations() {
  console.log('\n\n📍 Processing Multiple Locations');
  console.log('=================================');
  
  // Replace these with your actual coordinates
  const yourLocations = [
    { lat: 28.6139, lon: 77.2090, id: 'New_Delhi' },
    { lat: 19.0760, lon: 72.8777, id: 'Mumbai' },
    { lat: 13.0827, lon: 80.2707, id: 'Chennai' },
    { lat: 22.5726, lon: 88.3639, id: 'Kolkata' }
  ];
  
  try {
    const results = await processBatch(yourLocations, {
      startDate: '2023-06-01',
      endDate: '2023-06-30',
      cloudCoverage: 30,
      concurrency: 2  // Process 2 locations at a time
    });
    
    console.log('\n📊 Batch Results Summary:');
    console.log('==========================');
    
    results.forEach(result => {
      if (result.success) {
        console.log(`✅ ${result.id}: NDVI = ${result.ndvi} (${result.interpretation})`);
      } else {
        console.log(`❌ ${result.id}: ${result.error}`);
      }
    });
    
  } catch (error) {
    console.error('❌ Batch processing error:', error.message);
  }
}

// Function to validate coordinates before processing
function validateCoordinates(lat, lon) {
  if (lat < -90 || lat > 90) {
    throw new Error(`Invalid latitude: ${lat}. Must be between -90 and 90.`);
  }
  if (lon < -180 || lon > 180) {
    throw new Error(`Invalid longitude: ${lon}. Must be between -180 and 180.`);
  }
  return true;
}

// Main function to run examples
async function main() {
  console.log('🌍 Sentinel NDVI Calculator - Your Usage Guide');
  console.log('===============================================');
  
  try {
    // Run single location example
    await calculateNDVIForYourLocation();
    
    // Run multiple locations example
    await processMultipleLocations();
    
    console.log('\n🎉 Processing completed!');
    console.log('\n💡 Tips for better results:');
    console.log('- Use dates during growing season for vegetation analysis');
    console.log('- Lower cloud coverage values give more accurate results');
    console.log('- NDVI values change seasonally - compare same months');
    console.log('- For agriculture, monitor NDVI trends over time');
    
  } catch (error) {
    console.error('❌ Application error:', error.message);
  }
}

// Export for use in other files
module.exports = {
  calculateNDVIForYourLocation,
  processMultipleLocations,
  validateCoordinates,
  main
};

// Run if executed directly
if (require.main === module) {
  main();
}
