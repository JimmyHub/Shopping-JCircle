<template src='@/assets/templates/home/order.html'></template>
<style scoped src='@/assets/css/common/common_in.css'></style>
<style scoped src='@/assets/css/home/order.css'></style>

<script type="text/javascript">
    import { orders } from '@/api/orders.js'
    import { info } from '@/api/users.js'
    //import { url, port } from '@/assets/js/set.js'
    import { url } from '@/assets/js/set.js'
    import { get_session, go_home, go_cart, orders_detail_0, search, logout} from'@/assets/js/often.js'     

    export default{
        name:'order',
        data(){
            return{
                info:[],
                order:[],
                order1:[],
                order2:[],
                order3:[],
                order4:[],
                order5:[],
                products_list:[],
                status_show:[],
                isStatus:0,
                keyword:'',
            }
        },
        methods:{
            //常見功能
            go_home, go_cart, orders_detail_0, search, logout,
            //切換顯示不同 訂單狀態的訂單
            show(index){
                this.isStatus = index
            },
        },
        async beforeRouteEnter(to,from,next){
          let token = get_session('token')
          var keyword = '0'
          if(token){
            await Promise.all([info(token),orders(keyword,0,token)]).then(([infoResponse,orderResponse]) =>{
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
                                for(var i=0;i<5;i++){
                                    if(vm.order[j].status == (i+1)){
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