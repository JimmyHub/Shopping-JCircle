import { url } from '@/assets/js/set.js'

//localstorage 設置
export function set_Storage(item,value){
    window.localStorage.setItem(item,value)
}

export function get_Storage(item){
    return window.localStorage.getItem(item)
}

export function del_Storage(item){
    window.localStorage.removeItem(item)
}

//sessionstorage設置
export function set_session(item,value){
    window.sessionStorage.setItem(item,value)
}
export function get_session(item){
    return window.sessionStorage.getItem(item)
}
export function del_session(item){
    window.sessionStorage.removeItem(item)
}

//搜尋
export function search(){
    set_Storage('keyword',this.keyword);
    if(window.location.href ==`${url()}/#/product_all`){
        location.reload()
    }else{
        window.location.href='#/product_all'
    }
}
//登出
export function logout(){
    del_session('token')
    del_session('username')
    if(window.location.href ==`${url()}/#/index`){
        location.reload()
    }else{
        window.location.href='#/index'
    }
}

//返回首頁
export function go_home(){
    window.location.href='#/index'
}
//返回上一頁
export function go_back(){
     window.history.go(-1)
}

//前往瀏覽商品
export function go_products_all(kind){
    set_Storage('keyword',kind)
}

//前往購物車
export function go_cart(){
    window.location.href='#/shoppings'
}
//前往商品上架頁面
export function go_floor(){
    window.location.href='#/product_up'
}

//前往商品詳細內容
export function product_detail(pid){
    set_Storage('keyword',pid)
    let num=0
    //從localStorage取道的值為str, 要轉換成陣列
    let record_key = get_Storage('list_key').split(',')
    for(var zr=0;zr<record_key.length;zr++){
        if(record_key[zr] == pid){
            num+=1
        }
    }
    if(num == 0){
        //替換 瀏覽紀錄的商品id
        record_key[0]=record_key[1]
        record_key[1]=record_key[2]
        record_key[2]=pid
        //替換完 更新頁面中的list_key
        set_Storage('list_key',record_key)

        /*for(var n=0;n<record_key.length;n++){
            if(n==2){
                record_key[n]=pid
            }else{
                record_key[n]=record_key[n+1]
            }
        }*/
    }
}

//賣場 前往訂單詳細內容
export function orders_detail_1(num){
    set_Storage('list_id',num)
    set_Storage('mode',1)
}
//客戶 前往訂單詳細內容
export function orders_detail_0(num){
    set_Storage('list_id',num)
    set_Storage('mode',0)
}