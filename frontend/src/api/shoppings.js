import axios from 'axios'
import { url, port } from '@/assets/js/set.js'

//購物車瀏覽
export function shoppingcart_show(token){
	return axios.get(`${url()}${port()}/v1/shoppings/0`,{
		headers:{
			'AUTHORIZATION':token
		}
	})
}
//購物車加入
export function shoppingcart_add(pid,data,token){
	return axios.post(`${url()}${port()}/v1/shoppings/${pid}`,data,{
		headers:{
			'AUTHORIZATION':token
		}
	})
}
//購物車修改
export function shoppingcart_change(pid,data,token){
	return axios.put(`${url()}${port()}/v1/shoppings/${pid}`,data,{
		headers:{
			'AUTHORIZATION':token
		}
	})
}
//購物車新增
export function shoppingcart_delete(pid,token){
	return axios.delete(`${url()}${port()}/v1/shoppings/${pid}`,{
		headers:{
			'AUTHORIZATION':token
		}
	})
}

