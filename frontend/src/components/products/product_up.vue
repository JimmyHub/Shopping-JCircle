<template src='@/assets/templates/products/product_up.html'></template>
<style scoped src='@/assets/css/common/common_in.css'></style>
<style scoped src='@/assets/css/products/product_up.css'></style>

<script type="text/javascript">
    import { info } from '@/api/users.js'
    import { pinfo, upload_p, delete_p, upload_photo } from '@/api/products.js'
    //import { url, port } from '@/assets/js/set.js'
    import { url } from '@/assets/js/set.js'
    import { set_Storage, get_session, go_home, go_cart, search, logout } from'@/assets/js/often.js'

    export default{
        name:'product_up',
        data(){
            return{
                info:[],
                list:[],
                pname:'',
                pkind:'',
                pprice:'',
                pcontent:'',
                pway: [],
                keyword:'',
                file:null,
                options:[
                    { text: '信用卡付款', value: '1',disabled: true },
                    { text: '超 商  繳 費', value: '2',disabled: true },
                ],
            }
        },
        methods:{
            go_home,go_cart,search,logout,
            //商品上傳
            upload(){
                let token = get_session('token')
                let pway = 3
                let data ={
                    'pname':this.pname,
                    'pkind':this.pkind,
                    'pprice':this.pprice,
                    'pcontent':this.pcontent,
                    'pway':pway,
                }
                upload_p(JSON.stringify(data),token).then((response)=>{
                    if(response.data.code < 400){
                        let formData = new FormData()
                        formData.append('photo',this.file[0])
                        console.log(this.file[0])
                        let pid = response.data.pid
                        upload_photo(pid,formData,token).then((response) =>{
                            if(response.data.code < 400){
                                alert('上傳成功')
                                location.reload()
                            }else{
                                alert('上傳失敗,原因:'+ response.data.error)
                                location.reload()
                            }
                        })
                    }else{
                        alert('資料上傳失敗,原因:'+ response.data.error)
                        location.reload()
                    }
                })
            },
            get_file(event){
                this.file=event.target.files
            },
            //進入修改商品頁面
            adjust_p(pid){
                set_Storage('keyword',pid)
                window.location.href='#/product_adjust'
            },
            //刪除商品
            delete_p(pid){
                let token = get_session('token')
                let keyword = pid
                delete_p(keyword,token).then((response) =>{
                    if(response.data.code < 400){
                        alert('刪除成功囉')
                        for(var i =0;i<this.list.length;i++){
                            if(this.list[i].id == pid){
                                this.list.splice(i,1)
                            }
                        }
                    }else{
                        if(response.data.data){
                            alert('刪除失敗,原因:'+ response.data.error)
                            let op =response.data.data
                            let op_msg=''
                            for(var p =0;p<op.length;p++){
                               op_msg +=`訂單編號: ${op[p].list_num},有${op[p].count}個未出貨`
                            }
                            alert(op_msg)
                        }else{
                            alert('刪除失敗,原因:'+ response.data.error)
                            location.reload()
                        }

                    }
                })
            }
        },
        async beforeRouteEnter(to,from,next){
            let token = get_session('token')
            let keyword = '0'
            let personal = '1'
            let pattern ='all'
            await Promise.all([info(token),pinfo(keyword,pattern,personal,token)]).then(([infoResponse,pinfoResponse]) =>{
                next( vm=>{
                    //用戶資料請求
                    if(infoResponse.data.code < 400){
                        vm.info= infoResponse.data.data
                        if(vm.info.avatar){
                            vm.info.avatar = `${url()}/media/${vm.info.avatar}`
                        }else{
                            vm.info.avatar = `${url()}/media/avatar/a.jpg`
                        }
                    }
                    //商品資料請求
                    if(pinfoResponse.data.code < 400){
                        vm.list= pinfoResponse.data.data
                        for(var i=0;i<vm.list.length;i++){
                            if(vm.list[i].pphoto){
                                vm.list[i].pphoto =`${url()}/media/${vm.list[i].pphoto}`
                                //vm.list[i].pphoto = 'http://127.0.0.1:8000/media/product/milkcoffee.jpg'
                            }else{
                                vm.list[i].pphoto = `${url()}/media/product/milkcoffee.jpg`
                            }
                        }                 
                    }
                })
            })
        },
    }
</script>
