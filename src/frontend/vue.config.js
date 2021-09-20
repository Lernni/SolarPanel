module.exports = {
  css: {
    loaderOptions: {
      scss: {
        additionalData: `
          @import "@/assets/css/global.scss";
        ` 
      }
    }
  }
}