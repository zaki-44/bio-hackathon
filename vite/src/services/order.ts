import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

const api = axios.create({
    baseURL: API_URL,
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const orderAPI = {
    create: async (items: any[]) => {
        try {
            const response = await api.post('/orders', { items });
            return response.data;
        } catch (error: any) {
            throw new Error(error.response?.data?.message || 'Failed to create order');
        }
    },

    getAll: async () => {
        try {
            const response = await api.get('/orders');
            return response.data;
        } catch (error: any) {
            throw new Error(error.response?.data?.message || 'Failed to fetch orders');
        }
    },
};
