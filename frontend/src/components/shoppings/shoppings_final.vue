<template src='@/assets/templates/shoppings/shoppings_final.html'></template>
<style scoped src='@/assets/css/common/common_in.css'></style>
<style scoped src='@/assets/css/shoppings/shoppings_final.css'></style>

<script type="text/javascript">
    import { info } from '@/api/users.js'
    import { orders, orders_del, porders, porders_del } from '@/api/orders.js'
    //import { url, port } from '@/assets/js/set.js'
    import { url } from '@/assets/js/set.js'
    import { get_Storage, go_home, get_session, go_cart, go_back, search, logout} from'@/assets/js/often.js'

    export default{
        name:'shoppings_final',
        data(){
            return{
                info:[],
                list:[],
                order:[],
                keyword:'',
            }
        },
        methods:{
            go_home,go_cart,go_back,search,logout,
            //返回上一頁時 要刪除已經創立的訂單
            delete_l(list_id){
                let token = get_session('token')
                let mode = get_Storage('mode')
                porders_del(list_id,mode,token).then((response)=>{
                    if(response.data.code < 400){
                        orders_del(list_id,token).then((response)=>{
                            if(response.data.code < 400){
                                window.history.go(-1)
                            }else{
                                alert('刪除失敗，原因:'+response.data.error)
                            }
                        })
                    }else{
                        alert('咦好像有點問題喔，原因:'+response.data.error)
                    }
                })
            },
        },
        async beforeRouteEnter(to,from,next){
            let token = get_session('token')
            let num = get_Storage('num_list')
            let mode = get_Storage('mode')
            if(token){
                await Promise.all([info(token),orders(num,mode,token),porders(num,mode,token)]).then(([infoResponse,ordersResponse,pordersResponse])=>{
                    next(vm =>{ 
                        //用戶資料請求
                        if(infoResponse.data.code < 400){
                            vm.info = infoResponse.data.data
                            if(vm.info.avatar){
                                vm.info.avatar = `${url()}/media/${vm.info.avatar}`
                            }else{
                                vm.info.avatar = `${url()}/media/avatar/a.jpg`
                            }
                        }
                        //訂單資料請求
                        if(ordersResponse.data.code < 400){
                            vm.order=ordersResponse.data.data
                        }
                        //訂單商品資料請求
                        if(pordersResponse.data.code < 400 ){
                            vm.list= pordersResponse.data.data
                            for(var i=0;i<vm.list.length;i++){
                                if(vm.list[i].photo){
                                    vm.list[i].photo=`${url()}/media/${vm.list[i].photo}`
                                }else{
                                    vm.list[i].photo=`${url()}/media/product/milkcoffee.jpg`
                                }
                                vm.list[i].item_total = vm.list[i].price * vm.list[i].count
                            }
                        }
                    })    
                })
            }else{
                alert('請登入在操作')
            }
        },
    }
</script>
