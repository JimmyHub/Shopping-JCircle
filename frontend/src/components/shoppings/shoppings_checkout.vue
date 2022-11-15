<template src='@/assets/templates/shoppings/shoppings_checkout.html'></template>
<style scoped src='@/assets/css/common/common_in.css'></style>
<style scoped src='@/assets/css/shoppings/shoppings_checkout.css'></style>

<script type="text/javascript">
    import { info } from '@/api/users.js'
    import { shoppingcart_show} from '@/api/shoppings.js'
    import { checkout, checkout_list } from '@/api/orders.js'
    //import { url, port } from '@/assets/js/set.js'
    import { url } from '@/assets/js/set.js'
    import { set_Storage, get_session, go_home, go_cart, go_back, search, logout} from'@/assets/js/often.js'

    export default{
        name:'shoppings_checkout',
        data(){
            return{
                info:[],
                list:[],
                gname:'',
                address:'',
                telephone:'',
                content:'',
                payway:'',
                keyword:'',
                options: [
                    { text: '信用卡付款', value: 1 },
                    { text: '超 商  繳 費', value: 2 },
                ],
            }
        },
        methods:{
            go_home,go_cart,go_back,search,logout,
            //結帳
            checkout(){
                let token = get_session('token')
                let data={
                    'number':this.list.list_num,
                    'num_time':this.list.list_time,
                    'status':1,
                    'gname':this.gname,
                    'address':this.address,
                    'phone':this.telephone,
                    'payway':this.payway,
                    'content':this.content,
                    'bonus':this.list.bonus_total,
                    'shipping':this.list.shipping,
                    'money_total':this.list.list_total,
                    'buyer':this.info.username,
                    'sales':this.list[0].sales
                }
                checkout(JSON.stringify(data),token).then((response)=>{
                    if(response.data.code < 400){
                        let list_id=[]
                        let counts=[]
                        let products=[]
                        let sales=[]
                        for(var c=0;c<this.list.length;c++){
                            list_id[c]=this.list[c].list_id
                            counts[c]=this.list[c].count
                            products[c]=this.list[c].pid
                            sales[c]=this.list[c].sales
                        }
                        let data_l={
                            'list_id':list_id, 
                            'counts':counts,
                            'products':products,
                            'num_list':response.data.data.number,
                            'sales':sales,
                        }
                        checkout_list(JSON.stringify(data_l),token).then((response)=>{
                            if(response.data.code < 400){
                                set_Storage('list_id',response.data.data)
                                set_Storage('mode',0)
                                window.location.href="#/shoppings_final"
                            }else{
                                alert('結帳失敗,原因:' + response.data.error)
                            }
                        })
                    }else{
                        alert('結帳失敗,原因:'+response.data.error)
                    }
                })
            },
        },
        async beforeRouteEnter(to,from,next){
            let token = get_session('token')
            if(token){
                await Promise.all([info(token),shoppingcart_show(token)]).then(([infoResponse,cartResponse])=>{
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
                        //購物車資料請求
                        if(cartResponse.data.code < 400){
                            vm.list=cartResponse.data.data
                            vm.list.list_total=0
                            vm.list.bonus_20=0
                            vm.list.bonus_25=0
                            vm.list.bonus_total=0
                            vm.list.bonus_kind=''
                            vm.list.shipping=60
                            vm.list.list_num = 115101+ parseInt(vm.list[0].list_id)
                            for(var i=0;i<vm.list.length;i++){
                                if(vm.list[i].pphoto){
                                    vm.list[i].pphoto =`${url()}/media/${vm.list[i].pphoto}`
                                }else{
                                    vm.list[i].pphoto =`${url()}/media/product/milkcoffee.jpg`
                                }
                                vm.list[i].item_total = vm.list[i].price * vm.list[i].count
                                vm.list.list_total+= vm.list[i].item_total
                                //優惠種類
                                if(vm.list[i].pkind =='茶類'){
                                   vm.list.bonus_kind ='20元以上茶類飲料同價錢第二件六折'
                                   if(vm.list[i].price == 20){
                                      vm.list.bonus_20+= vm.list[i].count
                                   }else if(vm.list[i].price == 25){
                                      vm.list.bonus_25+= vm.list[i].count
                                   }
                                }
                            }
                            //優惠計算
                            vm.list.bonus_total += Math.round(vm.list.bonus_20*20-Math.floor(vm.list.bonus_20/2)*1.6*20)
                            vm.list.bonus_total += Math.round(vm.list.bonus_25*25-Math.floor(vm.list.bonus_25/2)*1.6*25)
                            vm.list.list_total -=  vm.list.bonus_total
                            vm.list.list_total +=  vm.list.shipping
                            //訂單成立時間
                            let date = new Date()
                            let y = date.getFullYear()
                            let Mo = date.getMonth()+1
                            Mo = Mo < 10 ? ('0' + Mo) : Mo
                            let d = date.getDate()
                            d = d < 10 ? ('0' + d) : d
                            let h = date.getHours()
                            h = h < 10 ? ('0' + h) : h
                            let m = date.getMinutes()
                            m = m < 10 ? ('0' + m) : m
                            let s = date.getSeconds()
                            s = s < 10 ? ('0' + s) : s
                            vm.list.list_time =  y + '/' + Mo + '/' + d + ' ' + h + ':' + m + ':' + s
                        }
                    })    
                })
            }else{
                alert('請登入在操作')
            }
        },
    }
</script>
