<template src='@/assets/templates/home/info.html'></template>
<style scoped src='@/assets/css/common/common_in.css'></style>
<style scoped src='@/assets/css/home/info.css'></style>


<script type="text/javascript">
    import { info, info_change, avatar_change } from '@/api/users.js'
    //import { url, port } from '@/assets/js/set.js'
    import { url } from '@/assets/js/set.js'
    import { get_session, go_home, go_cart, search, logout} from'@/assets/js/often.js'    

    export default{
        name:'info',
        data(){
            return{
                info:[],
                avatar:null,
                isAdjust:0,
                password_o:'',
                password_n:'',
                birthday:'',
                phone:'',
                gender:'',
                email:'',
                keyword:'',
                file:'',
                options:[
                    { text: 'Male', value: 'Male' },
                    { text: 'Female', value: 'Female' },
                ],
            }
        },
        methods:{
            //常見功能
            go_home, go_cart, search, logout,
            adjust(key){
                this.isAdjust = key
            },
            //更新資料
            upload(){
                let token = get_session('token')
                let list_get=['password','birthday','gender','phone','email']
                let list_value=[[this.password_o,this.password_n],this.birthday,this.gender,this.phone,this.email]
                let data_dic={}
                //資料要更新前，先判斷哪一種項目有變動
                //有變動的數據會加入data_dic 被傳入後台
                for(var i = 0;i<list_get.length;i++){
                    if(i == 0){
                        if(list_value[i][0]){
                            if(list_value[i][1]){
                                data_dic['password_o']=list_value[i][0]
                                data_dic['password_n']=list_value[i][1]
                            }
                        }
                    }else if(i > 0 ){
                        if(list_value[i]){
                            data_dic[list_get[i]]=list_value[i]
                        }
                    }
                }
                info_change(JSON.stringify(data_dic),token).then((response) => {
                    if(response.data.code == 200){
                        alert('修改成功')
                        location.reload()
                    }else{
                        alert('修改失敗,原因:'+response.data.error)
                        location.reload()
                    }
                })
            },
            get_file(event){
                this.file=event.target.files
            },
            //上傳頭像
            upload_av(){
                let formData = new FormData()
                formData.append('avatar',this.file[0])
                console.log(formData)
                let token = get_session('token')
                avatar_change(formData,token).then((response) =>{
                    if(response.data.code ==200){
                        alert('上傳成功')
                        location.reload()

                    }else{
                        alert('上傳失敗,原因:'+response.data.error)
                        location.reload()
                    }
                })
            }
        },
        async beforeRouteEnter(to,from,next){
            let token = get_session('token')
            if(token){
                //用戶資料請求
                info(token).then(response => {
                    if(response.data.code ==200){
                        //response.data.data
                        next(vm => {
                            vm.info = response.data.data
                            console.log(vm.info)
                            if(vm.info.avatar){
                                vm.info.avatar =`${url()}/media/${vm.info.avatar}`
                            }else{
                                vm.info.avatar = `${url()}/media/avatar/a.jpg`
                            }     
                        })
                    }
                })  
            }else{
                alert('請登入在操作')
                window.location.href='#/login'
            }
        },
    }
</script>