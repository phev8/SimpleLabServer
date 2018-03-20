import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import DataViewer from '@/components/DataViewer'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/data-viewer',
      name: 'DataViewer',
      component: DataViewer
    }
  ],
  mode: 'history'
})
