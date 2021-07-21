<template src='@/assets/templates/users/register.html'></template>
<style scoped src='@/assets/css/common/common.css'></style>
<style scoped src='@/assets/css/users/reg.css'></style>

<script >
    import { reg } from '@/api/users.js'
    import { set_session, go_home, search } from '@/assets/js/often.js'

    export default{
        name:'register',
        data(){
            return{
                username:'',
                password1:'',
                password2:'',
                phone:'',
                email:'',
                keyword:'',
            }
        },
        methods:{
            go_home,search,
            //註冊
            register(){
                let data={
                    'username':this.username,
                    'pwd1':this.password1,
                    'pwd2':this.password2,
                    'phone':this.phone,
                    'email':this.email
                }
                reg(JSON.stringify(data)).then((response) =>{
                    if(response.data.code == 200){
                        alert(response.data.data.username+'註冊成功')
                        set_session('username',response.data.data.username)
                        set_session('token',response.data.data.token)
                        window.location.href = '#/login'
                    }else{
                        alert('註冊失敗,原因:'+response.data.error)
                    }
                })
            }
        }
    }
</script>