import axios from 'axios'
import { url, port } from '@/assets/js/set.js'
//瀏覽紀錄
export function precord(key1,key2,key3,token){
	return axios.get(`${url()}${port()}/v1/products/record/0/${key1}/${key2}/${key3}`,{
		headers:{
			"AUTHORIZATION":token
		}
	})
}
//獲取商品資料
export function pinfo(keyword,personal,token){
	return axios.get(`${url()}${port()}/v1/products/${keyword}/${personal}`,{
		headers:{
			"AUTHORIZATION":token
		}
	})
}

//上傳商品
export function upload_p(data,token){
	return axios.post(`${url()}${port()}/v1/products/0/1`,data,{
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
export function adjust_p(keyword,data,token){
	return axios.put(`${url()}${port()}/v1/products/${keyword}/1`,data,{
		headers:{
			"AUTHORIZATION":token
		}
	})
}

//刪除商品
export function delete_p(keyword,token){
    return axios.delete(`${url()}${port()}/v1/products/${keyword}/delete`,{
        headers:{
            "AUTHORIZATION":token
        }
    })
}