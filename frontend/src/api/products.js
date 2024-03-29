import axios from 'axios'
import { url, port } from '@/assets/js/set.js'
//瀏覽紀錄
export function precord(pattern,record,token){
	return axios.get(`${url()}${port()}/v1/products/0/${pattern}/0/${record}`,{
		headers:{
			"AUTHORIZATION":token
		}
	})
}
//獲取商品資料
export function pinfo(keyword,pattern,personal,token){
	return axios.get(`${url()}${port()}/v1/products/${keyword}/${pattern}/${personal}/0`,{
		headers:{
			"AUTHORIZATION":token
		}
	})
}
//獲取商品種類
export function pkind_all(token){
	return axios.get(`${url()}${port()}/v1/products/0/allkind/0/0`,{
		headers:{
			"AUTHORIZATION":token
		}
	})
}
//上傳商品
export function upload_p(data,token){
	return axios.post(`${url()}${port()}/v1/products/`,data,{
		headers:{
			"AUTHORIZATION":token
		}
	})
}

//上傳商品圖片
export function upload_photo(pid,formData,token){
    return axios.post(`${url()}${port()}/v1/products/${pid}/photo`,formData,{
        headers:{
            "AUTHORIZATION":token
        }
    })
}

//修改商品資料
export function adjust_p(pid,data,token){
	return axios.patch(`${url()}${port()}/v1/products/${pid}`,data,{
		headers:{
			"AUTHORIZATION":token
		}
	})
}

//刪除商品
export function delete_p(keyword,token){
    return axios.delete(`${url()}${port()}/v1/products/${keyword}`,{
        headers:{
            "AUTHORIZATION":token
        }
    })
}