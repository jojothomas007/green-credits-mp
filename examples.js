// Example usage of the Sentinel Data Processing library

const { calculateNDVI, calculateNDVITimeSeries } = require('./src/ndvi-calculator');
const { processBatch, exportToCSV, createGrid } = require('./src/batch-processor');

// Example 1: Calculate NDVI for a single location
async function exampleSingleLocation() {
  console.log('Example 1: Single Location NDVI');
  console.log('================================');
  
  try {
    const result = await calculateNDVI({
      latitude: 40.7128,    // New York City
      longitude: -74.0060,
      startDate: '2023-07-01',
      endDate: '2023-07-31',
      cloudCoverage: 20
    });
    
    console.log('📍 Location: New York City');
    console.log(`🌱 NDVI: ${result.ndvi}`);
    console.log(`📅 Date: ${result.date}`);
    console.log(`☁️  Clouds: ${result.cloudCoverage}%`);
    console.log(`🔍 Interpretation: ${result.interpretation}`);
    
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// Example 2: Agricultural monitoring for multiple fields
async function exampleAgriculturalMonitoring() {
  console.log('\nExample 2: Agricultural Field Monitoring');
  console.log('========================================');
  
  // Sample agricultural fields (replace with your actual coordinates)
  const agriculturalFields = [
    { lat: 41.8781, lon: -87.6298, id: 'Field_A_Corn' },      // Illinois
    { lat: 40.4173, lon: -82.9071, id: 'Field_B_Soybeans' }, // Ohio
    { lat: 39.7391, lon: -104.9847, id: 'Field_C_Wheat' },   // Colorado
    { lat: 36.1627, lon: -86.7816, id: 'Field_D_Cotton' }    // Tennessee
  ];
  
  try {
    const results = await processBatch(agriculturalFields, {
      startDate: '2023-06-15',  // Growing season
      endDate: '2023-08-15',
      cloudCoverage: 15,        // Strict cloud coverage for agriculture
      concurrency: 2
    });
    
    console.log('\n📊 Agricultural Field Results:');
    results.forEach(result => {
      if (result.success) {
        console.log(`${result.id}: NDVI = ${result.ndvi} (${result.interpretation})`);
      }
    });
    
    // Export results to CSV
    const csvData = exportToCSV(results);
    console.log('\n💾 Results exported to CSV format (first few lines):');
    console.log(csvData.split('\n').slice(0, 3).join('\n'));
    
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// Example 3: Forest health monitoring with time series
async function exampleForestMonitoring() {
  console.log('\nExample 3: Forest Health Time Series');
  console.log('====================================');
  
  try {
    const forestLocation = {
      latitude: 47.6062,   // Seattle area forest
      longitude: -122.3321,
      startDate: '2023-04-01',
      endDate: '2023-09-30',
      cloudCoverage: 25
    };
    
    console.log('🌲 Analyzing forest health over growing season...');
    
    const timeSeries = await calculateNDVITimeSeries(forestLocation);
    
    console.log('\n📈 Time Series Statistics:');
    console.log(`   Count: ${timeSeries.statistics.count} observations`);
    console.log(`   Mean NDVI: ${timeSeries.statistics.mean}`);
    console.log(`   Min NDVI: ${timeSeries.statistics.min}`);
    console.log(`   Max NDVI: ${timeSeries.statistics.max}`);
    console.log(`   Std Dev: ${timeSeries.statistics.std}`);
    
    console.log('\n📅 Individual Observations:');
    timeSeries.timeSeries.slice(0, 5).forEach(obs => {
      console.log(`   ${obs.date}: NDVI = ${obs.ndvi} (${obs.cloudCoverage}% clouds)`);
    });
    
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// Example 4: Urban green space analysis
async function exampleUrbanGreenSpace() {
  console.log('\nExample 4: Urban Green Space Analysis');
  console.log('====================================');
  
  // Create a small grid around Central Park, NYC
  const centralParkArea = {
    north: 40.7829,
    south: 40.7648,
    east: -73.9441,
    west: -73.9821
  };
  
  try {
    console.log('🏙️  Creating analysis grid for Central Park area...');
    
    const gridCoordinates = createGrid(centralParkArea, 0.002); // ~200m resolution
    console.log(`📐 Created grid with ${gridCoordinates.length} points`);
    
    // Sample a few points for demonstration
    const samplePoints = gridCoordinates.slice(0, 3);
    
    const results = await processBatch(samplePoints, {
      startDate: '2023-07-01',
      endDate: '2023-07-31',
      cloudCoverage: 30,
      concurrency: 3
    });
    
    console.log('\n🌳 Urban Green Space Results (sample):');
    results.forEach(result => {
      if (result.success) {
        console.log(`Point ${result.id}: NDVI = ${result.ndvi} (${result.interpretation})`);
      }
    });
    
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// Example 5: Drought monitoring
async function exampleDroughtMonitoring() {
  console.log('\nExample 5: Drought Impact Assessment');
  console.log('===================================');
  
  const droughtProneAreas = [
    { lat: 34.0522, lon: -118.2437, id: 'Los_Angeles_CA' },
    { lat: 31.7619, lon: -106.4850, id: 'El_Paso_TX' },
    { lat: 33.4484, lon: -112.0740, id: 'Phoenix_AZ' }
  ];
  
  try {
    console.log('🏜️  Analyzing vegetation health in drought-prone areas...');
    
    // Compare early summer vs late summer
    const earlySummer = await processBatch(droughtProneAreas, {
      startDate: '2023-05-01',
      endDate: '2023-05-31',
      cloudCoverage: 20
    });
    
    const lateSummer = await processBatch(droughtProneAreas, {
      startDate: '2023-08-01',
      endDate: '2023-08-31',
      cloudCoverage: 20
    });
    
    console.log('\n📊 Drought Impact Analysis:');
    console.log('Location               | Early Summer | Late Summer | Change');
    console.log('----------------------|--------------|-------------|--------');
    
    for (let i = 0; i < droughtProneAreas.length; i++) {
      const early = earlySummer[i];
      const late = lateSummer[i];
      
      if (early.success && late.success) {
        const change = late.ndvi - early.ndvi;
        const changeStr = change > 0 ? `+${change.toFixed(3)}` : change.toFixed(3);
        console.log(`${early.id.padEnd(21)} | ${early.ndvi.toString().padEnd(12)} | ${late.ndvi.toString().padEnd(11)} | ${changeStr}`);
      }
    }
    
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// Run all examples
async function runAllExamples() {
  console.log('🛰️  Sentinel Data Processing - Usage Examples');
  console.log('==============================================\n');
  
  await exampleSingleLocation();
  await exampleAgriculturalMonitoring();
  await exampleForestMonitoring();
  await exampleUrbanGreenSpace();
  await exampleDroughtMonitoring();
  
  console.log('\n✨ All examples completed!');
  console.log('\n💡 Tips:');
  console.log('- Adjust date ranges based on your specific needs');
  console.log('- Lower cloud coverage values give better data quality');
  console.log('- Use batch processing for efficiency with multiple locations');
  console.log('- Consider seasonal variations when interpreting NDVI values');
}

// Export functions for use in other modules
module.exports = {
  exampleSingleLocation,
  exampleAgriculturalMonitoring,
  exampleForestMonitoring,
  exampleUrbanGreenSpace,
  exampleDroughtMonitoring,
  runAllExamples
};

// Run examples if this file is executed directly
if (require.main === module) {
  runAllExamples().catch(console.error);
}
