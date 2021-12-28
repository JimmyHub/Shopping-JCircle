//瀏覽紀錄
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
    }
}

//瀏覽紀錄
export function precord(key1,key2,key3,token){
    return axios.get(`${url()}${port()}/v1/products/record/0/${key1}/${key2}/${key3}`,{
        headers:{
            "AUTHORIZATION":token
        }
    })
}