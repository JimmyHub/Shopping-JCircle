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
            delete_l(order_num){
                let token = get_session('token')
                let mode = get_Storage('mode')
                porders_del(order_num,mode,token).then((response)=>{
                    if(response.data.code ==200){
                        orders_del(order_num,token).then((response)=>{
                            if(response.data.code == 200){
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
            let num_list = get_Storage('num_list')
            let mode = get_Storage('mode')
            if(token){
                await Promise.all([info(token),orders(num_list,mode,token),porders(num_list,mode,token)]).then(([infoResponse,ordersResponse,pordersResponse])=>{
                    next(vm =>{ 
                        //用戶資料請求
                        if(infoResponse.data.code == 200){
                            vm.info = infoResponse.data.data
                            if(vm.info.avatar){
                                vm.info.avatar = `${url()}/media/${vm.info.avatar}`
                            }else{
                                vm.info.avatar = `${url()}/media/avatar/a.jpg`
                            }
                        }
                        //訂單資料請求
                        if(ordersResponse.data.code == 200){
                            vm.order=ordersResponse.data.data
                            vm.order.order_num = vm.order.num_list.slice(7,13)
                            vm.order.url=`http://www.jcircle.ml/api/v1/CheckMacValue/${vm.order.order_num}`
                            vm.order.url_c=`http://www.jcircle.ml/#/orders`
                            vm.order.url_o=`http://www.jcircle.ml/#/orders`
                            vm.order.num_time= `${vm.order.num_time.slice(0,10)} ${vm.order.num_time.slice(11,19)}`
                        }
                        //訂單商品資料請求
                        if(pordersResponse.data.code == 200 ){
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
