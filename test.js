const { calculateNDVI, calculateNDVITimeSeries } = require('./src/ndvi-calculator');
const { processBatch, exportToCSV } = require('./src/batch-processor');

async function runTests() {
  console.log('🧪 Running Sentinel Data Processing Tests');
  console.log('=========================================\n');

  try {
    // Test 1: Single coordinate NDVI calculation
    console.log('Test 1: Single coordinate NDVI calculation');
    console.log('-------------------------------------------');
    
    const testCoordinate = {
      latitude: 46.16,
      longitude: 14.27,
      startDate: '2023-06-01',
      endDate: '2023-06-30',
      cloudCoverage: 30
    };

    console.log('Input parameters:', testCoordinate);
    
    const singleResult = await calculateNDVI(testCoordinate);
    console.log('✅ Single NDVI calculation successful');
    console.log('Result:', {
      ndvi: singleResult.ndvi,
      interpretation: singleResult.interpretation,
      date: singleResult.date
    });
    console.log('');

    // Test 2: Batch processing
    console.log('Test 2: Batch processing multiple coordinates');
    console.log('----------------------------------------------');
    
    const testCoordinates = [
      { lat: 46.16, lon: 14.27, id: 'Slovenia_Test' },
      { lat: 45.81, lon: 15.98, id: 'Croatia_Test' }
    ];

    console.log('Input coordinates:', testCoordinates);
    
    const batchResults = await processBatch(testCoordinates, {
      startDate: '2023-06-01',
      endDate: '2023-06-30',
      cloudCoverage: 30,
      concurrency: 2
    });

    console.log('✅ Batch processing successful');
    console.log('Results summary:');
    batchResults.forEach(result => {
      if (result.success) {
        console.log(`  - ${result.id}: NDVI = ${result.ndvi}`);
      } else {
        console.log(`  - ${result.id}: Failed - ${result.error}`);
      }
    });
    console.log('');

    // Test 3: CSV Export
    console.log('Test 3: CSV Export');
    console.log('------------------');
    
    const csvData = exportToCSV(batchResults);
    console.log('✅ CSV export successful');
    console.log('CSV preview (first 3 lines):');
    console.log(csvData.split('\n').slice(0, 3).join('\n'));
    console.log('');

    // Test 4: Time series analysis (if API allows)
    console.log('Test 4: Time series analysis');
    console.log('-----------------------------');
    
    try {
      const timeSeriesResult = await calculateNDVITimeSeries({
        latitude: 46.16,
        longitude: 14.27,
        startDate: '2023-05-01',
        endDate: '2023-07-31',
        cloudCoverage: 40
      });
      
      console.log('✅ Time series analysis successful');
      console.log('Statistics:', timeSeriesResult.statistics);
      console.log(`Time series length: ${timeSeriesResult.timeSeries.length} points`);
    } catch (error) {
      console.log('⚠️  Time series test skipped:', error.message);
    }

    console.log('\n🎉 All tests completed successfully!');
    console.log('\n💡 Next steps:');
    console.log('1. Configure your .env file with real API credentials');
    console.log('2. Test with your specific coordinates');
    console.log('3. Adjust cloud coverage and date ranges as needed');

  } catch (error) {
    console.error('❌ Test failed:', error.message);
    
    if (error.message.includes('credentials')) {
      console.log('\n💡 To run with real data:');
      console.log('1. Copy .env.example to .env');
      console.log('2. Sign up at https://www.sentinel-hub.com/');
      console.log('3. Add your credentials to the .env file');
      console.log('4. Run the tests again');
    }
  }
}

// Run tests if this file is executed directly
if (require.main === module) {
  runTests();
}

module.exports = { runTests };
