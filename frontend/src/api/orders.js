import axios from 'axios'
import { url, port } from '@/assets/js/set.js'

/*GET*/
/*訂單總攬 & 訂單總攬商品清單 顯示 */
export function orders(keyword,mode,token){
     return axios.get(`${url()}${port()}/v1/orders/${keyword}/${mode}`,{
          headers:{
               'AUTHORIZATION':token
          }
    })

}
/*訂單商品個別詳細顯示*/
export function porders(keyword,mode,token){
     return axios.get(`${url()}${port()}/v1/orderlists/${keyword}/${mode}`,{
          headers:{
               'AUTHORIZATION':token
          }
    })

}

/*留言板訊息獲取*/
export function msgs(keyword,token){
     return axios.get(`${url()}${port()}/v1/messages/${keyword}`,{
          headers:{
               'AUTHORIZATION':token
          }
    })

}

/*POST*/
/*訂單創建*/
export function checkout(data,token){
     return axios.post(`${url()}${port()}/v1/orders/`,data,{
          headers:{
               'AUTHORIZATION':token
          }
    })

}
/*訂單商品清單創建*/
export function checkout_list(data,token){
     return axios.post(`${url()}${port()}/v1/orderlists/`,data,{
          headers:{
               'AUTHORIZATION':token
          }
    })

}

/*查詢金流網站訂單是否成立  keyword = 訂單編號 */ 
export function check_list(keyword,token){
     return axios.post(`${url()}${port()}/v1/orderCheck/${keyword}`,{
          headers:{
               'AUTHORIZATION':token
          }
    })

}

/*留言板訊息發送*/
export function msgs_send(keyword,data,token){
     return axios.post(`${url()}${port()}/v1/messages/${keyword}`,data,{
          headers:{
               'AUTHORIZATION':token
          }
    })

}



/*PUT*/
/*訂單狀態改變 */
export function orders_status(data,token){
     return axios.put(`${url()}${port()}/v1/orders/0/2`,data,{
          headers:{
               "AUTHORIZATION":token
          }
    })

}

/*DELETE*/
/*訂單刪除 keyword = num_list*/
export function orders_del(keyword,token){
     return axios.delete(`${url()}${port()}/v1/orders/${keyword}`,{
          headers:{
               'AUTHORIZATION':token
          }
    })

}
/*訂單商品刪除 keyword = num_list*/
export function porders_del(keyword,mode,token){
     return axios.delete(`${url()}${port()}/v1/orderlists/${keyword}/${mode}`,{
          headers:{
               'AUTHORIZATION':token
          }
    })

}
