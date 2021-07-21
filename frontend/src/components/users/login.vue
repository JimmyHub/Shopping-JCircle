<template src='@/assets/templates/users/login.html'></template>
<style scoped src='@/assets/css/common/common.css'></style>
<style scoped src='@/assets/css/users/reg.css'></style>


<script >
    import { login } from '@/api/users.js'
    import { set_session, go_home, search } from '@/assets/js/often.js'

    export default{
        name:'login',
        data(){
            return{
                username:'',
                password:'',
                keyword:''
            }
        },
        methods:{
            go_home,search,
            //登入
            submit(){
                if (this.username !== null && this.password !== null){
                    let data={
                        'username':this.username,
                        'pwd':this.password
                    }
                    login(JSON.stringify(data)).then((response)=>{
                        if(response.data.code == 200){
                            set_session('username',response.data.data.username)
                            set_session('token',response.data.data.token)
                            set_session('loglevel:webpack-dev-server','SILENT')
                            alert(response.data.data.username+'歡迎登入!')
                            window.location.href='#/index'
                        }else{
                            console.log(response)
                            alert(response.data.error+'登入失敗!')
                            location.reload()
                        }
                    })
                }
            },
        }
    }
</script>