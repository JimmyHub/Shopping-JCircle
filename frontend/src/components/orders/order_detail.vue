<template src='@/assets/templates/orders/order_detail.html'></template>
<style scoped src='@/assets/css/common/common_in.css'></style>
<style scoped src='@/assets/css/orders/order_detail.css'></style>

<script type="text/javascript">
    import { info } from '@/api/users.js'
    import { orders,orders_status, orders_del, porders, porders_del, check_list } from '@/api/orders.js'
    //import { url, port } from '@/assets/js/set.js'
    import { url } from '@/assets/js/set.js'
    import { get_Storage, get_session, go_home, go_cart, search, logout} from'@/assets/js/often.js'

    export default{
        name:'order_detail',
        data(){
            return{
                info:[],
                list:[],
                order:[],
                messages:[],
                //msg:'',
                keyword:null,
                checkShow:false,
            }
        },
        methods:{
            go_home, go_cart, search, logout,
            //獲取金流訂單驗證碼
            check_order(list_id){
                let token = get_session('token')
                this.checkShow=true
                check_list(list_id,token).then((response)=>{
                    if(response.data.code< 400){
                        let check=response.data.data
                        let form = document.getElementsByTagName('form')[0]
                        let html_ = `<div style="display:none">
                                        <input  type="text" name="CheckMacValue" value='${check.check}'>
                                        <input  type="text" name="MerchantID" value="2000132">
                                        <input  type="text"   name="MerchantTradeNo" value='${this.order.num_list}'>
                                        <input  type="text"  name="TimeStamp"  value='${check.time}'>
                                    </div>`
                        form.innerHTML += html_ 
                    }else{
                        alert('失敗')
                    }
                })
            },
            //刪除訂單(在是客戶情況下 且 未繳款 才會顯示此功能)
            delete_l(list_id){
                let token = get_session('token')
                let mode = '1'
                porders_del(list_id,mode,token).then((response)=>{
                    if(response.data.code < 400){
                        orders_del(list_id,token).then((response)=>{
                            if(response.data.code == 200){
                                alert('刪除成功!')
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
            //控制訂單狀態
            next_status(list_id){
                let token = get_session('token')
                let data={
                    'keyword':list_id
                }
                orders_status(JSON.stringify(data),token).then((response)=>{
                    if(response.data.code < 400){
                        let mode =get_Storage('mode')
                        if(mode =='0'){
                            alert("已經通知賣家囉，敬請稍後")
                        }else if(mode == '1'){
                            alert("已經通知買家囉，敬請稍後")
                        }
                        location.reload()
                    }else{
                        alert('咦好像有點問題喔，原因:'+response.data.error)
                    }
                })
            },
            //訂單留言發送訊息用
            /*send_msg(list_id){
                let token = get_session('token')
                let data={
                    'content':this.msg
                }
                let keyword = list_id
                msgs_send(keyword,JSON.stringify(data),token).then((response)=>{
                    if(response.data.code ==200 ){
                        let msg = document.getElementById('msg_show')
                        let msg_get=response.data.data
                        let msg_show=`${msg_get.user}(${msg_get.con_time.slice(0,10)} ${msg_get.con_time.slice(11,19)}):`
                        let new_msg =`<div class='message_msg' style="font-size:12px">
                                          <p style="margin:0">${msg_show}</p>
                                          <p style="margin:0">${msg_get.content}</p>
                                      </div>`
                        msg.innerHTML+=new_msg
                        this.msg=''
                    }else{
                        alert('發送訊息失敗,原因:'+response.data.error)
                    }
                })
            }*/
        },
        async beforeRouteEnter(to,from,next){
            let token =get_session('token')
            let num = get_Storage('list_id')
            let mode = get_Storage('mode')
            if(token){
                await Promise.all([info(token),orders(num,mode,token),porders(num,mode,token)]).then(([infoResponse,orderResponse,pordersResponse])=>{

                /*await Promise.all([info(token),orders(num,mode,token),porders(num,mode,token),msgs(num,token)]).then(([infoResponse,orderResponse,pordersResponse,msgsResponse])=>{*/
                    next(vm =>{ 
                        //用戶資料請求
                        if(infoResponse.data.code < 400){
                            vm.info = infoResponse.data.data
                            console.log(vm.info)
                            if(vm.info.avatar){
                                vm.info.avatar = `${url()}/media/${vm.info.avatar}`
                            }else{
                                vm.info.avatar = `${url()}/media/avatar/a.jpg`
                            }
                        }
                        //訂單資料請求
                        if(orderResponse.data.code< 400){
                            vm.order= orderResponse.data.data
                            //根據不同訂單狀態 改變顯示資料 
                            for(var i=0;i<5;i++){
                                if(vm.order.status == (i+1)){
                                    let list_status=['待繳款 ','待出貨 ','已出貨 ','待取貨 ','完成 ']
                                    vm.order.status_show=`${list_status[i]}${vm.order.status_time.slice(5,7)}/${vm.order.status_time.slice(8,10)}` 
                                }
                            }
                            if(vm.order.payway == '1'){
                                vm.order.payway = '信用卡繳費'
                            }else{
                                vm.order.payway = '超 商 繳 費'
                            }
                            vm.order.mode=parseInt(mode)
                        }
                        //商品資料請求
                        if(pordersResponse.data.code < 400 ){
                            vm.list= pordersResponse.data.data
                            for(var l=0;l<vm.list.length;l++){
                                if(vm.list[l].photo){
                                    vm.list[l].photo=`${url()}/media/${vm.list[l].photo}`
                                }else{
                                    vm.list[l].photo=`${url()}/media/product/a.jpg`
                                }
                                vm.list[l].item_total = vm.list[l].price * vm.list[l].count
                            }
                        }
                        /*if(msgsResponse.data.code ==200){
                            vm.messages=msgsResponse.data.data
                            if(vm.messages == 'norecord'){
                                vm.messages=''
                            }else{
                                for(var m=0;m<vm.messages.length;m++){
                                    vm.messages[m].msg_show=`${vm.messages[m].user}(${vm.messages[m].con_time.slice(0,10)} ${vm.messages[m].con_time.slice(11,19)}):`
                                }
                            }
                        }*/
                    })   
                })
            }else{
                alert('請登入在操作')
            }
        },
    }
</script>
