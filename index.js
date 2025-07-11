require('dotenv').config();

const { calculateNDVI } = require('./src/ndvi-calculator');
const { processBatch } = require('./src/batch-processor');

async function main() {
  try {
    console.log('🛰️  Sentinel Data Processing - NDVI Calculator');
    console.log('===============================================\n');

    // Example 1: Single coordinate NDVI calculation
    console.log('📍 Calculating NDVI for single location...');
    
    const singleResult = await calculateNDVI({
      latitude: 46.16,
      longitude: 14.27,
      startDate: '2023-06-01',
      endDate: '2023-06-30',
      cloudCoverage: 20
    });

    console.log('Single Location Result:');
    console.log(`- Coordinates: ${singleResult.latitude}, ${singleResult.longitude}`);
    console.log(`- NDVI Value: ${singleResult.ndvi}`);
    console.log(`- Date: ${singleResult.date}`);
    console.log(`- Cloud Coverage: ${singleResult.cloudCoverage}%\n`);

    // Example 2: Batch processing multiple coordinates
    console.log('📍 Processing multiple locations...');
    
    const coordinates = [
      { lat: 46.16, lon: 14.27, id: 'Slovenia_Forest' },
      { lat: 45.81, lon: 15.98, id: 'Croatia_Agricultural' },
      { lat: 48.85, lon: 2.35, id: 'Paris_Urban' }
    ];

    const batchResults = await processBatch(coordinates, {
      startDate: '2023-06-01',
      endDate: '2023-06-30',
      cloudCoverage: 15
    });

    console.log('Batch Processing Results:');
    batchResults.forEach(result => {
      if (result.success) {
        console.log(`- ${result.id}: NDVI = ${result.ndvi} (${result.date})`);
      } else {
        console.log(`- ${result.id}: Error - ${result.error}`);
      }
    });

  } catch (error) {
    console.error('❌ Error:', error.message);
    
    if (error.message.includes('credentials')) {
      console.log('\n💡 Setup Help:');
      console.log('1. Copy .env.example to .env');
      console.log('2. Sign up at https://www.sentinel-hub.com/');
      console.log('3. Add your credentials to the .env file');
    }
  }
}

// Run the main function if this file is executed directly
if (require.main === module) {
  main();
}
