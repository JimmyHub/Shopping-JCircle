<template src='@/assets/templates/home/store.html'></template>
<style scoped src='@/assets/css/common/common_in.css'></style>
<style scoped src='@/assets/css/home/store.css'></style>

<script type="text/javascript">
    import { orders } from '@/api/orders.js'
    import { info } from '@/api/users.js'
    import { pinfo } from '@/api/products.js'
    //import { url, port } from '@/assets/js/set.js'
    import { url } from '@/assets/js/set.js'
    import { get_session, go_home, go_cart, go_floor, orders_detail_1, search, logout} from'@/assets/js/often.js'

    export default{
        name:'store',
        data(){
            return{
                info:[],
                list:[],
                order:[],
                order1:[],
                order2:[],
                order3:[],
                order4:[],
                order5:[],
                products_list:[],
                isStatus:1,
                keyword:'',
            }
        },
        methods:{
            go_home, go_cart,go_floor,orders_detail_1,search, logout,
            //切換顯示不同 訂單狀態的訂單
            show(index){
                this.isStatus = index
            },
        },
        async beforeRouteEnter(to,from,next){
            let token = get_session('token')
            let keyword = '0'
            let personal = '1'
            let pattern ='all'
            if(token){
                await Promise.all([info(token),pinfo(keyword,pattern,personal,token),orders(keyword,1,token)]).then(([infoResponse,pinfoResponse,orderResponse]) =>{
                    next( vm=>{
                        //用戶資料請求
                        if(infoResponse.data.code == 200){
                            vm.info= infoResponse.data.data
                            if(vm.info.avatar){
                                vm.info.avatar = `${url()}/media/${vm.info.avatar}`
                            }else{
                                vm.info.avatar = `${url()}/media/avatar/a.jpg`
                            }
                        }
                        //商品資料請求
                        if(pinfoResponse.data.code == 200){
                            if(pinfoResponse.data.data){
                                vm.list= pinfoResponse.data.data
                                for(var l=0;l<vm.list.length;l++){
                                    if(vm.list[l].pphoto){
                                        vm.list[l].pphoto = `${url()}/media/${vm.list[l].pphoto}`
                                        //vm.list[i].pphoto = 'http://127.0.0.1:8000/media/product/milkcoffee.jpg'
                                    }else{
                                        vm.list[l].pphoto = `${url()}/media/product/milkcoffee.jpg`
                                    }
                                }
                            }else{
                                vm.list=[]
                            }
                        }
                        //訂單資料請求
                        if(orderResponse.data.code==200){
                            vm.order= orderResponse.data.data
                            if(vm.order == 'noorders'){
                                vm.order=''
                            }else{
                                vm.order= orderResponse.data.data
                                //將不同訂單狀態的訂單進行分類
                                let list_status=['待繳款 ','待出貨 ','已出貨 ','待取貨 ','完成 ']
                                let list_orders=[[],[],[],[],[]]
                                for(var j=0;j<vm.order.length;j++){
                                    vm.order[j].products_list= `${vm.order[j].products[0]} * ${vm.order[j].products[1]} ...`
                                    vm.order[j].order_num = vm.order[j].num_list.slice(7,13)
                                    for(var i=0;i<5;i++){
                                        if(vm.order[j].status == (i+1)){
                                            list_orders[i].status = (i+1)
                                            vm.order[j].status_show=`${list_status[i]}${vm.order[j].status_time.slice(5,7)}/${vm.order[j].status_time.slice(8,10)}`
                                            list_orders[i].push(vm.order[j]) 
                                        }
                                    }
                                }
                                vm.order1=list_orders[0]
                                vm.order2=list_orders[1]
                                vm.order3=list_orders[2]
                                vm.order4=list_orders[3]
                                vm.order5=list_orders[4]
                                vm.order.all=[vm.order1,vm.order2,vm.order3,vm.order4,vm.order5]          
                            }
                        }   
                    })
                })
            }else{
                alert('請登入在操作')
                window.location.href='#/login'
            }
        },
    }
</script>