
<script type="text/javascript">
//瀏覽紀錄
async beforeRouteEnter(to,from,next){
let list_key_check = get_Storage('list_key')
if(list_key_check == null){
    let list_orgin =[0,0,0]
    set_Storage('list_key',list_orgin)
}
let token = get_session('token')
let keyword =  get_Storage('keyword')
let list_key = get_Storage('list_key').split(',')
let key1 =list_key[0]
let key2 =list_key[1]
let key3 =list_key[2]
//小視窗

data(){
    return{
        isCart:false,
    }
},
methods:{
    //切換 購物車/瀏覽紀錄
    cart_show(){
        this.isCart = true
    },
    //切換 購物車/瀏覽紀錄
    record_show(){
        this.isCart = false
    },
</script>