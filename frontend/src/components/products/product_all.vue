<template src='@/assets/templates/products/product_all.html'></template>
<style scoped src='@/assets/css/common/common_in.css'></style>
<style scoped src='@/assets/css/products/product_all.css'></style>


<script type="text/javascript">
    import { index } from '@/api/home.js'
    import { pinfo, precord ,pkind_all} from '@/api/products.js'
    import { shoppingcart_show } from '@/api/shoppings.js'
    //import { url, port } from '@/assets/js/set.js'
    import { url } from '@/assets/js/set.js'
    import { set_Storage, get_Storage, get_session, go_home, go_cart,search,go_products_all, product_detail, logout } from'@/assets/js/often.js'

    export default{
        name:'product_all',
        data(){
            return{
                info:[],
                list:[],
                list_output:[],
                cart:[],
                record:[],
                list_kind:[],
                keyword:'',        
                isCart:false,
            }
        },
        methods:{
            go_home,go_cart,search,go_products_all,product_detail,logout,
            //切換 購物車/瀏覽紀錄
            cart_show(){
                this.isCart = true
            },
            //切換 購物車/瀏覽紀錄
            record_show(){
                this.isCart = false
            },
        },
        async beforeRouteEnter(to,from,next){
            let list_key_check = get_Storage('list_key')
            if(list_key_check == null){
                let list_orgin =[0,0,0]
                set_Storage('list_key',list_orgin)
            }
            let token = get_session('token')
            let keyword =  get_Storage('keyword')
            let personal = '0'
            let list_key = get_Storage('list_key').split(',')
            let record = `${list_key[2]}&${list_key[1]}&${list_key[0]}`
            let pattern = get_Storage('pattern')

            await Promise.all([index(token),pinfo(keyword,'all',personal,token),pkind_all(token),precord("record",record,token),shoppingcart_show(token)]).then(([indexResponse,pinfoResponse,pkindResponse,precordResponse,cartResponse]) =>{
                next( vm=>{
                    //用戶資料請求
                    if(indexResponse.data.code < 400){
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
                    if(pinfoResponse.data.code < 400){
                        if(pinfoResponse.data.data == "NoProduct"){
                            vm.list=''
                        }else{
                            vm.list= pinfoResponse.data.data
                            for(var i=0;i<vm.list.length;i++){
                                if(vm.list[i].pphoto){
                                    vm.list[i].pphoto = `${url()}/media/${vm.list[i].pphoto}`
                                    //vm.list[i].pphoto = 'http://127.0.0.1:8000/media/product/milkcoffee.jpg'
                                }else{
                                    vm.list[i].pphoto = `${url()}/media/product/a.jpg`
                                }
                            }
                            if(pattern == 'search'){
                                let list_tmp = []
                                for(var p=0;p<vm.list.length;p++){
                                    if(vm.list[p].pkind.includes(keyword)){
                                        list_tmp.splice(0,0,vm.list[p])
                                    }
                                }
                                vm.list_output = list_tmp
                                console.log(vm.list_output)
                            }else{
                                vm.list_output = vm.list
                            }
                        }
                    }
                    //商品分類請求
                    if(pkindResponse.data.code ==200){
                        vm.origin_kind = pkindResponse.data.data
                        //商品欄顯示種類
                        vm.list_kind =[]
                        for(var k=0;k<vm.origin_kind.length;k++){
                            let count_exist = 0
                            for(var lk=0;lk<vm.list_kind.length;lk++){
                                if(vm.list_kind[lk] !== vm.origin_kind[k].pkind){
                                    count_exist = count_exist + 1
                                }
                            }
                            if(count_exist == vm.list_kind.length){
                                vm.list_kind[k] =  vm.origin_kind[k].pkind
                            }
                        }
                        vm.list_kind.splice(0,0,'全部')
                    }
                    //購物車資料請求
                    if(cartResponse.data.code < 400){
                        vm.cart = cartResponse.data.data
                        vm.cart.cart_total = cartResponse.data.cart_total
                        for(var c=0;c<vm.cart.length;c++){
                            if(vm.cart[c].pphoto){
                                vm.cart[c].pphoto = `${url()}/media/${vm.cart[c].pphoto}`
                            }else{
                                vm.cart[c].pphoto =  `${url()}/media/product/a.jpg`
                            }
                        }
                    }else{
                        vm.cart.cart_total=0
                    }
                    //瀏覽紀錄請求
                    if(precordResponse.data.code < 400){
                        vm.record=precordResponse.data.data
                        if(vm.record == 'norecord'){
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