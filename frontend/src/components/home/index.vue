<template src='@/assets/templates/home/index.html'></template>
<style scoped src='@/assets/css/common/common_in.css'></style>
<style scoped src='@/assets/css/home/index.css'></style>

<script type="text/javascript">
    import { index } from '@/api/home.js'
    import { pinfo, precord } from '@/api/products.js'
    import { shoppingcart_show } from '@/api/shoppings.js'
    import { random_get2 } from '@/assets/js/test.js'
    //import { url, port } from '@/assets/js/set.js'
    import { url } from '@/assets/js/set.js'
    import { set_Storage, get_Storage, get_session, go_home,go_cart, go_products_all, product_detail, search, logout} from'@/assets/js/often.js'

    export default{
        name:'index',
        data(){
            return{
               info:[],
               list:[],
               cart:[],
               record:[],
               isCart:false,
               keyword:'',
            }
        },
        methods:{
            //常見功能
            go_home, go_cart, go_products_all, product_detail,search, logout,
            //切換 購物車/瀏覽紀錄
            cart_show(){
               this.isCart = true
            },
            //切換 購物車/瀏覽紀錄
            record_show(){
               this.isCart = false
            },
            //點詳細資料時 會將keyword 進行設置,頁面轉換時告知其他頁面 當前應該要顯示的商品

        },
        async beforeRouteEnter(to,from,next){
            let list_key_check = get_Storage('list_key')
            if(list_key_check == null){
                let list_orgin =[0,0,0]
                set_Storage('list_key',list_orgin)
            }
            //登入狀態獲得
            let token = get_session('token')
            //獲取商品資料用 參數
            let keyword =  '0'
            let personal = '0'
            //獲取瀏覽紀錄
            let list_key = get_Storage('list_key').split(',')
            let key1 =list_key[0]
            let key2 =list_key[1]
            let key3 =list_key[2]
            await Promise.all([index(token),pinfo(keyword,personal,token),precord(key1,key2,key3,token),shoppingcart_show(token)]).then(([indexResponse,pinfoResponse,precordResponse,cartResponse]) =>{
                next( vm=>{
                    //用戶資料請求
                    if(indexResponse.data.code ==200){
                        if(indexResponse.data.data == 'nouser'){
                            console.log('nouser')
                            vm.info=''
                        }else{
                            vm.info= indexResponse.data.data
                            if(vm.info.avatar){
                            vm.info.avatar = `${url()}/media/${vm.info.avatar}`
                            }else{
                                vm.info.avatar = `${url()}/media/avatar/a.jpg`
                            }
                        }   
                    }
                    //商品資料請求
                    if(pinfoResponse.data.code == 200){
                        if(pinfoResponse.data.data !== []){
                            vm.list= pinfoResponse.data.data
                            vm.list_id=[]
                            for(var i=0;i<vm.list.length;i++){
                                if(vm.list[i].pphoto){
                                    vm.list[i].pphoto = `${url()}/media/${vm.list[i].pphoto}`
                                    //vm.list[i].pphoto = 'http://127.0.0.1:8000/media/product/milkcoffee.jpg'
                                }else{
                                    vm.list[i].pphoto = `${url()}/media/product/a.jpg`
                                }
                                //或取到的商品id都存到list_id裡面
                                vm.list_id[i]=vm.list[i].pid
                            }
                            //商品隨機顯示(一開始)
                            vm.list_show=[0,0,0,0]
                            //隨機產生要顯示的 4個商品位置
                            let array_in=random_get2(vm.list.length,4)
                            for(var li=0;li<vm.list.length;li++){
                                var num = array_in[li]
                                for(var j=0;j<vm.list.length;j++){
                                    //list_id中依照或取到的順序 儲存各種商品id 
                                    //若num位置的商品id 跟 商品請求獲取到的 商品id 相同 
                                    //將此商品資訊 儲存到 要顯示的list_show裡面
                                    if(vm.list_id[num] == vm.list[j].pid){
                                        vm.list_show[li]=vm.list[j]
                                    }
                                } 
                            }
                            //商品隨機顯示(每15秒 變動一次)
                            vm.list_show_time = window.setInterval(() =>{
                                vm.list_show=[0,0,0,0]

                                let array_in=random_get2(vm.list.length,4)
                                for(var li=0;li<vm.list.length;li++){
                                    var num = array_in[li]
                                    for(var j=0;j<vm.list.length;j++){
                                        if(vm.list_id[num] == vm.list[j].pid){
                                            vm.list_show[li]=vm.list[j]
                                        }
                                    } 
                                }
                                //更換頁面時停止此功能
                                if(window.location.href !=`${url()}/#/index`){
                                    console.log('停止了')
                                    clearTimeout(vm.list_show_time)
                                }
                            } , 15000)
                        }else{
                            vm.list=''
                        }
                    }
                    //獲取購物車資料
                    if(cartResponse.data.code ==200){
                        vm.cart = cartResponse.data.data
                        vm.cart.cart_total=0
                        for(var c=0;c<vm.cart.length;c++){
                            if(vm.cart[c].pphoto){
                                vm.cart[c].pphoto = `${url()}/media/${vm.cart[c].pphoto}`
                            }else{
                                vm.cart[c].pphoto =`${url()}/media/product/a.jpg`
                            }
                            vm.cart.cart_total += vm.cart[c].count * vm.cart[c].price
                        }
                    }else{
                        vm.cart.cart_total=0
                    }
                    if(precordResponse.data.code == 200){
                        vm.record=precordResponse.data.data
                        if(vm.record == 'norecode'){
                            vm.record=''
                        }else{
                            for(var r=0;r<vm.record.length;r++){
                                if(vm.record[r].pphoto){
                                    vm.record[r].pphoto = `${url()}/media/${vm.record[r].pphoto}`
                                    //vm.record[r].pphoto = 'http://127.0.0.1:8000/media/product/milkcoffee.jpg'
                                }else{
                                    vm.record[r].pphoto = `${url()}/media/product/a.jpg`
                                }
                            }
                        }
                    }
                })
            })
        },
    }
</script>