// var url = 'ws://127.0.0.1:8000/echo';
var url = 'ws://129.204.225.110:8000/echo';

function connect(user, func) {
  wx.connectSocket({
    url: url,
    header: { 'content-type': 'application/json' },
    success: function () {
      console.log('信道连接成功~')
    },
    fail: function () {
      console.log('信道连接失败~')
    }
  })
  wx.onSocketOpen(function (res) {
    wx.showToast({
      title: '信道已开通~',
      icon: "success",
      duration: 2000
    })
    //接受服务器消息
    wx.onSocketMessage(func);//func回调可以拿到服务器返回的数据
  });
  wx.onSocketError(function (res) {
    wx.showToast({
      title: '信道连接失败，请检查！',
      icon: "none",
      duration: 2000
    })
    console.log(res)
  })
}

module.exports = {
  connect: connect,
  send: send
}