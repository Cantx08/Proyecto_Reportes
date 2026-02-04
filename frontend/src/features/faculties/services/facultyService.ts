import {Faculty} from "@/src/features/faculties/types";
import {axiosInstance} from "@/src/lib/axios";

export const facultyService = {
    getFaculties: async (): Promise<Faculty[]> => {
        const {data} = await axiosInstance.get('/faculties');
        return data;
    },
};