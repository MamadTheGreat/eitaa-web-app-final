/**
 * API utility functions
 */

const API = {
    /**
     * Fetch videos for a disease
     */
    fetchVideos: async (disease) => {
        try {
            const response = await fetch(`${CONFIG.API_URL}/api/videos/${disease}`);
            if (!response.ok) {
                throw new Error('خطا در دریافت اطلاعات');
            }
            const data = await response.json();
            return { success: true, data: data.videos || [] };
        } catch (error) {
            console.error('Error fetching videos:', error);
            return { success: false, error: error.message };
        }
    },

    /**
     * Save a symptom
     */
    saveSymptom: async (userId, symptomType, value) => {
        try {
            const response = await fetch(`${CONFIG.API_URL}/api/symptoms`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_id: userId,
                    symptom_type: symptomType,
                    value: value
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'خطا در ثبت علامت');
            }

            return { success: true, data };
        } catch (error) {
            console.error('Error saving symptom:', error);
            return { success: false, error: error.message };
        }
    },

    /**
     * Fetch symptom history
     */
    fetchHistory: async (userId, filter = null) => {
        try {
            const response = await fetch(`${CONFIG.API_URL}/api/symptoms/history`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_id: userId,
                    symptom_filter: filter
                })
            });

            if (!response.ok) {
                throw new Error('خطا در دریافت اطلاعات');
            }

            const data = await response.json();
            return { success: true, data: data.data || [] };
        } catch (error) {
            console.error('Error fetching history:', error);
            return { success: false, error: error.message };
        }
    },

    /**
     * Get contact information
     */
    getContactInfo: async () => {
        try {
            const response = await fetch(`${CONFIG.API_URL}/api/contact`);
            if (!response.ok) {
                throw new Error('خطا در دریافت اطلاعات');
            }
            const data = await response.json();
            return { success: true, data };
        } catch (error) {
            console.error('Error fetching contact info:', error);
            return { success: false, error: error.message };
        }
    },

    /**
     * Check API health
     */
    checkHealth: async () => {
        try {
            const response = await fetch(`${CONFIG.API_URL}/api/health`);
            const data = await response.json();
            return { success: response.ok, data };
        } catch (error) {
            console.error('Error checking health:', error);
            return { success: false, error: error.message };
        }
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = API;
}
