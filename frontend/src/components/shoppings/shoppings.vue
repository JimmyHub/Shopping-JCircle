<template src='@/assets/templates/shoppings/shoppings.html'></template>
<style scoped src='@/assets/css/common/common_in.css'></style>
<style scoped src='@/assets/css/shoppings/shoppings.css'></style>

<script type="text/javascript">
    import { info } from '@/api/users.js'
    import { precord } from'@/api/products.js'
    import { shoppingcart_show, shoppingcart_change, shoppingcart_delete } from '@/api/shoppings.js'
    //import { url, port } from '@/assets/js/set.js'
    import { url } from '@/assets/js/set.js'
    import { set_Storage, get_Storage,get_session, go_home,go_cart, product_detail, search, logout} from'@/assets/js/often.js'

    export default{
        name:'shopping',
        data(){
            return{
                info:[],
                list:[],
                keyword:'',
            }
        },
        methods:{
            go_home,go_cart,product_detail,search,logout,
            count_change(pid,count){
                let token = get_session('token')
                let data={
                    'count':count
                }
                //商品數量修改
                shoppingcart_change(pid,JSON.stringify(data),token).then((response)=>{
                    if(response.data.code < 400){
                        this.list.list_total=0
                        for(var i=0;i<this.list.length;i++){
                            this.list[i].item_total = this.list[i].price * this.list[i].count
                            this.list.list_total+=this.list[i].item_total
                            if(this.list[i].list_id == pid){
                                let total = document.getElementById(String(pid))
                                total.innerText = String(this.list[i].item_total) + '元'
                            }
                        }
                        let list_total=document.getElementById('total')
                        list_total.innerText = String(this.list.list_total)+'元'
                    }else{
                        alert('更改失敗,原因:'+response.data.error+response.data.code)
                        location.reload()
                    }
                })
            },
            //刪除購物車商品
            delete_l(pid){
                let token = get_session('token')
                shoppingcart_delete(pid,token).then((response)=>{
                    if(response.data.code < 400){
                        alert('刪除成功')
                        location.reload()
                    }else{
                        alert('刪除失敗,')
                        location.reload()
                    }
                })
            },
        },
        async beforeRouteEnter(to,from,next){
            let list_key_check = get_Storage('list_key')
            if(list_key_check == null){
                let list_orgin =[0,0,0]
                set_Storage('list_key',list_orgin)
            }
            let token = get_session('token')
            let list_key = get_Storage('list_key').split(',')
            let record = `${list_key[2]}&${list_key[1]}&${list_key[0]}`
            if(token){
                await Promise.all([info(token),shoppingcart_show(token),precord("record",record,token)]).then(([infoResponse,cartResponse,precordResponse])=>{
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
                            for(var i=0;i<vm.list.length;i++){
                                if(vm.list[i].pphoto){
                                    vm.list[i].pphoto =`${url()}/media/${vm.list[i].pphoto}`
                                }else{
                                    vm.list[i].pphoto =`${url()}/media/product/milkcoffee.jpg`
                                }
                                vm.list[i].item_total = vm.list[i].price * vm.list[i].count
                                vm.list.list_total+= vm.list[i].item_total
                            }
                        }else{
                            vm.list.list_total=0
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
            }else{
                alert('請登入在操作')
                window.location.href="#/login"
            }
        },
    }
</script>
