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
                nError:'',
                p1Error:'',
                p2Error:'',
                phError:'',
                emError:'',
                isCheck:false,
            }
        },
        methods:{
            go_home,search,
            //註冊
            register(){
                //用戶名稱驗證
                if(this.username == ''){
                    this.nError = 'n_empty'
                }else if(this.username.length < 5){
                    this.nError = 'n_form'
                }else{
                    this.nError=''
                }
                //密碼驗證
                if(this.password1 ==''){
                    this.p1Error = 'p1_empty'
                }else if(this.password1.length < 5){
                    this.p1Error = 'p1_form'
                }else{
                    this.p1Error=''
                }
                //再次輸入密碼驗證
                if(this.password2 ==''){
                    this.p2Error = 'p2_empty'
                }else if(this.password1 != this.password2){
                    this.p2Error = 'p2_form'
                }else{
                    this.p2Error=''
                }
                //電話驗證
                if(this.phone ==''){
                    this.phError = 'ph_empty'
                }else if(this.phone.length !=10){
                    this.phError = 'ph_form'
                }else{
                    this.phError=''
                }
                //信箱驗證
                var isEmail = /^\w+@\w+[-.]\w+/
                if(this.email ==''){
                    this.emError = 'em_empty'
                }else if(!isEmail.test(this.email)){
                    this.emError = 'em_form'
                }else{
                    this.emError=''
                }
                //確認驗證都沒有問題
                if(this.nError== '' && this.p1Error=='' &&this.p2Error=='' && this.phError=='' && this.emError==''){
                    this.isCheck=true
                }else{
                    this.isCheck=false
                }
                //無錯誤情況下才可以發出請求
                if(this.isCheck){
                    let data={
                        'username':this.username,
                        'pwd1':this.password1,
                        'pwd2':this.password2,
                        'phone':this.phone,
                        'email':this.email,
                    }
                    reg(JSON.stringify(data)).then((response) =>{
                        if(response.data.code == 200){
                            console.log('here')
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
    }
</script>