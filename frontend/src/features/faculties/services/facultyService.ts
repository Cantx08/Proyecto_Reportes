import {Faculty} from "@/features/faculties/types";
import {axiosInstance} from "@/lib/axios";

export const facultyService = {
    getFaculties: async (): Promise<Faculty[]> => {
        const response = await axiosInstance.get<{ success: boolean; data: Faculty[] }>('/faculties');
        return response.data.data;
    },
};