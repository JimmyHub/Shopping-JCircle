<template src='@/assets/templates/products/product.html'></template>
<style scoped src='@/assets/css/common/common_in.css'></style>
<style scoped src='@/assets/css/products/product.css'></style>

<script type="text/javascript">
    import { index } from '@/api/home.js'
    import { pinfo, precord } from '@/api/products.js'
    import { shoppingcart_add, shoppingcart_show} from '@/api/shoppings.js'
    //import { url, port } from '@/assets/js/set.js'
    import { url } from '@/assets/js/set.js'
    import { set_Storage, get_Storage, get_session, go_home, go_cart, go_products_all, product_detail ,search, logout } from'@/assets/js/often.js'

    export default{
        name:'product',
        data(){
            return{
                list:[],
                cart:[],
                record:[],
                number:1,
                isCart:false,
                keyword:'',
            }
        },
        methods:{
            go_home,go_cart, go_products_all, product_detail ,search,logout,
            //切換 購物車/瀏覽紀錄
            cart_show(){
                this.isCart = true
            },
            //切換 購物車/瀏覽紀錄
            record_show(){
                this.isCart = false
            },
            //將商品加入購物車
            add_cart(price_get){
                let pid = get_Storage('keyword')
                let token = get_session('token')
                let price = price_get
                let count = this.number
                let data={
                    'count':count,
                    'price':price
                }
                if(token){
                    shoppingcart_add(pid,JSON.stringify(data),token).then((response)=>{
                        if(response.data.code == 200){
                            alert('成功加入購物車')
                            location.reload()
                        }else{
                            alert('加入購物車失敗，原因:'+ response.data.error)
                        }
                    })
                }else{
                    alert('請登入後再操作')
                }
            },
        },
        async beforeRouteEnter(to,from,next){
            let list_key_check = get_Storage('list_key')
            if(list_key_check == null){
                let list_orgin =[0,0,0]
                set_Storage('list_key',list_orgin)
            }
            let token = get_session('token')
            let keyword = get_Storage('keyword')
            let personal='0'
            let list_key = get_Storage('list_key').split(',')
            let key1 =list_key[0]
            let key2 =list_key[1]
            let key3 =list_key[2]
            await Promise.all([index(token),pinfo(keyword,personal,token),precord(key1,key2,key3,token),shoppingcart_show(token)]).then(([indexResponse,pinfoResponse,precordResponse,cartResponse]) =>{
                next( vm=>{
                    //用戶資料請求
                    if(indexResponse.data.code ==200){
                        if(indexResponse.data.data == 'nouser'){
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
                        vm.list= pinfoResponse.data.data
                        if(vm.list.pphoto){
                            vm.list.pphoto = `${url()}/media/${vm.list.pphoto}`
                            //vm.list.pphoto = 'http://127.0.0.1:8000/media/product/milkcoffee.jpg'
                        }else{
                            vm.list.pphoto = `${url()}/media/product/a.jpg`
                        }
                        if(vm.list.pway == 1){
                            vm.list.pway ='線上付款'
                        }else if(vm.list.pway == 2){
                            vm.list.pway ='超商繳費'
                        }else if(vm.list.pway == 3){
                            vm.list.pway ='線上付款\n'
                            vm.list.pway+='超商繳費'
                        }  
                    }
                    //購物車資料請求
                    if(cartResponse.data.code ==200){
                        vm.cart = cartResponse.data.data
                        vm.cart.cart_total=0
                        for(var c=0;c<vm.cart.length;c++){
                            if(vm.cart[c].pphoto){
                                vm.cart[c].pphoto =`${url()}/media/${vm.cart[c].pphoto}`
                            }else{
                                vm.cart[c].pphoto = `${url()}/media/product/a.jpg`
                            }
                            vm.cart.cart_total += vm.cart[c].count * vm.cart[c].price
                        }
                    }else{
                        vm.cart.cart_total=0
                    }
                    //瀏覽紀錄請求
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