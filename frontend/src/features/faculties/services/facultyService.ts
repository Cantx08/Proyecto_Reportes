import {Faculty} from "@/features/faculties/types";
import {axiosInstance} from "@/lib/axios";

export const facultyService = {
    getFaculties: async (): Promise<Faculty[]> => {
        const {data} = await axiosInstance.get('/faculties');
        return data;
    },
};