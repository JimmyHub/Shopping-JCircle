import Vue from 'vue'
import App from './App.vue'
import router from './router'
import { BootstrapVue, BIcon, BIconSearch, BIconLock, BIconLockFill, BIconPersonFill, BIconTelephoneFill, BIconEnvelope, BBreadcrumb} from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css' 
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue)
Vue.component('BIcon', BIcon)
Vue.component('BIconSearch', BIconSearch)
Vue.component('BIconLock', BIconLock)
Vue.component('BIconLockFill',BIconLockFill)
Vue.component('BIconPersonFill', BIconPersonFill)
Vue.component('BIconTelephoneFill', BIconTelephoneFill)
Vue.component('BIconEnvelope', BIconEnvelope)
Vue.component('b-breadcrumb', BBreadcrumb)


Vue.config.productionTip = false

new Vue({
  render: h => h(App),
  router
}).$mount('#app')
