const path = require('path');

module.exports = { 
  // css: {
  //   loaderOptions:{
  //     less: {
  //       javascriptEnabled: true
  //     }
  //   }
  // }
  configureWebpack: {
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
            '@i': path.resolve(__dirname, './src/assets'),
        }
    }
  }
}