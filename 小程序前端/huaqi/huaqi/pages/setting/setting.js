// pages/setting.js

const app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    totalHeight: 0,
    barHeight: 120,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this;
    wx.getSystemInfo({
      success: function (res) {
        var heightPx = res.windowHeight;
        var widthPx = res.windowWidth;
        var heightRpx = heightPx * 750 / widthPx;
        that.setData({
          totalHeight: heightRpx
        });
      },
    })
    this.setData({
      barHeight: app.globalData.height
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },

  /**
   * 用户点击返回按钮
   */
  returnBindTap: function(){
    wx.navigateBack({
      delta: 1
    })
  }
})