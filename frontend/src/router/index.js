import Vue from 'vue'
import Router from 'vue-router'
import index from '@/components/home/index.vue'
import info from '@/components/home/info.vue'
import store from '@/components/home/store.vue'
import order from '@/components/home/order.vue'
import login from '@/components/users/login.vue'
import register from '@/components/users/register.vue'
import product_up from '@/components/products/product_up.vue'
import product from '@/components/products/product.vue'
import product_all from '@/components/products/product_all.vue'
import product_adjust from '@/components/products/product_adjust.vue'
import shoppings from '@/components/shoppings/shoppings.vue'
import shoppings_checkout from '@/components/shoppings/shoppings_checkout.vue'
import shoppings_final from '@/components/shoppings/shoppings_final.vue'
import order_detail from '@/components/orders/order_detail.vue'
Vue.use(Router)

export default new Router({
     routes:[
        //主頁
        { 
          name:'index',
          path:'/index',
          component:index
        },
        //我的帳戶
        {
          name:'info',
          path:'/info',
          component:info
        },
        //我的訂單
        { 
          name:'order',
          path:'/orders',
          component:order
        },
        //我的賣場
        { 
          name:'store',
          path:'/store',
          component:store
        },
        //users 用戶頁面
        //登入頁面
        { 
          name:'login',
          path:'/login',
          component:login
        },
        //註冊頁面
        {
          name:'register',
          path:'/register',
          component:register
        },
        //products 商品頁面
        //商品總攬
        {
          name:'product_all',
          path:'/product_all',
          component:product_all
        },
        //商品個別顯示
        {
          name:'product',
          path:'/product',
          component:product
        },
        //商品資料上傳
        {
          name:'product_up',
          path:'/product_up',
          component:product_up
        },
        //商品資料修改
        {
          name:'product_adjust',
          path:'/product_adjust',
          component:product_adjust
        },
        //shoppings 購物車顯示頁面
        //購物車總攬
        {
          name:'shoppings',
          path:'/shoppings',
          component:shoppings
        },
        //購物車結帳
        {
          name:'shoppings_checkout',
          path:'/shoppings_checkout',
          component:shoppings_checkout
        },
        //購物車再次確認結帳(金流訂單建立)
        {
          name:'shoppings_final',
          path:'/shoppings_final',
          component:shoppings_final
        },
        //orders 訂單顯示頁面
        {
          name:'order_detail',
          path:'/order_detail',
          component:order_detail
        },        

        ]
})