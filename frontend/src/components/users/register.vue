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
                let check = 0
                let list_check=[this.username,this.password1,this.password2,this.phone,this.email]
                let list_item=['用戶名','密碼','第二次密碼','電話','信箱']
                var isEmail = /^\w+@\w+[-.]\w+/
                for(var i=0;i<list_check.length;i++){
                    if(list_check[i] ==''){
                        alert(`請輸入 ${list_item[i]}`)
                        check+=1
                    }else{
                        if(3>i){
                            if(list_check[i].length < 5){
                                alert(`請輸入更長的${list_item[i]}`)
                                check+=1
                            }
                        }else if(i == 3){
                                if(list_check[i].length != 10 ){
                                alert(`請輸入正確的${list_item[i]}號碼`)
                                check+=1
                            }
                        }else if(i == 4){
                                if(!isEmail.test(this.email)){
                                alert(`請輸入正確的${list_item[i]}格式`)
                                check+=1
                            }
                        }
                    }
                }
                if(this.password1 != this.password2){
                    alert('兩次密碼輸入不一致,請重新輸入')
                    check+=1
                }
                if(check == 0){
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
    }
</script>