import Vue from 'vue'
import Router from 'vue-router'
import DataViewer from '@/components/DataViewer'
import DataDownloader from '@/components/DataDownloader'
import VideoCreator from '@/components/VideoCreator'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/data-viewer',
      name: 'DataViewer',
      component: DataViewer
    },
    {
      path: '/downloader',
      name: 'DataDownloader',
      component: DataDownloader
    },
    {
      path: '/video-creator',
      name: 'VideoCreator',
      component: VideoCreator
    },
    {
      path: '*',
      redirect: '/data-viewer'
    }
  ],
  mode: 'history'
})
