import axios from 'axios'
import { url, port } from '@/assets/js/set.js'

export function check_code(list_id,data){
   return axios.post(`${url()}${port()}/v1/CheckMacValue/${list_id}`,data)
}