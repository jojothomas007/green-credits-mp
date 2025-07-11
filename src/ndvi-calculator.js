const SentinelHubAPI = require('./sentinel-api');
const { format, subDays } = require('date-fns');

/**
 * Calculate NDVI for given coordinates and parameters
 * @param {Object} options - Configuration options
 * @param {number} options.latitude - Latitude coordinate
 * @param {number} options.longitude - Longitude coordinate
 * @param {string} options.startDate - Start date in YYYY-MM-DD format
 * @param {string} options.endDate - End date in YYYY-MM-DD format
 * @param {number} [options.cloudCoverage=20] - Maximum cloud coverage percentage
 * @param {number} [options.resolution=10] - Spatial resolution in meters
 * @returns {Promise<Object>} NDVI calculation result
 */
async function calculateNDVI(options) {
  const {
    latitude,
    longitude,
    startDate,
    endDate,
    cloudCoverage = 20,
    resolution = 10
  } = options;

  // Validate inputs
  if (!latitude || !longitude) {
    throw new Error('Latitude and longitude are required');
  }

  if (latitude < -90 || latitude > 90) {
    throw new Error('Latitude must be between -90 and 90');
  }

  if (longitude < -180 || longitude > 180) {
    throw new Error('Longitude must be between -180 and 180');
  }

  if (!startDate || !endDate) {
    throw new Error('Start date and end date are required');
  }

  console.log(`🔍 Searching for Sentinel-2 data...`);
  console.log(`   Location: ${latitude}, ${longitude}`);
  console.log(`   Period: ${startDate} to ${endDate}`);
  console.log(`   Max cloud coverage: ${cloudCoverage}%`);

  const api = new SentinelHubAPI();

  try {
    // Get available dates first
    const availableDates = await api.getAvailableDates(
      latitude, 
      longitude, 
      startDate, 
      endDate, 
      cloudCoverage
    );

    if (availableDates.length === 0) {
      throw new Error('No cloud-free Sentinel-2 images found for the specified criteria');
    }

    console.log(`📅 Found ${availableDates.length} available dates`);

    // Use the most recent date with lowest cloud coverage
    const bestDate = availableDates.sort((a, b) => {
      // First sort by cloud coverage, then by date (most recent)
      if (a.cloudCoverage !== b.cloudCoverage) {
        return a.cloudCoverage - b.cloudCoverage;
      }
      return new Date(b.date) - new Date(a.date);
    })[0];

    console.log(`🎯 Using date: ${bestDate.date} (${bestDate.cloudCoverage}% clouds)`);

    // Get NDVI data for the best available date
    const ndviData = await api.getNDVIData(
      latitude,
      longitude,
      bestDate.date,
      bestDate.date,
      cloudCoverage
    );

    if (!ndviData.hasData) {
      throw new Error('No valid NDVI data available for the specified location');
    }

    const result = {
      latitude,
      longitude,
      ndvi: ndviData.ndvi,
      date: bestDate.date,
      cloudCoverage: bestDate.cloudCoverage,
      quality: ndviData.quality,
      interpretation: interpretNDVI(ndviData.ndvi),
      metadata: {
        resolution,
        source: 'Sentinel-2 L2A',
        searchPeriod: `${startDate} to ${endDate}`,
        availableDates: availableDates.length
      }
    };

    console.log(`✅ NDVI calculated: ${result.ndvi} (${result.interpretation})`);
    return result;

  } catch (error) {
    console.error(`❌ Error calculating NDVI: ${error.message}`);
    throw error;
  }
}

/**
 * Interpret NDVI value
 * @param {number} ndvi - NDVI value
 * @returns {string} Interpretation of the NDVI value
 */
function interpretNDVI(ndvi) {
  if (ndvi < -0.1) return 'Water/Snow';
  if (ndvi < 0.1) return 'Bare soil/Rock';
  if (ndvi < 0.2) return 'Sparse vegetation';
  if (ndvi < 0.4) return 'Moderate vegetation';
  if (ndvi < 0.6) return 'Dense vegetation';
  return 'Very dense vegetation';
}

/**
 * Calculate NDVI statistics for a time series
 * @param {Object} options - Configuration options
 * @param {number} options.latitude - Latitude coordinate
 * @param {number} options.longitude - Longitude coordinate
 * @param {string} options.startDate - Start date in YYYY-MM-DD format
 * @param {string} options.endDate - End date in YYYY-MM-DD format
 * @param {number} [options.cloudCoverage=20] - Maximum cloud coverage percentage
 * @returns {Promise<Object>} Time series NDVI statistics
 */
async function calculateNDVITimeSeries(options) {
  const {
    latitude,
    longitude,
    startDate,
    endDate,
    cloudCoverage = 20
  } = options;

  console.log(`📊 Calculating NDVI time series...`);

  const api = new SentinelHubAPI();
  const availableDates = await api.getAvailableDates(
    latitude,
    longitude,
    startDate,
    endDate,
    cloudCoverage
  );

  if (availableDates.length === 0) {
    throw new Error('No suitable dates found for time series analysis');
  }

  const ndviValues = [];
  const maxDates = Math.min(10, availableDates.length); // Limit to 10 dates to avoid rate limits

  for (let i = 0; i < maxDates; i++) {
    const date = availableDates[i];
    try {
      const ndviData = await api.getNDVIData(
        latitude,
        longitude,
        date.date,
        date.date,
        cloudCoverage
      );

      if (ndviData.hasData) {
        ndviValues.push({
          date: date.date,
          ndvi: ndviData.ndvi,
          cloudCoverage: date.cloudCoverage
        });
      }
    } catch (error) {
      console.warn(`Skipping date ${date.date}: ${error.message}`);
    }
  }

  if (ndviValues.length === 0) {
    throw new Error('No valid NDVI values found for time series');
  }

  // Calculate statistics
  const ndviOnly = ndviValues.map(v => v.ndvi);
  const stats = {
    count: ndviValues.length,
    mean: ndviOnly.reduce((a, b) => a + b, 0) / ndviOnly.length,
    min: Math.min(...ndviOnly),
    max: Math.max(...ndviOnly),
    std: calculateStandardDeviation(ndviOnly)
  };

  return {
    latitude,
    longitude,
    timeSeries: ndviValues,
    statistics: {
      ...stats,
      mean: parseFloat(stats.mean.toFixed(3)),
      std: parseFloat(stats.std.toFixed(3))
    },
    searchPeriod: `${startDate} to ${endDate}`,
    totalAvailableDates: availableDates.length
  };
}

/**
 * Calculate standard deviation
 */
function calculateStandardDeviation(values) {
  const mean = values.reduce((a, b) => a + b, 0) / values.length;
  const squaredDiffs = values.map(value => Math.pow(value - mean, 2));
  const avgSquaredDiff = squaredDiffs.reduce((a, b) => a + b, 0) / values.length;
  return Math.sqrt(avgSquaredDiff);
}

module.exports = {
  calculateNDVI,
  calculateNDVITimeSeries,
  interpretNDVI
};
