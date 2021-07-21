import axios from 'axios'
import { url, port } from '@/assets/js/set.js'

export function shoppingcart_show(token){
	return axios.get(`${url()}${port()}/v1/shoppings/`,{
		headers:{
			'AUTHORIZATION':token
		}
	})
}


export function shoppingcart_add(pid,data,token){
	return axios.post(`${url()}${port()}/v1/shoppings/${pid}`,data,{
		headers:{
			'AUTHORIZATION':token
		}
	})
}
export function shoppingcart_change(lid,data,token){
	return axios.put(`${url()}${port()}/v1/shoppings/${lid}`,data,{
		headers:{
			'AUTHORIZATION':token
		}
	})
}

export function shoppingcart_delete(lid,token){
	return axios.delete(`${url()}${port()}/v1/shoppings/${lid}/delete`,{
		headers:{
			'AUTHORIZATION':token
		}
	})
}

