import axios from 'axios'
import { url, port } from '@/assets/js/set.js'


export function reg(data){
    return axios.post(`${url()}${port()}/v1/users/`,data)
}

export function login(data){
    return axios.post(`${url()}${port()}/v1/users/login`,data)
}

export function info(token){
    return axios.get(`${url()}${port()}/v1/users/`,{
        headers:{
            "AUTHORIZATION":token
        }
    })
}

export function info_change(data,token){
    return axios.put(`${url()}${port()}/v1/users/`,data,{
        headers:{
            "AUTHORIZATION":token
        }
    })
}

export function avatar_change(formData,token){
    return axios.post(`${url()}${port()}/v1/users/avatar`,formData,{
        headers:{
            "AUTHORIZATION":token
        }
    })
}
