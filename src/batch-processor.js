const { calculateNDVI } = require('./ndvi-calculator');

/**
 * Process multiple coordinates in batch
 * @param {Array} coordinates - Array of coordinate objects {lat, lon, id}
 * @param {Object} options - Configuration options
 * @param {string} options.startDate - Start date in YYYY-MM-DD format
 * @param {string} options.endDate - End date in YYYY-MM-DD format
 * @param {number} [options.cloudCoverage=20] - Maximum cloud coverage percentage
 * @param {number} [options.concurrency=3] - Number of concurrent requests
 * @returns {Promise<Array>} Array of results for each coordinate
 */
async function processBatch(coordinates, options = {}) {
  const {
    startDate,
    endDate,
    cloudCoverage = 20,
    concurrency = 3
  } = options;

  if (!Array.isArray(coordinates) || coordinates.length === 0) {
    throw new Error('Coordinates array is required and must not be empty');
  }

  if (!startDate || !endDate) {
    throw new Error('Start date and end date are required');
  }

  console.log(`🔄 Processing ${coordinates.length} locations in batches of ${concurrency}`);

  const results = [];
  
  // Process coordinates in batches to avoid overwhelming the API
  for (let i = 0; i < coordinates.length; i += concurrency) {
    const batch = coordinates.slice(i, i + concurrency);
    
    console.log(`\n📦 Processing batch ${Math.floor(i / concurrency) + 1}/${Math.ceil(coordinates.length / concurrency)}`);
    
    const batchPromises = batch.map(async (coord) => {
      try {
        const result = await calculateNDVI({
          latitude: coord.lat,
          longitude: coord.lon,
          startDate,
          endDate,
          cloudCoverage
        });
        
        return {
          id: coord.id,
          latitude: coord.lat,
          longitude: coord.lon,
          success: true,
          ...result
        };
      } catch (error) {
        console.error(`❌ Error processing ${coord.id}: ${error.message}`);
        return {
          id: coord.id,
          latitude: coord.lat,
          longitude: coord.lon,
          success: false,
          error: error.message
        };
      }
    });

    const batchResults = await Promise.all(batchPromises);
    results.push(...batchResults);

    // Add delay between batches to respect rate limits
    if (i + concurrency < coordinates.length) {
      console.log('⏳ Waiting 2 seconds before next batch...');
      await new Promise(resolve => setTimeout(resolve, 2000));
    }
  }

  // Generate summary
  const successful = results.filter(r => r.success);
  const failed = results.filter(r => !r.success);

  console.log(`\n📊 Batch Processing Summary:`);
  console.log(`   ✅ Successful: ${successful.length}`);
  console.log(`   ❌ Failed: ${failed.length}`);
  console.log(`   📈 Success rate: ${((successful.length / results.length) * 100).toFixed(1)}%`);

  if (successful.length > 0) {
    const ndviValues = successful.map(r => r.ndvi);
    const avgNdvi = ndviValues.reduce((a, b) => a + b, 0) / ndviValues.length;
    console.log(`   🌱 Average NDVI: ${avgNdvi.toFixed(3)}`);
  }

  return results;
}

/**
 * Export results to CSV format
 * @param {Array} results - Results from processBatch
 * @returns {string} CSV formatted string
 */
function exportToCSV(results) {
  const headers = [
    'ID',
    'Latitude',
    'Longitude',
    'Success',
    'NDVI',
    'Date',
    'Cloud_Coverage',
    'Interpretation',
    'Error'
  ];

  const rows = results.map(result => [
    result.id,
    result.latitude,
    result.longitude,
    result.success,
    result.success ? result.ndvi : '',
    result.success ? result.date : '',
    result.success ? result.cloudCoverage : '',
    result.success ? result.interpretation : '',
    result.success ? '' : result.error
  ]);

  const csvContent = [headers, ...rows]
    .map(row => row.map(field => `"${field}"`).join(','))
    .join('\n');

  return csvContent;
}

/**
 * Filter coordinates by geographic region
 * @param {Array} coordinates - Array of coordinate objects
 * @param {Object} bounds - Bounding box {north, south, east, west}
 * @returns {Array} Filtered coordinates
 */
function filterByRegion(coordinates, bounds) {
  const { north, south, east, west } = bounds;
  
  return coordinates.filter(coord => 
    coord.lat >= south && 
    coord.lat <= north && 
    coord.lon >= west && 
    coord.lon <= east
  );
}

/**
 * Create a grid of coordinates for area analysis
 * @param {Object} bounds - Bounding box {north, south, east, west}
 * @param {number} resolution - Grid resolution (degrees)
 * @returns {Array} Array of coordinate objects
 */
function createGrid(bounds, resolution = 0.01) {
  const { north, south, east, west } = bounds;
  const coordinates = [];
  
  let idCounter = 1;
  
  for (let lat = south; lat <= north; lat += resolution) {
    for (let lon = west; lon <= east; lon += resolution) {
      coordinates.push({
        lat: parseFloat(lat.toFixed(6)),
        lon: parseFloat(lon.toFixed(6)),
        id: `grid_${idCounter++}`
      });
    }
  }
  
  return coordinates;
}

module.exports = {
  processBatch,
  exportToCSV,
  filterByRegion,
  createGrid
};
