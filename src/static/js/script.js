// Utility Functions

/**
 * Debounce function to limit the rate at which a function can fire.
 * @param {Function} func - The function to debounce.
 * @param {number} wait - The number of milliseconds to wait before calling the function.
 * @returns {Function} - A debounced version of the function.
 */
const debounce = (func, wait) => {
    let timeout;
    return function (...args) {
        const context = this;
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(context, args), wait);
    };
};

/**
 * Throttle function to limit the number of times a function can be called.
 * @param {Function} func - The function to throttle.
 * @param {number} limit - The number of milliseconds to wait before the next call.
 * @returns {Function} - A throttled version of the function.
 */
const throttle = (func, limit) => {
    let lastFunc;
    let lastRan;
    return function (...args) {
        const context = this;
        if (!lastRan) {
            func.apply(context, args);
            lastRan = Date.now();
        } else {
            clearTimeout(lastFunc);
            lastFunc = setTimeout(() => {
                if ((Date.now() - lastRan) >= limit) {
                    func.apply(context, args);
                    lastRan = Date.now();
                }
            }, limit - (Date.now() - lastRan));
        }
    };
};

/**
 * Fetch data from an API with error handling.
 * @param {string} url - The API endpoint.
 * @returns {Promise} - A promise that resolves to the response data.
 */
const fetchData = async (url) => {
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Network response was not ok');
        return await response.json();
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
};

// Export utility functions for use in other modules
export { debounce, throttle, fetchData };
