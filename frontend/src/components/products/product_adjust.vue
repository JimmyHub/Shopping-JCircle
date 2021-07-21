<template src='@/assets/templates/products/product_adjust.html'></template>
<style scoped src='@/assets/css/common/common_in.css'></style>
<style scoped src='@/assets/css/products/product_adjust.css'></style>

<script type="text/javascript">
    import { info } from '@/api/users.js'
    import { pinfo, adjust_p, upload_photo } from '@/api/products.js'
    //import { url, port } from '@/assets/js/set.js'
    import { url } from '@/assets/js/set.js'
    import { get_Storage, get_session, go_home, go_cart, go_back, search, logout,} from'@/assets/js/often.js'

    export default{
        name:'product_adjust',
        data(){
            return{
                info:[],
                list:[],
                pname:'',
                pkind:'',
                pprice:'',
                pcontent:'',
                keyword:'',
                file:null,
                pway: [],
                options: [
                    { text: '信用卡付款', value: '1',disabled: true },
                    { text: '超 商  繳 費', value: '2',disabled: true },
                ],
           }
        },
        methods:{
            go_home,go_cart,go_back,search,logout,
            //修改商品內容
            adjust_pinfo(id){
                let token = get_session('token')
                let keyword = id
                let pway = 0
                for(var i=0;i<this.pway.length;i++){
                    pway +=parseInt(this.pway[i])
                }
                let data={
                    'pname':this.pname,
                    'pkind':this.pkind,
                    'pprice':this.pprice,
                    'pcontent':this.pcontent,
                    'pway':pway,
                } 
                adjust_p(keyword,JSON.stringify(data),token).then((response)=>{
                    if(response.data.code == 200){
                        alert('修改成功')
                        location.reload()
                    }else{
                        alert('修改失敗,原因:'+ response.data.error)
                        location.reload()
                    }
                })
            },
            get_file(event){
                this.file=event.target.files
            },
            //修改照片
            upload_ph(pid){
                let token = get_session('token')
                let formData = new FormData()
                formData.append('photo',this.file[0])
                upload_photo(pid,formData,token).then((response) =>{   
                    if(response.data.code == 200){
                        alert('上傳成功')
                        location.reload()
                    }else{
                        alert('上傳失敗,原因:'+ response.data.error)
                    }
               })
            },
        },
        async beforeRouteEnter(to,from,next){
            let token = get_session('token')
            let keyword = get_Storage('keyword')
            let personal='0'
            await Promise.all([info(token),pinfo(keyword,personal,token)]).then(([infoResponse,pinfoResponse]) =>{
                next( vm=>{
                //用戶資料請求
                    if(infoResponse.data.code ==200){
                        vm.info= infoResponse.data.data
                        if(vm.info.avatar){
                            vm.info.avatar =`${url()}/media/${vm.info.avatar}`
                        }else{
                            vm.info.avatar = `${url()}/media/avatar/a.jpg`
                        }
                    }
                //商品資料請求
                    if(pinfoResponse.data.code == 200){
                        vm.list= pinfoResponse.data.data
                        if(vm.list.pphoto){
                            vm.list.pphoto = `${url()}/media/${vm.list.pphoto}`
                        //vm.list.pphoto = 'http://127.0.0.1:8000/media/product/milkcoffee.jpg'
                        }else{
                            vm.list.pphoto = `${url()}/media/product/milkcoffee.jpg`
                        }
                        if(vm.list.pway == 1){
                            vm.list.pway ='線上付款'
                        }else if(vm.list.pway == 2){
                            vm.list.pway ='超商繳費'
                        }else if(vm.list.pway == 3){
                            vm.list.pway ='信用卡付款\n'
                            vm.list.pway+='超 商  繳 費'
                        }  
                    }
                })  
            })
        },
    }
</script>