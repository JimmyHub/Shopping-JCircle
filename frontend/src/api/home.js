import axios from 'axios'
import { url, port } from '@/assets/js/set.js'
export function index(token){
    return axios.get(`${url()}${port()}/v1/index`,{
            headers:{
            "AUTHORIZATION": token
            }
    })
}